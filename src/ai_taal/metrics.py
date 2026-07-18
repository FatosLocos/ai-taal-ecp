"""Protocol measurements that go beyond task accuracy alone."""

from __future__ import annotations

import math
from collections import Counter
from itertools import combinations
from typing import Any, Iterable

import numpy as np

from ai_taal.world import Meaning


MAX_TOPOGRAPHIC_PAIRS = 1_000_000


def prediction_metrics(
    meanings: Iterable[Meaning], predictions: np.ndarray
) -> dict[str, Any]:
    targets = np.asarray([meaning.factors for meaning in meanings], dtype=np.int64)
    predictions = np.asarray(predictions, dtype=np.int64)
    if predictions.shape != targets.shape:
        raise ValueError(f"Predictions have shape {predictions.shape}; expected {targets.shape}.")
    correct = predictions == targets
    return {
        "exact_match": float(np.mean(np.all(correct, axis=1))),
        "factor_accuracy": [float(np.mean(correct[:, index])) for index in range(4)],
    }


def protocol_statistics(
    meanings: Iterable[Meaning], messages: np.ndarray
) -> dict[str, Any]:
    meanings = tuple(meanings)
    semantic = np.asarray([meaning.factors for meaning in meanings], dtype=np.int16)
    messages = np.asarray(messages, dtype=np.int16)
    if messages.ndim != 2 or messages.shape[0] != semantic.shape[0]:
        raise ValueError("Messages and meanings have incompatible shapes.")

    message_tuples = [tuple(int(value) for value in row) for row in messages]
    counts = Counter(message_tuples)
    probabilities = np.asarray(list(counts.values()), dtype=np.float64) / len(messages)
    entropy = -float(np.sum(probabilities * np.log2(probabilities)))
    topographic, topographic_pair_count, topographic_sampling = (
        _topographic_similarity(semantic, messages)
    )
    minimal = _minimal_pair_statistics(semantic, messages)
    return {
        "meaning_count": len(meanings),
        "unique_message_count": len(counts),
        "collision_meaning_count": len(messages) - len(counts),
        "max_meanings_per_message": max(counts.values()),
        "message_entropy_bits": entropy,
        "message_entropy_fraction_of_source": entropy / math.log2(len(meanings)),
        "topographic_similarity_spearman": topographic,
        "topographic_pair_count": topographic_pair_count,
        "topographic_pair_sampling": topographic_sampling,
        **minimal,
    }


def shuffled_exact_match(
    meanings: Iterable[Meaning],
    messages: np.ndarray,
    decode,
    *,
    seed: int,
) -> float:
    rng = np.random.default_rng(seed)
    shuffled = np.asarray(messages)[rng.permutation(len(messages))]
    predictions = decode(shuffled)
    return prediction_metrics(meanings, predictions)["exact_match"]


def topographic_permutation_test(
    semantic: np.ndarray,
    messages: np.ndarray,
    *,
    repetitions: int,
    seed: int,
) -> dict[str, Any]:
    """Compare observed semantic geometry with random assignments."""
    if repetitions < 1:
        raise ValueError("At least one permutation is required.")
    semantic = np.asarray(semantic, dtype=np.int16)
    messages = np.asarray(messages, dtype=np.int16)
    if semantic.shape[0] != messages.shape[0]:
        raise ValueError("Meanings and messages must have the same number of rows.")

    left_indices, right_indices, sampling = _topographic_pair_indices(
        len(semantic), max_pairs=MAX_TOPOGRAPHIC_PAIRS, seed=seed + 31
    )
    semantic_distance = np.count_nonzero(
        semantic[left_indices] != semantic[right_indices], axis=1
    )
    semantic_rank = _rank_discrete(semantic_distance)
    observed_distance = np.count_nonzero(
        messages[left_indices] != messages[right_indices], axis=1
    )
    observed = _pearson(semantic_rank, _rank_discrete(observed_distance))

    rng = np.random.default_rng(seed)
    null_values = np.empty(repetitions, dtype=np.float64)
    for index in range(repetitions):
        permutation = rng.permutation(len(messages))
        permuted_distance = np.count_nonzero(
            messages[permutation[left_indices]]
            != messages[permutation[right_indices]],
            axis=1,
        )
        null_values[index] = _pearson(
            semantic_rank, _rank_discrete(permuted_distance)
        )
    p_value = (1 + int(np.count_nonzero(null_values >= observed))) / (repetitions + 1)
    return {
        "observed": observed,
        "pair_count": len(left_indices),
        "pair_sampling": sampling,
        "null_repetitions": repetitions,
        "null_mean": float(null_values.mean()),
        "null_standard_deviation": float(null_values.std()),
        "null_maximum": float(null_values.max()),
        "empirical_one_sided_p": p_value,
    }


