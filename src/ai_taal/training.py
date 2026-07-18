"""Training loops that never use the compositional test set for selection."""

from __future__ import annotations

import copy
import math
import random
import time
from dataclasses import dataclass
from typing import Any, Iterable

import numpy as np
import torch
from torch import Tensor, nn

from ai_taal.models import (
    CommunicationSystem,
    ModelSpec,
    PopulationSystem,
    Receiver,
    ReceiverModel,
    SenderModel,
    make_receiver,
    make_sender,
)
from ai_taal.world import Meaning


@dataclass(slots=True)
class TrainingResult:
    best_step: int
    best_validation_exact: float
    elapsed_seconds: float
    history: list[dict[str, float | int]]
    binding_calibration: dict[str, Any] | None = None


@dataclass(slots=True)
class PopulationTrainingResult:
    best_step: int
    best_validation_mean_exact: float
    best_validation_worst_pair_exact: float
    elapsed_seconds: float
    history: list[dict[str, Any]]


def set_reproducible_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True)
    torch.set_num_threads(1)


def meanings_tensor(meanings: Iterable[Meaning], device: str = "cpu") -> Tensor:
    return torch.tensor(
        [meaning.factors for meaning in meanings], dtype=torch.long, device=device
    )


def train_communication_system(
    config: dict[str, Any],
    train_meanings: tuple[Meaning, ...],
    validation_meanings: tuple[Meaning, ...],
    *,
    seed: int,
    max_steps_override: int | None = None,
) -> tuple[CommunicationSystem, TrainingResult]:
    set_reproducible_seed(seed)
    training = config["training"]
    device = training["device"]
    spec = ModelSpec.from_config(config)
    system = CommunicationSystem(spec).to(device)
    optimizer = torch.optim.AdamW(
        system.parameters(),
        lr=training["learning_rate"],
        weight_decay=training["weight_decay"],
    )
    train_values = meanings_tensor(train_meanings, device)
    validation_values = meanings_tensor(validation_meanings, device)
    max_steps = max_steps_override or training["max_steps"]
    evaluation_interval = min(training["evaluation_interval"], max_steps)
    minimum_steps = min(training["minimum_steps"], max_steps)
    patience_steps = training["patience_steps"]
    batch_size = training["batch_size"]
    generator = torch.Generator(device="cpu").manual_seed(seed + 101)

    best_score = (-1, -1.0, -1.0, -1.0)
    best_step = 0
    best_state: dict[str, Any] | None = None
    history: list[dict[str, float | int]] = []
    started = time.perf_counter()

    for step in range(1, max_steps + 1):
        system.train()
        indices = torch.randint(
            len(train_values), (batch_size,), generator=generator, device="cpu"
        ).to(device)
        batch = train_values[indices]
        progress = (step - 1) / max(max_steps - 1, 1)
        temperature = _geometric_schedule(
            training["temperature_start"], training["temperature_end"], progress
        )
        logits, _ = system(batch, temperature=temperature)
        loss = _factor_loss(logits, batch)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        nn.utils.clip_grad_norm_(system.parameters(), training["gradient_clip_norm"])
        optimizer.step()

        should_evaluate = step == 1 or step % evaluation_interval == 0 or step == max_steps
        if not should_evaluate:
            continue
        train_metrics = evaluate_system(system, train_values)
        validation_metrics = evaluate_system(system, validation_values)
        record: dict[str, float | int] = {
            "step": step,
            "loss": float(loss.detach().cpu()),
            "temperature": float(temperature),
            "train_exact": train_metrics["exact_match"],
            "validation_exact": validation_metrics["exact_match"],
        }
        history.append(record)
        eligible = int(
            train_metrics["exact_match"] >= training["selection_known_exact_min"]
        )
        score = (
            eligible,
            validation_metrics["exact_match"],
            float(np.mean(validation_metrics["factor_accuracy"])),
            train_metrics["exact_match"],
        )
        if score > best_score:
            best_score = score
            best_step = step
            best_state = copy.deepcopy(system.state_dict())
        if step >= minimum_steps and step - best_step >= patience_steps:
            break

    if best_state is None:
        raise RuntimeError("Training produced no selectable model.")
    system.load_state_dict(best_state)
    system.eval()
    return system, TrainingResult(
        best_step=best_step,
        best_validation_exact=best_score[1],
        elapsed_seconds=time.perf_counter() - started,
        history=history,
    )


