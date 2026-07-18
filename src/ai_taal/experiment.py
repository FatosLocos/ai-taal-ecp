"""Orchestration, isolation, artifacts, and classification for ECP runs."""

from __future__ import annotations

import copy
import importlib.metadata
import json
import math
import os
import platform
import subprocess
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import jsonschema
import numpy as np
import torch
import yaml
from referencing import Registry, Resource

from ai_taal.baselines import compute_baselines
from ai_taal.config import canonical_sha256, file_sha256
from ai_taal.metrics import prediction_metrics, protocol_statistics
from ai_taal.models import Receiver, save_agent_checkpoint
from ai_taal.training import (
    encode_meanings,
    meanings_tensor,
    train_communication_system,
    train_translator,
)
from ai_taal.world import Meaning, WorldSplit, build_splits, meaning_from_factors


def create_run_directory(output_root: str | Path, experiment_id: str, *, mode: str) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    candidate = Path(output_root) / f"{timestamp}-{experiment_id}-{mode}"
    number = 1
    while candidate.exists():
        candidate = Path(output_root) / f"{timestamp}-{experiment_id}-{mode}-{number}"
        number += 1
    candidate.mkdir(parents=True)
    return candidate


def run_experiment(
    config: dict[str, Any],
    *,
    config_path: str | Path,
    output_root: str | Path,
    smoke: bool,
    unseal_test: bool,
    development: bool = False,
    seeds: list[int] | None = None,
) -> Path:
    if smoke and development:
        raise ValueError("A run cannot be both smoke and development.")
    if not smoke and not development and not unseal_test:
        raise ValueError("A full run requires the explicit --unseal-test flag.")
    if (smoke or development) and unseal_test:
        raise ValueError("A non-confirmatory run must not open the test set.")

    split = build_splits(config)
    mode = "smoke" if smoke else "development" if development else "experiment"
    run_dir = create_run_directory(output_root, config["experiment"]["id"], mode=mode)
    selected_seeds = seeds or list(config["reproducibility"]["training_seeds"])
    if smoke:
        selected_seeds = selected_seeds[:1]

    _write_json(run_dir / "environment.json", _environment_manifest())
    effective_config = copy.deepcopy(config)
    effective_config["execution"] = {
        "smoke": smoke,
        "development": development,
        "test_unsealed": unseal_test,
        "selected_seeds": selected_seeds,
        "source_config_sha256": file_sha256(config_path),
    }
    with (run_dir / "effective_config.yaml").open("w", encoding="utf-8") as handle:
        yaml.safe_dump(effective_config, handle, sort_keys=False, allow_unicode=True)
    _write_json(run_dir / "split_manifest.json", split.manifest())
    all_meanings = split.train + split.validation + split.compositional_test
    _write_json(run_dir / "baselines.json", compute_baselines(all_meanings))

    results = []
    for seed in selected_seeds:
        seed_dir = run_dir / f"seed-{seed}"
        seed_dir.mkdir()
        results.append(
            run_seed(
                config,
                split,
                seed=seed,
                output_dir=seed_dir,
                smoke=smoke,
                unseal_test=unseal_test,
                development=development,
            )
        )

    summary = _summarize_experiment(
        config, results, smoke=smoke, development=development
    )
    summary["run_directory"] = str(run_dir)
    summary["artifact_sha256"] = _artifact_hashes(run_dir)
    _write_json(run_dir / "summary.json", summary)
    (run_dir / "report.md").write_text(
        _render_report(
            config, results, summary, smoke=smoke, development=development
        ),
        encoding="utf-8",
    )
    return run_dir


