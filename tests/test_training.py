from copy import deepcopy

import torch

from ai_taal.models import (
    BoundedAutoregressiveSender,
    FactorizedPermutationSlotReceiver,
    ModelSpec,
    PopulationSystem,
    Sender,
)
from ai_taal.training import (
    algebraic_consistency_loss,
    atom_code_consensus_loss,
    build_algebraic_quadruples,
    calibrate_receiver_binding,
    factor_agnostic_code_utilization_loss,
    slot_binding_consensus_loss,
    train_communication_system,
)
from ai_taal.world import build_splits, enumerate_world


def test_two_training_steps_complete(config):
    split = build_splits(config)
    system, result = train_communication_system(
        config,
        split.train,
        split.validation,
        seed=11,
        max_steps_override=2,
    )
    assert result.best_step in {1, 2}
    assert 0.0 <= result.best_validation_exact <= 1.0
    assert system.sender.spec.message_length == 4


def test_algebraic_quadruples_use_only_training_meanings_and_same_transition(
    ecp2_config,
):
    split = build_splits(ecp2_config)
    quadruples = build_algebraic_quadruples(
        split.train,
        factor_sizes=ModelSpec.from_config(ecp2_config).factor_sizes,
        sample_count=64,
        seed=123,
    )
    train_rows = {meaning.factors for meaning in split.train}
    for left, right, left_changed, right_changed in quadruples.tolist():
        assert all(
            tuple(row) in train_rows
            for row in (left, right, left_changed, right_changed)
        )
        left_delta = [index for index in range(4) if left[index] != left_changed[index]]
        right_delta = [
            index for index in range(4) if right[index] != right_changed[index]
        ]
        assert left_delta == right_delta
        assert len(left_delta) == 1
        factor = left_delta[0]
        assert (left[factor], left_changed[factor]) == (
            right[factor],
            right_changed[factor],
        )


def test_algebraic_consistency_loss_backpropagates(ecp2_config):
    split = build_splits(ecp2_config)
    sender = Sender(ModelSpec.from_config(ecp2_config))
    quadruples = build_algebraic_quadruples(
        split.train,
        factor_sizes=sender.spec.factor_sizes,
        sample_count=8,
        seed=456,
    )

    loss = algebraic_consistency_loss(sender, quadruples, temperature=1.0)
    loss.backward()

    assert torch.isfinite(loss)
    assert loss.item() >= 0.0
    assert any(parameter.grad is not None for parameter in sender.parameters())


def test_slot_binding_consensus_loss_backpropagates(ecp2_config):
    config = deepcopy(ecp2_config)
    config["agents"]["sender"]["family"] = "learned_permutation_slot_sender"
    population = PopulationSystem(
        ModelSpec.from_config(config), sender_count=4, receiver_count=4
    )
    loss = slot_binding_consensus_loss(population, sharpness_weight=0.1)

    loss.backward()

    assert torch.isfinite(loss)
    assert loss.item() > 0.0
    assert all(sender.binding_logits.grad is not None for sender in population.senders)


def test_atom_code_consensus_loss_backpropagates(ecp2_config):
    config = deepcopy(ecp2_config)
    config["agents"]["sender"]["family"] = "injective_permutation_slot_sender"
    population = PopulationSystem(
        ModelSpec.from_config(config), sender_count=4, receiver_count=4
    )
    loss = atom_code_consensus_loss(population, sharpness_weight=0.1)

    loss.backward()

    assert torch.isfinite(loss)
    assert loss.item() > 0.0
    assert all(
        all(logits.grad is not None for logits in sender.codebook_logits)
        for sender in population.senders
    )


def test_factor_agnostic_code_utilization_backpropagates(ecp7_b2_config):
    sender = BoundedAutoregressiveSender(ModelSpec.from_config(ecp7_b2_config))
    meanings = torch.tensor(
        [[0, 0, 0, 0], [1, 2, 3, 4], [15, 15, 7, 7]], dtype=torch.long
    )

    loss = factor_agnostic_code_utilization_loss(
        sender,
        meanings,
        temperature=1.0,
        independence_weight=1.0,
    )
    loss.backward()

    assert torch.isfinite(loss)
    assert any(parameter.grad is not None for parameter in sender.parameters())


def test_straight_through_code_utilization_is_discrete_and_backpropagates(
    ecp7_b3_config,
):
    sender = BoundedAutoregressiveSender(ModelSpec.from_config(ecp7_b3_config))
    meanings = torch.tensor(
        [[0, 0, 0, 0], [1, 2, 3, 4], [15, 15, 7, 7]], dtype=torch.long
    )
    messages, _ = sender(meanings, temperature=1.0, sample=True)

    assert torch.all((messages == 0) | (messages == 1))
    loss = factor_agnostic_code_utilization_loss(
        sender,
        meanings,
        temperature=1.0,
        independence_weight=1.0,
        message_distributions=messages,
    )
    loss.backward()

    assert torch.isfinite(loss)
    assert any(parameter.grad is not None for parameter in sender.parameters())


def test_code_utilization_prefers_independent_balanced_slots():
    class FixedSender:
        class Spec:
            slot_alphabet_sizes = (2, 2)
            message_length = 2

        spec = Spec()

        def __init__(self, symbols):
            self.distributions = torch.nn.functional.one_hot(
                torch.tensor(symbols), num_classes=2
            ).to(torch.float32)

        def relaxed_message(self, meanings, *, temperature):
            return self.distributions

    meanings = torch.zeros((4, 4), dtype=torch.long)
    independent = FixedSender([[0, 0], [0, 1], [1, 0], [1, 1]])
    correlated = FixedSender([[0, 0], [0, 0], [1, 1], [1, 1]])

    independent_loss = factor_agnostic_code_utilization_loss(
        independent, meanings, temperature=1.0, independence_weight=1.0
    )
    correlated_loss = factor_agnostic_code_utilization_loss(
        correlated, meanings, temperature=1.0, independence_weight=1.0
    )

    assert abs(float(independent_loss) + 1.0) < 1e-6
    assert abs(float(correlated_loss)) < 1e-6


def test_receiver_binding_calibration_recovers_exact_permutation(ecp4_config):
    receiver = FactorizedPermutationSlotReceiver(ModelSpec.from_config(ecp4_config))
    meanings = torch.tensor(
        [meaning.factors for meaning in enumerate_world(ecp4_config)],
        dtype=torch.long,
    )
    slot_by_factor = [2, 0, 3, 1]
    messages = torch.zeros(len(meanings), 4, dtype=torch.long)
    for factor_index, slot_index in enumerate(slot_by_factor):
        messages[:, slot_index] = meanings[:, factor_index]

    diagnostics = calibrate_receiver_binding(
        receiver, messages, meanings, confidence=8.0, freeze=True
    )

    assert diagnostics["hard_slot_by_factor"] == slot_by_factor
    assert (
        receiver.binding_matrix(straight_through=False).argmax(dim=1).tolist()
        == slot_by_factor
    )
    assert receiver.binding_logits.requires_grad is False
