"""Load configurations and enforce preregistration invariants."""

from __future__ import annotations

import hashlib
import math
from pathlib import Path
from typing import Any

import yaml


class ConfigError(ValueError):
    """The experiment configuration is internally inconsistent."""


def load_config(path: str | Path) -> dict[str, Any]:
    config = _load_config(Path(path).resolve(), seen=set())
    validate_config(config)
    return config


def _load_config(config_path: Path, *, seen: set[Path]) -> dict[str, Any]:
    if config_path in seen:
        raise ConfigError(f"Cyclic configuration inheritance through {config_path}.")
    seen.add(config_path)
    with config_path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    if not isinstance(config, dict):
        raise ConfigError("The configuration must be a YAML object.")
    parent = config.pop("extends", None)
    if parent is not None:
        parent_path = (config_path.parent / str(parent)).resolve()
        inherited = _load_config(parent_path, seen=seen)
        config = _deep_merge(inherited, config)
    seen.remove(config_path)
    return config


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def validate_config(config: dict[str, Any]) -> None:
    try:
        factors = config["world"]["factors"]
        factor_sizes = [len(spec["values"]) for spec in factors.values()]
        meaning_count = config["world"]["meaning_count"]
        split = config["dataset"]
        channel = config["channel"]
        training = config["training"]
    except (KeyError, TypeError) as exc:
        raise ConfigError(f"Required configuration field is missing: {exc}") from exc

    calculated_meanings = math.prod(factor_sizes)
    if calculated_meanings != meaning_count:
        raise ConfigError(
            f"World contains {calculated_meanings} combinations, not {meaning_count}."
        )

    split_total = sum(
        split[key]
        for key in (
            "train_meanings",
            "validation_meanings",
            "compositional_test_meanings",
        )
    )
    if split_total != meaning_count:
        raise ConfigError(f"Data splits total {split_total}, not {meaning_count}.")

    if channel["type"] in {
        "factor_local_discrete_fixed_length",
        "slot_local_discrete_fixed_length",
    }:
        if channel["type"] == "factor_local_discrete_fixed_length":
            alphabet_sizes = channel["factor_alphabet_sizes"]
            width_key = "bits_per_symbol_by_factor"
            if alphabet_sizes != factor_sizes:
                raise ConfigError("Factor-local alphabets do not match the world.")
        else:
            alphabet_sizes = channel["slot_alphabet_sizes"]
            width_key = "bits_per_symbol_by_slot"
            if len(alphabet_sizes) != channel["message_length"]:
                raise ConfigError(
                    "Slot-local alphabets must match the message length."
                )
        if any(size < 2 for size in alphabet_sizes):
            raise ConfigError("Local alphabets must contain at least two symbols.")
        expected_message_bits = sum(
            math.ceil(math.log2(size)) for size in alphabet_sizes
        )
        expected_widths = [math.ceil(math.log2(size)) for size in alphabet_sizes]
        if channel.get(width_key) != expected_widths:
            raise ConfigError(f"{width_key} does not match the local alphabets.")
        if channel["vocabulary_size"] != max(alphabet_sizes):
            raise ConfigError("Global token space does not match the local alphabets.")
        if math.prod(alphabet_sizes) < meaning_count:
            raise ConfigError(
                "Local channel code space cannot represent every world meaning."
            )
    else:
        expected_bits_per_symbol = math.ceil(math.log2(channel["vocabulary_size"]))
        if expected_bits_per_symbol != channel["bits_per_symbol"]:
            raise ConfigError("bits_per_symbol does not match vocabulary_size.")
        expected_message_bits = channel["message_length"] * channel["bits_per_symbol"]
    if expected_message_bits != channel["bits_per_message"]:
        raise ConfigError("bits_per_message does not match message length and symbol cost.")

    entropy = math.log2(meaning_count)
    if not math.isclose(entropy, config["world"]["source_entropy_bits"]):
        raise ConfigError("source_entropy_bits does not match the uniform world.")

    seeds = config["reproducibility"]["training_seeds"]
    if len(seeds) != len(set(seeds)):
        raise ConfigError("Every training run must use a unique seed.")

    if training["selection_never_uses_test"] is not True:
        raise ConfigError("Test data must not be used for model selection.")
    if training["evaluation_uses_hard_symbols_only"] is not True:
        raise ConfigError("Evaluation must use hard symbols only.")

    temperature_schedule_steps = training.get("temperature_schedule_steps")
    if temperature_schedule_steps is not None:
        if (
            isinstance(temperature_schedule_steps, bool)
            or not isinstance(temperature_schedule_steps, int)
            or temperature_schedule_steps < 2
        ):
            raise ConfigError(
                "Temperature schedule steps must be an integer of at least 2."
            )
        if temperature_schedule_steps > training["max_steps"]:
            raise ConfigError("Temperature schedule steps cannot exceed max_steps.")

    learning_rate_decay = training.get("learning_rate_decay", {})
    if learning_rate_decay.get("enabled", False):
        start_step = learning_rate_decay.get("start_step", 0)
        end_step = learning_rate_decay.get("end_step", 0)
        final_learning_rate = learning_rate_decay.get("final_learning_rate", 0)
        if not isinstance(start_step, int) or isinstance(start_step, bool):
            raise ConfigError("Learning-rate decay start must be an integer.")
        if not isinstance(end_step, int) or isinstance(end_step, bool):
            raise ConfigError("Learning-rate decay end must be an integer.")
        if start_step < 1:
            raise ConfigError("Learning-rate decay start must be positive.")
        if end_step <= start_step or end_step > training["max_steps"]:
            raise ConfigError(
                "Learning-rate decay end must follow its start and fit max_steps."
            )
        if (
            final_learning_rate <= 0
            or final_learning_rate >= training["learning_rate"]
        ):
            raise ConfigError(
                "Final learning rate must be positive and below its initial value."
            )

    utilization = training.get("code_utilization", {})
    if utilization.get("enabled", False):
        if utilization.get("weight", -1) < 0:
            raise ConfigError("Code-utilization weight cannot be negative.")
        if utilization.get("independence_weight", -1) < 0:
            raise ConfigError("Slot-independence weight cannot be negative.")
        if utilization.get("warmup_steps", 0) < 1:
            raise ConfigError("Code-utilization warmup must be positive.")
        if utilization.get("relaxed_temperature", 0) <= 0:
            raise ConfigError("Code-utilization temperature must be positive.")
        if utilization.get("message_source", "relaxed") not in {
            "relaxed",
            "straight_through",
        }:
            raise ConfigError(
                "Code-utilization message_source must be relaxed or straight_through."
            )
        weight_decay = utilization.get("weight_decay", {})
        if weight_decay.get("enabled", False):
            start_step = weight_decay.get("start_step", 0)
            end_step = weight_decay.get("end_step", 0)
            final_weight = weight_decay.get("final_weight", -1)
            if not isinstance(start_step, int) or isinstance(start_step, bool):
                raise ConfigError("Code-utilization decay start must be an integer.")
            if not isinstance(end_step, int) or isinstance(end_step, bool):
                raise ConfigError("Code-utilization decay end must be an integer.")
            if start_step < utilization["warmup_steps"]:
                raise ConfigError(
                    "Code-utilization decay cannot start before warmup completes."
                )
            if end_step <= start_step or end_step > training["max_steps"]:
                raise ConfigError(
                    "Code-utilization decay end must follow its start and fit max_steps."
                )
            if final_weight < 0 or final_weight >= utilization["weight"]:
                raise ConfigError(
                    "Code-utilization final weight must be non-negative and below its initial weight."
                )

    joint_collision = training.get("joint_message_collision", {})
    if joint_collision.get("enabled", False):
        if joint_collision.get("weight", -1) < 0:
            raise ConfigError("Joint-collision weight cannot be negative.")
        if joint_collision.get("warmup_steps", 0) < 1:
            raise ConfigError("Joint-collision warmup must be positive.")

    collision_replay = training.get("global_collision_replay", {})
    if collision_replay.get("enabled", False):
        if collision_replay.get("weight", -1) < 0:
            raise ConfigError("Global collision-replay weight cannot be negative.")
        start_step = collision_replay.get("start_step", -1)
        warmup_steps = collision_replay.get("warmup_steps", 0)
        pair_batch_size = collision_replay.get("pair_batch_size", 0)
        refresh_interval = collision_replay.get("refresh_interval", 0)
        for value, label in (
            (start_step, "start"),
            (warmup_steps, "warmup"),
            (pair_batch_size, "pair batch size"),
            (refresh_interval, "refresh interval"),
        ):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ConfigError(
                    f"Global collision-replay {label} must be an integer."
                )
        if start_step < 0:
            raise ConfigError("Global collision-replay start cannot be negative.")
        if warmup_steps < 1:
            raise ConfigError("Global collision-replay warmup must be positive.")
        if start_step + warmup_steps > training["max_steps"]:
            raise ConfigError(
                "Global collision-replay warmup must complete within max_steps."
            )
        if pair_batch_size < 1:
            raise ConfigError(
                "Global collision-replay pair batch size must be positive."
            )
        if refresh_interval < 1:
            raise ConfigError(
                "Global collision-replay refresh interval must be positive."
            )
        evaluation_interval = training["evaluation_interval"]
        if (
            start_step % evaluation_interval != 0
            or refresh_interval % evaluation_interval != 0
        ):
            raise ConfigError(
                "Global collision replay must start and refresh on evaluation boundaries."
            )
        if collision_replay.get("relaxed_temperature", 0) <= 0:
            raise ConfigError(
                "Global collision-replay temperature must be positive."
            )
        decay = collision_replay.get("weight_decay", {})
        if decay.get("enabled", False):
            decay_start = decay.get("start_step", 0)
            decay_end = decay.get("end_step", 0)
            final_weight = decay.get("final_weight", -1)
            if isinstance(decay_start, bool) or not isinstance(decay_start, int):
                raise ConfigError(
                    "Global collision-replay decay start must be an integer."
                )
            if isinstance(decay_end, bool) or not isinstance(decay_end, int):
                raise ConfigError(
                    "Global collision-replay decay end must be an integer."
                )
            if decay_start < start_step + warmup_steps:
                raise ConfigError(
                    "Global collision-replay decay cannot start before warmup completes."
                )
            if decay_end <= decay_start or decay_end > training["max_steps"]:
                raise ConfigError(
                    "Global collision-replay decay end must follow its start and fit max_steps."
                )
            if final_weight < 0 or final_weight >= collision_replay["weight"]:
                raise ConfigError(
                    "Global collision-replay final weight must be non-negative and below its initial weight."
                )

    hard_replay = training.get("global_hard_meaning_replay", {})
    if hard_replay.get("enabled", False):
        if hard_replay.get("weight", -1) < 0:
            raise ConfigError(
                "Global hard-meaning replay weight cannot be negative."
            )
        start_step = hard_replay.get("start_step", -1)
        warmup_steps = hard_replay.get("warmup_steps", 0)
        batch_size = hard_replay.get("batch_size", 0)
        refresh_interval = hard_replay.get("refresh_interval", 0)
        minimum_failed_links = hard_replay.get("minimum_failed_links", 1)
        for value, label in (
            (start_step, "start"),
            (warmup_steps, "warmup"),
            (batch_size, "batch size"),
            (refresh_interval, "refresh interval"),
            (minimum_failed_links, "minimum failed links"),
        ):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ConfigError(
                    f"Global hard-meaning replay {label} must be an integer."
                )
        if start_step < 0:
            raise ConfigError(
                "Global hard-meaning replay start cannot be negative."
            )
        if warmup_steps < 1:
            raise ConfigError(
                "Global hard-meaning replay warmup must be positive."
            )
        if start_step + warmup_steps > training["max_steps"]:
            raise ConfigError(
                "Global hard-meaning replay warmup must complete within max_steps."
            )
        if batch_size < 1:
            raise ConfigError(
                "Global hard-meaning replay batch size must be positive."
            )
        if refresh_interval < 1:
            raise ConfigError(
                "Global hard-meaning replay refresh interval must be positive."
            )
        population = config["agents"]["population"]
        population_link_count = (
            population["sender_count"] * population["receiver_count"]
        )
        if not 1 <= minimum_failed_links <= population_link_count:
            raise ConfigError(
                "Global hard-meaning replay minimum failed links must fit the population."
            )
        evaluation_interval = training["evaluation_interval"]
        if (
            start_step % evaluation_interval != 0
            or refresh_interval % evaluation_interval != 0
        ):
            raise ConfigError(
                "Global hard-meaning replay must start and refresh on evaluation boundaries."
            )

    sender_consensus = training.get("sender_message_consensus", {})
    if sender_consensus.get("enabled", False):
        if sender_consensus.get("weight", -1) < 0:
            raise ConfigError("Sender-message consensus weight cannot be negative.")
        if sender_consensus.get("warmup_steps", 0) < 1:
            raise ConfigError("Sender-message consensus warmup must be positive.")

    factor_minimax = training.get("factor_minimax", {})
    if factor_minimax.get("enabled", False):
        if factor_minimax.get("weight", -1) < 0:
            raise ConfigError("Factor-minimax weight cannot be negative.")
        warmup_steps = factor_minimax.get("warmup_steps", 0)
        if (
            isinstance(warmup_steps, bool)
            or not isinstance(warmup_steps, int)
            or warmup_steps < 1
        ):
            raise ConfigError("Factor-minimax warmup must be positive.")
        start_step = factor_minimax.get("start_step", 0)
        if isinstance(start_step, bool) or not isinstance(start_step, int):
            raise ConfigError("Factor-minimax start must be an integer.")
        if start_step < 0:
            raise ConfigError("Factor-minimax start cannot be negative.")
        if start_step + warmup_steps > training["max_steps"]:
            raise ConfigError(
                "Factor-minimax warmup must complete within max_steps."
            )


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    import json

    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
