"""Expliciete menselijke, technische en niet-compositionele vergelijkingen."""

from __future__ import annotations

import json
import math
from typing import Any, Iterable

import numpy as np

from ai_taal.world import Meaning


def compute_baselines(meanings: Iterable[Meaning]) -> dict[str, Any]:
    meanings = tuple(meanings)
    dutch_bits = []
    json_bits = []
    for meaning in meanings:
        labels = meaning.to_schema_dict()
        dutch = (
            f"kleur {labels['color']}, vorm {labels['shape']}, "
            f"grootte {labels['size']}, textuur {labels['texture']}"
        )
        canonical_json = json.dumps(
            {
                "color": labels["color"],
                "shape": labels["shape"],
                "size": labels["size"],
                "texture": labels["texture"],
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        dutch_bits.append(len(dutch.encode("utf-8")) * 8)
        json_bits.append(len(canonical_json.encode("utf-8")) * 8)

    factor_sizes = tuple(
        max(meaning.factors[index] for meaning in meanings) + 1
        for index in range(4)
    )
    source_bits = math.ceil(math.log2(math.prod(factor_sizes)))
    local_factor_bits = sum(math.ceil(math.log2(size)) for size in factor_sizes)
    handcrafted_messages = np.asarray(
        [
            [
                meaning.color,
                meaning.shape,
                meaning.size * factor_sizes[3] + meaning.texture,
            ]
            for meaning in meanings
        ],
        dtype=np.int64,
    )
    result = {
        "dutch_template_utf8": _size_summary(dutch_bits),
        "canonical_json_utf8": _size_summary(json_bits),
        "packed_factor_code_optimal": {
            "bits_per_message": source_bits,
            "known_exact_match": 1.0,
            "compositional_exact_match": 1.0,
            "note": "Ontworpen technische referentie en bronondergrens.",
        },
        "random_lookup_code": {
            "bits_per_message": source_bits,
            "known_exact_match": 1.0,
            "compositional_exact_match": 0.0,
            "note": "Onbekende betekenissen hebben per definitie geen geleerd codeboekitem.",
        },
        "factor_local_compositional_code": {
            "bits_per_message": local_factor_bits,
            "known_exact_match": 1.0,
            "compositional_exact_match": 1.0,
            "unique_message_count": int(len(np.unique(handcrafted_messages, axis=0))),
            "note": "Handmatig factor-lokaal referentieprotocol.",
        },
    }
    if factor_sizes == (8, 8, 4, 4):
        result["packed_factor_code_10_bit"] = dict(
            result["packed_factor_code_optimal"]
        )
        result["handcrafted_compositional_code"] = {
            "bits_per_message": 12,
            "known_exact_match": 1.0,
            "compositional_exact_match": 1.0,
            "unique_message_count": int(len(np.unique(handcrafted_messages, axis=0))),
            "note": "Positie 1=kleur, positie 2=vorm, positie 3=grootte-textuur.",
        }
    return result


def _size_summary(values: list[int]) -> dict[str, float | str]:
    array = np.asarray(values, dtype=np.float64)
    return {
        "mean_bits_per_message": float(array.mean()),
        "minimum_bits_per_message": float(array.min()),
        "maximum_bits_per_message": float(array.max()),
        "note": "Representatiegrootte; geen vergelijking van algemene expressiviteit.",
    }
