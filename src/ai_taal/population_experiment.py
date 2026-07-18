"""Populatie-experimenten met universele vertaling en overdraagbaarheid."""

from __future__ import annotations

import copy
from concurrent.futures import ProcessPoolExecutor
import json
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np
import torch
import yaml

from ai_taal.baselines import compute_baselines
from ai_taal.config import file_sha256
from ai_taal.experiment import (
    _artifact_hashes,
    _environment_manifest,
    _read_matrix,
    _run_worker,
    _validate_episodes,
    _write_json,
    _write_jsonl,
    create_run_directory,
)
from ai_taal.metrics import prediction_metrics, protocol_statistics
from ai_taal.models import PopulationSystem, Receiver, save_agent_checkpoint
from ai_taal.training import (
    encode_meanings,
    meanings_tensor,
    train_population_system,
    train_translator,
)
from ai_taal.world import Meaning, WorldSplit, build_splits, meaning_from_factors


def run_population_experiment(
    config: dict[str, Any],
    *,
    config_path: str | Path,
    output_root: str | Path,
    smoke: bool,
    unseal_test: bool,
    development: bool = False,
    seeds: list[int] | None = None,
) -> Path:
    experiment_id = config["experiment"]["id"].upper()
    if smoke and development:
        raise ValueError("Een run kan niet tegelijk smoke en development zijn.")
    if not smoke and not development and not unseal_test:
        raise ValueError(
            f"Een confirmatieve {experiment_id}-run vereist --unseal-test."
        )
    if (smoke or development) and unseal_test:
        raise ValueError(
            f"Een niet-confirmatieve {experiment_id}-run mag de testset niet openen."
        )

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
    _write_json(
        run_dir / "baselines.json",
        compute_baselines(split.train + split.validation + split.compositional_test),
    )

    seed_jobs = []
    for seed in selected_seeds:
        seed_dir = run_dir / f"seed-{seed}"
        seed_dir.mkdir()
        seed_jobs.append((seed, seed_dir))
    worker_count = min(
        config["reproducibility"].get("parallel_seed_workers", 1),
        len(seed_jobs),
    )
    if worker_count > 1:
        with ProcessPoolExecutor(max_workers=worker_count) as executor:
            futures = [
                executor.submit(
                    run_population_seed,
                    config,
                    split,
                    seed=seed,
                    output_dir=seed_dir,
                    smoke=smoke,
                    unseal_test=unseal_test,
                    development=development,
                )
                for seed, seed_dir in seed_jobs
            ]
            results = [future.result() for future in futures]
    else:
        results = [
            run_population_seed(
                config,
                split,
                seed=seed,
                output_dir=seed_dir,
                smoke=smoke,
                unseal_test=unseal_test,
                development=development,
            )
            for seed, seed_dir in seed_jobs
        ]
    results.sort(key=lambda result: result["seed"])
    summary = _summarize(config, results, smoke=smoke, development=development)
    summary["run_directory"] = str(run_dir)
    summary["artifact_sha256"] = _artifact_hashes(run_dir)
    _write_json(run_dir / "summary.json", summary)
    (run_dir / "report.md").write_text(
        _render_report(results, summary, smoke=smoke, development=development),
        encoding="utf-8",
    )
    return run_dir


