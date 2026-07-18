# ECP-8 Sealed Development Log

The ECP-8 confirmatory split is sealed. This log records every development arm,
including negative results, before any possible confirmatory access.

## Batch 1 preregistration — Global channel capacity

Preregistered: July 18, 2026 at 19:58:58 UTC<br>
Seed: `11`<br>
Test unsealed: **no**<br>
Split SHA-256: `241acd2ee42ff658ddf0c8c897d4e4df0f52a18098b3ef68c009c74c2134592a`

| Arm | Configuration | Raw SHA-256 | Effective SHA-256 |
|---|---|---|---|
| ECP8-B1-P | `config/ecp8-positive-control-development.yaml` | `e996bf66c30b3e699b27046e9824c13c7ecf3f2cb9831c4b9f0528d17b7b5f05` | `3a8e55ee262418f1005405afec3eeee7ebaaad164cb83274bd95c95e2c0939c3` |
| ECP8-B1-C | `config/ecp8-control-development.yaml` | `9e3c865fcec9698bb95fcfc3ad429a354e26ffd39f2533dd7dc836dfdd3ab34a` | `fcaf5e8f39df2349cb3dedefcc233e5a08d813763a5b644d6a2ed2c050748f06` |
| ECP8-B1-I | `config/ecp8-development.yaml` | `f6219110ebfe8f26248d9dbd646d80e1033f63d618a2524f7b96668ebd7fdaea` | `0572857aa786e0a41995aedd1cee8c2bb6dbdbc47f46025411bb8c06615b9693` |

ECP8-B1-C reruns the strongest ECP-7 weak-structure setup on the fresh ECP-8
split. ECP8-B1-I changes only the local channel capacities: `[16,16,8,8]`
becomes `[16,16,16,16]`, increasing fixed payload size from 14 to 16 bits.
The sender still has one generic joint context and four position heads; neither
sender nor receiver receives a factor-slot binding.

The full decision gate is fixed in `docs/research-design-ecp8.md`. In addition
to the existing train, validation and translator thresholds, the intervention
must be injective over all 15,360 accessible meanings, improve the paired
control's minimum codebook, and preserve both mean and worst-link validation.
Only these three seed-11 runs are admitted. The confirmatory test remains
unauthorized regardless of a single development result.

## Batch 1 results

Positive-control run: `runs/ecp8-batch1-positive-control-development/20260718T200136Z-ecp8-development`<br>
Paired-control run: `runs/ecp8-batch1-control-development/20260718T200256Z-ecp8-development`<br>
Intervention run: `runs/ecp8-batch1-intervention-development/20260718T200637Z-ecp8-development`<br>
Test unsealed: **no**

| Metric | Positive control | 14-bit control | 16-bit intervention |
|---|---:|---:|---:|
| Population train, mean | 100% | 79.5476% | 98.7566% |
| Population train, worst link | 100% | 78.6551% | 98.6886% |
| Population validation, mean | 100% | 70.2698% | 74.4629% |
| Population validation, worst link | 100% | 64.8438% | 73.3398% |
| Universal translator, validation | 100% | 75.1953% | 81.0547% |
| Exact sender-message agreement | 100% | 93.74% | 77.56% |
| Unique messages per sender | 15,360 | 12,048–12,255 | 15,095–15,135 |
| Collision meanings per sender | 0 | 3,105–3,312 | 225–265 |
| Message entropy | 13.91 bits | 13.45–13.48 bits | 13.87–13.88 bits |
| Declared payload | 14 bits | 14 bits | 16 bits |
| Registered development gate | pass | fail | **fail** |

The positive control passes every validity requirement at 100%, proving that
the fresh split remains fully solvable under the factorized 14-bit protocol.
The paired weak-structure control selects step 7,400 and stops at the registered
15,000-step minimum. The 16-bit intervention keeps improving, selects step
16,200 and stops at step 21,200.

The extra two bits have a large isolated effect. Mean train exactness improves
by 19.21 percentage points and worst-link train by 20.03 points. Mean
validation improves by 4.19 points, worst-link validation by 8.50 points and
translator validation by 5.86 points. The minimum sender codebook gains 3,047
occupied messages and the final all-link hard-error replay pool falls from
1,953 to 119.

Capacity is nevertheless insufficient. The intervention retains 225–265 hard
collisions per sender, so none is injective. Mean and worst-link validation are
74.46% and 73.34%, below their registered 80% thresholds. The intervention
passes both train thresholds, the translator threshold and both paired
non-regression checks, but fails injectivity and both validation thresholds.

The error pattern also distinguishes memorization from learned compositional
structure. The 16-bit arm reaches near-perfect training and perfect texture
validation, while held-out color and shape remain at 94.66% and 79.77% factor
accuracy. Sender agreement falls from 93.74% to 77.56%, and sender topographic
correlations fall from 0.761–0.771 to 0.693–0.700. The surplus code space lets
independent senders separate most training meanings, but it does not induce a
shared compositional organization for the withheld relation.

All three post-hoc analyses verify 65 artifact hashes, 16,384 validation-only
episodes, absent confirmatory-test metrics and valid hard messages. The global
channel audit checks every intervention message for four symbols in `0..15`
and exactly 16 declared bits.

## Batch 1 decision

ECP8-B1-I is a valid negative development result. Two surplus unallocated bits
substantially reduce the hard-code bottleneck and improve every joint accuracy
metric, but they do not produce an injective or sufficiently compositional
protocol. The pure-capacity hypothesis is rejected, and the ECP-8 confirmatory
split remains sealed.

Do not continue with an 18-bit, 20-bit or longer fixed message search. A Batch
2, if attempted, must keep the 16-bit channel and Batch 1 training fixed while
preregistering exactly one structure-induction mechanism. The most direct
candidate is the previously defined context-invariant transition objective,
because Batch 1 now supplies the code capacity that was missing when that
objective collapsed in ECP7-B8. It must be tested without a slot binding or
additional simultaneous change.
