# Development log ECP-6

The ECP-6 test set remained sealed throughout all work described below.

## Scale invariants

The code is generalized from the original factor sizes `[8,8,4,4]` to `[16,16,8,8]`. Configuration validation, meaning IDs, schemas, factor-local alphabets, and baselines now follow the actual factor sizes. The complete test suite has 39 passing tests.

The first smoke attempt revealed one geometric scaling problem: topographic similarity materialized all `n(n-1)/2` pairs. The attempt was canceled before completion and without test access. The measurement now uses up to 1,000,000 deterministic, uniformly sampled pairs. A second smoke run completed normally and logged validation only.

## Sealed development run

Run: `runs/20260718T065639Z-ecp6-development`<br>
Seed: 11<br>
Test unsealed: no

| Metric | Outcome |
|---|---:|
| Population known, mean | 100% |
| Worst known link | 100% |
| New color-shape validation, mean | 100% |
| Worst validation link | 100% |
| Universal translator on train | 100% |
| Universal translator on validation | 100% |
| Transfer with 32 examples, validation | 81.25% |
| Transfer with 128 examples, validation | 100% |
| Transfer with 512 examples, validation | 100% |
| Transfer with 2,048 examples, validation | 100% |

Binding calibration selected the slot order `[1,0,3,2]`. The total mutual-information score was exactly 14.0 bits; the runner-up scored 8.0 bits. All four channels encoded the 15,360 accessible training and validation meanings.

The development run wrote 16,384 episodes: `1,024 validation meanings × 4 senders × 4 receivers`. No test episode was written.

## Freezing decision

Development provided no reason for an additional variant. The world, explicit holdout pairs, 14-bit channel, training budgets, binding calibration, transfer budgets, topographic sampling rule, five seeds, and success criteria are therefore frozen unchanged for confirmation.