def train_population_system(
    config: dict[str, Any],
    train_meanings: tuple[Meaning, ...],
    validation_meanings: tuple[Meaning, ...],
    *,
    seed: int,
    max_steps_override: int | None = None,
) -> tuple[PopulationSystem, PopulationTrainingResult]:
    set_reproducible_seed(seed)
    training = config["training"]
    population_config = config["agents"]["population"]
    device = training["device"]
    population = PopulationSystem(
        ModelSpec.from_config(config),
        sender_count=population_config["sender_count"],
        receiver_count=population_config["receiver_count"],
    ).to(device)
    optimizer = _population_optimizer(population, training)
    train_values = meanings_tensor(train_meanings, device)
    validation_values = meanings_tensor(validation_meanings, device)
    max_steps = max_steps_override or training["max_steps"]
    evaluation_interval = min(training["evaluation_interval"], max_steps)
    minimum_steps = min(training["minimum_steps"], max_steps)
    batch_generator = torch.Generator(device="cpu").manual_seed(seed + 101)
    consistency_config = training.get("algebraic_consistency", {})
    consistency_enabled = bool(consistency_config.get("enabled", False))
    consistency_quadruples = None
    if consistency_enabled:
        consistency_quadruples = build_algebraic_quadruples(
            train_meanings,
            factor_sizes=ModelSpec.from_config(config).factor_sizes,
            sample_count=consistency_config["quadruple_pool_size"],
            seed=seed + 707,
        ).to(device)
    slot_consensus_config = training.get("slot_binding_consensus", {})
    slot_consensus_enabled = bool(slot_consensus_config.get("enabled", False))
    atom_consensus_config = training.get("atom_code_consensus", {})
    atom_consensus_enabled = bool(atom_consensus_config.get("enabled", False))
    utilization_config = training.get("code_utilization", {})
    utilization_enabled = bool(utilization_config.get("enabled", False))
    utilization_message_source = utilization_config.get(
        "message_source", "relaxed"
    )
    if utilization_enabled:
        if float(utilization_config.get("weight", 0.0)) < 0:
            raise ValueError("Code-utilization weight cannot be negative.")
        if float(utilization_config.get("independence_weight", 0.0)) < 0:
            raise ValueError("Slot-independence weight cannot be negative.")
        if float(utilization_config.get("relaxed_temperature", 0.0)) <= 0:
            raise ValueError("Code-utilization temperature must be positive.")
        if utilization_message_source not in {"relaxed", "straight_through"}:
            raise ValueError(
                "Code-utilization message source must be relaxed or straight_through."
            )
    joint_collision_config = training.get("joint_message_collision", {})
    joint_collision_enabled = bool(joint_collision_config.get("enabled", False))
    if joint_collision_enabled and float(
        joint_collision_config.get("weight", 0.0)
    ) < 0:
        raise ValueError("Joint-collision weight cannot be negative.")
    sender_consensus_config = training.get("sender_message_consensus", {})
    sender_consensus_enabled = bool(sender_consensus_config.get("enabled", False))
    if sender_consensus_enabled and float(
        sender_consensus_config.get("weight", 0.0)
    ) < 0:
        raise ValueError("Sender-message consensus weight cannot be negative.")
    factor_minimax_config = training.get("factor_minimax", {})
    factor_minimax_enabled = bool(factor_minimax_config.get("enabled", False))
    if factor_minimax_enabled and float(
        factor_minimax_config.get("weight", 0.0)
    ) < 0:
        raise ValueError("Factor-minimax weight cannot be negative.")
    if population_config["pairing"] != "all_senders_all_receivers":
        raise ValueError(
            "Population training supports all_senders_all_receivers only."
        )
    transmission_config = training.get("cultural_transmission", {})
    transmission_enabled = bool(transmission_config.get("enabled", False))
    replacement_interval = int(transmission_config.get("replacement_interval", 0))
    maximum_replacements = int(transmission_config.get("maximum_replacements", 0))
    if transmission_enabled and replacement_interval < evaluation_interval:
        raise ValueError(
            "Replacement interval must span at least one evaluation interval."
        )
    required_replacements = (
        max(len(population.senders), len(population.receivers))
        * int(transmission_config.get("minimum_full_turnovers", 1))
        if transmission_enabled
        else 0
    )
    replacement_count = 0

    best_score = (-1, -1, -1, -1.0, -1.0, -1.0)
    best_step = 0
    best_state: dict[str, Any] | None = None
    history: list[dict[str, Any]] = []
    started = time.perf_counter()

    for step in range(1, max_steps + 1):
        population.train()
        indices = torch.randint(
            len(train_values),
            (training["batch_size"],),
            generator=batch_generator,
            device="cpu",
        ).to(device)
        batch = train_values[indices]
        progress = (step - 1) / max(max_steps - 1, 1)
        temperature = _geometric_schedule(
            training["temperature_start"], training["temperature_end"], progress
        )
        messages = [
            sender(batch, temperature=temperature, sample=True)[0]
            for sender in population.senders
        ]
        receiver_logits = [
            receiver(message)
            for message in messages
            for receiver in population.receivers
        ]
        task_loss = torch.stack(
            [_factor_loss(logits, batch) for logits in receiver_logits]
        ).mean()
        factor_minimax_loss = torch.zeros((), device=device)
        factor_minimax_weight = 0.0
        if factor_minimax_enabled:
            factor_minimax_loss = torch.stack(
                [
                    normalized_factor_minimax_loss(logits, batch)
                    for logits in receiver_logits
                ]
            ).mean()
            factor_minimax_warmup = max(
                int(factor_minimax_config.get("warmup_steps", 1)), 1
            )
            factor_minimax_weight = float(factor_minimax_config["weight"]) * min(
                step / factor_minimax_warmup, 1.0
            )
        consistency_loss = torch.zeros((), device=device)
        consistency_weight = 0.0
        if consistency_quadruples is not None:
            consistency_indices = torch.randint(
                len(consistency_quadruples),
                (consistency_config["batch_size"],),
                generator=batch_generator,
                device="cpu",
            ).to(device)
            consistency_batch = consistency_quadruples[consistency_indices]
            consistency_loss = torch.stack(
                [
                    algebraic_consistency_loss(
                        sender,
                        consistency_batch,
                        temperature=consistency_config.get(
                            "relaxed_temperature", 1.0
                        ),
                    )
                    for sender in population.senders
                ]
            ).mean()
            warmup_steps = max(int(consistency_config.get("warmup_steps", 1)), 1)
            consistency_weight = consistency_config["weight"] * min(
                step / warmup_steps, 1.0
            )
        slot_consensus_loss = torch.zeros((), device=device)
        slot_consensus_weight = 0.0
        if slot_consensus_enabled:
            slot_consensus_loss = slot_binding_consensus_loss(
                population,
                sharpness_weight=slot_consensus_config.get(
                    "sharpness_weight", 0.1
                ),
            )
            slot_warmup = max(
                int(slot_consensus_config.get("warmup_steps", 1)), 1
            )
            slot_consensus_weight = slot_consensus_config["weight"] * min(
                step / slot_warmup, 1.0
            )
        atom_consensus_loss = torch.zeros((), device=device)
        atom_consensus_weight = 0.0
        if atom_consensus_enabled:
            atom_consensus_loss = atom_code_consensus_loss(
                population,
                sharpness_weight=atom_consensus_config.get(
                    "sharpness_weight", 0.1
                ),
            )
            atom_warmup = max(
                int(atom_consensus_config.get("warmup_steps", 1)), 1
            )
            atom_consensus_weight = atom_consensus_config["weight"] * min(
                step / atom_warmup, 1.0
            )
        utilization_loss = torch.zeros((), device=device)
        utilization_weight = 0.0
        if utilization_enabled:
            utilization_loss = torch.stack(
                [
                    factor_agnostic_code_utilization_loss(
                        sender,
                        batch,
                        temperature=float(
                            utilization_config["relaxed_temperature"]
                        ),
                        independence_weight=float(
                            utilization_config["independence_weight"]
                        ),
                        message_distributions=(
                            message
                            if utilization_message_source == "straight_through"
                            else None
                        ),
                    )
                    for sender, message in zip(
                        population.senders, messages, strict=True
                    )
                ]
            ).mean()
            utilization_warmup = max(
                int(utilization_config.get("warmup_steps", 1)), 1
            )
            utilization_weight = float(utilization_config["weight"]) * min(
                step / utilization_warmup, 1.0
            )
        joint_collision_loss = torch.zeros((), device=device)
        joint_collision_weight = 0.0
        if joint_collision_enabled:
            joint_collision_loss = torch.stack(
                [
                    straight_through_joint_collision_loss(message, batch)
                    for message in messages
                ]
            ).mean()
            joint_collision_warmup = max(
                int(joint_collision_config.get("warmup_steps", 1)), 1
            )
            joint_collision_weight = float(
                joint_collision_config["weight"]
            ) * min(step / joint_collision_warmup, 1.0)
        sender_consensus_loss = torch.zeros((), device=device)
        sender_consensus_weight = 0.0
        if sender_consensus_enabled:
            sender_consensus_loss = straight_through_sender_consensus_loss(messages)
            sender_consensus_warmup = max(
                int(sender_consensus_config.get("warmup_steps", 1)), 1
            )
            sender_consensus_weight = float(
                sender_consensus_config["weight"]
            ) * min(step / sender_consensus_warmup, 1.0)
        loss = (
            task_loss
            + factor_minimax_weight * factor_minimax_loss
            + consistency_weight * consistency_loss
            + slot_consensus_weight * slot_consensus_loss
            + atom_consensus_weight * atom_consensus_loss
            + utilization_weight * utilization_loss
            + joint_collision_weight * joint_collision_loss
            + sender_consensus_weight * sender_consensus_loss
        )
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        nn.utils.clip_grad_norm_(
            population.parameters(), training["gradient_clip_norm"]
        )
        optimizer.step()

        should_evaluate = step == 1 or step % evaluation_interval == 0 or step == max_steps
        if not should_evaluate:
            continue
        train_metrics = evaluate_population(population, train_values)
        validation_metrics = evaluate_population(population, validation_values)
        history.append(
            {
                "step": step,
                "loss": float(loss.detach().cpu()),
                "task_loss": float(task_loss.detach().cpu()),
                "factor_minimax_loss": float(factor_minimax_loss.detach().cpu()),
                "factor_minimax_weight": float(factor_minimax_weight),
                "algebraic_consistency_loss": float(
                    consistency_loss.detach().cpu()
                ),
                "algebraic_consistency_weight": float(consistency_weight),
                "slot_binding_consensus_loss": float(
                    slot_consensus_loss.detach().cpu()
                ),
                "slot_binding_consensus_weight": float(slot_consensus_weight),
                "atom_code_consensus_loss": float(
                    atom_consensus_loss.detach().cpu()
                ),
                "atom_code_consensus_weight": float(atom_consensus_weight),
                "code_utilization_loss": float(utilization_loss.detach().cpu()),
                "code_utilization_weight": float(utilization_weight),
                "joint_message_collision_loss": float(
                    joint_collision_loss.detach().cpu()
                ),
                "joint_message_collision_weight": float(joint_collision_weight),
                "sender_message_consensus_loss": float(
                    sender_consensus_loss.detach().cpu()
                ),
                "sender_message_consensus_weight": float(
                    sender_consensus_weight
                ),
                "temperature": float(temperature),
                "train_mean_exact": train_metrics["mean_exact_match"],
                "train_worst_pair_exact": train_metrics["worst_pair_exact_match"],
                "validation_mean_exact": validation_metrics["mean_exact_match"],
                "validation_worst_pair_exact": validation_metrics[
                    "worst_pair_exact_match"
                ],
                "replacement_count": replacement_count,
                "full_population_turnovers": replacement_count
                / max(len(population.senders), len(population.receivers)),
            }
        )
        mean_eligible = int(
            train_metrics["mean_exact_match"]
            >= training["selection_known_mean_min"]
        )
        worst_eligible = int(
            train_metrics["worst_pair_exact_match"]
            >= training["selection_known_worst_pair_min"]
        )
        transmission_eligible = int(replacement_count >= required_replacements)
        score = (
            transmission_eligible,
            mean_eligible,
            worst_eligible,
            validation_metrics["mean_exact_match"],
            validation_metrics["worst_pair_exact_match"],
            train_metrics["mean_exact_match"],
        )
        if score > best_score:
            best_score = score
            best_step = step
            best_state = copy.deepcopy(population.state_dict())
        if (
            transmission_eligible
            and step >= minimum_steps
            and step - best_step >= training["patience_steps"]
        ):
            break
        if (
            transmission_enabled
            and step < max_steps
            and step % replacement_interval == 0
            and (
                maximum_replacements == 0
                or replacement_count < maximum_replacements
            )
        ):
            _replace_population_members(
                population,
                sender_index=replacement_count % len(population.senders),
                receiver_index=replacement_count % len(population.receivers),
                device=device,
            )
            replacement_count += 1
            optimizer = _population_optimizer(population, training)

    if best_state is None:
        raise RuntimeError("Population training produced no selectable model.")
    population.load_state_dict(best_state)
    population.eval()
    return population, PopulationTrainingResult(
        best_step=best_step,
        best_validation_mean_exact=best_score[3],
        best_validation_worst_pair_exact=best_score[4],
        elapsed_seconds=time.perf_counter() - started,
        history=history,
    )