def run_population_seed(
    config: dict[str, Any],
    split: WorldSplit,
    *,
    seed: int,
    output_dir: Path,
    smoke: bool,
    unseal_test: bool,
    development: bool,
) -> dict[str, Any]:
    population_steps = 32 if smoke else None
    translator_steps = 32 if smoke else None
    population, training_result = train_population_system(
        config,
        split.train,
        split.validation,
        seed=seed,
        max_steps_override=population_steps,
    )
    sender_checkpoints, receiver_checkpoints = _save_population(
        population, output_dir
    )

    train_values = meanings_tensor(split.train, config["training"]["device"])
    validation_values = meanings_tensor(
        split.validation, config["training"]["device"]
    )
    train_messages = [
        encode_meanings(sender, train_values).cpu() for sender in population.senders
    ]
    validation_messages = [
        encode_meanings(sender, validation_values).cpu()
        for sender in population.senders
    ]
    repeated_train = _repeat_meanings(split.train, len(population.senders))
    repeated_validation = _repeat_meanings(
        split.validation, len(population.senders)
    )
    translator, translator_result = train_translator(
        config,
        torch.cat(train_messages, dim=0),
        repeated_train,
        torch.cat(validation_messages, dim=0),
        repeated_validation,
        seed=seed + 1_000_003,
        max_steps_override=translator_steps,
    )
    translator_checkpoint = output_dir / "universal-translator.pt"
    save_agent_checkpoint(
        translator_checkpoint, translator, kind="translator"
    )

    transfer_models, transfer_training = _train_transfer_curve(
        config,
        split,
        train_messages,
        validation_messages,
        seed=seed,
        output_dir=output_dir,
        smoke=smoke,
    )

    evaluated_splits: list[tuple[str, tuple[Meaning, ...]]] = [
        ("train", split.train),
        ("validation", split.validation),
    ]
    if unseal_test:
        evaluated_splits.append(("compositional_test", split.compositional_test))
    all_meanings = tuple(
        meaning for _, meanings in evaluated_splits for meaning in meanings
    )
    split_slices = _split_slices(evaluated_splits)

    isolated_messages = [
        _isolated_encode(
            checkpoint,
            all_meanings,
            output_dir / "isolated" / f"sender-{index}",
        )
        for index, checkpoint in enumerate(sender_checkpoints)
    ]
    combined_messages = np.concatenate(isolated_messages, axis=0)
    receiver_predictions = [
        _isolated_decode(
            checkpoint,
            combined_messages,
            output_dir / "isolated" / f"receiver-{index}",
        )
        for index, checkpoint in enumerate(receiver_checkpoints)
    ]
    translator_predictions = _isolated_decode(
        translator_checkpoint,
        combined_messages,
        output_dir / "isolated" / "universal-translator",
    )
    transfer_predictions = {
        str(budget): _isolated_decode(
            checkpoint,
            combined_messages,
            output_dir / "isolated" / f"transfer-{budget}",
        )
        for budget, checkpoint in transfer_models.items()
    }

    population_metrics = _population_metrics(
        evaluated_splits,
        split_slices,
        isolated_messages,
        receiver_predictions,
    )
    translator_metrics = _shared_decoder_metrics(
        evaluated_splits,
        split_slices,
        translator_predictions,
        sender_count=len(sender_checkpoints),
    )
    transfer_metrics = {
        budget: _shared_decoder_metrics(
            evaluated_splits,
            split_slices,
            predictions,
            sender_count=len(sender_checkpoints),
        )
        for budget, predictions in transfer_predictions.items()
    }
    protocols = _sender_protocols(all_meanings, isolated_messages)
    agreement = _sender_message_agreement(isolated_messages)
    bindings = _sender_binding_diagnostics(population)
    atom_codes = _sender_atom_code_diagnostics(population)
    receiver_bindings = _receiver_binding_diagnostics(population)
    controls = _population_controls(
        config,
        receiver_checkpoints,
        population,
        all_meanings,
        isolated_messages,
        receiver_predictions,
        output_dir,
        seed=seed,
    )
    logged_split_names = set(
        config["artifacts"].get(
            "episode_logging_splits",
            [name for name, _ in evaluated_splits],
        )
    )
    unknown_logged_splits = logged_split_names - {
        "train", "validation", "compositional_test"
    }
    if unknown_logged_splits:
        raise ValueError(f"Onbekende episode-logsplits: {unknown_logged_splits}")
    logged_splits = [
        (name, meanings)
        for name, meanings in evaluated_splits
        if name in logged_split_names
    ]
    episodes = _population_episodes(
        config,
        seed,
        logged_splits,
        split_slices,
        isolated_messages,
        receiver_predictions,
    )
    _validate_episodes(episodes, config)
    _write_jsonl(output_dir / "episodes.jsonl", episodes)

    result: dict[str, Any] = {
        "seed": seed,
        "smoke": smoke,
        "test_unsealed": unseal_test,
        "population_training": asdict(training_result),
        "translator_training": asdict(translator_result),
        "transfer_training": transfer_training,
        "population": population_metrics,
        "universal_translator": translator_metrics,
        "transfer_curve": transfer_metrics,
        "sender_protocols": protocols,
        "sender_message_agreement": agreement,
        "sender_binding_diagnostics": bindings,
        "sender_atom_code_diagnostics": atom_codes,
        "receiver_binding_diagnostics": receiver_bindings,
        "controls": controls,
        "checkpoint_sha256": {
            "senders": [file_sha256(path) for path in sender_checkpoints],
            "receivers": [file_sha256(path) for path in receiver_checkpoints],
            "universal_translator": file_sha256(translator_checkpoint),
            "transfer": {
                str(budget): file_sha256(path)
                for budget, path in transfer_models.items()
            },
        },
    }
    result["classification"] = _classify(
        config, result, development=development
    )
    _write_json(output_dir / "metrics.json", result)
    return result