def _topographic_similarity(
    semantic: np.ndarray, messages: np.ndarray
) -> tuple[float, int, str]:
    left_indices, right_indices, sampling = _topographic_pair_indices(
        len(semantic), max_pairs=MAX_TOPOGRAPHIC_PAIRS, seed=0
    )
    semantic_distance = np.count_nonzero(
        semantic[left_indices] != semantic[right_indices], axis=1
    )
    message_distance = np.count_nonzero(
        messages[left_indices] != messages[right_indices], axis=1
    )
    return (
        _spearman_with_ties(semantic_distance, message_distance),
        len(left_indices),
        sampling,
    )


def _topographic_pair_indices(
    row_count: int, *, max_pairs: int, seed: int
) -> tuple[np.ndarray, np.ndarray, str]:
    """Return all pairs or a reproducible uniform sample without replacement."""
    if row_count < 2:
        raise ValueError("Topographic similarity requires at least two rows.")
    if max_pairs < 1:
        raise ValueError("max_pairs must be positive.")

    total_pairs = row_count * (row_count - 1) // 2
    if total_pairs <= max_pairs:
        left, right = np.triu_indices(row_count, k=1)
        return left, right, "all_unordered_pairs"

    rng = np.random.default_rng(seed)
    ranks = rng.choice(total_pairs, size=max_pairs, replace=False, shuffle=False)
    diagonal = 2 * row_count - 1
    left = np.floor(
        (diagonal - np.sqrt(diagonal * diagonal - 8 * ranks)) / 2
    ).astype(np.int64)
    row_start = left * (2 * row_count - left - 1) // 2
    right = left + 1 + (ranks - row_start)
    return left, right.astype(np.int64), "uniform_without_replacement_seeded"


def _spearman_with_ties(left: np.ndarray, right: np.ndarray) -> float:
    left_rank = _rankdata(left)
    right_rank = _rankdata(right)
    if np.std(left_rank) == 0 or np.std(right_rank) == 0:
        return 0.0
    return float(np.corrcoef(left_rank, right_rank)[0, 1])


def _rankdata(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values)
    order = np.argsort(values, kind="mergesort")
    sorted_values = values[order]
    ranks = np.empty(len(values), dtype=np.float64)
    start = 0
    while start < len(values):
        end = start + 1
        while end < len(values) and sorted_values[end] == sorted_values[start]:
            end += 1
        average_rank = (start + end - 1) / 2.0
        ranks[order[start:end]] = average_rank
        start = end
    return ranks


def _rank_discrete(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=np.int64)
    counts = np.bincount(values)
    average_ranks = np.zeros(len(counts), dtype=np.float64)
    offset = 0
    for value, count in enumerate(counts):
        if count:
            average_ranks[value] = offset + (count - 1) / 2.0
            offset += int(count)
    return average_ranks[values]


def _pearson(left: np.ndarray, right: np.ndarray) -> float:
    if np.std(left) == 0 or np.std(right) == 0:
        return 0.0
    return float(np.corrcoef(left, right)[0, 1])


def _minimal_pair_statistics(
    semantic: np.ndarray, messages: np.ndarray
) -> dict[str, Any]:
    factor_distance: list[float] = []
    factor_position_concentration: list[float] = []
    for factor_index in range(semantic.shape[1]):
        groups: dict[tuple[int, ...], list[int]] = {}
        for index, row in enumerate(semantic):
            key = tuple(
                int(value) for position, value in enumerate(row) if position != factor_index
            )
            groups.setdefault(key, []).append(index)

        distances: list[int] = []
        changed_positions = np.zeros(messages.shape[1], dtype=np.int64)
        for indices in groups.values():
            for left, right in combinations(indices, 2):
                changes = messages[left] != messages[right]
                distance = int(np.count_nonzero(changes))
                distances.append(distance)
                changed_positions += changes.astype(np.int64)
        factor_distance.append(float(np.mean(distances)) if distances else 0.0)
        total_changes = int(changed_positions.sum())
        factor_position_concentration.append(
            float(changed_positions.max() / total_changes) if total_changes else 0.0
        )

    return {
        "minimal_pair_mean_message_distance_by_factor": factor_distance,
        "minimal_pair_position_concentration_by_factor": factor_position_concentration,
        "minimal_pair_mean_message_distance": float(np.mean(factor_distance)),
        "minimal_pair_mean_position_concentration": float(
            np.mean(factor_position_concentration)
        ),
    }