def _population_optimizer(
    population: PopulationSystem, training: dict[str, Any]
) -> torch.optim.Optimizer:
    return torch.optim.AdamW(
        population.parameters(),
        lr=training["learning_rate"],
        weight_decay=training["weight_decay"],
    )


def _replace_population_members(
    population: PopulationSystem,
    *,
    sender_index: int,
    receiver_index: int,
    device: str,
) -> None:
    """Replace one generational pair without sharing surviving-agent state."""
    population.senders[sender_index] = make_sender(population.spec).to(device)
    population.receivers[receiver_index] = make_receiver(population.spec).to(device)


def slot_binding_consensus_loss(
    population: PopulationSystem, *, sharpness_weight: float
) -> Tensor:
    bindings = []
    for sender in population.senders:
        method = getattr(sender, "soft_binding_matrix", None)
        if method is None:
            raise ValueError(
                "Binding consensus requires learned_permutation_slot_sender."
            )
        bindings.append(method())
    stacked = torch.stack(bindings)
    consensus = (stacked - stacked.mean(dim=0, keepdim=True)).square().mean()
    sharpness = (stacked * (1.0 - stacked)).mean()
    return consensus + sharpness_weight * sharpness


def atom_code_consensus_loss(
    population: PopulationSystem, *, sharpness_weight: float
) -> Tensor:
    """Align free injective value codes across independent senders."""
    codebooks_by_sender = []
    for sender in population.senders:
        method = getattr(sender, "soft_codebook_matrices", None)
        if method is None:
            raise ValueError(
                "Atomic-code consensus requires injective_permutation_slot_sender."
            )
        codebooks_by_sender.append(method())
    losses = []
    for factor_index in range(len(codebooks_by_sender[0])):
        stacked = torch.stack(
            [codebooks[factor_index] for codebooks in codebooks_by_sender]
        )
        consensus = (stacked - stacked.mean(dim=0, keepdim=True)).square().mean()
        sharpness = (stacked * (1.0 - stacked)).mean()
        losses.append(consensus + sharpness_weight * sharpness)
    return torch.stack(losses).mean()