def _save_population(
    population: PopulationSystem, output_dir: Path
) -> tuple[list[Path], list[Path]]:
    sender_paths = []
    receiver_paths = []
    for index, sender in enumerate(population.senders):
        path = output_dir / f"sender-{index}.pt"
        save_agent_checkpoint(path, sender, kind="sender")
        sender_paths.append(path)
    for index, receiver in enumerate(population.receivers):
        path = output_dir / f"receiver-{index}.pt"
        save_agent_checkpoint(path, receiver, kind="receiver")
        receiver_paths.append(path)
    return sender_paths, receiver_paths


def _train_transfer_curve(
    config: dict[str, Any],
    split: WorldSplit,
    train_messages: list[torch.Tensor],
    validation_messages: list[torch.Tensor],
    *,
    seed: int,
    output_dir: Path,
    smoke: bool,
) -> tuple[dict[int, Path], dict[str, Any]]:
    if not config["transfer"]["enabled"]:
        return {}, {}
    rng = np.random.default_rng(seed + 4_004)
    order = rng.permutation(len(split.train))
    budgets = [config["transfer"]["meaning_budgets"][0]] if smoke else config[
        "transfer"
    ]["meaning_budgets"]
    checkpoints: dict[int, Path] = {}
    results: dict[str, Any] = {}
    sender_count = len(train_messages)
    repeated_validation = _repeat_meanings(split.validation, sender_count)
    validation_matrix = torch.cat(validation_messages, dim=0)
    for budget in budgets:
        indices = np.sort(order[:budget])
        selected_meanings = tuple(split.train[int(index)] for index in indices)
        selected_messages = torch.cat(
            [messages[torch.as_tensor(indices)] for messages in train_messages], dim=0
        )
        repeated_selected = _repeat_meanings(selected_meanings, sender_count)
        transfer_config = copy.deepcopy(config)
        transfer_config["translator_training"].update(
            max_steps=config["transfer"]["max_steps"],
            minimum_steps=config["transfer"]["minimum_steps"],
            patience_steps=config["transfer"]["patience_steps"],
        )
        steps = 32 if smoke else config["transfer"]["max_steps"]
        receiver, training_result = train_translator(
            transfer_config,
            selected_messages,
            repeated_selected,
            validation_matrix,
            repeated_validation,
            seed=seed + 2_000_000 + budget,
            max_steps_override=steps,
        )
        path = output_dir / f"transfer-{budget}.pt"
        save_agent_checkpoint(path, receiver, kind="translator")
        checkpoints[budget] = path
        results[str(budget)] = asdict(training_result)
    return checkpoints, results


def _isolated_encode(
    checkpoint: Path, meanings: tuple[Meaning, ...], directory: Path
) -> np.ndarray:
    directory.mkdir(parents=True, exist_ok=True)
    sender_input = directory / "sender-input.json"
    sender_output = directory / "sender-output.json"
    _write_json(
        sender_input, [list(meaning.factors) for meaning in meanings], compact=True
    )
    _run_worker("encode", checkpoint, sender_input, sender_output)
    return _read_matrix(sender_output)


