# Results ECP-2

Confirmatory intervention: `ecp2-confirmatory/intervention/20260718T013310Z-ecp2-experiment`<br>
Paired control: `ecp2-confirmatory/control/20260718T013310Z-ecp2-experiment`<br>
Split-SHA-256: `7a227e22d86f00d8ab5078690de37de794774cdab636e7db374c5adbd0985126`<br>
Formal primary classification: **mixed evidence**

## Conclusion

ECP-2 delivers the first clearly compositional protocol in this series, but not yet a robust final model. The intervention gives each factor a separate slot, allows the senders to choose a one-to-one factor-slot permutation, and applies consensus only to that free choice. All intervention channels converge on the same slot binding within each seed.

Mean exact reconstruction of entirely new color-shape combinations increases from 58.2% to 66.1% relative to the paired control. Four of five seeds improve, but the exact one-sided paired sign-flip test is not significant with five pairs (`p = 0.15625`). Universal-translator accuracy rises from 66.2% to 77.6%, improves in all five seeds, and has `p = 0.03125`.

Yet only two of five intervention seeds reach every preset threshold. The weak seeds still contain collisions among the freely learned symbols for factor values. Slot structure alone does not guarantee that each value receives a unique atomic code.

## Primary results

| Seed | Known | Worst known pair | Compositional validation | New test pairs | Worst test pair | Universal translator | Classification |
|---:|---:|---:|---:|---:|---:|---:|---|
| 11 | 100.0% | 100.0% | 97.0% | 86.4% | 76.6% | 98.2% | strong |
| 23 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | strong |
| 37 | 89.6% | 89.6% | 55.5% | 35.4% | 21.9% | 75.0% | Mixed |
| 53 | 91.7% | 91.7% | 72.7% | 55.3% | 49.2% | 51.6% | Mixed |
| 71 | 100.0% | 100.0% | 40.1% | 53.2% | 34.4% | 63.3% | Mixed |
| **Average** | **96.3%** | **96.3%** | **73.0%** | **66.1%** | **56.4%** | **77.6%** | **mixed** |

## Paired comparison

| Metric | Without binding consensus | With binding consensus | Difference | Seeds better | Exact one-sided `p` |
|---|---:|---:|---:|---:|---:|
| New test pairs | 58.2% | 66.1% | +7.9 percentage points | 4/5 | 0.15625 |
| Universal translator | 66.2% | 77.6% | +11.4 percentage points | 5/5 | 0.03125 |
| Strong seeds | 1/5 | 2/5 | +1 seed | — | — |

The final architecture itself is powerful: also the control without consensus achieves on average much more compositional generalization than ECP-1. The combined comparison only isolates the extra effect of binding consensus, not the effect of the structural slot bias.

## Interpretation

ECP-2 operates beyond words and alphabets: a message is a sequence of four discrete symbols, and both symbol usage and slot order are arbitrary. In successful seeds the code is perfectly injective, has topographic similarity 1.0, and composes new combinations exactly.

However, this success is not entirely spontaneous linguistic emergence. The architecture prescribes that the four meaning factors must be expressed in four separate slots. It does not determine what those slots mean, but it does impose the grammatical form “one factor per position.” This experiment therefore shows that an efficient non-human convention can be learned within a compositional channel, not that neural agents discover that channel structure without an inductive bias.

## Validity and integrity

- Intervention and control use exactly the same split, five seeds, architecture and training budget; only binding consensus differs.
- ECP-0 and ECP-1 test pairs are excluded. The ECP-2 test split remained sealed during development and model selection.
- All final senders and receivers turned into isolated processes; receivers only received the four hard symbols.
- Shuffled-message controls remained below the defined threshold, and consistent symbol renaming preserved all predictions.
- 81,920 episodes and 309 artifacts were checked per arm; all hashes matched byte for byte.
- The twenty channel seed combinations were above all hundred permutations for topographic similarity.

## Decision for ECP-3

ECP-3 retains the freely learned final permutation but makes the atomic code within each factor injective: different factor values must use different symbols. The symbols themselves remain meaningless and freely chosen. Population consensus is extended from slot binding to atomic code. A completely new validation and test split excludes both previous test pairs and the ECP-2 validation pairs already used.

The goal is not a higher peak score—ECP-2 already has a seed with 100% accuracy—but stability across seeds. Only if at least four of five seeds are classified as strong, preferably all five, does this become a candidate for the first usable base model.

## Local Evidence Files

The untracked source runs are stored locally under `runs/ecp2-confirmatory/intervention/20260718T013310Z-ecp2-experiment/` and `runs/ecp2-confirmatory/control/20260718T013310Z-ecp2-experiment/`. They contain the paired comparisons, post-hoc analyses, and all per-seed artifacts.
