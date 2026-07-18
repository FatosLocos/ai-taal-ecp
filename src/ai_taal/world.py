"""The fully synthetic ECP world and deterministic data splitting."""

from __future__ import annotations

import itertools
import random
from dataclasses import dataclass
from typing import Any, Iterable

from ai_taal.config import canonical_sha256


FACTOR_NAMES = ("color", "shape", "size", "texture")


@dataclass(frozen=True, slots=True)
class Meaning:
    meaning_id: int
    color: int
    shape: int
    size: int
    texture: int

    @property
    def factors(self) -> tuple[int, int, int, int]:
        return (self.color, self.shape, self.size, self.texture)

    def to_schema_dict(self) -> dict[str, int | str]:
        return {
            "meaning_id": self.meaning_id,
            "color": f"c{self.color}",
            "shape": f"s{self.shape}",
            "size": f"z{self.size}",
            "texture": f"t{self.texture}",
        }


@dataclass(frozen=True, slots=True)
class WorldSplit:
    train: tuple[Meaning, ...]
    validation: tuple[Meaning, ...]
    compositional_test: tuple[Meaning, ...]
    held_out_color_shape_pairs: tuple[tuple[int, int], ...]
    held_out_validation_color_shape_pairs: tuple[tuple[int, int], ...] = ()
    held_out_factor_names: tuple[str, str] = ("color", "shape")

    def manifest(self) -> dict[str, Any]:
        payload = {
            "splits": {
                "train": [meaning.meaning_id for meaning in self.train],
                "validation": [meaning.meaning_id for meaning in self.validation],
                "compositional_test": [
                    meaning.meaning_id for meaning in self.compositional_test
                ],
            },
        }
        left_name, right_name = self.held_out_factor_names
        if self.held_out_factor_names == ("color", "shape"):
            payload["held_out_color_shape_pairs"] = [
                {"color": left, "shape": right}
                for left, right in self.held_out_color_shape_pairs
            ]
            if self.held_out_validation_color_shape_pairs:
                payload["held_out_validation_color_shape_pairs"] = [
                    {"color": left, "shape": right}
                    for left, right in self.held_out_validation_color_shape_pairs
                ]
        else:
            payload["held_out_factor_names"] = [left_name, right_name]
            payload["held_out_factor_pairs"] = [
                {left_name: left, right_name: right}
                for left, right in self.held_out_color_shape_pairs
            ]
            if self.held_out_validation_color_shape_pairs:
                payload["held_out_validation_factor_pairs"] = [
                    {left_name: left, right_name: right}
                    for left, right in self.held_out_validation_color_shape_pairs
                ]
        return {**payload, "sha256": canonical_sha256(payload)}


def enumerate_world(config: dict[str, Any]) -> tuple[Meaning, ...]:
    factors = config["world"]["factors"]
    sizes = [len(factors[name]["values"]) for name in FACTOR_NAMES]
    meanings: list[Meaning] = []
    for meaning_id, values in enumerate(itertools.product(*(range(size) for size in sizes))):
        meanings.append(Meaning(meaning_id, *values))
    return tuple(meanings)


def build_splits(config: dict[str, Any]) -> WorldSplit:
    meanings = enumerate_world(config)
    dataset = config["dataset"]
    rng = random.Random(config["reproducibility"]["dataset_seed"])

    held_out_factor_names = tuple(dataset.get("holdout_factors", ("color", "shape")))
    if len(held_out_factor_names) != 2 or any(
        name not in FACTOR_NAMES for name in held_out_factor_names
    ):
        raise ValueError("holdout_factors must contain two valid, distinct factors.")
    if held_out_factor_names[0] == held_out_factor_names[1]:
        raise ValueError("holdout_factors must contain two distinct factors.")
    left_name, right_name = held_out_factor_names
    left_index = FACTOR_NAMES.index(left_name)
    right_index = FACTOR_NAMES.index(right_name)
    left_count = len(config["world"]["factors"][left_name]["values"])
    right_count = len(config["world"]["factors"][right_name]["values"])
    holdout_count = dataset.get(
        "held_out_factor_pairs", dataset.get("held_out_color_shape_pairs")
    )
    if left_count != right_count or holdout_count != left_count:
        raise ValueError(
            "A held-out matching requires equal factor sizes and one pair per value."
        )

    excluded_values = dataset.get(
        "excluded_factor_pairs", dataset.get("excluded_color_shape_pairs", [])
    )
    excluded_pairs = {
        (int(pair[left_name]), int(pair[right_name])) for pair in excluded_values
    }
    validation_holdout_count = dataset.get(
        "validation_held_out_factor_pairs",
        dataset.get("validation_held_out_color_shape_pairs", 0),
    )
    held_out_validation: tuple[tuple[int, int], ...] = ()
    explicit_validation = dataset.get(
        "explicit_validation_factor_pairs",
        dataset.get("explicit_validation_color_shape_pairs"),
    )
    explicit_test = dataset.get(
        "explicit_test_factor_pairs", dataset.get("explicit_test_color_shape_pairs")
    )
    if (explicit_validation is None) != (explicit_test is None):
        raise ValueError(
            "Explicit validation and test matchings must be provided together."
        )
    if explicit_validation is not None:
        held_out_validation = _parse_explicit_matching(
            explicit_validation,
            left_count,
            left_name=left_name,
            right_name=right_name,
            purpose="validation matching",
        )
        held_out = _parse_explicit_matching(
            explicit_test,
            left_count,
            left_name=left_name,
            right_name=right_name,
            purpose="test matching",
        )
        if set(held_out_validation) & set(held_out):
            raise ValueError("Explicit validation and test matchings overlap.")
        if not (set(held_out_validation) | set(held_out)).isdisjoint(excluded_pairs):
            raise ValueError("Explicit matchings contain previously excluded pairs.")
    elif validation_holdout_count:
        if validation_holdout_count != left_count:
            raise ValueError(
                "A compositional validation matching requires one pair per value."
            )
        held_out_validation = _sample_matching(
            rng, left_count, excluded_pairs, purpose="validation matching"
        )
        held_out = _sample_matching(
            rng,
            left_count,
            excluded_pairs | set(held_out_validation),
            purpose="test matching",
        )
    else:
        held_out = _sample_matching(
            rng,
            left_count,
            excluded_pairs,
            purpose="test matching",
        )
    held_out_set = set(held_out)

    test = tuple(
        meaning
        for meaning in meanings
        if (meaning.factors[left_index], meaning.factors[right_index]) in held_out_set
    )
    candidates = [
        meaning
        for meaning in meanings
        if (meaning.factors[left_index], meaning.factors[right_index]) not in held_out_set
    ]

    validation_count = dataset["validation_meanings"]
    if held_out_validation:
        validation_set = set(held_out_validation)
        validation = [
            meaning
            for meaning in candidates
            if (meaning.factors[left_index], meaning.factors[right_index])
            in validation_set
        ]
        train = [
            meaning
            for meaning in candidates
            if (meaning.factors[left_index], meaning.factors[right_index])
            not in validation_set
        ]
        if len(validation) != validation_count:
            raise RuntimeError("Compositional validation matching has the wrong size.")
    else:
        validation = None
        train = None
        for _ in range(1000):
            rng.shuffle(candidates)
            proposed_validation = candidates[:validation_count]
            proposed_train = candidates[validation_count:]
            if _covers_all_atomic_values(
                proposed_validation, config
            ) and _covers_all_atomic_values(proposed_train, config):
                validation = proposed_validation
                train = proposed_train
                break
        if validation is None or train is None:
            raise RuntimeError("Could not create a stratified train/validation split.")

    result = WorldSplit(
        train=tuple(sorted(train, key=lambda item: item.meaning_id)),
        validation=tuple(sorted(validation, key=lambda item: item.meaning_id)),
        compositional_test=tuple(sorted(test, key=lambda item: item.meaning_id)),
        held_out_color_shape_pairs=tuple(sorted(held_out)),
        held_out_validation_color_shape_pairs=tuple(sorted(held_out_validation)),
        held_out_factor_names=(left_name, right_name),
    )
    _validate_split(result, config)
    return result


