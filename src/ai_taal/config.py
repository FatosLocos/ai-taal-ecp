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