def factor_agnostic_code_utilization_loss(
    sender: nn.Module,
    meanings: Tensor,
    *,
    temperature: float,
    independence_weight: float,
    message_distributions: Tensor | None = None,
) -> Tensor:
    """Use the available code space without assigning factors to slots.

    The objective favors deterministic, balanced symbols in every slot and
    penalizes mutual information between slots. It receives no factor labels,
    factor identities, or desired factor-to-slot mapping.
    """
    if temperature <= 0:
        raise ValueError("Code-utilization temperature must be positive.")
    if independence_weight < 0:
        raise ValueError("Slot-independence weight cannot be negative.")
    if message_distributions is None:
        relaxed_message = getattr(sender, "relaxed_message", None)
        if relaxed_message is None:
            raise ValueError("Code utilization requires a relaxed sender message.")
        distributions = relaxed_message(meanings, temperature=temperature)
    else:
        distributions = message_distributions
        if distributions.shape[:2] != (
            meanings.shape[0],
            sender.spec.message_length,
        ):
            raise ValueError(
                "Code-utilization messages do not match the input batch and slots."
            )
    alphabet_sizes = sender.spec.slot_alphabet_sizes
    if len(alphabet_sizes) != sender.spec.message_length:
        raise ValueError("Code utilization requires one alphabet size per slot.")

    conditional_entropies = []
    marginal_entropies = []
    local_distributions = []
    epsilon = torch.finfo(distributions.dtype).eps
    for slot_index, alphabet_size in enumerate(alphabet_sizes):
        local = distributions[:, slot_index, :alphabet_size]
        local = local / local.sum(dim=-1, keepdim=True).clamp_min(epsilon)
        local_distributions.append(local)
        log_base = math.log(alphabet_size)
        conditional_entropy = -(
            local * local.clamp_min(epsilon).log()
        ).sum(dim=-1).mean() / log_base
        marginal = local.mean(dim=0)
        marginal_entropy = -(
            marginal * marginal.clamp_min(epsilon).log()
        ).sum() / log_base
        conditional_entropies.append(conditional_entropy)
        marginal_entropies.append(marginal_entropy)

    pairwise_mutual_information = []
    for left_index in range(len(local_distributions)):
        for right_index in range(left_index + 1, len(local_distributions)):
            left = local_distributions[left_index]
            right = local_distributions[right_index]
            joint = torch.einsum("bi,bj->ij", left, right) / left.shape[0]
            left_marginal = joint.sum(dim=1, keepdim=True)
            right_marginal = joint.sum(dim=0, keepdim=True)
            independent = left_marginal * right_marginal
            mutual_information = (
                joint
                * (
                    joint.clamp_min(epsilon).log()
                    - independent.clamp_min(epsilon).log()
                )
            ).sum()
            normalizer = min(
                math.log(alphabet_sizes[left_index]),
                math.log(alphabet_sizes[right_index]),
            )
            pairwise_mutual_information.append(mutual_information / normalizer)

    determinism = torch.stack(conditional_entropies).mean()
    utilization = torch.stack(marginal_entropies).mean()
    independence = torch.stack(pairwise_mutual_information).mean()
    return determinism - utilization + independence_weight * independence


