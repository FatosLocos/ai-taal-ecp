# Results ECP-0.2

Confirmatory run: `20260717T221924Z-ecp0-experiment`<br>
Configuration frozen: July 17, 2026 at 22:18:41 UTC<br>
Configuration SHA-256: `7415f5732fed4d5e7e72ca82e917e4110a9f9f8ba68566daba3aa26e652b90cc`<br>
Primary classification: **mixed evidence**

## Summary

ECP-0.2 shows that two trained agents can independently develop an almost injective communication protocol within a 16-bit channel. In four of five runs, the protocol reconstructs known meanings with at least 99% accuracy. It also transfers semantic structure to an independent translator.

However, the protocol does not yet generalize reliably to color-shape pairs that were completely held out from training. Mean exact test performance is 15.9%, ranging from 0% to 43.8%. This provides evidence of partial structural generalization, but not of a stable new language form.

## Primary results

| Seed | Known exact | Validation exact | Held-out pairs | Translator on held-out pairs | Classification |
|---:|---:|---:|---:|---:|---|
| 11 | 99.5% | 73.4% | 7.8% | 12.5% | Mixed |
| 23 | 99.9% | 83.6% | 0.0% | 3.1% | Mixed |
| 37 | 99.1% | 79.7% | 20.3% | 12.5% | Mixed |
| 53 | 91.3% | 60.9% | 7.8% | 7.0% | negative |
| 71 | 99.2% | 95.3% | 43.8% | 38.3% | Mixed |
| **Average** | **97.8%** | **78.6%** | **15.9%** | **14.7%** | **mixed** |
| **Median** | **99.2%** | **79.7%** | **7.8%** | **12.5%** | — |

By definition, the non-compositional lookup baseline scores 0% on unknown meanings. The hand-crafted compositional baseline scores 100% with 12 bits; the optimally packed factor code scores 100% with 10 bits.

## Hypothesis

### H1 — Reliability: supported

Four of five runs exceed the previously established threshold of 99% known reconstruction. One seed remains clearly behind at 91.3%. The base result is therefore reproducible, but the training process still has an unfavorable local optimum.

### H2 — Compositional generalization: partially supported

Four of five runs perform above the 0% lookup baseline on fully held-out color-shape pairs. The median is only 7.8%, and one run reaches 0%. At 43.8%, seed 71 shows that substantially better generalization is possible within the same architecture, but not that it is reliable.

### H3 — Independent translatability: partially supported

The translator reconstructs training messages almost flawlessly and scores above the lookup baseline on held-out pairs in all five runs. However, mean test performance of 14.7% remains too low to call the protocol generally translatable.

### H4 — Structural semantics: supported

Topographic similarity between meaning distance and message distance ranges from 0.308 to 0.448 across seeds. A post-run analysis with 100 random meaning-message assignments per seed found null values no higher than 0.004. All five observed values exceeded every randomized value; the empirical one-sided `p`-value is `1/101 ≈ 0.0099` for each seed.

This permutation test completes the pre-recorded diagnostic comparison, but is performed after the primary run and does not change the primary classification.

### H5 and H6 — Not yet tested

Transfer to new agents and compression via a bit penalty belong to step 2.

## What kind of protocol came into being?

The agents did not develop a simple dictionary with one fixed message position per factor:

- between 955 and 1015 of the 1024 meanings received a unique message;
- message entropy was between 9.86 and 9.98 bits, close to the 10-bit source entropy;
- any message position was important in ablation;
- the mean concentration of factor changes in one position was approximately 0.31, only slightly above 0.25 for a uniform distribution;
- semantic structure is clearly visible in message distances.

The best description is therefore: **a largely distributed, almost injective code with partial semantic geometry**. That is more than a random lookup code, but even less systematic than a compositional language.

## Efficiency

| Representation | Bits per meaning | Exactly on unknown combinations |
|---|---:|---:|
| Dutch fixed template, UTF-8 | 328 | 100% in case of correct production |
| Canonical JSON, UTF-8 | 432 | 100% |
| ECP-0.2 | 16 | average 15.9% |
| Manual compositional | 12 | 100% |
| Optimally packed factors | 10 | 100% |

ECP-0.2 is very compact compared to uncompressed text and JSON. It is no more efficient than a designed domain code and the error rate on unknown combinations is still too high. So there is no basis for the claim that AI has developed a superior general form of communication.

## Validity and integrity

- All five seeds used the same frozen configuration.
- The compositional test set was not used for training or model selection.
- Sender and receiver were running in separate processes during evaluation.
- The receiver received only a matrix with four symbol IDs.
- All shuffled-message controls remained at 0% or 0.098% exact reconstruction.
- Consistent renaming of all symbol IDs retained exactly the same predictions in each run.
- Each seed contains 1024 schema-validated episodes.
- All 179 pre-hashed artifacts matched post-run analysis byte for byte.

## Decision for step 2

Compressing directly from 16 to 12 bits is now methodologically premature. The bottleneck is not message size, but reliable compositionality and transfer.

The recommended order for ECP-1 is:

1. use a new data split seed and hidden pairs; the ECP-0 test set is now used;
2. train a population of senders and receivers with changing links to reduce co-adjustment of one pair;
3. periodically add a newly initialized receiver and measure the number of examples needed;
4. investigate iterative learning across generations and progressive reconstruction after each symbol;
5. first maintain the 16-bit channel to measure the effect on generalization purely;
6. then compare the same method at 16 and 12 bits before adding variable length and a bit penalty.

Only when generalization and portability are stable can step 3 fairly focus on maximum efficiency.

## Local Evidence Files

The untracked source run is located locally `runs/20260717T221924Z-ecp0-experiment/`. It contains `report.md`, `summary.json`, `posthoc-analysis.json` and the per-seed metrics, episodes, models and isolated process input.
