"""Reproduceerbare post-runanalyse van een voltooid ECP-0-experiment."""

from __future__ import annotations

import hashlib
import itertools
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from ai_taal.metrics import topographic_permutation_test


def analyze_run(
    run_directory: str | Path, *, permutations: int = 100
) -> dict[str, Any]:
    run_directory = Path(run_directory)
    summary = _read_json(run_directory / "summary.json")
    mismatches = _hash_mismatches(run_directory, summary["artifact_sha256"])

    metrics_paths = sorted(run_directory.glob("seed-*/metrics.json"))
    if not metrics_paths:
        raise ValueError(f"Geen seedmetrics gevonden in {run_directory}.")
    first_metrics = _read_json(metrics_paths[0])
    if "population" in first_metrics:
        return _analyze_population_run(
            run_directory,
            summary,
            metrics_paths,
            mismatches,
            permutations=permutations,
        )

    rows = []
    for metrics_path in metrics_paths:
        metrics = _read_json(metrics_path)
        semantic, messages = _episode_matrices(metrics_path.parent / "episodes.jsonl")
        topology_null = topographic_permutation_test(
            semantic,
            messages,
            repetitions=permutations,
            seed=metrics["seed"] + 9_001,
        )
        rows.append(
            {
                "seed": metrics["seed"],
                "classification": metrics["classification"],
                "known_exact_match": metrics["receiver"]["train"]["exact_match"],
                "validation_exact_match": metrics["receiver"]["validation"][
                    "exact_match"
                ],
                "compositional_exact_match": metrics["receiver"][
                    "compositional_test"
                ]["exact_match"],
                "translator_compositional_exact_match": metrics["translator"][
                    "compositional_test"
                ]["exact_match"],
                "topographic_permutation_test": topology_null,
            }
        )

    metric_names = (
        "known_exact_match",
        "validation_exact_match",
        "compositional_exact_match",
        "translator_compositional_exact_match",
    )
    aggregates = {
        name: {
            "mean": statistics.mean(row[name] for row in rows),
            "median": statistics.median(row[name] for row in rows),
            "minimum": min(row[name] for row in rows),
            "maximum": max(row[name] for row in rows),
        }
        for name in metric_names
    }
    analysis = {
        "analysis_type": "post_run_preregistered_diagnostic_completion",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "run_directory": str(run_directory),
        "primary_summary_classification": summary["overall_classification"],
        "integrity": {
            "checked_artifact_count": len(summary["artifact_sha256"]),
            "hash_mismatches": mismatches,
            "all_artifacts_match": not mismatches,
        },
        "aggregates": aggregates,
        "hypothesis_counts": {
            "known_accuracy_at_least_0_99": sum(
                row["known_exact_match"] >= 0.99 for row in rows
            ),
            "composition_above_zero_lookup": sum(
                row["compositional_exact_match"] > 0 for row in rows
            ),
            "translator_composition_above_zero_lookup": sum(
                row["translator_compositional_exact_match"] > 0 for row in rows
            ),
            "topography_above_permutation_null_p_le_0_01": sum(
                row["topographic_permutation_test"]["empirical_one_sided_p"] <= 0.01
                for row in rows
            ),
        },
        "seeds": rows,
    }
    output_path = run_directory / "posthoc-analysis.json"
    output_path.write_text(
        json.dumps(analysis, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return analysis


def compare_population_runs(
    intervention_directory: str | Path,
    control_directory: str | Path,
) -> dict[str, Any]:
    intervention_directory = Path(intervention_directory)
    control_directory = Path(control_directory)
    intervention_summary = _read_json(intervention_directory / "summary.json")
    control_summary = _read_json(control_directory / "summary.json")
    intervention_split = _read_json(intervention_directory / "split_manifest.json")
    control_split = _read_json(control_directory / "split_manifest.json")
    if intervention_split["sha256"] != control_split["sha256"]:
        raise ValueError("Interventie en controle gebruiken niet dezelfde datasplit.")

    intervention_metrics = {
        int(metrics["seed"]): metrics
        for path in intervention_directory.glob("seed-*/metrics.json")
        for metrics in [_read_json(path)]
    }
    control_metrics = {
        int(metrics["seed"]): metrics
        for path in control_directory.glob("seed-*/metrics.json")
        for metrics in [_read_json(path)]
    }
    if intervention_metrics.keys() != control_metrics.keys():
        raise ValueError("Interventie en controle bevatten niet dezelfde seeds.")

    rows = []
    for seed in sorted(intervention_metrics):
        intervention = intervention_metrics[seed]
        control = control_metrics[seed]
        intervention_test = intervention["population"]["compositional_test"][
            "mean_exact_match"
        ]
        control_test = control["population"]["compositional_test"][
            "mean_exact_match"
        ]
        intervention_translator = intervention["universal_translator"][
            "compositional_test"
        ]["exact_match"]
        control_translator = control["universal_translator"][
            "compositional_test"
        ]["exact_match"]
        rows.append(
            {
                "seed": seed,
                "intervention_classification": intervention["classification"],
                "control_classification": control["classification"],
                "intervention_test_exact": intervention_test,
                "control_test_exact": control_test,
                "test_exact_difference": intervention_test - control_test,
                "intervention_translator_test_exact": intervention_translator,
                "control_translator_test_exact": control_translator,
                "translator_test_exact_difference": (
                    intervention_translator - control_translator
                ),
            }
        )

    test_differences = [row["test_exact_difference"] for row in rows]
    translator_differences = [
        row["translator_test_exact_difference"] for row in rows
    ]
    comparison = {
        "analysis_type": "preregistered_paired_population_comparison",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "intervention_directory": str(intervention_directory),
        "control_directory": str(control_directory),
        "split_sha256": intervention_split["sha256"],
        "integrity": {
            "intervention_all_artifacts_match": not _hash_mismatches(
                intervention_directory, intervention_summary["artifact_sha256"]
            ),
            "control_all_artifacts_match": not _hash_mismatches(
                control_directory, control_summary["artifact_sha256"]
            ),
        },
        "population_compositional_test": {
            "intervention_mean": statistics.mean(
                row["intervention_test_exact"] for row in rows
            ),
            "control_mean": statistics.mean(
                row["control_test_exact"] for row in rows
            ),
            "paired_mean_difference": statistics.mean(test_differences),
            "paired_median_difference": statistics.median(test_differences),
            "intervention_better_seed_count": sum(
                difference > 0 for difference in test_differences
            ),
            "paired_sign_flip_test": _paired_sign_flip_test(test_differences),
        },
        "universal_translator_compositional_test": {
            "intervention_mean": statistics.mean(
                row["intervention_translator_test_exact"] for row in rows
            ),
            "control_mean": statistics.mean(
                row["control_translator_test_exact"] for row in rows
            ),
            "paired_mean_difference": statistics.mean(translator_differences),
            "paired_median_difference": statistics.median(translator_differences),
            "intervention_better_seed_count": sum(
                difference > 0 for difference in translator_differences
            ),
            "paired_sign_flip_test": _paired_sign_flip_test(
                translator_differences
            ),
        },
        "intervention_strong_seed_count": sum(
            row["intervention_classification"] == "strong_evidence" for row in rows
        ),
        "control_strong_seed_count": sum(
            row["control_classification"] == "strong_evidence" for row in rows
        ),
        "seeds": rows,
    }
    _write_json_file(intervention_directory / "paired-comparison.json", comparison)
    return comparison


def _paired_sign_flip_test(differences: list[float]) -> dict[str, Any]:
    if not differences:
        raise ValueError("Minstens één gepaard verschil is vereist.")
    observed = statistics.mean(differences)
    null_values = [
        statistics.mean(
            sign * difference
            for sign, difference in zip(signs, differences, strict=True)
        )
        for signs in itertools.product((-1, 1), repeat=len(differences))
    ]
    return {
        "observed_mean_difference": observed,
        "null_combinations": len(null_values),
        "exact_one_sided_p": sum(value >= observed for value in null_values)
        / len(null_values),
    }


def _analyze_population_run(
    run_directory: Path,
    summary: dict[str, Any],
    metrics_paths: list[Path],
    mismatches: list[str],
    *,
    permutations: int,
) -> dict[str, Any]:
    config = yaml.safe_load(
        (run_directory / "effective_config.yaml").read_text(encoding="utf-8")
    )
    thresholds = config["outcome_thresholds"]["strong_evidence"]
    outcome_thresholds = config["outcome_thresholds"]
    comparison_reference = outcome_thresholds.get(
        "compositional_mean_reference",
        outcome_thresholds.get("ecp0_compositional_mean_reference", 0.0),
    )

    rows = []
    for metrics_path in metrics_paths:
        metrics = _read_json(metrics_path)
        sender_matrices, episode_count = _population_episode_matrices(
            metrics_path.parent / "episodes.jsonl"
        )
        topology = {
            sender_id: topographic_permutation_test(
                semantic,
                messages,
                repetitions=permutations,
                seed=metrics["seed"] + 9_001 + int(sender_id.rsplit("-", 1)[1]),
            )
            for sender_id, (semantic, messages) in sender_matrices.items()
        }
        factor_local_audit = _factor_local_channel_audit(
            metrics_path.parent / "episodes.jsonl", metrics, config
        )
        rows.append(
            {
                "seed": metrics["seed"],
                "classification": metrics["classification"],
                "population_known_mean_exact_match": metrics["population"]["train"][
                    "mean_exact_match"
                ],
                "population_known_worst_pair_exact_match": metrics["population"][
                    "train"
                ]["worst_pair_exact_match"],
                "population_validation_mean_exact_match": metrics["population"][
                    "validation"
                ]["mean_exact_match"],
                "population_compositional_mean_exact_match": metrics["population"][
                    "compositional_test"
                ]["mean_exact_match"],
                "population_compositional_worst_pair_exact_match": metrics[
                    "population"
                ]["compositional_test"]["worst_pair_exact_match"],
                "universal_translator_compositional_exact_match": metrics[
                    "universal_translator"
                ]["compositional_test"]["exact_match"],
                "sender_message_agreement": metrics["sender_message_agreement"][
                    "mean_exact_message_agreement"
                ],
                "transfer_compositional_exact_match": {
                    budget: result["compositional_test"]["exact_match"]
                    for budget, result in metrics["transfer_curve"].items()
                },
                "sender_topographic_permutation_tests": topology,
                "episode_count": episode_count,
                "factor_local_channel_audit": factor_local_audit,
            }
        )

    metric_names = (
        "population_known_mean_exact_match",
        "population_known_worst_pair_exact_match",
        "population_validation_mean_exact_match",
        "population_compositional_mean_exact_match",
        "population_compositional_worst_pair_exact_match",
        "universal_translator_compositional_exact_match",
        "sender_message_agreement",
    )
    aggregates = {
        name: {
            "mean": statistics.mean(row[name] for row in rows),
            "median": statistics.median(row[name] for row in rows),
            "minimum": min(row[name] for row in rows),
            "maximum": max(row[name] for row in rows),
        }
        for name in metric_names
    }
    budgets = sorted(rows[0]["transfer_compositional_exact_match"], key=int)
    aggregates["transfer_compositional_exact_match"] = {
        budget: {
            "mean": statistics.mean(
                row["transfer_compositional_exact_match"][budget] for row in rows
            ),
            "median": statistics.median(
                row["transfer_compositional_exact_match"][budget] for row in rows
            ),
        }
        for budget in budgets
    }

    analysis = {
        "analysis_type": "post_run_preregistered_population_diagnostic_completion",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "run_directory": str(run_directory),
        "primary_summary_classification": summary["overall_classification"],
        "integrity": {
            "checked_artifact_count": len(summary["artifact_sha256"]),
            "hash_mismatches": mismatches,
            "all_artifacts_match": not mismatches,
            "episode_counts": {str(row["seed"]): row["episode_count"] for row in rows},
            "total_episode_count": sum(row["episode_count"] for row in rows),
            "factor_local_channel_audits": {
                str(row["seed"]): row["factor_local_channel_audit"] for row in rows
            },
            "all_factor_local_messages_valid": all(
                audit["valid"]
                for row in rows
                for audit in [row["factor_local_channel_audit"]]
                if audit["applicable"]
            ),
        },
        "aggregates": aggregates,
        "hypothesis_counts": {
            "population_known_mean_at_threshold": sum(
                row["population_known_mean_exact_match"]
                >= thresholds["population_known_mean_min"]
                for row in rows
            ),
            "population_known_worst_pair_at_threshold": sum(
                row["population_known_worst_pair_exact_match"]
                >= thresholds["population_known_worst_pair_min"]
                for row in rows
            ),
            "population_composition_at_threshold": sum(
                row["population_compositional_mean_exact_match"]
                >= thresholds["population_compositional_mean_min"]
                for row in rows
            ),
            "universal_translator_composition_at_threshold": sum(
                row["universal_translator_compositional_exact_match"]
                >= thresholds["universal_translator_compositional_min"]
                for row in rows
            ),
            "composition_above_registered_reference": sum(
                row["population_compositional_mean_exact_match"]
                > comparison_reference
                for row in rows
            ),
            "sender_topography_above_permutation_null_p_le_0_01": sum(
                test["empirical_one_sided_p"] <= 0.01
                for row in rows
                for test in row["sender_topographic_permutation_tests"].values()
            ),
        },
        "seeds": rows,
    }
    _write_analysis(run_directory, analysis)
    return analysis


def _episode_matrices(path: Path) -> tuple[np.ndarray, np.ndarray]:
    semantic = []
    messages = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            episode = json.loads(line)
            meaning = episode["meaning"]
            semantic.append(
                [
                    int(meaning["color"][1:]),
                    int(meaning["shape"][1:]),
                    int(meaning["size"][1:]),
                    int(meaning["texture"][1:]),
                ]
            )
            messages.append(episode["message"]["symbols"])
    return np.asarray(semantic, dtype=np.int16), np.asarray(messages, dtype=np.int16)


def _population_episode_matrices(
    path: Path,
) -> tuple[dict[str, tuple[np.ndarray, np.ndarray]], int]:
    rows: dict[str, tuple[list[list[int]], list[list[int]]]] = {}
    episode_count = 0
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            episode_count += 1
            episode = json.loads(line)
            message = episode["message"]
            if message["receiver_id"] != "receiver-0":
                continue
            sender_id = message["sender_id"]
            semantic, messages = rows.setdefault(sender_id, ([], []))
            meaning = episode["meaning"]
            semantic.append(
                [
                    int(meaning["color"][1:]),
                    int(meaning["shape"][1:]),
                    int(meaning["size"][1:]),
                    int(meaning["texture"][1:]),
                ]
            )
            messages.append(message["symbols"])
    return {
        sender_id: (
            np.asarray(semantic, dtype=np.int16),
            np.asarray(messages, dtype=np.int16),
        )
        for sender_id, (semantic, messages) in sorted(rows.items())
    }, episode_count


def _factor_local_channel_audit(
    path: Path, metrics: dict[str, Any], config: dict[str, Any]
) -> dict[str, Any]:
    channel = config["channel"]
    if channel["type"] != "factor_local_discrete_fixed_length":
        return {"applicable": False, "valid": True}
    factor_sizes = channel["factor_alphabet_sizes"]
    bindings = metrics["sender_binding_diagnostics"]["hard_factor_by_slot"]
    violations = []
    checked = 0
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            episode = json.loads(line)
            message = episode["message"]
            sender_index = int(message["sender_id"].rsplit("-", 1)[1])
            factor_by_slot = bindings[sender_index]
            checked += 1
            if message["channel_bits"] != channel["bits_per_message"]:
                violations.append(
                    {"line": line_number, "reason": "incorrect_channel_bits"}
                )
            for slot_index, symbol in enumerate(message["symbols"]):
                factor_index = factor_by_slot[slot_index]
                if symbol < 0 or symbol >= factor_sizes[factor_index]:
                    violations.append(
                        {
                            "line": line_number,
                            "reason": "symbol_outside_local_alphabet",
                            "slot": slot_index,
                            "factor": factor_index,
                            "symbol": symbol,
                            "alphabet_size": factor_sizes[factor_index],
                        }
                    )
            if len(violations) >= 20:
                break
    return {
        "applicable": True,
        "valid": not violations,
        "checked_episode_messages": checked,
        "bits_per_message": channel["bits_per_message"],
        "factor_alphabet_sizes": factor_sizes,
        "violation_count_capped_at_20": len(violations),
        "violations": violations,
    }


def _hash_mismatches(
    run_directory: Path, expected_hashes: dict[str, str]
) -> list[str]:
    mismatches = []
    for relative_path, expected in expected_hashes.items():
        path = run_directory / relative_path
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            mismatches.append(relative_path)
    return mismatches


def _write_analysis(run_directory: Path, analysis: dict[str, Any]) -> None:
    output_path = run_directory / "posthoc-analysis.json"
    output_path.write_text(
        json.dumps(analysis, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_json_file(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