def straight_through_joint_collision_loss(
    message_distributions: Tensor, meanings: Tensor
) -> Tensor:
    """Average colliding distinct inputs per item in a straight-through batch."""
    if message_distributions.ndim != 3:
        raise ValueError("Joint-collision messages must have shape [batch,slots,vocab].")
    if meanings.ndim != 2 or meanings.shape[0] != message_distributions.shape[0]:
        raise ValueError("Joint-collision meanings must match the message batch.")
    per_slot_agreement = torch.einsum(
        "bsv,csv->bcs", message_distributions, message_distributions
    )
    full_message_agreement = per_slot_agreement.prod(dim=-1)
    same_input = meanings[:, None, :].eq(meanings[None, :, :]).all(dim=-1)
    distinct_input = (~same_input).to(full_message_agreement.dtype)
    return (full_message_agreement * distinct_input).sum() / meanings.shape[0]


def straight_through_sender_consensus_loss(
    message_distributions: list[Tensor],
) -> Tensor:
    """Align complete straight-through messages across independent senders."""
    if len(message_distributions) < 2:
        raise ValueError("Sender consensus requires at least two senders.")
    reference_shape = message_distributions[0].shape
    if len(reference_shape) != 3:
        raise ValueError(
            "Sender-consensus messages must have shape [batch,slots,vocab]."
        )
    if any(
        message.shape != reference_shape for message in message_distributions[1:]
    ):
        raise ValueError("Sender-consensus messages must share one shape.")

    pair_losses = []
    for left_index, left in enumerate(message_distributions):
        for right in message_distributions[left_index + 1 :]:
            symbol_agreement = (left * right).sum(dim=-1)
            pair_losses.append(1.0 - symbol_agreement.mean())
    return torch.stack(pair_losses).mean()