def _isolated_decode(
    checkpoint: Path, messages: np.ndarray, directory: Path
) -> np.ndarray:
    directory.mkdir(parents=True, exist_ok=True)
    decoder_input = directory / "decoder-input.json"
    decoder_output = directory / "decoder-output.json"
    _write_json(decoder_input, messages.tolist(), compact=True)
    _run_worker("decode", checkpoint, decoder_input, decoder_output)
    return _read_matrix(decoder_output)


def _split_slices(
    evaluated_splits: list[tuple[str, tuple[Meaning, ...]]]
) -> dict[str, slice]:
    result = {}
    offset = 0
    for name, meanings in evaluated_splits:
        result[name] = slice(offset, offset + len(meanings))
        offset += len(meanings)
    return result


def _population_metrics(
    evaluated_splits: list[tuple[str, tuple[Meaning, ...]]],
    split_slices: dict[str, slice],
    messages_by_sender: list[np.ndarray],
    predictions_by_receiver: list[np.ndarray],
) -> dict[str, Any]:
    sender_count = len(messages_by_sender)
    block_size = len(messages_by_sender[0])
    result = {}
    for split_name, meanings in evaluated_splits:
        pair_metrics = {}
        exact_values = []
        factor_values = []
        split_slice = split_slices[split_name]
        for sender_index in range(sender_count):
            sender_offset = sender_index * block_size
            indices = slice(
                sender_offset + split_slice.start,
                sender_offset + split_slice.stop,
            )
            for receiver_index, predictions in enumerate(predictions_by_receiver):
                metrics = prediction_metrics(meanings, predictions[indices])
                pair_metrics[f"s{sender_index}-r{receiver_index}"] = metrics
                exact_values.append(metrics["exact_match"])
                factor_values.append(metrics["factor_accuracy"])
        result[split_name] = {
            "mean_exact_match": float(np.mean(exact_values)),
            "worst_pair_exact_match": float(np.min(exact_values)),
            "best_pair_exact_match": float(np.max(exact_values)),
            "mean_factor_accuracy": np.mean(factor_values, axis=0).tolist(),
            "pairs": pair_metrics,
        }
    return result


def _shared_decoder_metrics(
    evaluated_splits: list[tuple[str, tuple[Meaning, ...]]],
    split_slices: dict[str, slice],
    predictions: np.ndarray,
    *,
    sender_count: int,
) -> dict[str, Any]:
    block_size = sum(len(meanings) for _, meanings in evaluated_splits)
    result = {}
    for split_name, meanings in evaluated_splits:
        split_predictions = []
        split_slice = split_slices[split_name]
        for sender_index in range(sender_count):
            offset = sender_index * block_size
            split_predictions.append(
                predictions[
                    offset + split_slice.start : offset + split_slice.stop
                ]
            )
        repeated_meanings = _repeat_meanings(meanings, sender_count)
        result[split_name] = prediction_metrics(
            repeated_meanings, np.concatenate(split_predictions, axis=0)
        )
    return result


def _sender_protocols(
    meanings: tuple[Meaning, ...], messages_by_sender: list[np.ndarray]
) -> dict[str, Any]:
    return {
        f"sender-{index}": protocol_statistics(meanings, messages)
        for index, messages in enumerate(messages_by_sender)
    }


def _sender_message_agreement(messages_by_sender: list[np.ndarray]) -> dict[str, Any]:
    pairs = {}
    values = []
    for left in range(len(messages_by_sender)):
        for right in range(left + 1, len(messages_by_sender)):
            agreement = float(
                np.mean(np.all(messages_by_sender[left] == messages_by_sender[right], axis=1))
            )
            pairs[f"s{left}-s{right}"] = agreement
            values.append(agreement)
    return {"mean_exact_message_agreement": float(np.mean(values)), "pairs": pairs}


