# Results ECP-6 — Scale Replication at 14 Bits

Confirmatory run: `runs/20260718T070018Z-ecp6-experiment`<br>
Configuration SHA-256: `994ca086e1542e4608fec935ec5b72471b2e2cf73c2193f99ab6997044c40133`<br>
Split-SHA-256: `da751db7853ddbb84f000464c2627d4880eb154aef2158fb958d9a3779117d33`<br>
Formal primary classification: **strong evidence**

## End result

ECP-6 replicates the fully efficient ECP-5 protocol on a sixteen times larger meaning space:

- 5/5 seeds strong;
- 100% communication on all known meanings;
- 100% on the explicitly sealed new color-shape combinations;
- 100% for the worst sender-receiver pair;
- 100% universal translation;
- 16,384 unique messages for 16,384 meanings, without collisions;
- exactly 14 bits per message, equal to the theoretical lower limit.

## Primary confirmatory results

| Seed | Known | New test combinations | Worst agent pair | Universal translator | Classification |
|---:|---:|---:|---:|---:|---|
| 11 | 100% | 100% | 100% | 100% | strong |
| 23 | 100% | 100% | 100% | 100% | strong |
| 37 | 100% | 100% | 100% | 100% | strong |
| 53 | 100% | 100% | 100% | 100% | strong |
| 71 | 100% | 100% | 100% | 100% | strong |
| **Average** | **100%** | **100%** | **100%** | **100%** | **strong** |

All compositional validation scores are also 100%. Within each seed, the four independently initialized senders produce exactly the same message for the same meaning.

## Efficiency and scale

Source entropy is `log2(16,384)=14` bits. The factor-local alphabets require `4+4+3+3=14` bits. Each sender achieves:

- message entropy: 14.0 bits;
- fraction of source entropy: 1.0;
- collisions: 0;
- mean message distance for a one-factor change: 1.0 slot;
- factor-position concentration: 1.0;
- topographic Spearman correlation: 1.0.

| Representation for the same defined task | Mean bits | Larger than ECP-6 |
|---|---:|---:|
| Canonical JSON in UTF-8 | 438 | 31.3× |
| Dutch template in UTF-8 | 334 | 23.9× |
| ECP-5-payload | 10 | smaller world; not directly sufficient |
| Hand-crafted factor-local reference | 14 | 1× |
| **ECP-6** | **14** | **1×; theoretically minimal** |

The text comparison covers only representation size within the same pre-shared schema. It does not compare the open-ended expressivity, robustness, or social function of human language.

## Universal readability

The universal translator finds the exact slot grammar in every seed. The chosen permutation scores 14.0 bits of empirical mutual information; the best alternative permutation scores 8.0 bits. The 6-bit margin makes the choice unambiguous.

| Labeled meanings for a new reader | Test exact match, mean | Median |
|---:|---:|---:|
| 32 | 76.25% | 75% |
| 128 | 100% | 100% |
| 512 | 100% | 100% |
| 2,048 | 100% | 100% |

The required transfer set therefore grows much more slowly than the complete codebook of 16,384 meanings. The shortfall with 32 examples comes from unseen color and shape atoms; size and texture are already flawless.

## Example outside an alphabet

Seed 11 used the slot order `[shape, color, texture, size]`. The sealed test meaning `(c0,s9,z0,t0)` is sent as:

`⟦15 · 1 · 3 · 1⟧`

and on the wire:

`1111 | 0001 | 011 | 001` → `11110001011001`.

This is not a shortened Dutch alphabet; it is a learned product code. Position carries factor type, the local symbol carries factor value, and the codebooks are meaningless permutations outside the shared convention.

## Integrity and controls

- All 309 captured artifact hashes match.
- All 163,840 episodes are present and schema-validated.
- All 163,840 messages use exactly 14 bits.
- Symbols outside their factor-local alphabet: 0.
- All twenty senders exceed 100 topographic permutation nulls (`p=0.00990099`).
- Shuffled-message control: mean exact match is `0.0092%`, well below the 1% threshold.
- Consistent symbol renaming preserves all predictions.
- Receivers and translators have been evaluated with only symbol matrices in isolated processes.

## What has been demonstrated

Within this synthetic, uniform and pre-factorised world, it has been demonstrated that independently initialised agents:

1. share a non-lingual and non-alphabetic code convention;
2. generalize that convention reliably to completely new factor combinations;
3. transfer it to an independent new reader;
4. scale it from 1,024 to 16,384 meanings without loss of efficiency;
5. use exactly the information-theoretically necessary payload.

## What has not been demonstrated

- The factor classification does not arise spontaneously; the architecture imposes four factor slots as inductive bias.
- The experiment does not cover natural images, sound, uncertainty, or continuous meaning.
- The code does not negotiate on its own about new factors or protocol versions.
- The 14 bits do not include transport headers, error correction or pre-learning costs of the convention.
- The result shows no replacement of general human language.

The sharpest conclusion is therefore: **a fully efficient, universally inductable machine convention can scale error-free on this product world**, not that a general autonomous AI language has already been realized.

## Evidence files

- [`report.md`](../evidence/ecp6/report.md)
- [`manifest.json`](../evidence/ecp6/manifest.json)
- [`baselines.json`](../evidence/ecp6/baselines.json)

The complete local run also includes checkpoints, isolated process matrices and 163,840 episodes. These large generated artifacts are not included in Git; the frozen configuration and reproduction command are in [`evidence/ecp6/README.md`](../evidence/ecp6/README.md).
