# Results ECP-4 — Perfect 10-Bit Population, Unstable Translator

Confirmatory intervention: `ecp4-confirmatory/intervention/20260718T061339Z-ecp4-experiment`<br>
Paired 16-bit control: `ecp4-confirmatory/control/20260718T061339Z-ecp4-experiment`<br>
Formal primary classification: **mixed evidence**

## Outcome

ECP-4 reaches the theoretical 10-bit lower bound without any loss in primary agent communication. All five seeds, all sixteen sender-receiver pairs, and all 2,048 test episodes per seed are exactly correct. The 16-bit control also reaches 100%; the paired compression difference is exactly zero.

However, the independently trained universal translator reaches the threshold only in seed 11. In the remaining four seeds, it chooses the wrong hard factor-slot permutation. The formal overall classification therefore remains mixed despite flawless primary communication.

## Primary results

| Seed | Known | New test pairs | Worst test pair | Universal translator | Classification |
|---:|---:|---:|---:|---:|---|
| 11 | 100% | 100% | 100% | 100.0% | strong |
| 23 | 100% | 100% | 100% | 9.4% | Mixed |
| 37 | 100% | 100% | 100% | 9.4% | Mixed |
| 53 | 100% | 100% | 100% | 9.4% | Mixed |
| 71 | 100% | 100% | 100% | 12.5% | Mixed |
| **Average** | **100%** | **100%** | **100%** | **28.1%** | **mixed** |

The 16-bit control also achieves 100% mean population exact-match accuracy and 65.9% translation exact-match accuracy. Two translator seeds fail there as well. The problem therefore does not arise from information lost through compression, but from learning one discrete choice among 24 possible final permutations.

## Efficiency

The four local factor alphabets use `3+3+2+2 = 10` bits. This exactly equals `log2(1024)` and cannot be reduced further for a uniform, unambiguous code. Each sender uses 1,024 unique messages for 1,024 meanings without collisions. ECP-4 therefore has 100% theoretical channel efficiency.

## Integrity

- All five populations reach exactly 100% on training, validation, and test data.
- All 20 senders have topographic similarity 1.0.
- Each arm contains 81,920 schema-validated episodes.
- All 309 artifacts per arm and their hashes are fully valid.
- Shuffled-message and consistent symbol-permutation controls passed.

## Decision for ECP-5

The 10-bit code and factor-isolated population remain unchanged. ECP-5 replaces only the error-sensitive gradient-based selection of the translator binding with exact calibration across the 24 possible permutations. Calibration uses only the labeled training messages already available to each universal translator.

## Local Evidence Files

The untracked post-hoc analysis and associated comparison are locally below `runs/ecp4-confirmatory/intervention/20260718T061339Z-ecp4-experiment/`.
