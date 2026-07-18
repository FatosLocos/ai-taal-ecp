from copy import deepcopy

import torch

from ai_taal.models import (
    BoundedAutoregressiveSender,
    BoundedParallelSender,
    FactorizedPermutationSlotReceiver,
    ModelSpec,
    PopulationSystem,
    Sender,
)
from ai_taal.training import (
    _scheduled_code_utilization_weight,
    _scheduled_collision_replay_weight,
    _scheduled_factor_minimax_weight,
    _scheduled_learning_rate,
    _scheduled_temperature,
    algebraic_consistency_loss,
    atom_code_consensus_loss,
    build_algebraic_quadruples,
    calibrate_receiver_binding,
    collision_pairs_from_messages,
    factor_agnostic_code_utilization_loss,
    mine_sender_collision_pairs,
    normalized_factor_minimax_loss,
    relaxed_collision_pair_probability,
    slot_binding_consensus_loss,
    straight_through_joint_collision_loss,
    straight_through_sender_consensus_loss,
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


def test_extended_horizon_preserves_then_holds_the_registered_temperature(
    ecp7_b9_config, ecp7_b10_config
):
    for step in (1, 200, 2000, 5000):
        assert _scheduled_temperature(
            ecp7_b10_config["training"], step, 15000
        ) == _scheduled_temperature(ecp7_b9_config["training"], step, 5000)

    final_temperature = ecp7_b9_config["training"]["temperature_end"]
    assert _scheduled_temperature(ecp7_b10_config["training"], 5000, 15000) == (
        final_temperature
    )
    assert _scheduled_temperature(ecp7_b10_config["training"], 10000, 15000) == (
        final_temperature
    )
    assert _scheduled_temperature(ecp7_b10_config["training"], 15000, 15000) == (
        final_temperature
    )


def test_utilization_weight_holds_then_decays_linearly(ecp7_b11_config):
    utilization = ecp7_b11_config["training"]["code_utilization"]
    assert _scheduled_code_utilization_weight(utilization, 1) == 0.0025
    assert _scheduled_code_utilization_weight(utilization, 400) == 1.0
    assert _scheduled_code_utilization_weight(utilization, 5000) == 1.0
    assert _scheduled_code_utilization_weight(utilization, 10000) == 0.55
    assert _scheduled_code_utilization_weight(utilization, 15000) == 0.1
    assert _scheduled_code_utilization_weight(utilization, 16000) == 0.1


def test_learning_rate_holds_then_decays_linearly(ecp7_b14_config):
    training = ecp7_b14_config["training"]
    assert _scheduled_learning_rate(training, 1) == 0.001
    assert _scheduled_learning_rate(training, 5000) == 0.001
    assert _scheduled_learning_rate(training, 10000) == 0.00055
    assert _scheduled_learning_rate(training, 15000) == 0.0001
    assert _scheduled_learning_rate(training, 16000) == 0.0001


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


def test_algebraic_consistency_supports_the_bounded_parallel_sender(
    ecp7_b8_config,
):
    split = build_splits(ecp7_b8_config)
    sender = BoundedParallelSender(ModelSpec.from_config(ecp7_b8_config))
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


def test_joint_collision_loss_counts_only_distinct_input_collisions():
    symbols = torch.tensor(
        [
            [0, 1, 0, 1],
            [0, 1, 0, 1],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
        ]
    )
    messages = torch.nn.functional.one_hot(symbols, num_classes=2).to(torch.float32)
    meanings = torch.tensor(
        [
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0],
        ]
    )

    loss = straight_through_joint_collision_loss(messages, meanings)

    assert abs(float(loss) - 1.0) < 1e-6


def test_joint_collision_loss_backpropagates_through_hard_messages(ecp7_b4_config):
    sender = BoundedAutoregressiveSender(ModelSpec.from_config(ecp7_b4_config))
    meanings = torch.tensor(
        [[0, 0, 0, 0], [1, 2, 3, 4], [15, 15, 7, 7]], dtype=torch.long
    )
    messages, _ = sender(meanings, temperature=1.0, sample=True)

    loss = straight_through_joint_collision_loss(messages, meanings)
    loss.backward()

    assert torch.isfinite(loss)
    assert any(parameter.grad is not None for parameter in sender.parameters())


def test_collision_pair_mining_returns_all_unordered_collisions():
    messages = torch.tensor(
        [[0, 0], [1, 1], [0, 0], [0, 0], [1, 1], [2, 2]]
    )

    pairs = collision_pairs_from_messages(messages)

    assert pairs.tolist() == [[0, 2], [0, 3], [2, 3], [1, 4]]


def test_collision_pair_mining_uses_a_senders_hard_training_code(
    ecp7_b17_config,
):
    sender = BoundedParallelSender(ModelSpec.from_config(ecp7_b17_config))
    with torch.no_grad():
        for parameter in sender.parameters():
            parameter.zero_()
    meanings = torch.tensor(
        [[0, 0, 0, 0], [1, 0, 0, 0], [2, 1, 0, 0], [3, 1, 1, 0]],
        dtype=torch.long,
    )

    pairs = mine_sender_collision_pairs(sender, meanings)

    assert len(pairs) == 6