def run_seed(
    config: dict[str, Any],
    split: WorldSplit,
    *,
    seed: int,
    output_dir: Path,
    smoke: bool,
    unseal_test: bool,
    development: bool = False,
) -> dict[str, Any]:
    communication_steps = 25 if smoke else None
    translator_steps = 25 if smoke else None
    system, communication_training = train_communication_system(
        config,
        split.train,
        split.validation,
        seed=seed,
        max_steps_override=communication_steps,
    )
    sender_checkpoint = output_dir / "sender.pt"
    receiver_checkpoint = output_dir / "receiver.pt"
    save_agent_checkpoint(sender_checkpoint, system.sender, kind="sender")
    save_agent_checkpoint(receiver_checkpoint, system.receiver, kind="receiver")

    train_values = meanings_tensor(split.train, config["training"]["device"])
    validation_values = meanings_tensor(split.validation, config["training"]["device"])
    train_messages = encode_meanings(system.sender, train_values).cpu()
    validation_messages = encode_meanings(system.sender, validation_values).cpu()
    translator, translator_training = train_translator(
        config,
        train_messages,
        split.train,
        validation_messages,
        split.validation,
        seed=seed + 1_000_003,
        max_steps_override=translator_steps,
    )
    translator_checkpoint = output_dir / "translator.pt"
    save_agent_checkpoint(translator_checkpoint, translator, kind="translator")

    evaluated_splits: list[tuple[str, tuple[Meaning, ...]]] = [
        ("train", split.train),
        ("validation", split.validation),
    ]
    if unseal_test:
        evaluated_splits.append(("compositional_test", split.compositional_test))

    split_metrics: dict[str, Any] = {}
    translator_metrics: dict[str, Any] = {}
    messages_by_split: dict[str, np.ndarray] = {}
    predictions_by_split: dict[str, np.ndarray] = {}
    episodes: list[dict[str, Any]] = []
    for split_name, meanings in evaluated_splits:
        isolation_dir = output_dir / "isolated" / split_name
        messages, predictions = _isolated_roundtrip(
            sender_checkpoint, receiver_checkpoint, meanings, isolation_dir
        )
        translator_predictions = _isolated_decode(
            translator_checkpoint,
            messages,
            isolation_dir / "translator",
        )
        metrics = prediction_metrics(meanings, predictions)
        metrics["meaning_count"] = len(meanings)
        split_metrics[split_name] = metrics
        translator_metrics[split_name] = prediction_metrics(
            meanings, translator_predictions
        )
        messages_by_split[split_name] = messages
        predictions_by_split[split_name] = predictions
        episodes.extend(
            _episode_records(
                config,
                seed=seed,
                split_name=split_name,
                meanings=meanings,
                messages=messages,
                predictions=predictions,
            )
        )

    analysis_names = [name for name, _ in evaluated_splits]
    analysis_meanings = tuple(
        meaning
        for name, meanings in evaluated_splits
        if name in analysis_names
        for meaning in meanings
    )
    analysis_messages = np.concatenate(
        [messages_by_split[name] for name in analysis_names], axis=0
    )
    protocol = protocol_statistics(analysis_meanings, analysis_messages)
    controls = _run_controls(
        config,
        receiver_checkpoint,
        system.receiver,
        analysis_meanings,
        analysis_messages,
        output_dir,
        seed=seed,
    )

    _validate_episodes(episodes, config)
    _write_jsonl(output_dir / "episodes.jsonl", episodes)
    result = {
        "seed": seed,
        "smoke": smoke,
        "test_unsealed": unseal_test,
        "communication_training": asdict(communication_training),
        "translator_training": asdict(translator_training),
        "receiver": split_metrics,
        "translator": translator_metrics,
        "protocol": protocol,
        "controls": controls,
        "checkpoint_sha256": {
            "sender": file_sha256(sender_checkpoint),
            "receiver": file_sha256(receiver_checkpoint),
            "translator": file_sha256(translator_checkpoint),
        },
    }
    result["classification"] = _classify_seed(
        config, result, development=development
    )
    _write_json(output_dir / "metrics.json", result)
    return result


def _isolated_roundtrip(
    sender_checkpoint: Path,
    receiver_checkpoint: Path,
    meanings: tuple[Meaning, ...],
    directory: Path,
) -> tuple[np.ndarray, np.ndarray]:
    directory.mkdir(parents=True, exist_ok=True)
    sender_input = directory / "sender-input.json"
    receiver_input = directory / "receiver-input.json"
    receiver_output = directory / "receiver-output.json"
    _write_json(sender_input, [list(meaning.factors) for meaning in meanings], compact=True)
    _run_worker("encode", sender_checkpoint, sender_input, receiver_input)
    _run_worker("decode", receiver_checkpoint, receiver_input, receiver_output)
    return _read_matrix(receiver_input), _read_matrix(receiver_output)


