import numpy as np

from ai_taal.baselines import compute_baselines
from ai_taal.metrics import (
    _topographic_pair_indices,
    prediction_metrics,
    protocol_statistics,
    topographic_permutation_test,
)
from ai_taal.world import enumerate_world


def test_handcrafted_protocol_is_unique_and_exact(config):
    meanings = enumerate_world(config)
    messages = np.asarray(
        [
            [meaning.color, meaning.shape, meaning.size * 4 + meaning.texture]
            for meaning in meanings
        ]
    )
    predictions = np.asarray([meaning.factors for meaning in meanings])
    stats = protocol_statistics(meanings, messages)
    accuracy = prediction_metrics(meanings, predictions)
    assert accuracy["exact_match"] == 1.0
    assert stats["unique_message_count"] == 1024
    assert stats["collision_meaning_count"] == 0
    assert stats["topographic_similarity_spearman"] > 0.4
    assert stats["topographic_pair_count"] == 1024 * 1023 // 2
    assert stats["topographic_pair_sampling"] == "all_unordered_pairs"
    assert stats["minimal_pair_mean_position_concentration"] > 0.9


def test_baseline_bit_accounting(config):
    baselines = compute_baselines(enumerate_world(config))
    assert baselines["packed_factor_code_10_bit"]["bits_per_message"] == 10
    assert baselines["handcrafted_compositional_code"]["bits_per_message"] == 12
    assert baselines["dutch_template_utf8"]["mean_bits_per_message"] > 12


def test_scaled_baselines_follow_ecp6_entropy(ecp6_config):
    baselines = compute_baselines(enumerate_world(ecp6_config))
    assert baselines["packed_factor_code_optimal"]["bits_per_message"] == 14
    assert baselines["factor_local_compositional_code"]["bits_per_message"] == 14


def test_handcrafted_topography_beats_random_pairing(config):
    meanings = enumerate_world(config)[:128]
    semantic = np.asarray([meaning.factors for meaning in meanings])
    messages = np.asarray(
        [
            [meaning.color, meaning.shape, meaning.size, meaning.texture]
            for meaning in meanings
        ]
    )
    result = topographic_permutation_test(
        semantic, messages, repetitions=19, seed=123
    )
    assert result["observed"] > result["null_maximum"]
    assert result["empirical_one_sided_p"] == 0.05


def test_topographic_pair_sampling_is_bounded_unique_and_deterministic():
    first = _topographic_pair_indices(2_000, max_pairs=10_000, seed=7)
    second = _topographic_pair_indices(2_000, max_pairs=10_000, seed=7)
    left, right, method = first

    assert np.array_equal(left, second[0])
    assert np.array_equal(right, second[1])
    assert method == "uniform_without_replacement_seeded"
    assert len(left) == 10_000
    assert np.all(left < right)
    assert len(np.unique(left * 2_000 + right)) == 10_000