def build_algebraic_quadruples(
    train_meanings: tuple[Meaning, ...],
    *,
    factor_sizes: tuple[int, ...],
    sample_count: int,
    seed: int,
) -> Tensor:
    """Build contextual pairs for the same atomic meaning change.

    Every row contains A, B, A', and B'. A→A' and B→B' change exactly
    the same factor value, but in different contexts. Only meanings from
    the training set are included.
    """
    if sample_count < 1:
        raise ValueError("At least one algebraic quadruple is required.")
    lookup = {meaning.factors: meaning.factors for meaning in train_meanings}
    transitions: dict[
        tuple[int, int, int], list[tuple[tuple[int, ...], tuple[int, ...]]]
    ] = {}
    for factors in lookup:
        for factor_index, factor_size in enumerate(factor_sizes):
            source = factors[factor_index]
            for target in range(factor_size):
                if target == source:
                    continue
                changed = list(factors)
                changed[factor_index] = target
                changed_tuple = tuple(changed)
                if changed_tuple in lookup:
                    transitions.setdefault(
                        (factor_index, source, target), []
                    ).append((factors, changed_tuple))
    valid = [(key, pairs) for key, pairs in transitions.items() if len(pairs) >= 2]
    if not valid:
        raise ValueError("Training set contains no repeated atomic transitions.")

    rng = random.Random(seed)
    quadruples = []
    for _ in range(sample_count):
        _, pairs = valid[rng.randrange(len(valid))]
        left_index, right_index = rng.sample(range(len(pairs)), 2)
        left, left_changed = pairs[left_index]
        right, right_changed = pairs[right_index]
        quadruples.append((left, right, left_changed, right_changed))
    return torch.tensor(quadruples, dtype=torch.long)


def algebraic_consistency_loss(
    sender: SenderModel, quadruples: Tensor, *, temperature: float
) -> Tensor:
    """Make the same factor change context-invariant in message distribution."""
    if quadruples.ndim != 3 or quadruples.shape[1:] != (4, 4):
        raise ValueError("Algebraic quadruples must have shape [batch,4,4].")
    batch_size = quadruples.shape[0]
    distributions = sender.relaxed_message(
        quadruples.reshape(batch_size * 4, 4), temperature=temperature
    ).reshape(batch_size, 4, sender.spec.message_length, sender.spec.vocabulary_size)
    left, right, left_changed, right_changed = distributions.unbind(dim=1)
    transition_difference = (left_changed - left) - (right_changed - right)
    return transition_difference.square().sum(dim=-1).mean()


