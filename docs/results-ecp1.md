# Results ECP-1

Confirmatory run: `20260718T001805Z-ecp1-experiment`<br>
Configuration frozen: July 18, 2026 at 00:17:09 UTC<br>
Configuration SHA-256: `13ebb1186aa87e98093f64a02a9961d35a2fdf6b06b6f56e47ab5a53c2a6e977`<br>
Formal primary classification: **mixed evidence**<br>
Substantive outcome for the population hypothesis: **not supported**

## Summary

ECP-1 tested four independently parameterized senders against four independently parameterized receivers. All sixteen links were trained together. This created a shared convention: a randomly selected receiver reconstructs known messages from each sender with 98.5% mean accuracy, and even the mean accuracy of the worst sender-receiver pair reaches 98.1%.

However, population training does not solve the main problem of ECP-0. On fully held-out color-shape pairs, mean exact reconstruction decreases from 15.9% in ECP-0 to 10.1% in ECP-1. The universal translator achieves 15.2%. No seed approaches the preregistered thresholds of 60% population generalization or 50% translatability.

The correct conclusion is therefore not that a new efficient AI language has already been created. However, there is strong evidence that several independent agents can agree a compact, shared and structural code. That code is not yet sufficiently compositional: known combinations are largely memorized and new combinations are not systematically composed of well-known components.

## Primary results

| Seed | Known mean | Worst known pair | Validation | New pairs | Worst test pair | Universal translator | New receiver, 768 examples | Classification |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 11 | 99.2% | 98.8% | 77.6% | 17.0% | 7.8% | 24.4% | 18.8% | Mixed |
| 23 | 99.2% | 98.8% | 82.4% | 7.2% | 2.3% | 9.2% | 9.4% | negative |
| 37 | 97.5% | 97.1% | 73.6% | 6.5% | 3.9% | 13.1% | 12.5% | negative |
| 53 | 99.1% | 98.4% | 76.5% | 5.4% | 2.3% | 10.9% | 7.8% | negative |
| 71 | 97.6% | 97.4% | 81.7% | 14.5% | 10.9% | 18.6% | 18.8% | negative |
| **Average** | **98.5%** | **98.1%** | **78.4%** | **10.1%** | **5.5%** | **15.2%** | **13.4%** | **mixed** |

The test factors color and shape are reconstructed for 39.4% and 46.5% on average. Size and texture remain virtually intact by 98.6% and 97.9% on average, so the error is directed at combining the two excluded factors again, not in an overall defect of the decoder.

## Comparison with ECP-0

| Metric | ECP-0 | ECP-1 | Difference |
|---|---:|---:|---:|
| Known meanings | 97.8% | 98.5% | +0.7 percentage points |
| Validation | 78.6% | 78.4% | −0.2 percentage point |
| Fully new color-shape pairs | 15.9% | 10.1% | **−5.8 percentage points** |
| Independent/universal translator | 14.7% | 15.2% | +0.5 percentage point |

This comparison is directional rather than a measurement on identical test items: ECP-1 deliberately used a new dataset split and eight new held-out pairs because the ECP-0 test set had already been opened. Of the five ECP-1 seeds, only seed 11, at 17.0%, performs close to the ECP-0 mean of 15.9%.

The formal classification remains **mixed evidence**, because the pre-implemented aggregation rule assigns that label once at least one valid seed exceeds the ECP-0 reference; the rule was not changed after opening the test set. For the scientific interpretation, the mean effect is decisive: population training did not improve generalization in this experiment. A subsequent protocol should explicitly define an aggregation rule based on the mean and its uncertainty.

## Hypothesis

### A shared population protocol arises: supported

All sixteen sender-receiver pairs learn the same task. Mean known accuracy is 98.5%, and the worst pair per seed still averages 98.1%. All five seeds pass the 95% threshold for the worst pair; three of five also pass the stricter 99% mean threshold.

The four senders produce the same message for the same meaning on average in 54.3% of the cases, which is not a complete uniformity, but significant convergence between models without shared parameters.

### H2 • Population training improves compositional generalization: unsupported

The mean of 10.1% is below ECP-0 and well below the predefined 60% threshold. None of the five seeds crosses that threshold. Exchanging communication partners therefore prevents exclusive co-adaptation within one pair, but does not by itself produce a factorized language.

### One universal translator unlocks all channels: partially structural, performance threshold not met

The translator is only trained after freezing the four channels and averages 15.2% on new pairs. This shows that one model can read the partially shared convention, but no seed reaches the required 50%.

### A new receiver learns the protocol quickly: unsupported

| Labeled meanings | Average exact on new pairs |
|---:|---:|
| 32 | 1.3% |
| 128 | 7.9% |
| 512 | 11.7% |
| 768 | 13.4% |

The learning curve increases with more examples, but there is no few-shot transfer. Even after all 768 training concepts, the new receiver remains far below a reliable level.

### The messages contain semantic structure: supported as diagnostics

Topographic similarity between meaning distance and message distance ranges from 0.308 to 0.432 across the twenty sender-seed combinations. In the pre-announced post-run analysis, every observation exceeds all 100 random reassociations; the empirical one-sided `p`-value is `1/101 ≈ 0.0099` for each observation.

This proves structure, not enough compositionality. A code can give semantic near meanings similar messages and yet fail with a completely new combination of two factors.

## What kind of protocol came into being?

Each sender uses 960 to 1,007 unique messages for 1,024 meanings. Message entropy ranges from 9.864 to 9.967 bits, close to the 10-bit source entropy. Together with the high known accuracy, this again indicates an almost injective, distributed code.

ECP-1 adds an important result: several independent senders and receivers can stabilize such a code together. However, the shared convention remains more like a compact geometric codebook than a grammar that consistently combines color, shape, size, and texture as reusable parts.

## Validity and integrity

- The ECP-1 configuration is frozen before the confirmatory run.
- The eight ECP-0 test pairs are explicitly excluded when creating the new split.
- The compositional ECP-1 test set is not used for training or model selection.
- Four channels and four receivers have completely independent parameters.
- Final decoding took place in individual processes that received only symbol matrices.
- All shuffled-message controls remained at or below 1.0%, with approximately 0.09% mean exact reconstruction.
- Consistent renaming of the sixteen symbols retained all predictions in all seeds.
- Each seed contains 16,384 schema-validated episodes; together these are 81,920 episodes.
- All 309 pre-hashed artifacts matched the post-run analysis byte for byte.

## Decision for ECP-2

Adding more agents is not the logical next step. ECP-1 shows that partner swap creates compatibility, but doesn't automatically create compositionality. ECp-2 should therefore introduce a learning pressure that makes memorization more difficult without programming semantics in symbols in advance.

The recommended confirmatory comparison is:

1. maintain the independent population and 16-bit channel;
2. train iteratively across generations, where new receivers receive only messages and a limited number of examples from the previous generation;
3. systematically make the training world incomplete with varying combinations per generation;
4. select only for validation generalization and the speed at which a new receiver learns;
5. compare this method against an exact equal ECP-1 check without generation replacement;
6. re-use a completely new sealed test set;
7. define the primary group comparison and uncertainty margin in advance.

Compression to 12 or 10 bits remains delayed. First, a robust reusable protocol needs to be created; only after that maximum efficiency is a meaningful key question.

## Local Evidence Files

The untracked source run is located locally `runs/20260718T001805Z-ecp1-experiment/`. It contains `report.md`, `summary.json`, `posthoc-analysis.json` and the per-seed metrics, 81,920 episodes, checkpoints and isolated process input.
