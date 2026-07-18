# Results ECP-5 — Fully Efficient 10-Bit Model

Confirmatory intervention: `ecp5-confirmatory/intervention/20260718T062848Z-ecp5-experiment`<br>
Paired control: `ecp5-confirmatory/control/20260718T062848Z-ecp5-experiment`<br>
Split-SHA-256: `cc487fd9042c5190bee93278c4be5180363f46a46d0e8af2f9d7d75a4f173140`<br>
Formal primary classification: **strong evidence**

## End result

ECP-5 is a fully efficient and robust communication protocol within the defined synthetic world:

- 5/5 seeds strong;
- 100% known communication;
- 100% on completely new size-texture combinations;
- 100% for the worst sender-receiver pair;
- 100% universal translation;
- exactly 10 bits per message, equal to the theoretical lower limit;
- 1,024 unique messages for 1,024 meanings, without collisions.

## Confirmatory results

| Seed | Known | New test combinations | Worst agent pair | Universal translator | Classification |
|---:|---:|---:|---:|---:|---|
| 11 | 100% | 100% | 100% | 100% | strong |
| 23 | 100% | 100% | 100% | 100% | strong |
| 37 | 100% | 100% | 100% | 100% | strong |
| 53 | 100% | 100% | 100% | 100% | strong |
| 71 | 100% | 100% | 100% | 100% | strong |
| **Average** | **100%** | **100%** | **100%** | **100%** | **strong** |

All compositional validation scores are 100%. The four channels within each seed produce exactly the same message for the same meaning.

## Effect of binding calibration

Uncalibrated control also retains 100% primary population communication, but only two of five universal translators find the right slot grammar.

| Seed | Uncalibrated translator | Calibrated translator | Difference |
|---:|---:|---:|---:|
| 11 | 100.0% | 100.0% | 0.0 pp |
| 23 | 12.5% | 100.0% | +87.5 pp |
| 37 | 100.0% | 100.0% | 0.0 pp |
| 53 | 9.4% | 100.0% | +90.6 pp |
| 71 | 9.4% | 100.0% | +90.6 pp |
| **Average** | **46.3%** | **100.0%** | **+53.8 pp** |

The intervention is better in all three seeds where improvement was possible and remains at 100% in the other two. The exact paired sign-flip test gives `p=0.125`, because only three differences are nonzero and therefore only eight effective sign combinations exist. The effect size and failure mode are unambiguous: calibration corrects every wrong control binding.

In all five interventions the chosen final permutation scores exactly 10.0 bits of mutual information compared to 8.0 bits for the number two.

## Transferability

| Labeled meanings | Exact match on new test combinations |
|---:|---:|
| 32 | 97.5% average; median 100% |
| 128 | 100% |
| 256 | 100% |
| 512 | 100% |

A new reader does not need to see a complete codebook of 1024 meanings. From 128 examples the factor grammar is transferred error-free in all seeds.

## Actually 10 bits

The source entropy is `log2(1024)=10` bits. ECP-5 uses local alphabets of 8, 8, 4, and 4 symbols, so `3+3+2+2=10` bits. The post-run analysis rechecked all 81,920 episode messages against the per-slot factor binding:

- controlled messages: 81,920;
- incorrect bit lengths: 0;
- symbols outside local alphabets: 0;
- channel efficiency: 100% of the theoretically necessary capacity.

| Representation for this task | Bits | Larger than ECP-5 |
|---|---:|---:|
| Canonical JSON in UTF-8 | 432 | 43.2× |
| Dutch template in UTF-8 | 328 | 32.8× |
| ECP-3 | 16 | 1.6× |
| Hand-crafted compositional reference | 12 | 1.2× |
| **ECP-5** | **10** | **1×; theoretically minimal** |

This only compares the representation of the same defined meaning space, not the general expressivity of human language.

## Example of the machine convention

Seed 11 chose the slot order `[size, texture, color, shape]`. The never-trained combination `(c0,s0,z0,t1)` is sent as:

`⟦0 · 3 · 5 · 4⟧`

In the local alphabets, the wire representation is:

`00 | 11 | 101 | 100` → `0011101100`

The slot order and all value symbol permutations have been selected by the agents. The bits have no fixed human meaning without the learned protocol.

## What has and has not been demonstrated with this

Demonstrated:

- independent agents can share an arbitrary non-alphabetic convention;
- the convention combines known atoms flawlessly into new meanings;
- an independent reader can reliably induce grammar;
- for this world, the channel reaches the information-theoretic lower bound.

Not shown:

- that the factor classification without architectural bias occurs spontaneously;
- that this protocol can replace open human language;
- that the same method adds dynamically unknown factors without new agreements;
- that efficiency in this uniform laboratory world transfers directly to natural multimodal data.

ECP-5 is therefore the **fully efficient final model of this research case**, not a general universal AI language.

## Integrity

- All 309 artifacts and hashes are valid.
- All 81,920 episodes are present and schema-validated.
- All 20 senders beat their hundred topographic permutations.
- Shuffled-message controls remain below 1%.
- Consistent symbol renaming preserves all predictions.
- The final receivers and translators turned into isolated processes.

## Local Evidence Files

The untracked intervention and control artifacts are stored locally under `runs/ecp5-confirmatory/`. They include reports, summaries, post-hoc analyses, the paired comparison, and all per-seed artifacts.