def train_translator(
    config: dict[str, Any],
    train_messages: Tensor,
    train_meanings: tuple[Meaning, ...],
    validation_messages: Tensor,
    validation_meanings: tuple[Meaning, ...],
    *,
    seed: int,
    max_steps_override: int | None = None,
) -> tuple[ReceiverModel, TrainingResult]:
    translator_config = config["translator_training"]
    device = config["training"]["device"]
    set_reproducible_seed(seed)
    translator = make_receiver(ModelSpec.from_config(config)).to(device)
    train_messages = train_messages.to(device)
    validation_messages = validation_messages.to(device)
    train_values = meanings_tensor(train_meanings, device)
    validation_values = meanings_tensor(validation_meanings, device)
    binding_calibration = None
    calibration_config = translator_config.get("binding_calibration", {})
    if calibration_config.get("enabled", False):
        binding_calibration = calibrate_receiver_binding(
            translator,
            train_messages,
            train_values,
            confidence=float(calibration_config.get("confidence", 8.0)),
            freeze=bool(calibration_config.get("freeze", True)),
        )
    optimizer = torch.optim.AdamW(
        [parameter for parameter in translator.parameters() if parameter.requires_grad],
        lr=translator_config["learning_rate"],
        weight_decay=translator_config["weight_decay"],
    )
    max_steps = max_steps_override or translator_config["max_steps"]
    evaluation_interval = min(translator_config["evaluation_interval"], max_steps)
    minimum_steps = min(translator_config["minimum_steps"], max_steps)
    generator = torch.Generator(device="cpu").manual_seed(seed + 303)

    best_score = (-1.0, -1.0, -1.0)
    best_step = 0
    best_state: dict[str, Any] | None = None
    history: list[dict[str, float | int]] = []
    started = time.perf_counter()

    for step in range(1, max_steps + 1):
        translator.train()
        indices = torch.randint(
            len(train_values),
            (translator_config["batch_size"],),
            generator=generator,
            device="cpu",
        ).to(device)
        batch_messages = train_messages[indices]
        batch_targets = train_values[indices]
        logits = translator(batch_messages)
        loss = _factor_loss(logits, batch_targets)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        nn.utils.clip_grad_norm_(
            translator.parameters(), translator_config["gradient_clip_norm"]
        )
        optimizer.step()

        should_evaluate = step == 1 or step % evaluation_interval == 0 or step == max_steps
        if not should_evaluate:
            continue
        train_metrics = evaluate_receiver(translator, train_messages, train_values)
        validation_metrics = evaluate_receiver(
            translator, validation_messages, validation_values
        )
        history.append(
            {
                "step": step,
                "loss": float(loss.detach().cpu()),
                "train_exact": train_metrics["exact_match"],
                "validation_exact": validation_metrics["exact_match"],
            }
        )
        score = (
            validation_metrics["exact_match"],
            float(np.mean(validation_metrics["factor_accuracy"])),
            train_metrics["exact_match"],
        )
        if score > best_score:
            best_score = score
            best_step = step
            best_state = copy.deepcopy(translator.state_dict())
        if step >= minimum_steps and step - best_step >= translator_config["patience_steps"]:
            break

    if best_state is None:
        raise RuntimeError("Translator training produced no selectable model.")
    translator.load_state_dict(best_state)
    translator.eval()
    return translator, TrainingResult(
        best_step=best_step,
        best_validation_exact=best_score[0],
        elapsed_seconds=time.perf_counter() - started,
        history=history,
        binding_calibration=binding_calibration,
    )


@torch.no_grad()
def calibrate_receiver_binding(
    receiver: ReceiverModel,
    messages: Tensor,
    meanings: Tensor,
    *,
    confidence: float,
    freeze: bool,
) -> dict[str, Any]:
    """Select the exact best factor-slot permutation from empirical information."""
    binding_logits = getattr(receiver, "binding_logits", None)
    permutation_matrices = getattr(receiver, "permutation_matrices", None)
    if binding_logits is None or permutation_matrices is None:
        raise ValueError("Binding calibration requires a permutation-slot receiver.")
    if confidence <= 0:
        raise ValueError("Calibration confidence must be positive.")
    factor_count = meanings.shape[1]
    slot_count = messages.shape[1]
    vocabulary_size = receiver.spec.vocabulary_size
    mutual_information = torch.zeros(
        factor_count, slot_count, dtype=torch.float64, device=messages.device
    )
    for factor_index, factor_size in enumerate(receiver.spec.factor_sizes):
        factor_values = meanings[:, factor_index]
        for slot_index in range(slot_count):
            symbols = messages[:, slot_index]
            joint = torch.bincount(
                factor_values * vocabulary_size + symbols,
                minlength=factor_size * vocabulary_size,
            ).reshape(factor_size, vocabulary_size).to(torch.float64)
            joint = joint / joint.sum()
            factor_probability = joint.sum(dim=1, keepdim=True)
            symbol_probability = joint.sum(dim=0, keepdim=True)
            independent = factor_probability * symbol_probability
            mask = joint > 0
            mutual_information[factor_index, slot_index] = (
                joint[mask] * torch.log2(joint[mask] / independent[mask])
            ).sum()
    scores = torch.einsum(
        "pfs,fs->p",
        permutation_matrices.to(mutual_information.dtype),
        mutual_information,
    )
    chosen_index = int(scores.argmax())
    chosen = permutation_matrices[chosen_index]
    binding_logits.copy_(chosen * confidence - (1.0 - chosen) * confidence)
    if freeze:
        binding_logits.requires_grad_(False)
    return {
        "method": "exhaustive_mutual_information_over_24_permutations",
        "chosen_permutation_index": chosen_index,
        "hard_slot_by_factor": chosen.argmax(dim=1).cpu().tolist(),
        "mutual_information_bits": mutual_information.cpu().tolist(),
        "chosen_score": float(scores[chosen_index].cpu()),
        "runner_up_score": float(scores.topk(2).values[1].cpu()),
        "confidence": confidence,
        "binding_frozen": freeze,
    }