def _sample_matching(
    rng: random.Random,
    size: int,
    excluded_pairs: set[tuple[int, int]],
    *,
    purpose: str,
) -> tuple[tuple[int, int], ...]:
    for _ in range(10_000):
        permutation = list(range(size))
        rng.shuffle(permutation)
        pairs = tuple((color, permutation[color]) for color in range(size))
        if set(pairs).isdisjoint(excluded_pairs):
            return pairs
    raise RuntimeError(f"Could not create a {purpose} outside the excluded pairs.")


def _parse_explicit_matching(
    values: list[dict[str, int]],
    size: int,
    *,
    left_name: str = "color",
    right_name: str = "shape",
    purpose: str,
) -> tuple[tuple[int, int], ...]:
    pairs = tuple(
        (int(value[left_name]), int(value[right_name])) for value in values
    )
    if len(pairs) != size or len(set(pairs)) != size:
        raise ValueError(f"Explicit {purpose} must contain {size} unique pairs.")
    if {color for color, _ in pairs} != set(range(size)):
        raise ValueError(f"Explicit {purpose} does not contain every left value exactly once.")
    if {shape for _, shape in pairs} != set(range(size)):
        raise ValueError(f"Explicit {purpose} does not contain every right value exactly once.")
    return tuple(sorted(pairs))


def meaning_from_factors(factors: Iterable[int], config: dict[str, Any]) -> Meaning:
    values = tuple(int(value) for value in factors)
    if len(values) != len(FACTOR_NAMES):
        raise ValueError("An ECP meaning has exactly four factors.")
    sizes = [len(config["world"]["factors"][name]["values"]) for name in FACTOR_NAMES]
    for value, size in zip(values, sizes, strict=True):
        if value < 0 or value >= size:
            raise ValueError(f"Factor value {value} is outside 0..{size - 1}.")
    meaning_id = 0
    for value, size in zip(values, sizes, strict=True):
        meaning_id = meaning_id * size + value
    return Meaning(meaning_id, *values)


def _covers_all_atomic_values(
    meanings: Iterable[Meaning], config: dict[str, Any]
) -> bool:
    meanings = tuple(meanings)
    sizes = [len(config["world"]["factors"][name]["values"]) for name in FACTOR_NAMES]
    return all(
        {meaning.factors[index] for meaning in meanings} == set(range(size))
        for index, size in enumerate(sizes)
    )


def _validate_split(split: WorldSplit, config: dict[str, Any]) -> None:
    dataset = config["dataset"]
    expected = {
        "train": dataset["train_meanings"],
        "validation": dataset["validation_meanings"],
        "compositional_test": dataset["compositional_test_meanings"],
    }
    actual = {
        "train": len(split.train),
        "validation": len(split.validation),
        "compositional_test": len(split.compositional_test),
    }
    if actual != expected:
        raise AssertionError(f"Incorrect split sizes: {actual} versus {expected}.")

    groups = [split.train, split.validation, split.compositional_test]
    id_sets = [{meaning.meaning_id for meaning in group} for group in groups]
    if any(id_sets[left] & id_sets[right] for left, right in ((0, 1), (0, 2), (1, 2))):
        raise AssertionError("Data splits overlap.")
    if len(set.union(*id_sets)) != config["world"]["meaning_count"]:
        raise AssertionError("Data splits do not cover the complete world.")