def _isolated_decode(
    checkpoint: Path, messages: np.ndarray, directory: Path
) -> np.ndarray:
    directory.mkdir(parents=True, exist_ok=True)
    decoder_input = directory / "decoder-input.json"
    decoder_output = directory / "decoder-output.json"
    _write_json(decoder_input, messages.tolist(), compact=True)
    _run_worker("decode", checkpoint, decoder_input, decoder_output)
    return _read_matrix(decoder_output)


def _run_worker(mode: str, checkpoint: Path, input_path: Path, output_path: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_taal.worker",
            mode,
            "--checkpoint",
            str(checkpoint.resolve()),
            "--input",
            str(input_path.resolve()),
            "--output",
            str(output_path.resolve()),
        ],
        check=True,
        cwd=Path.cwd(),
        env={**os.environ, "PYTHONHASHSEED": "0"},
        capture_output=True,
        text=True,
    )


def _run_controls(
    config: dict[str, Any],
    receiver_checkpoint: Path,
    receiver: Receiver,
    meanings: tuple[Meaning, ...],
    messages: np.ndarray,
    output_dir: Path,
    *,
    seed: int,
) -> dict[str, Any]:
    rng = np.random.default_rng(seed + 707)
    shuffled = messages[rng.permutation(len(messages))]
    shuffled_predictions = _isolated_decode(
        receiver_checkpoint, shuffled, output_dir / "controls" / "shuffled"
    )
    shuffled_exact = prediction_metrics(meanings, shuffled_predictions)["exact_match"]

    permutation = rng.permutation(config["channel"]["vocabulary_size"])
    permuted_messages = permutation[messages]
    permuted_receiver = copy.deepcopy(receiver).cpu()
    with torch.no_grad():
        old_weight = permuted_receiver.symbol_embedding.weight.detach().clone()
        permuted_receiver.symbol_embedding.weight[torch.as_tensor(permutation)] = old_weight
    permuted_checkpoint = output_dir / "controls" / "permuted-receiver.pt"
    permuted_checkpoint.parent.mkdir(parents=True, exist_ok=True)
    save_agent_checkpoint(permuted_checkpoint, permuted_receiver, kind="receiver")
    original_predictions = _isolated_decode(
        receiver_checkpoint, messages, output_dir / "controls" / "original"
    )
    permuted_predictions = _isolated_decode(
        permuted_checkpoint, permuted_messages, output_dir / "controls" / "permuted"
    )
    permutation_preserves = bool(np.array_equal(original_predictions, permuted_predictions))

    ablation = []
    original_exact = prediction_metrics(meanings, original_predictions)["exact_match"]
    for position in range(messages.shape[1]):
        altered = messages.copy()
        modal_symbol = int(np.bincount(altered[:, position]).argmax())
        altered[:, position] = modal_symbol
        predictions = _isolated_decode(
            receiver_checkpoint,
            altered,
            output_dir / "controls" / f"ablation-position-{position}",
        )
        exact = prediction_metrics(meanings, predictions)["exact_match"]
        ablation.append(
            {
                "position": position,
                "replacement_symbol": modal_symbol,
                "exact_match": exact,
                "accuracy_drop": original_exact - exact,
            }
        )

    shuffled_max = config["controls"]["shuffled_messages_expected_exact_match_max"]
    return {
        "shuffled_messages_exact_match": shuffled_exact,
        "shuffled_messages_pass": shuffled_exact <= shuffled_max,
        "shuffled_messages_maximum": shuffled_max,
        "consistent_symbol_permutation": permutation.tolist(),
        "consistent_symbol_permutation_preserves_predictions": permutation_preserves,
        "symbol_ablation": ablation,
        "channel_isolation": {
            "sender_process_input": "factor matrix only",
            "receiver_process_input": "symbol matrix only",
            "receiver_input_contains_ids": False,
            "separate_processes": True,
        },
    }


