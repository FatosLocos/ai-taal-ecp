# Results ECP-3 — First Robust Base Model

Confirmatory intervention: `ecp3-confirmatory/intervention/20260718T020939Z-ecp3-experiment`<br>
Paired control: `ecp3-confirmatory/control/20260718T020939Z-ecp3-experiment`<br>
Split-SHA-256: `91d6439fada82b1384a8d03f7cc1f5602091f794477be31c179c5a26e1b0464b`<br>
Formal primary classification: **strong evidence**

## Outcome

ECP-3 meets the predefined definition of a usable base model. Four of five independent seeds reach every threshold; in those four seeds, the population and the universal translator reconstruct every entirely new test meaning without error. Across all five seeds, mean test exact-match accuracy is 89.0% and mean translation accuracy is 95.0%.

The protocol does not use words, letters or predefined symbols. A message consists of four whole symbol IDs between 0 and 15. The senders themselves learn which factor is in which position and which symbol represents a factor value. The only prescribed grammatical conditions are one factor at a time and a unique code for different values within the same factor.

## Primary results

| Seed | Known | Worst known pair | Compositional validation | New test pairs | Worst test pair | Universal translator | Classification |
|---:|---:|---:|---:|---:|---:|---:|---|
| 11 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | strong |
| 23 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | strong |
| 37 | 100.0% | 100.0% | 99.6% | 100.0% | 100.0% | 100.0% | strong |
| 53 | 100.0% | 100.0% | 51.8% | 45.0% | 38.3% | 75.0% | negative |
| 71 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | strong |
| **Average** | **100.0%** | **100.0%** | **90.3%** | **89.0%** | **87.7%** | **95.0%** | **strong** |

The median is 100% for both test exact-match and translation exact-match accuracy. The lower mean score is entirely caused by one outlier, not by small errors across all runs.

## Paired control: what does consensus do?

The control uses the same injective sender architecture but without consensus on slot bindings or atomic codes.

| Metric | Without consensus | With consensus | Difference | Intervention better | Exact one-sided `p` |
|---|---:|---:|---:|---:|---:|
| New test pairs | 79.0% | 89.0% | +10.0 percentage points | 5/5 seeds | 0.03125 |
| Universal translator | 79.2% | 95.0% | +15.8 percentage points | 3 better, 1 equal, 1 lower | 0.125 |
| Strong seeds | 3/5 | 4/5 | +1 seed | — | — |

The intervention increases the exact message agreement between channels from 27.2% on average to 77.0%. Consensus is not a semantic dictionary, but a mechanism through which independent agents often choose the same arbitrary dialect.

## What the new form of communication looks like

Seed 11 chose the slot order for all four channels:

`[shape, texture, size, color]`

Sender 0 chose, among other things, the free atomic codes:

- colors `c0..c7` → `[1,12,2,6,10,5,8,11]`;
- shapes `s0..s7` → `[10,13,11,2,12,3,9,14]`;
- sizes `z0..z3` → `[3,15,7,4]`;
- textures `t0..t3` → `[0,2,7,15]`.

This makes the never-trained combination `(c0,s0,z0,t0)` sent as:

`⟦10 · 0 · 3 · 1⟧`

The four receivers and the individually trained universal translator exactly reconstruct this. The numbers have no fixed human meaning outside of this one learned protocol; consistent renaming of all sixteen symbols does not change any prediction.

## Efficiency

| Representation for this synthetic task | Bits per message | Relative to ECP-3 |
|---|---:|---:|
| Dutch template in UTF-8 | 328 | 20.5× larger |
| Canonical JSON in UTF-8 | 432 | 27× larger |
| **ECP-3** | **16** | **1×** |
| Hand-crafted compositional reference | 12 | 25% less than ECP-3 |
| Theoretical lower bound | 10 | 37.5% less than ECP-3 |

ECP-3 uses 16 channel bits for 10 bits of source entropy: 62.5% of the capacity carries theoretically necessary information. It is therefore much more compact than human text for this precisely defined meaning space, but is not yet bit-optimal. The comparison says nothing about the general expressivity of Dutch; it is only a task-specific representation comparison.

Each sender uses 1,024 unique messages across all 1,024 meanings and has zero message collisions. The protocol is therefore unambiguous. Message topology is exactly factorized: changing one factor changes exactly one symbol position on average, and topographic Spearman correlation is 1.0.

## What seed 53 teaches us

Seed 53 also has injective channels, a shared hard slot binding, and 100% known communication. However, the generic GRU receivers learned color and shape partly as a joint contextual rule. On new combinations, color remains 90.7% correct but shape only 48.2%, causing exact accuracy to fall to 45.0%.

This is not a collision or ambiguity in the transmitted protocol; the universal translator reaches 75.0% on the same messages. It is a decoder-local optimum. Under the preselected 4/5 rule, ECP-3 is therefore robust enough as a base model, but is not guaranteed to be error-free for every initialization. A subsequent model version can also make the receiver factor-isolated.

## Validity and integrity

- The configurations and decision rules are frozen before test access.
- All 48 pairs previously used in ECP-0, ECP-1, or ECP-2 were excluded from the new validation and test splits.
- The test split is not used for training, early stopping, or model selection.
- Four senders and four receivers are independently parametrized.
- Final evaluation was conducted in separate processes that received only the permitted matrices.
- All hub and symbol permutation controls have been successful.
- Each arm contains 81,920 schema-validated episodes.
- All 309 artifacts per arm matched their hashes at recalculation byte for byte.
- All twenty sender seed combinations were above all hundred permutations for topographic similarity.

## Scientific conclusion

Within this synthetic world, it has now been demonstrated that independent AI agents can learn a meaningful, non-alphabetic and task-efficient convention that systematically composes new combinations from reusable atoms and can be read by an independent translator.

It has not been shown that such grammar emerges spontaneously without architectural bias, that it is better than human language for open communication, or that it reaches the theoretical bit lower bound. ECP-3 is therefore the **first working base model**, not the endpoint of the research program.

## Local Evidence Files

The untracked source run is stored locally at `runs/ecp3-confirmatory/intervention/20260718T020939Z-ecp3-experiment/`. It contains the report, summary, post-hoc analysis, paired comparison, and all per-seed artifacts.
