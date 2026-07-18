from copy import deepcopy

import torch

from ai_taal.models import (
    BoundedAutoregressiveSender,
    BoundedParallelSender,
    DeepPositionAwareMLPReceiver,
    CommunicationSystem,
    FactorizedPermutationSlotReceiver,
    InjectivePermutationSlotSender,
    LearnedPermutationSlotSender,
    MinimalPermutationSlotSender,
    ModelSpec,
    PositionAwareMLPReceiver,
    load_agent_checkpoint,
    save_agent_checkpoint,
)
from ai_taal.training import meanings_tensor
from ai_taal.worker import main as worker_main
from ai_taal.world import build_splits


def test_discrete_message_and_receiver_shapes(config):
    spec = ModelSpec.from_config(config)
    system = CommunicationSystem(spec)
    meanings = meanings_tensor(build_splits(config).train[:5])
    soft_message, tokens = system.sender(meanings, temperature=1.0, sample=False)
    outputs = system.receiver(soft_message)
    assert soft_message.shape == (5, 4, 16)
    assert tokens.shape == (5, 4)
    assert tokens.dtype == torch.int64
    assert [output.shape for output in outputs] == [
        (5, 8),
        (5, 8),
        (5, 4),
        (5, 4),
    ]
    assert torch.allclose(soft_message.sum(dim=-1), torch.ones(5, 4))


def test_agent_checkpoints_are_separate(config, tmp_path):
    system = CommunicationSystem(ModelSpec.from_config(config))
    sender_path = tmp_path / "sender.pt"
    receiver_path = tmp_path / "receiver.pt"
    save_agent_checkpoint(sender_path, system.sender, kind="sender")
    save_agent_checkpoint(receiver_path, system.receiver, kind="receiver")
    sender = load_agent_checkpoint(sender_path, expected_kind="sender")
    receiver = load_agent_checkpoint(receiver_path, expected_kind="receiver")
    assert type(sender).__name__ == "Sender"
    assert type(receiver).__name__ == "Receiver"
    assert not set(sender.state_dict()).intersection(receiver.state_dict()) == set(
        sender.state_dict()
    )


def test_learned_slot_sender_uses_a_hard_one_to_one_binding(ecp2_config):
    config = deepcopy(ecp2_config)
    config["agents"]["sender"]["family"] = "learned_permutation_slot_sender"
    sender = LearnedPermutationSlotSender(ModelSpec.from_config(config))
    binding = sender.binding_matrix(straight_through=False)

    assert torch.equal(binding.sum(dim=0), torch.ones(4))
    assert torch.equal(binding.sum(dim=1), torch.ones(4))

    left = torch.tensor([[0, 0, 0, 0]])
    right = torch.tensor([[1, 0, 0, 0]])
    left_message = sender.relaxed_message(left)
    right_message = sender.relaxed_message(right)
    color_slot = int(binding[:, 0].argmax())
    unchanged_slots = [index for index in range(4) if index != color_slot]
    assert torch.equal(
        left_message[:, unchanged_slots], right_message[:, unchanged_slots]
    )


def test_learned_slot_sender_checkpoint_round_trip(ecp2_config, tmp_path):
    config = deepcopy(ecp2_config)
    config["agents"]["sender"]["family"] = "learned_permutation_slot_sender"
    sender = LearnedPermutationSlotSender(ModelSpec.from_config(config))
    path = tmp_path / "slot-sender.pt"
    save_agent_checkpoint(path, sender, kind="sender")

    loaded = load_agent_checkpoint(path, expected_kind="sender")

    assert isinstance(loaded, LearnedPermutationSlotSender)
    assert torch.equal(
        sender.binding_matrix(straight_through=False),
        loaded.binding_matrix(straight_through=False),
    )

    input_path = tmp_path / "input.json"
    output_path = tmp_path / "output.json"
    input_path.write_text("[[0,0,0,0],[1,2,3,3]]\n", encoding="utf-8")
    exit_code = worker_main(
        [
            "encode",
            "--checkpoint",
            str(path),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ]
    )
    assert exit_code == 0
    assert output_path.read_text(encoding="utf-8").startswith("[[")


