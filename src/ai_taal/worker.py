"""Isolated sender and decoder processes for final evaluation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch

from ai_taal.models import (
    FactorizedPermutationSlotReceiver,
    InjectivePermutationSlotSender,
    LearnedPermutationSlotSender,
    MinimalPermutationSlotSender,
    Receiver,
    Sender,
    load_agent_checkpoint,
)
from ai_taal.training import encode_meanings, predict_receiver


def _read_matrix(path: Path) -> torch.Tensor:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, list) or any(not isinstance(row, list) for row in value):
        raise ValueError("Worker input must be a JSON matrix.")
    return torch.tensor(value, dtype=torch.long)


def _write_matrix(path: Path, value: torch.Tensor) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(value.detach().cpu().tolist(), handle, separators=(",", ":"))
        handle.write("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("encode", "decode"))
    parser.add_argument("--checkpoint", required=True, type=Path)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)

    matrix = _read_matrix(args.input)
    if args.mode == "encode":
        agent = load_agent_checkpoint(args.checkpoint, expected_kind="sender")
        if not isinstance(
            agent,
            (
                Sender,
                LearnedPermutationSlotSender,
                InjectivePermutationSlotSender,
                MinimalPermutationSlotSender,
            ),
        ):
            raise TypeError("Sender checkpoint did not load a sender.")
        output = encode_meanings(agent, matrix)
    else:
        agent = load_agent_checkpoint(args.checkpoint)
        if not isinstance(agent, (Receiver, FactorizedPermutationSlotReceiver)):
            raise TypeError("Decoder checkpoint did not load a receiver.")
        output = predict_receiver(agent, matrix)
    _write_matrix(args.output, output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
    MinimalPermutationSlotSender,