@torch.no_grad()
def encode_meanings(sender: nn.Module, meanings: Tensor) -> Tensor:
    sender.eval()
    _, tokens = sender(meanings, sample=False)
    return tokens


@torch.no_grad()
def predict_receiver(receiver: ReceiverModel, messages: Tensor) -> Tensor:
    receiver.eval()
    return torch.stack([head.argmax(dim=-1) for head in receiver(messages)], dim=1)


@torch.no_grad()
def evaluate_system(system: CommunicationSystem, meanings: Tensor) -> dict[str, Any]:
    system.eval()
    messages = encode_meanings(system.sender, meanings)
    return evaluate_receiver(system.receiver, messages, meanings)


@torch.no_grad()
def evaluate_population(
    population: PopulationSystem, meanings: Tensor
) -> dict[str, Any]:
    population.eval()
    pair_metrics: dict[str, dict[str, Any]] = {}
    exact_values = []
    factor_values = []
    for sender_index, sender in enumerate(population.senders):
        messages = encode_meanings(sender, meanings)
        for receiver_index, receiver in enumerate(population.receivers):
            metrics = evaluate_receiver(receiver, messages, meanings)
            pair_metrics[f"s{sender_index}-r{receiver_index}"] = metrics
            exact_values.append(metrics["exact_match"])
            factor_values.append(metrics["factor_accuracy"])
    return {
        "mean_exact_match": float(np.mean(exact_values)),
        "worst_pair_exact_match": float(np.min(exact_values)),
        "best_pair_exact_match": float(np.max(exact_values)),
        "mean_factor_accuracy": np.mean(factor_values, axis=0).tolist(),
        "pairs": pair_metrics,
    }


@torch.no_grad()
def evaluate_receiver(
    receiver: ReceiverModel, messages: Tensor, meanings: Tensor
) -> dict[str, Any]:
    predictions = predict_receiver(receiver, messages)
    factor_correct = predictions.eq(meanings)
    return {
        "exact_match": float(factor_correct.all(dim=1).float().mean().cpu()),
        "factor_accuracy": [
            float(factor_correct[:, index].float().mean().cpu())
            for index in range(factor_correct.shape[1])
        ],
    }


def _factor_loss(logits: tuple[Tensor, ...], targets: Tensor) -> Tensor:
    losses = [
        nn.functional.cross_entropy(factor_logits, targets[:, index])
        for index, factor_logits in enumerate(logits)
    ]
    return torch.stack(losses).mean()


def normalized_factor_minimax_loss(
    logits: tuple[Tensor, ...], targets: Tensor
) -> Tensor:
    """Emphasize the worst relative factor error without binding it to a slot."""
    if len(logits) != targets.shape[1]:
        raise ValueError("Factor-minimax logits must match the target factors.")
    normalized_losses = []
    for index, factor_logits in enumerate(logits):
        class_count = factor_logits.shape[-1]
        if class_count < 2:
            raise ValueError("Factor-minimax factors require at least two classes.")
        factor_loss = nn.functional.cross_entropy(factor_logits, targets[:, index])
        normalized_losses.append(factor_loss / math.log(class_count))
    return torch.stack(normalized_losses).max()


def _geometric_schedule(start: float, end: float, progress: float) -> float:
    if start <= 0 or end <= 0:
        raise ValueError("Temperatures must be positive.")
    return start * math.pow(end / start, progress)
    make_receiver,