def test_injective_slot_sender_uses_unique_symbols_per_factor(ecp2_config):
    config = deepcopy(ecp2_config)
    config["agents"]["sender"]["family"] = "injective_permutation_slot_sender"
    sender = InjectivePermutationSlotSender(ModelSpec.from_config(config))

    binding = sender.binding_matrix(straight_through=False)
    assert torch.equal(binding.sum(dim=0), torch.ones(4))
    assert torch.equal(binding.sum(dim=1), torch.ones(4))
    for factor_index, factor_size in enumerate(sender.spec.factor_sizes):
        codebook = sender.codebook_matrix(
            factor_index, straight_through=False
        )
        assert codebook.shape == (factor_size, 16)
        assert torch.equal(codebook.sum(dim=1), torch.ones(factor_size))
        assert len(set(codebook.argmax(dim=1).tolist())) == factor_size

    meanings = torch.tensor([[0, 0, 0, 0], [1, 2, 3, 3]])
    symbols, tokens = sender(meanings, sample=False)
    assert symbols.shape == (2, 4, 16)
    assert tokens.shape == (2, 4)
    assert torch.equal(symbols.sum(dim=-1), torch.ones(2, 4))


def test_injective_slot_sender_checkpoint_round_trip(ecp2_config, tmp_path):
    config = deepcopy(ecp2_config)
    config["agents"]["sender"]["family"] = "injective_permutation_slot_sender"
    sender = InjectivePermutationSlotSender(ModelSpec.from_config(config))
    path = tmp_path / "injective-slot-sender.pt"
    save_agent_checkpoint(path, sender, kind="sender")

    loaded = load_agent_checkpoint(path, expected_kind="sender")

    assert isinstance(loaded, InjectivePermutationSlotSender)
    for factor_index in range(4):
        assert torch.equal(
            sender.codebook_matrix(factor_index, straight_through=False),
            loaded.codebook_matrix(factor_index, straight_through=False),
        )


def test_minimal_sender_uses_exact_factor_local_alphabets(ecp4_config):
    sender = MinimalPermutationSlotSender(ModelSpec.from_config(ecp4_config))
    meanings = meanings_tensor(build_splits(ecp4_config).train[:32])
    _, tokens = sender(meanings, sample=False)
    binding = sender.binding_matrix(straight_through=False)

    for factor_index, factor_size in enumerate(sender.spec.factor_sizes):
        codebook = sender.codebook_matrix(factor_index, straight_through=False)
        assert codebook.shape == (factor_size, factor_size)
        assert torch.equal(codebook.sum(dim=0), torch.ones(factor_size))
        assert torch.equal(codebook.sum(dim=1), torch.ones(factor_size))
        slot = int(binding[:, factor_index].argmax())
        assert int(tokens[:, slot].max()) < factor_size


def test_factorized_receiver_cannot_mix_slots(ecp4_config):
    receiver = FactorizedPermutationSlotReceiver(ModelSpec.from_config(ecp4_config))
    binding = receiver.binding_matrix(straight_through=False)
    message = torch.tensor([[0, 1, 2, 3]])
    original = receiver(message)

    for factor_index in range(4):
        selected_slot = int(binding[factor_index].argmax())
        other_slot = (selected_slot + 1) % 4
        changed = message.clone()
        changed[:, other_slot] = (changed[:, other_slot] + 1) % 4
        updated = receiver(changed)
        assert torch.equal(original[factor_index], updated[factor_index])


