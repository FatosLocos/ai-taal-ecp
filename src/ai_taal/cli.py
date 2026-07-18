"""Commandoregelinterface voor ECP-0."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

from ai_taal.analysis import analyze_run, compare_population_runs
from ai_taal.config import load_config
from ai_taal.experiment import run_experiment, validate_schemas
from ai_taal.population_experiment import run_population_experiment
from ai_taal.world import build_splits


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ecp0", description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("config/ecp0.yaml"))
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate", help="Valideer configuratie en JSON-schema's.")
    subparsers.add_parser("split", help="Toon de deterministische datasplitsing.")

    analyze = subparsers.add_parser(
        "analyze", help="Controleer en analyseer een voltooide confirmatieve run."
    )
    analyze.add_argument("run_directory", type=Path)
    analyze.add_argument("--permutations", type=int, default=100)

    compare = subparsers.add_parser(
        "compare", help="Vergelijk gepaarde confirmatieve populatiearmen."
    )
    compare.add_argument("intervention_directory", type=Path)
    compare.add_argument("control_directory", type=Path)

    smoke = subparsers.add_parser(
        "smoke", help="Draai 25 stappen zonder de compositionele testset te openen."
    )
    smoke.add_argument("--output-root", type=Path, default=Path("runs"))
    smoke.add_argument("--seed", type=int)

    development = subparsers.add_parser(
        "develop",
        help="Train volledig op train/validatie en houd de compositionele testset gesloten.",
    )
    development.add_argument("--output-root", type=Path, default=Path("runs"))
    development.add_argument("--seed", action="append", type=int)
    development.add_argument(
        "--algebraic-weight",
        type=float,
        help=(
            "Alleen voor ontwikkeling: overschrijf het gewicht van de "
            "algebraïsche consistentiedruk; 0 schakelt haar uit."
        ),
    )
    development.add_argument(
        "--replacement-interval",
        type=int,
        help=(
            "Alleen voor ontwikkeling: vervang na dit aantal stappen één zender "
            "en ontvanger; 0 schakelt culturele transmissie uit."
        ),
    )
    development.add_argument(
        "--maximum-replacements",
        type=int,
        help=(
            "Alleen voor ontwikkeling: stop culturele vervanging na dit aantal "
            "agents; 0 betekent doorgaan tot het einde."
        ),
    )
    development.add_argument(
        "--sender-family",
        choices=(
            "categorical_encoder_autoregressive_sender",
            "learned_permutation_slot_sender",
            "injective_permutation_slot_sender",
            "minimal_permutation_slot_sender",
        ),
        help="Alleen voor ontwikkeling: overschrijf de zenderarchitectuur.",
    )
    development.add_argument(
        "--slot-consensus-weight",
        type=float,
        help=(
            "Alleen voor ontwikkeling: gebruik de permutationslotzender met "
            "dit gewicht voor betekenisvrije bindingsconsensus."
        ),
    )

    experiment = subparsers.add_parser(
        "experiment", help="Draai de vooraf vastgelegde confirmatieve runs."
    )
    experiment.add_argument("--output-root", type=Path, default=Path("runs"))
    experiment.add_argument(
        "--unseal-test",
        action="store_true",
        help="Bevestig expliciet dat de compositionele testset eenmalig mag worden gebruikt.",
    )
    experiment.add_argument(
        "--seed",
        action="append",
        type=int,
        help="Beperk tot één of meer seeds; zonder deze vlag worden alle vijf gebruikt.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = load_config(args.config)
    experiment_runner = (
        run_population_experiment
        if config.get("agents", {}).get("population", {}).get("enabled", False)
        else run_experiment
    )
    if args.command == "validate":
        validate_schemas(Path(config["artifacts"]["meaning_schema"]).parent)
        split = build_splits(config)
        print(
            "Configuratie, schema's en splitsing geldig: "
            f"{len(split.train)}/{len(split.validation)}/{len(split.compositional_test)}"
        )
        return 0
    if args.command == "split":
        print(json.dumps(build_splits(config).manifest(), indent=2, sort_keys=True))
        return 0
    if args.command == "analyze":
        analysis = analyze_run(args.run_directory, permutations=args.permutations)
        print(json.dumps(analysis, indent=2, sort_keys=True))
        return 0
    if args.command == "compare":
        comparison = compare_population_runs(
            args.intervention_directory, args.control_directory
        )
        print(json.dumps(comparison, indent=2, sort_keys=True))
        return 0
    if args.command == "smoke":
        seeds = [args.seed] if args.seed is not None else None
        run_dir = experiment_runner(
            config,
            config_path=args.config,
            output_root=args.output_root,
            smoke=True,
            unseal_test=False,
            development=False,
            seeds=seeds,
        )
        print(run_dir)
        return 0
    if args.command == "develop":
        if (
            args.algebraic_weight is not None
            and args.replacement_interval is not None
            and args.algebraic_weight > 0
            and args.replacement_interval > 0
        ):
            raise ValueError(
                "Ontwikkel één interventie tegelijk: algebraïsch of generationeel."
            )
        if args.sender_family is not None and (
            (args.algebraic_weight or 0) > 0
            or (args.replacement_interval or 0) > 0
        ):
            raise ValueError(
                "Test een nieuwe zenderarchitectuur eerst zonder tweede interventie."
            )
        if args.slot_consensus_weight is not None and (
            (args.algebraic_weight or 0) > 0
            or (args.replacement_interval or 0) > 0
        ):
            raise ValueError(
                "Bindingsconsensus wordt zonder tweede interventie ontwikkeld."
            )
        if (
            args.algebraic_weight is not None
            or args.replacement_interval is not None
            or args.slot_consensus_weight is not None
        ):
            config = copy.deepcopy(config)
        if args.sender_family is not None:
            config = copy.deepcopy(config)
        if args.algebraic_weight is not None:
            if args.algebraic_weight < 0:
                raise ValueError("Algebraïsch gewicht mag niet negatief zijn.")
            regularizer = config["training"]["algebraic_consistency"]
            regularizer["enabled"] = args.algebraic_weight > 0
            regularizer["weight"] = args.algebraic_weight
            config["experiment"]["development_variant"] = {
                "algebraic_weight": args.algebraic_weight
            }
        if args.replacement_interval is not None:
            if args.replacement_interval < 0:
                raise ValueError("Vervangingsinterval mag niet negatief zijn.")
            config["training"]["algebraic_consistency"]["enabled"] = False
            transmission = config["training"]["cultural_transmission"]
            transmission["enabled"] = args.replacement_interval > 0
            transmission["replacement_interval"] = args.replacement_interval
            config["experiment"]["development_variant"] = {
                "replacement_interval": args.replacement_interval
            }
        if args.maximum_replacements is not None:
            if args.maximum_replacements < 0:
                raise ValueError("Maximum aantal vervangingen mag niet negatief zijn.")
            if args.replacement_interval is None:
                raise ValueError(
                    "--maximum-replacements vereist --replacement-interval."
                )
            transmission["maximum_replacements"] = args.maximum_replacements
            config["experiment"]["development_variant"][
                "maximum_replacements"
            ] = args.maximum_replacements
        if args.sender_family is not None:
            config["agents"]["sender"]["family"] = args.sender_family
            config["training"]["algebraic_consistency"]["enabled"] = False
            config["training"]["cultural_transmission"]["enabled"] = False
            config["experiment"]["development_variant"] = {
                "sender_family": args.sender_family
            }
        if args.slot_consensus_weight is not None:
            if args.slot_consensus_weight < 0:
                raise ValueError("Bindingsconsensusgewicht mag niet negatief zijn.")
            config["agents"]["sender"]["family"] = (
                "learned_permutation_slot_sender"
            )
            config["training"]["algebraic_consistency"]["enabled"] = False
            config["training"]["cultural_transmission"]["enabled"] = False
            consensus = config["training"]["slot_binding_consensus"]
            consensus["enabled"] = args.slot_consensus_weight > 0
            consensus["weight"] = args.slot_consensus_weight
            config["experiment"]["development_variant"] = {
                "sender_family": "learned_permutation_slot_sender",
                "slot_consensus_weight": args.slot_consensus_weight,
            }
        run_dir = experiment_runner(
            config,
            config_path=args.config,
            output_root=args.output_root,
            smoke=False,
            unseal_test=False,
            development=True,
            seeds=args.seed,
        )
        print(run_dir)
        return 0
    if args.command == "experiment":
        run_dir = experiment_runner(
            config,
            config_path=args.config,
            output_root=args.output_root,
            smoke=False,
            unseal_test=args.unseal_test,
            development=False,
            seeds=args.seed,
        )
        print(run_dir)
        return 0
    raise AssertionError(f"Onbekend commando: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