def _episode_records(
    config: dict[str, Any],
    *,
    seed: int,
    split_name: str,
    meanings: tuple[Meaning, ...],
    messages: np.ndarray,
    predictions: np.ndarray,
) -> list[dict[str, Any]]:
    run_id = f"ecp0-seed-{seed}"
    records = []
    for index, (meaning, message, prediction) in enumerate(
        zip(meanings, messages, predictions, strict=True)
    ):
        episode_id = f"{split_name}-{index:04d}"
        reconstruction = meaning_from_factors(prediction, config)
        factor_correct = [
            left == right for left, right in zip(meaning.factors, reconstruction.factors, strict=True)
        ]
        records.append(
            {
                "episode_id": episode_id,
                "run_id": run_id,
                "seed": seed,
                "split": split_name,
                "meaning": meaning.to_schema_dict(),
                "message": {
                    "protocol_version": "ecp0",
                    "run_id": run_id,
                    "episode_id": episode_id,
                    "sender_id": f"sender-{seed}",
                    "receiver_id": f"receiver-{seed}",
                    "symbols": [int(value) for value in message],
                    "channel_bits": config["channel"]["bits_per_message"],
                },
                "reconstruction": reconstruction.to_schema_dict(),
                "exact_match": all(factor_correct),
                "factor_correct": dict(
                    zip(("color", "shape", "size", "texture"), factor_correct, strict=True)
                ),
            }
        )
    return records


