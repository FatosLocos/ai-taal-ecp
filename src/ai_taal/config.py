"""Configuratie laden en de preregistratie-invarianten bewaken."""

from __future__ import annotations

import hashlib
import math
from pathlib import Path
from typing import Any

import yaml


class ConfigError(ValueError):
    """De experimentconfiguratie is intern tegenstrijdig."""


def load_config(path: str | Path) -> dict[str, Any]:
    config = _load_config(Path(path).resolve(), seen=set())
    validate_config(config)
    return config


def _load_config(config_path: Path, *, seen: set[Path]) -> dict[str, Any]:
    if config_path in seen:
        raise ConfigError(f"Cyclische configuratie-erfenis via {config_path}.")
    seen.add(config_path)
    with config_path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    if not isinstance(config, dict):
        raise ConfigError("De configuratie moet een YAML-object zijn.")
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
    except (KeyError, TypeError) as exc:
        raise ConfigError(f"Verplicht configuratieveld ontbreekt: {exc}") from exc

    calculated_meanings = math.prod(factor_sizes)
    if calculated_meanings != meaning_count:
        raise ConfigError(
            f"Wereld bevat {calculated_meanings} combinaties, niet {meaning_count}."
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
        raise ConfigError(f"Datasplitsingen tellen op tot {split_total}, niet {meaning_count}.")

    if channel["type"] == "factor_local_discrete_fixed_length":
        alphabet_sizes = channel["factor_alphabet_sizes"]
        if alphabet_sizes != factor_sizes:
            raise ConfigError("Lokale factoralfabetten passen niet bij de wereld.")
        expected_message_bits = sum(
            math.ceil(math.log2(size)) for size in alphabet_sizes
        )
        if channel["vocabulary_size"] != max(alphabet_sizes):
            raise ConfigError("Globale tokenruimte past niet bij lokale alfabetten.")
    else:
        expected_bits_per_symbol = math.ceil(math.log2(channel["vocabulary_size"]))
        if expected_bits_per_symbol != channel["bits_per_symbol"]:
            raise ConfigError("bits_per_symbol past niet bij vocabulary_size.")
        expected_message_bits = channel["message_length"] * channel["bits_per_symbol"]
    if expected_message_bits != channel["bits_per_message"]:
        raise ConfigError("bits_per_message past niet bij lengte en symboolkosten.")

    entropy = math.log2(meaning_count)
    if not math.isclose(entropy, config["world"]["source_entropy_bits"]):
        raise ConfigError("source_entropy_bits past niet bij de uniforme wereld.")

    seeds = config["reproducibility"]["training_seeds"]
    if len(seeds) != len(set(seeds)):
        raise ConfigError("Iedere trainingsrun moet een unieke seed hebben.")

    if config["training"]["selection_never_uses_test"] is not True:
        raise ConfigError("Testdata mag niet voor modelselectie worden gebruikt.")
    if config["training"]["evaluation_uses_hard_symbols_only"] is not True:
        raise ConfigError("Evaluatie moet uitsluitend harde symbolen gebruiken.")


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