def test_minimal_sender_and_factorized_receiver_checkpoint_round_trip(
    ecp4_config, tmp_path
):
    spec = ModelSpec.from_config(ecp4_config)
    sender = MinimalPermutationSlotSender(spec)
    receiver = FactorizedPermutationSlotReceiver(spec)
    sender_path = tmp_path / "minimal-sender.pt"
    receiver_path = tmp_path / "factorized-receiver.pt"
    save_agent_checkpoint(sender_path, sender, kind="sender")
    save_agent_checkpoint(receiver_path, receiver, kind="receiver")

    assert isinstance(
        load_agent_checkpoint(sender_path, expected_kind="sender"),
        MinimalPermutationSlotSender,
    )
    assert isinstance(
        load_agent_checkpoint(receiver_path, expected_kind="receiver"),
        FactorizedPermutationSlotReceiver,
    )


def test_bounded_sender_uses_slot_capacity_without_factor_binding(ecp7_config):
    sender = BoundedAutoregressiveSender(ModelSpec.from_config(ecp7_config))
    meanings = meanings_tensor(build_splits(ecp7_config).train[:32])
    symbols, tokens = sender(meanings, sample=False)

    assert symbols.shape == (32, 4, 16)
    assert tokens.shape == (32, 4)
    assert [head.out_features for head in sender.slot_heads] == [16, 16, 8, 8]
    assert int(tokens[:, 0].max()) < 16
    assert int(tokens[:, 1].max()) < 16
    assert int(tokens[:, 2].max()) < 8
    assert int(tokens[:, 3].max()) < 8
    assert not hasattr(sender, "binding_matrix")
    assert not hasattr(sender, "codebook_matrix")
    assert (
        sender.context_projection.in_features
        == 4 * sender.spec.factor_embedding_dim
    )


def test_bounded_sender_checkpoint_round_trip(ecp7_config, tmp_path):
    sender = BoundedAutoregressiveSender(ModelSpec.from_config(ecp7_config))
    path = tmp_path / "bounded-sender.pt"
    save_agent_checkpoint(path, sender, kind="sender")

    loaded = load_agent_checkpoint(path, expected_kind="sender")

    assert isinstance(loaded, BoundedAutoregressiveSender)
    assert loaded.spec.slot_alphabet_sizes == (16, 16, 8, 8)

    input_path = tmp_path / "input.json"
    output_path = tmp_path / "output.json"
    input_path.write_text("[[0,0,0,0],[15,15,7,7]]\n", encoding="utf-8")
    exit_code = worker_main(
        [
            "encode",
            "--checkpoint",
            str(path),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ]
    )
    assert exit_code == 0
    assert output_path.read_text(encoding="utf-8").startswith("[[")


def test_bounded_parallel_sender_uses_one_joint_context(ecp7_b7_config):
    sender = BoundedParallelSender(ModelSpec.from_config(ecp7_b7_config))
    meanings = meanings_tensor(build_splits(ecp7_b7_config).train[:32])
    symbols, tokens = sender(meanings, sample=False)

    assert symbols.shape == (32, 4, 16)
    assert tokens.shape == (32, 4)
    assert [head.out_features for head in sender.slot_heads] == [16, 16, 8, 8]
    assert int(tokens[:, 0].max()) < 16
    assert int(tokens[:, 1].max()) < 16
    assert int(tokens[:, 2].max()) < 8
    assert int(tokens[:, 3].max()) < 8
    assert not hasattr(sender, "recurrent")
    assert not hasattr(sender, "binding_matrix")
    assert not hasattr(sender, "codebook_matrix")
    assert sender.context_projection.in_features == 4 * sender.spec.factor_embedding_dim


