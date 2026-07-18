# Development log ECP-2

The confirmatory ECP-2 test set remained sealed throughout this work. All performance below comes exclusively from training and the separate compositional validation split.

## Variant A - algebraic consistency pressure

Seed: 11<br>
Architecture: four independent channels × four independent receivers<br>
Channel: four symbols from a vocabulary of sixteen, 16 bits<br>
Split: `7a227e22d86f00d8ab5078690de37de794774cdab636e7db374c5adbd0985126`

| Variant | Weight | Known mean | Worst known pair | Compositional validation | Universal translator validation |
|---|---:|---:|---:|---:|---:|
| Control | 0 | 97.0% | 96.5% | **9.5%** | **13.9%** |
| Light | 0.25 | 95.8% | 95.1% | 4.6% | 10.0% |
| Medium | 1.0 | 59.9% | 35.2% | 2.6% | 3.5% |
| Strong | 4.0 | 2.0% | 1.6% | 1.4% | 2.3% |

Local artifacts are underneath `runs/ecp2-variants/{control,light,medium,strong}/20260718T005403Z-ecp2-development/`.

### Conclusion

The intervention is rejected. No weight improves the compositional validation and only the control approaches the known performance threshold. The test set is not opened.

Regularization revealed an informative degeneration. Under strong pressure, size and texture are reconstructed perfectly on the validation set, while color and shape can fall to chance level. Because the algebraic requirement is minimized on average across all changes, the sender can satisfy it cheaply by omitting the most difficult factors. A higher task-loss weight would merely rebalance the two objectives and would not remove this fundamental escape route.

Under the predefined fallback, development continues with cultural transmission, which selects for learnability by introducing new agents instead of directly imposing a desired geometry on messages.

## Variant B - Cultural transmission by agent replacement

The population retains four channels and four receivers. After a fixed interval, one sender and one receiver are completely re-initialized. The remaining six agents form the temporary cultural memory. After four replacements, no original agent is present; checkpoints prior to that complete turnover are not selectable.

Three preselected intervals are compared with seed 11 and the same sealed test set:

| Variant | Steps between replacements | First complete turnover |
|---|---:|---:|
| Fast | 400 | Step 1,600 |
| Medium | 600 | Step 2,400 |
| Slow | 800 | Step 3,200 |

The training budget remains 5,000 steps. Selection first uses the known performance thresholds and then only the compositional validation. Algebraic regularization is out in these three variants.

### First outcome

| Variant | Known mean | Worst known pair | Compositional validation | Universal translator validation |
|---|---:|---:|---:|---:|
| Fast, continuous | 97.4% | 93.9% | **19.5%** | **18.4%** |
| Medium, continuous | 95.2% | 92.1% | 10.0% | 12.7% |
| Slow, continuous | 94.1% | 90.8% | 10.1% | 11.9% |

The fast variant almost doubles the compositional validation compared to the 9.5% control, but continues to introduce new agents. As a result, a recently replaced link is always the weakest. The following pre-defined refinement separates transmission and consolidation:

| Variant | Interval | Maximum replacements | Turnovers | Consolidation after last replacement |
|---|---:|---:|---:|---:|
| One fast turnover | 400 | 4 | 1 | 3,400 steps |
| Two fast turnovers | 400 | 8 | 2 | 1,800 steps |
| One medium turnover | 600 | 4 | 1 | 2,600 steps |

The final test remains sealed for this refinement.

### Consolidation outcome

| Variant | Known mean | Worst known pair | Compositional validation | Universal translator validation |
|---|---:|---:|---:|---:|
| One fast turnover | 98.8% | 97.5% | 10.3% | 15.0% |
| Two fast turnovers | **99.3%** | **98.8%** | **19.9%** | **25.2%** |
| One medium turnover | 97.2% | 96.6% | 7.3% | 10.4% |

Two fast turnovers form the best cultural variant. It meets the known-performance thresholds and doubles compositional validation relative to the control, but remains well below the development targets of 80% population and 70% translator accuracy. Cultural transmission is retained as the best weakly structured intervention, but not as the confirmatory ECP-2 candidate.

## Variant C — Learned permutation slots

If the consolidation variants fail to reach the compositional validation threshold, one structurally stronger architecture is tested. The sender contains four discrete message slots and internally chooses a hard one-to-one permutation between the four meaning factors and those slots.

The following are not defined in advance:

- which factor is linked to which slot;
- which of the sixteen symbols represents a factor value;
- whether different channels choose the same internal permutation or symbols;
- how receivers decode the four symbols.

This is an explicit compositional architectural bias and a stricter procedure than algebraic or cultural pressure. The variant is valuable as a working model and as a positive control, but a success should not be described as completely uninfluenced linguistic emergence.

The slot variant is first trained with seed 11, without algebraic regularization or agent replacement. The preselected development thresholds are 97% mean known accuracy, 95% for the worst pair, 80% compositional validation, and 70% universal-translation validation.

### First final outcome and consensus refinement

The first fully trained slot population achieves training/validation without test access:

- 100% known reconstruction for each sender-receiver pair;
- 69.4% average compositional validation;
- 30.5% for the worst compositional pair;
- 50.6% universal translation validation.

The four senders chose three different factor-slot permutations. Two independently converged on the same permutation; the other two chose different ones. One meaning-free refinement is therefore tested: minimize differences among the four soft binding matrices and make each matrix sharp. Consensus does not specify a factor-slot mapping in advance; any of the 24 permutations can win.

Preselected consensus weights:

| Variant | Consensus weight | Sharpness weight |
|---|---:|---:|
| Light | 0.1 | 0.1 |
| Medium | 1.0 | 0.1 |
| Strong | 5.0 | 0.1 |

The final test remains sealed. When validation scores are nearly equal, the lower consensus weight wins.

### Consensus outcome and final choice

| Variant | Known mean | Worst known pair | Compositional validation | Worst validation pair | Universal translator validation |
|---|---:|---:|---:|---:|---:|
| Light, 0.1 | 100% | 100% | 76.9% | 51.6% | 50.6% |
| Medium, 1.0 | 100% | 100% | 90.0% | 82.0% | 95.3% |
| **Strong, 5.0** | **100%** | **100%** | **97.0%** | **93.8%** | **95.3%** |

Weight 5.0 wins unequivocally and becomes the confirmatory ECP-2 candidate. All four channels chose the same internally determined permutation `[color, texture, shape, size]`; the final soft binding probabilities have maxima between 0.968 and 0.986. Across the 896 training and validation meanings, the population uses 896 unique messages, has zero collisions, a minimum-pair distance of exactly one, and topographic similarity 1.0.

The confirmatory intervention is accompanied by a control using exactly the same permutation-slot architecture, split, seeds, and training budget, but without binding consensus. Both configurations are frozen before any ECP-2 test access.
