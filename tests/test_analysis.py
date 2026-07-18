import json

from ai_taal.analysis import _paired_sign_flip_test, _population_episode_matrices


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