def _sender_binding_diagnostics(population: PopulationSystem) -> dict[str, Any] | None:
    if not all(hasattr(sender, "soft_binding_matrix") for sender in population.senders):
        return None
    hard_matrices = [
        sender.binding_matrix(straight_through=False).detach().cpu().numpy()
        for sender in population.senders
    ]
    soft_matrices = [
        sender.soft_binding_matrix().detach().cpu().numpy()
        for sender in population.senders
    ]
    exact_agreement = [
        bool(np.array_equal(hard_matrices[left], hard_matrices[right]))
        for left in range(len(hard_matrices))
        for right in range(left + 1, len(hard_matrices))
    ]
    return {
        "hard_factor_by_slot": [matrix.argmax(axis=1).tolist() for matrix in hard_matrices],
        "hard_matrices": [matrix.astype(int).tolist() for matrix in hard_matrices],
        "soft_matrices": [matrix.tolist() for matrix in soft_matrices],
        "all_senders_same_hard_binding": all(exact_agreement),
        "pairwise_hard_binding_agreement": float(np.mean(exact_agreement)),
    }


def _sender_atom_code_diagnostics(population: PopulationSystem) -> dict[str, Any] | None:
    if not all(hasattr(sender, "codebook_matrix") for sender in population.senders):
        return None
    hard_codes = [
        [
            sender.codebook_matrix(index, straight_through=False)
            .detach()
            .cpu()
            .numpy()
            for index in range(len(population.spec.factor_sizes))
        ]
        for sender in population.senders
    ]
    symbols = [
        [matrix.argmax(axis=1).tolist() for matrix in sender_codes]
        for sender_codes in hard_codes
    ]
    pair_agreements = []
    for left in range(len(hard_codes)):
        for right in range(left + 1, len(hard_codes)):
            pair_agreements.append(
                float(
                    np.mean(
                        [
                            np.array_equal(left_code, right_code)
                            for left_code, right_code in zip(
                                hard_codes[left], hard_codes[right], strict=True
                            )
                        ]
                    )
                )
            )
    injective = [
        all(len(set(code)) == len(code) for code in sender_codes)
        for sender_codes in symbols
    ]
    return {
        "hard_symbols_by_factor": symbols,
        "all_sender_factor_codes_injective": all(injective),
        "sender_factor_codes_injective": injective,
        "all_senders_same_hard_codes": all(value == 1.0 for value in pair_agreements),
        "pairwise_factor_code_agreement": float(np.mean(pair_agreements)),
    }


def _receiver_binding_diagnostics(population: PopulationSystem) -> dict[str, Any] | None:
    if not all(hasattr(receiver, "binding_matrix") for receiver in population.receivers):
        return None
    hard_matrices = [
        receiver.binding_matrix(straight_through=False).detach().cpu().numpy()
        for receiver in population.receivers
    ]
    exact_agreement = [
        bool(np.array_equal(hard_matrices[left], hard_matrices[right]))
        for left in range(len(hard_matrices))
        for right in range(left + 1, len(hard_matrices))
    ]
    return {
        "hard_slot_by_factor": [
            matrix.argmax(axis=1).tolist() for matrix in hard_matrices
        ],
        "hard_matrices": [matrix.astype(int).tolist() for matrix in hard_matrices],
        "all_receivers_same_hard_binding": all(exact_agreement),
        "pairwise_hard_binding_agreement": float(np.mean(exact_agreement)),
    }


