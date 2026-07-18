import json

from ai_taal.analysis import (
    _discrete_channel_audit,
    _paired_sign_flip_test,
    _population_episode_matrices,
)


def test_population_episode_matrices_count_all_rows_and_deduplicate_receivers(tmp_path):
    episodes = []
    for sender in range(2):
        for receiver in range(2):
            episodes.append(
                {
                    "meaning": {
                        "color": f"c{sender}",
                        "shape": "s0",
                        "size": "z0",
                        "texture": "t0",
                    },
                    "message": {
                        "sender_id": f"sender-{sender}",
                        "receiver_id": f"receiver-{receiver}",
                        "symbols": [sender, 1, 2, 3],
                    },
                }
            )
    path = tmp_path / "episodes.jsonl"
    path.write_text(
        "".join(json.dumps(episode) + "\n" for episode in episodes),
        encoding="utf-8",
    )

    matrices, episode_count = _population_episode_matrices(path)

    assert episode_count == 4
    assert sorted(matrices) == ["sender-0", "sender-1"]
    assert all(semantic.shape == (1, 4) for semantic, _ in matrices.values())
    assert all(messages.shape == (1, 4) for _, messages in matrices.values())


def test_paired_sign_flip_test_enumerates_exact_null():
    result = _paired_sign_flip_test([0.1, 0.2, 0.3, 0.4, 0.5])

    assert result["null_combinations"] == 32
    assert result["observed_mean_difference"] == 0.3
    assert result["exact_one_sided_p"] == 1 / 32


def test_slot_local_channel_audit_checks_each_position_capacity(tmp_path):
    episode = {
        "message": {
            "sender_id": "sender-0",
            "channel_bits": 14,
            "symbols": [15, 15, 7, 7],
        }
    }
    path = tmp_path / "episodes.jsonl"
    path.write_text(json.dumps(episode) + "\n", encoding="utf-8")
    config = {
        "channel": {
            "type": "slot_local_discrete_fixed_length",
            "bits_per_message": 14,
            "slot_alphabet_sizes": [16, 16, 8, 8],
        }
    }

    audit = _discrete_channel_audit(path, {}, config)

    assert audit["applicable"] is True
    assert audit["valid"] is True
    assert audit["checked_episode_messages"] == 1


def test_slot_local_channel_audit_rejects_a_symbol_outside_its_slot(tmp_path):
    episode = {
        "message": {
            "sender_id": "sender-0",
            "channel_bits": 14,
            "symbols": [15, 15, 8, 7],
        }
    }
    path = tmp_path / "episodes.jsonl"
    path.write_text(json.dumps(episode) + "\n", encoding="utf-8")
    config = {
        "channel": {
            "type": "slot_local_discrete_fixed_length",
            "bits_per_message": 14,
            "slot_alphabet_sizes": [16, 16, 8, 8],
        }
    }

    audit = _discrete_channel_audit(path, {}, config)

    assert audit["valid"] is False
    assert audit["violations"][0]["slot"] == 2


def test_global_fixed_length_channel_audit_checks_full_vocabulary(tmp_path):
    episode = {
        "message": {
            "sender_id": "sender-0",
            "channel_bits": 16,
            "symbols": [15, 8, 15, 8],
        }
    }
    path = tmp_path / "episodes.jsonl"
    path.write_text(json.dumps(episode) + "\n", encoding="utf-8")
    config = {
        "channel": {
            "type": "discrete_fixed_length",
            "bits_per_message": 16,
            "message_length": 4,
            "vocabulary_size": 16,
        }
    }

    audit = _discrete_channel_audit(path, {}, config)

    assert audit["applicable"] is True
    assert audit["valid"] is True
    assert audit["slot_alphabet_sizes"] == [16, 16, 16, 16]


def test_global_fixed_length_channel_audit_rejects_invalid_message(tmp_path):
    episode = {
        "message": {
            "sender_id": "sender-0",
            "channel_bits": 15,
            "symbols": [0, 16, 2],
        }
    }
    path = tmp_path / "episodes.jsonl"
    path.write_text(json.dumps(episode) + "\n", encoding="utf-8")
    config = {
        "channel": {
            "type": "discrete_fixed_length",
            "bits_per_message": 16,
            "message_length": 4,
            "vocabulary_size": 16,
        }
    }

    audit = _discrete_channel_audit(path, {}, config)

    assert audit["valid"] is False
    assert {violation["reason"] for violation in audit["violations"]} == {
        "incorrect_channel_bits",
        "incorrect_message_length",
        "symbol_outside_local_alphabet",
    }