def validate_schemas(schema_directory: str | Path) -> None:
    schemas = []
    registry = Registry()
    for path in sorted(Path(schema_directory).glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        jsonschema.validators.validator_for(schema).check_schema(schema)
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
        schemas.append(schema)
    if not schemas:
        raise ValueError("No JSON Schemas found.")


def _validate_episodes(episodes: list[dict[str, Any]], config: dict[str, Any]) -> None:
    schema_paths = [
        Path(config["artifacts"][key])
        for key in ("meaning_schema", "message_schema", "episode_schema")
    ]
    registry = Registry()
    loaded: dict[str, dict[str, Any]] = {}
    for path in schema_paths:
        schema = json.loads(path.read_text(encoding="utf-8"))
        jsonschema.validators.validator_for(schema).check_schema(schema)
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
        loaded[path.name] = schema
    validator = jsonschema.Draft202012Validator(
        loaded[Path(config["artifacts"]["episode_schema"]).name], registry=registry
    )
    for episode in episodes:
        validator.validate(episode)
        factor_specs = config["world"]["factors"]
        for meaning_key in ("meaning", "reconstruction"):
            meaning = episode[meaning_key]
            factors = []
            for factor_name, prefix in (
                ("color", "c"),
                ("shape", "s"),
                ("size", "z"),
                ("texture", "t"),
            ):
                value = int(meaning[factor_name][len(prefix) :])
                if value < 0 or value >= len(factor_specs[factor_name]["values"]):
                    raise ValueError("Episode contains a factor value outside the world.")
                factors.append(value)
            expected_meaning = meaning_from_factors(factors, config)
            if expected_meaning.meaning_id != meaning["meaning_id"]:
                raise ValueError("Episode contains an inconsistent meaning_id.")
        message = episode["message"]
        if message["channel_bits"] != config["channel"]["bits_per_message"]:
            raise ValueError("Episode contains an incorrect channel bit length.")
        symbols = message["symbols"]
        if len(symbols) != config["channel"]["message_length"]:
            raise ValueError("Episode contains an incorrect message length.")
        if any(
            symbol < config["channel"]["symbol_min"]
            or symbol > config["channel"]["symbol_max"]
            for symbol in symbols
        ):
            raise ValueError("Episode contains a symbol outside the channel alphabet.")


def _classify_seed(
    config: dict[str, Any], result: dict[str, Any], *, development: bool
) -> str:
    controls = result["controls"]
    valid = controls["shuffled_messages_pass"] and controls[
        "consistent_symbol_permutation_preserves_predictions"
    ]
    if not valid:
        return "invalid"
    if development:
        return "development_only"
    if not result["test_unsealed"]:
        return "technical_smoke_only"
    thresholds = config["outcome_thresholds"]["strong_evidence"]
    if (
        result["receiver"]["train"]["exact_match"] >= thresholds["known_exact_match_min"]
        and result["receiver"]["compositional_test"]["exact_match"]
        >= thresholds["compositional_exact_match_min"]
        and result["translator"]["compositional_test"]["exact_match"]
        >= thresholds["translator_compositional_exact_match_min"]
    ):
        return "strong_evidence"
    if result["receiver"]["train"]["exact_match"] >= thresholds["known_exact_match_min"]:
        return "mixed_evidence"
    return "negative_result"


def _summarize_experiment(
    config: dict[str, Any],
    results: list[dict[str, Any]],
    *,
    smoke: bool,
    development: bool,
) -> dict[str, Any]:
    classifications = [result["classification"] for result in results]
    if smoke:
        overall = "technical_smoke_only"
    elif development:
        overall = "development_only"
    else:
        strong_count = classifications.count("strong_evidence")
        required = config["outcome_thresholds"]["strong_evidence"]["minimum_valid_runs"]
        if classifications.count("invalid"):
            overall = "contains_invalid_runs"
        elif strong_count >= required:
            overall = "strong_evidence"
        elif classifications.count("mixed_evidence") or strong_count:
            overall = "mixed_evidence"
        else:
            overall = "negative_result"
    return {
        "experiment_id": config["experiment"]["id"],
        "smoke": smoke,
        "development": development,
        "overall_classification": overall,
        "seed_classifications": {
            str(result["seed"]): result["classification"] for result in results
        },
        "run_count": len(results),
    }


def _render_report(
    config: dict[str, Any],
    results: list[dict[str, Any]],
    summary: dict[str, Any],
    *,
    smoke: bool,
    development: bool,
) -> str:
    title = (
        "ECP-0 technical smoke run"
        if smoke
        else "ECP-0 ontwikkelrun"
        if development
        else "ECP-0 experimentrapport"
    )
    lines = [
        f"# {title}",
        "",
        f"Classification: **{summary['overall_classification']}**",
        "",
        "| Seed | Known exact | Validation exact | Compositional exact | Translator compositional | Classification |",
        "|---:|---:|---:|---:|---:|---|",
    ]
    for result in results:
        receiver = result["receiver"]
        translator = result["translator"]
        composition = receiver.get("compositional_test", {}).get("exact_match")
        translator_composition = translator.get("compositional_test", {}).get("exact_match")
        lines.append(
            "| {seed} | {known:.3f} | {validation:.3f} | {composition} | "
            "{translator} | {classification} |".format(
                seed=result["seed"],
                known=receiver["train"]["exact_match"],
                validation=receiver["validation"]["exact_match"],
                composition="—" if composition is None else f"{composition:.3f}",
                translator="—"
                if translator_composition is None
                else f"{translator_composition:.3f}",
                classification=result["classification"],
            )
        )
    lines.extend(
        [
            "",
            "## Methodological status",
            "",
            "The sender and receiver ran as separate processes for every reported evaluation. "
            "The receiver received only the discrete symbol matrix.",
            "",
        ]
    )
    if smoke:
        lines.append(
            "This short run checks only the technical pipeline and did not open the compositional test set."
        )
    elif development:
        lines.append(
            "This development run used training and validation only. The compositional test set remained sealed."
        )
    else:
        lines.append(
            "The compositional test set was explicitly unsealed for this confirmatory run and was not used for model selection."
        )
    lines.append("")
    return "\n".join(lines)


def _environment_manifest() -> dict[str, Any]:
    packages = {}
    for name in ("ai-taal-ecp", "jsonschema", "numpy", "PyYAML", "torch"):
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None
    return {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "torch_device": "cpu",
        "packages": packages,
    }


def _artifact_hashes(run_dir: Path) -> dict[str, str]:
    return {
        str(path.relative_to(run_dir)): file_sha256(path)
        for path in sorted(run_dir.rglob("*"))
        if path.is_file() and path.name not in {"summary.json", "report.md"}
    }


def _read_matrix(path: Path) -> np.ndarray:
    with path.open("r", encoding="utf-8") as handle:
        return np.asarray(json.load(handle), dtype=np.int64)


def _write_json(path: Path, value: Any, *, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(
            value,
            handle,
            ensure_ascii=False,
            sort_keys=not compact,
            indent=None if compact else 2,
            separators=(",", ":") if compact else None,
        )
        handle.write("\n")


def _write_jsonl(path: Path, values: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for value in values:
            handle.write(json.dumps(value, ensure_ascii=False, sort_keys=True))
            handle.write("\n")