def _population_controls(
    config: dict[str, Any],
    receiver_checkpoints: list[Path],
    population: PopulationSystem,
    meanings: tuple[Meaning, ...],
    messages_by_sender: list[np.ndarray],
    original_predictions: list[np.ndarray],
    output_dir: Path,
    *,
    seed: int,
) -> dict[str, Any]:
    rng = np.random.default_rng(seed + 7_007)
    shuffled_by_sender = [
        messages[rng.permutation(len(messages))] for messages in messages_by_sender
    ]
    shuffled_combined = np.concatenate(shuffled_by_sender, axis=0)
    repeated_meanings = _repeat_meanings(meanings, len(messages_by_sender))
    shuffled_scores = []
    for index, checkpoint in enumerate(receiver_checkpoints):
        predictions = _isolated_decode(
            checkpoint,
            shuffled_combined,
            output_dir / "controls" / f"shuffled-r{index}",
        )
        shuffled_scores.append(
            prediction_metrics(repeated_meanings, predictions)["exact_match"]
        )

    permutation = rng.permutation(config["channel"]["vocabulary_size"])
    permuted_messages = permutation[np.concatenate(messages_by_sender, axis=0)]
    permutation_preserves = True
    for index, (receiver, checkpoint, original) in enumerate(
        zip(population.receivers, receiver_checkpoints, original_predictions, strict=True)
    ):
        permuted_receiver = copy.deepcopy(receiver).cpu()
        with torch.no_grad():
            old_weight = permuted_receiver.symbol_embedding.weight.detach().clone()
            permuted_receiver.symbol_embedding.weight[torch.as_tensor(permutation)] = old_weight
        permuted_checkpoint = output_dir / "controls" / f"permuted-r{index}.pt"
        permuted_checkpoint.parent.mkdir(parents=True, exist_ok=True)
        save_agent_checkpoint(permuted_checkpoint, permuted_receiver, kind="receiver")
        predictions = _isolated_decode(
            permuted_checkpoint,
            permuted_messages,
            output_dir / "controls" / f"permuted-r{index}",
        )
        permutation_preserves = permutation_preserves and bool(
            np.array_equal(predictions, original)
        )

    shuffled_mean = float(np.mean(shuffled_scores))
    maximum = config["controls"]["shuffled_messages_expected_exact_match_max"]
    return {
        "shuffled_messages_mean_exact_match": shuffled_mean,
        "shuffled_messages_by_receiver": shuffled_scores,
        "shuffled_messages_maximum": maximum,
        "shuffled_messages_pass": shuffled_mean <= maximum,
        "consistent_symbol_permutation": permutation.tolist(),
        "consistent_symbol_permutation_preserves_all_predictions": permutation_preserves,
        "channel_isolation": {
            "sender_process_input": "factor matrix only",
            "receiver_process_input": "symbol matrix only",
            "receiver_input_contains_ids": False,
            "separate_processes": True,
        },
    }


def _population_episodes(
    config: dict[str, Any],
    seed: int,
    evaluated_splits: list[tuple[str, tuple[Meaning, ...]]],
    split_slices: dict[str, slice],
    messages_by_sender: list[np.ndarray],
    predictions_by_receiver: list[np.ndarray],
) -> list[dict[str, Any]]:
    protocol_version = config["experiment"]["id"]
    run_id = f"{protocol_version}-seed-{seed}"
    block_size = len(messages_by_sender[0])
    records = []
    for split_name, meanings in evaluated_splits:
        split_slice = split_slices[split_name]
        for sender_index, sender_messages in enumerate(messages_by_sender):
            for receiver_index, receiver_predictions in enumerate(predictions_by_receiver):
                offset = sender_index * block_size
                prediction_slice = receiver_predictions[
                    offset + split_slice.start : offset + split_slice.stop
                ]
                message_slice = sender_messages[split_slice]
                for local_index, (meaning, message, prediction) in enumerate(
                    zip(meanings, message_slice, prediction_slice, strict=True)
                ):
                    episode_id = (
                        f"{split_name}-s{sender_index}-r{receiver_index}-{local_index:04d}"
                    )
                    reconstruction = meaning_from_factors(prediction, config)
                    factor_correct = [
                        left == right
                        for left, right in zip(
                            meaning.factors, reconstruction.factors, strict=True
                        )
                    ]
                    records.append(
                        {
                            "episode_id": episode_id,
                            "run_id": run_id,
                            "seed": seed,
                            "split": split_name,
                            "meaning": meaning.to_schema_dict(),
                            "message": {
                                "protocol_version": protocol_version,
                                "run_id": run_id,
                                "episode_id": episode_id,
                                "sender_id": f"sender-{sender_index}",
                                "receiver_id": f"receiver-{receiver_index}",
                                "symbols": [int(value) for value in message],
                                "channel_bits": config["channel"]["bits_per_message"],
                            },
                            "reconstruction": reconstruction.to_schema_dict(),
                            "exact_match": all(factor_correct),
                            "factor_correct": dict(
                                zip(
                                    ("color", "shape", "size", "texture"),
                                    factor_correct,
                                    strict=True,
                                )
                            ),
                        }
                    )
    return records


