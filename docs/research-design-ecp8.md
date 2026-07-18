# Research Design ECP-8 — Surplus Capacity Without Factor Slots

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026 at 19:58:58 UTC<br>
Positive-control configuration: `config/ecp8-positive-control-development.yaml`<br>
Paired-control configuration: `config/ecp8-control-development.yaml`<br>
Intervention configuration: `config/ecp8-development.yaml`

## Question

Can two surplus, semantically unallocated channel bits eliminate hard-message
collisions in the strongest weak-structure ECP-7 system, without restoring a
factor-to-slot sender or receiver binding?

This is a new research phase, not ECP7-B30. ECP-7 established that the tested
generic 14-bit systems remain non-injective. ECP-8 isolates whether the exact
information-theoretic boundary itself is too restrictive for learning: the
weak sender and receiver, optimization, world and population stay fixed while
the four position alphabets change from `[16,16,8,8]` to `[16,16,16,16]`.

## World and fresh sealed split

The uniform world remains `16 × 16 × 8 × 8 = 16,384` meanings with 14 bits of
source entropy. The split is newly generated for ECP-8 and uses color-shape
matchings not used by ECP-6 or ECP-7:

| Split | Meanings | Matching |
|---|---:|---|
| Train | 14,336 | all pairs outside both sealed matchings |
| Validation | 1,024 | `shape = color + 12 mod 16` |
| Confirmatory test | 1,024 | `shape = color + 13 mod 16` |

Dataset seed: `18072058`<br>
Split SHA-256: `241acd2ee42ff658ddf0c8c897d4e4df0f52a18098b3ef68c009c74c2134592a`

Only train and validation may be used during development. The confirmatory
matching must not appear in metrics, episodes, selection or post-hoc analysis.

## Preregistered arms

1. **Factorized positive control.** The ECP-6 factorized population uses its
   minimal 14-bit channel on the fresh split. This validates the split and
   implementation independently of the weak-structure hypothesis.
2. **Weak-structure paired control.** The ECP7-B25 bounded-parallel sender,
   position-aware receiver, training schedule and 14-bit local capacities are
   rerun unchanged on the fresh split.
3. **Global-capacity intervention.** The paired control changes only the
   channel to four unrestricted positions over the same 16-symbol vocabulary.
   Every position can use symbols `0..15`, for a fixed 16-bit message.

The global positions retain order, but no position has a factor identity,
factor-local input, factor-specific decoder or restricted capacity. Sixteen
bits provide four times as many possible messages as the 16,384-meaning world,
with a 14.29% payload overhead over the source lower bound.

## Development execution

Batch 1 contains exactly three seed-11 development runs, one for each arm. All
population and translator training parameters are inherited unchanged. The
weak arms use at most 45,000 population steps, hard-symbol evaluation, the
registered B25 replay route and validation-only checkpoint selection. No loss,
architecture, optimizer, replay, horizon, temperature, seed, split or
translator variant may be added inside this batch.

The positive control is valid only if it reaches 100% mean and worst-link train
and validation exactness, 100% translator validation, and 15,360 distinct hard
messages per sender over the accessible train-plus-validation meanings.

The 16-bit intervention passes its development gate only if all conditions hold:

1. population train mean is at least 97%;
2. population train worst link is at least 95%;
3. population validation mean and worst link are each at least 80%;
4. universal-translator validation is at least 70%;
5. every sender uses exactly 15,360 distinct hard messages over accessible
   meanings;
6. its minimum sender codebook is larger than the paired control's minimum;
7. its mean and worst-link validation do not fall below the paired control;
8. channel, artifact-hash, isolation and sealed-test audits all pass.

Passing development would permit freezing at most one ECP-8 design in a later
commit. It does not authorize test access by itself. Failure is published as a
sealed development result and does not justify an unregistered coefficient or
capacity search.

## Frozen development identities

| Arm | Raw file SHA-256 | Effective configuration SHA-256 |
|---|---|---|
| Positive control | `e996bf66c30b3e699b27046e9824c13c7ecf3f2cb9831c4b9f0528d17b7b5f05` | `3a8e55ee262418f1005405afec3eeee7ebaaad164cb83274bd95c95e2c0939c3` |
| 14-bit paired control | `9e3c865fcec9698bb95fcfc3ad429a354e26ffd39f2533dd7dc836dfdd3ab34a` | `fcaf5e8f39df2349cb3dedefcc233e5a08d813763a5b644d6a2ed2c050748f06` |
| 16-bit intervention | `f6219110ebfe8f26248d9dbd646d80e1033f63d618a2524f7b96668ebd7fdaea` | `0572857aa786e0a41995aedd1cee8c2bb6dbdbc47f46025411bb8c06615b9693` |

These identities and thresholds were recorded before any ECP-8 training run.