def test_relaxed_collision_replay_measures_full_message_probability():
    symbol_pairs = torch.tensor(
        [
            [[0, 1], [0, 1]],
            [[0, 1], [1, 1]],
        ]
    )
    message_pairs = torch.nn.functional.one_hot(
        symbol_pairs, num_classes=2
    ).to(torch.float32)

    loss = relaxed_collision_pair_probability(message_pairs)

    assert abs(float(loss) - 0.5) < 1e-6


def test_relaxed_collision_replay_backpropagates(ecp7_b17_config):
    sender = BoundedParallelSender(ModelSpec.from_config(ecp7_b17_config))
    pair_meanings = torch.tensor(
        [
            [[0, 0, 0, 0], [1, 0, 0, 0]],
            [[2, 3, 4, 5], [2, 4, 4, 5]],
        ],
        dtype=torch.long,
    )
    messages = sender.relaxed_message(
        pair_meanings.reshape(4, 4), temperature=1.0
    ).reshape(2, 2, 4, 16)

    loss = relaxed_collision_pair_probability(messages)
    loss.backward()

    assert torch.isfinite(loss)
    assert any(parameter.grad is not None for parameter in sender.parameters())


def test_sender_consensus_loss_measures_pairwise_symbol_disagreement():
    left_symbols = torch.tensor([[0, 0], [1, 1]])
    right_symbols = torch.tensor([[0, 0], [0, 1]])
    left = torch.nn.functional.one_hot(left_symbols, num_classes=2).to(torch.float32)
    right = torch.nn.functional.one_hot(right_symbols, num_classes=2).to(
        torch.float32
    )

    identical_loss = straight_through_sender_consensus_loss([left, left])
    disagreement_loss = straight_through_sender_consensus_loss([left, right])

    assert abs(float(identical_loss)) < 1e-6
    assert abs(float(disagreement_loss) - 0.25) < 1e-6


def test_sender_consensus_loss_backpropagates_through_hard_messages(
    ecp7_b5_config,
):
    meanings = torch.tensor(
        [[0, 0, 0, 0], [1, 2, 3, 4], [15, 15, 7, 7]], dtype=torch.long
    )
    senders = [
        BoundedAutoregressiveSender(ModelSpec.from_config(ecp7_b5_config))
        for _ in range(2)
    ]
    messages = [
        sender(meanings, temperature=1.0, sample=True)[0] for sender in senders
    ]

    loss = straight_through_sender_consensus_loss(messages)
    loss.backward()

    assert torch.isfinite(loss)
    assert all(
        any(parameter.grad is not None for parameter in sender.parameters())
        for sender in senders
    )


def test_normalized_factor_minimax_targets_the_worst_relative_factor():
    easy_logits = torch.tensor([[10.0, -10.0]], requires_grad=True)
    worst_logits = torch.tensor([[0.0, 0.0]], requires_grad=True)
    targets = torch.tensor([[0, 0]])

    loss = normalized_factor_minimax_loss((easy_logits, worst_logits), targets)
    loss.backward()

    assert abs(float(loss.detach()) - 1.0) < 1e-6
    assert worst_logits.grad is not None
    assert bool(torch.any(worst_logits.grad != 0))
    assert easy_logits.grad is not None
    assert bool(torch.all(easy_logits.grad == 0))


def test_late_factor_minimax_weight_starts_warms_and_holds():
    schedule = {
        "weight": 1.0,
        "start_step": 15000,
        "warmup_steps": 5000,
    }

    assert _scheduled_factor_minimax_weight(schedule, 1) == 0.0
    assert _scheduled_factor_minimax_weight(schedule, 15000) == 0.0
    assert _scheduled_factor_minimax_weight(schedule, 17500) == 0.5
    assert _scheduled_factor_minimax_weight(schedule, 20000) == 1.0
    assert _scheduled_factor_minimax_weight(schedule, 30000) == 1.0


def test_factor_minimax_schedule_preserves_zero_start_behavior():
    schedule = {"weight": 1.0, "warmup_steps": 400}

    assert _scheduled_factor_minimax_weight(schedule, 1) == 1 / 400
    assert _scheduled_factor_minimax_weight(schedule, 400) == 1.0
    assert _scheduled_factor_minimax_weight(schedule, 5000) == 1.0


def test_late_collision_replay_weight_starts_warms_and_holds():
    schedule = {
        "weight": 1.0,
        "start_step": 15000,
        "warmup_steps": 5000,
    }

    assert _scheduled_collision_replay_weight(schedule, 1) == 0.0
    assert _scheduled_collision_replay_weight(schedule, 15000) == 0.0
    assert _scheduled_collision_replay_weight(schedule, 17500) == 0.5
    assert _scheduled_collision_replay_weight(schedule, 20000) == 1.0
    assert _scheduled_collision_replay_weight(schedule, 30000) == 1.0


def test_attenuated_collision_replay_weight_stays_at_task_scale(
    ecp7_b18_config,
):
    schedule = ecp7_b18_config["training"]["global_collision_replay"]

    assert _scheduled_collision_replay_weight(schedule, 15000) == 0.0
    assert _scheduled_collision_replay_weight(schedule, 17500) == 0.05
    assert _scheduled_collision_replay_weight(schedule, 20000) == 0.1
    assert _scheduled_collision_replay_weight(schedule, 30000) == 0.1


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