def test_bounded_parallel_sender_checkpoint_round_trip(ecp7_b7_config, tmp_path):
    sender = BoundedParallelSender(ModelSpec.from_config(ecp7_b7_config))
    path = tmp_path / "bounded-parallel-sender.pt"
    save_agent_checkpoint(path, sender, kind="sender")

    loaded = load_agent_checkpoint(path, expected_kind="sender")

    assert isinstance(loaded, BoundedParallelSender)
    assert loaded.spec.slot_alphabet_sizes == (16, 16, 8, 8)
    meanings = torch.tensor([[0, 0, 0, 0], [15, 15, 7, 7]])
    expected = sender(meanings, sample=False)[1]
    actual = loaded(meanings, sample=False)[1]
    assert torch.equal(actual, expected)

    input_path = tmp_path / "parallel-input.json"
    output_path = tmp_path / "parallel-output.json"
    input_path.write_text("[[0,0,0,0],[15,15,7,7]]\n", encoding="utf-8")
    exit_code = worker_main(
        [
            "encode",
            "--checkpoint",
            str(path),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ]
    )
    assert exit_code == 0
    assert output_path.read_text(encoding="utf-8").startswith("[[")


def test_position_aware_mlp_receiver_reads_the_complete_message(ecp7_b9_config):
    receiver = PositionAwareMLPReceiver(ModelSpec.from_config(ecp7_b9_config))
    message = torch.tensor([[0, 1, 2, 3], [15, 15, 7, 7]])

    outputs = receiver(message)

    assert [output.shape for output in outputs] == [
        (2, 16),
        (2, 16),
        (2, 8),
        (2, 8),
    ]
    assert receiver.message_projection.in_features == (
        receiver.spec.message_length * receiver.spec.symbol_embedding_dim
    )
    assert not hasattr(receiver, "recurrent")
    assert not hasattr(receiver, "binding_matrix")


def test_position_aware_mlp_receiver_checkpoint_round_trip(
    ecp7_b9_config, tmp_path
):
    receiver = PositionAwareMLPReceiver(ModelSpec.from_config(ecp7_b9_config))
    path = tmp_path / "position-aware-receiver.pt"
    save_agent_checkpoint(path, receiver, kind="receiver")

    loaded = load_agent_checkpoint(path, expected_kind="receiver")

    assert isinstance(loaded, PositionAwareMLPReceiver)
    message = torch.tensor([[0, 1, 2, 3], [15, 15, 7, 7]])
    expected = tuple(output.detach() for output in receiver(message))
    actual = loaded(message)
    assert all(torch.equal(left, right) for left, right in zip(actual, expected))

    input_path = tmp_path / "position-aware-input.json"
    output_path = tmp_path / "position-aware-output.json"
    input_path.write_text("[[0,1,2,3],[15,15,7,7]]\n", encoding="utf-8")
    exit_code = worker_main(
        [
            "decode",
            "--checkpoint",
            str(path),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ]
    )
    assert exit_code == 0
    assert output_path.read_text(encoding="utf-8").startswith("[[")


def test_deep_position_aware_receiver_adds_one_shared_layer(ecp7_b12_config):
    receiver = DeepPositionAwareMLPReceiver(ModelSpec.from_config(ecp7_b12_config))
    message = torch.tensor([[0, 1, 2, 3], [15, 15, 7, 7]])

    outputs = receiver(message)

    assert [output.shape for output in outputs] == [
        (2, 16),
        (2, 16),
        (2, 8),
        (2, 8),
    ]
    assert receiver.hidden_projection.in_features == receiver.spec.hidden_dim
    assert receiver.hidden_projection.out_features == receiver.spec.hidden_dim
    assert not hasattr(receiver, "binding_matrix")
    assert not hasattr(receiver, "factor_projections")


def test_deep_position_aware_receiver_checkpoint_round_trip(
    ecp7_b12_config, tmp_path
):
    receiver = DeepPositionAwareMLPReceiver(ModelSpec.from_config(ecp7_b12_config))
    path = tmp_path / "deep-position-aware-receiver.pt"
    save_agent_checkpoint(path, receiver, kind="receiver")

    loaded = load_agent_checkpoint(path, expected_kind="receiver")

    assert isinstance(loaded, DeepPositionAwareMLPReceiver)
    message = torch.tensor([[0, 1, 2, 3], [15, 15, 7, 7]])
    expected = tuple(output.detach() for output in receiver(message))
    actual = loaded(message)
    assert all(torch.equal(left, right) for left, right in zip(actual, expected))