def _repeat_meanings(
    meanings: tuple[Meaning, ...], repetitions: int
) -> tuple[Meaning, ...]:
    return tuple(meaning for _ in range(repetitions) for meaning in meanings)


def _classify(
    config: dict[str, Any], result: dict[str, Any], *, development: bool
) -> str:
    controls = result["controls"]
    if not (
        controls["shuffled_messages_pass"]
        and controls["consistent_symbol_permutation_preserves_all_predictions"]
    ):
        return "invalid"
    if development:
        return "development_only"
    if not result["test_unsealed"]:
        return "technical_smoke_only"
    thresholds = config["outcome_thresholds"]["strong_evidence"]
    known = result["population"]["train"]
    test = result["population"]["compositional_test"]
    translator_test = result["universal_translator"]["compositional_test"]
    if (
        known["mean_exact_match"] >= thresholds["population_known_mean_min"]
        and known["worst_pair_exact_match"]
        >= thresholds["population_known_worst_pair_min"]
        and test["mean_exact_match"]
        >= thresholds["population_compositional_mean_min"]
        and translator_test["exact_match"]
        >= thresholds["universal_translator_compositional_min"]
    ):
        return "strong_evidence"
    reference = config["outcome_thresholds"].get(
        "compositional_mean_reference",
        config["outcome_thresholds"].get("ecp0_compositional_mean_reference", 0.0),
    )
    if test["mean_exact_match"] > reference:
        return "mixed_evidence"
    return "negative_result"


def _summarize(
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
    elif classifications.count("invalid"):
        overall = "contains_invalid_runs"
    elif classifications.count("strong_evidence") >= config["outcome_thresholds"][
        "strong_evidence"
    ]["minimum_valid_runs"]:
        overall = "strong_evidence"
    elif any(value in {"strong_evidence", "mixed_evidence"} for value in classifications):
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
    results: list[dict[str, Any]],
    summary: dict[str, Any],
    *,
    smoke: bool,
    development: bool,
) -> str:
    experiment_id = summary["experiment_id"].upper()
    title = (
        f"{experiment_id} technische proefrun"
        if smoke
        else f"{experiment_id} ontwikkelrun"
        if development
        else f"{experiment_id} experimentrapport"
    )
    lines = [
        f"# {title}",
        "",
        f"Classificatie: **{summary['overall_classification']}**",
        "",
        "| Seed | Bekend gemiddeld | Bekend slechtste paar | Validatie gemiddeld | Test gemiddeld | Universele vertaler test | Classificatie |",
        "|---:|---:|---:|---:|---:|---:|---|",
    ]
    for result in results:
        population = result["population"]
        test = population.get("compositional_test")
        translator_test = result["universal_translator"].get("compositional_test")
        lines.append(
            "| {seed} | {known:.3f} | {worst:.3f} | {validation:.3f} | {test} | {translator} | {classification} |".format(
                seed=result["seed"],
                known=population["train"]["mean_exact_match"],
                worst=population["train"]["worst_pair_exact_match"],
                validation=population["validation"]["mean_exact_match"],
                test="—" if test is None else f"{test['mean_exact_match']:.3f}",
                translator="—"
                if translator_test is None
                else f"{translator_test['exact_match']:.3f}",
                classification=result["classification"],
            )
        )
    lines.extend(
        [
            "",
            "## Methodologische status",
            "",
            "Alle zenders en ontvangers hebben onafhankelijke parameters. Tijdens de definitieve evaluatie ontvingen afzonderlijke ontvangerprocessen uitsluitend symboolmatrices van alle zenders.",
            "",
        ]
    )
    if smoke:
        lines.append(
            f"Technische ketencontrole; de {experiment_id}-testset bleef gesloten."
        )
    elif development:
        lines.append(
            f"Volledige ontwikkeltraining; de {experiment_id}-testset bleef gesloten."
        )
    else:
        lines.append(
            f"Confirmatieve run met de vooraf bevroren {experiment_id}-configuratie en eenmalige testontzegeling."
        )
    lines.append("")
    return "\n".join(lines)
