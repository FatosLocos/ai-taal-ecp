# Research Design ECP-6 — Scalability at the Information Frontier

Status: **frozen before confirmatory test access**<br>
Frozen: July 18, 2026 at 06:58:14 UTC<br>
Configuration: `config/ecp6.yaml`<br>
Configuration-SHA-256: `994ca086e1542e4608fec935ec5b72471b2e2cf73c2193f99ab6997044c40133`

## Question

Does the universally readable protocol confirmed in ECP-5 remain completely correct when the meaning space increases sixteen times, while the messages remain exactly at the new theoretical lower limit of 14 bits?

## Scaling

The world contains four independent factors:

- 16 colors;
- 16 shapes;
- 8 sizes;
- 8 textures.

This gives `16 × 16 × 8 × 8 = 16,384 = 2^14` equiprobable meanings. The factor-local message uses four slots with alphabet sizes `[16,16,8,8]`. Their widths are `[4,4,3,3]` bits and sum to exactly 14 bits. A lossless fixed-length code cannot be shorter for this world.

## Sealed data split

Color and shape form the compositional holdout. Sixteen color-shape pairs are each explicitly recorded in advance for validation and testing. Each withheld pair contains at least one atomic value from the new half (`8–15`), so that the scaling is actually addressed.

| Split | Meanings | Color-shape pairs |
|---|---:|---:|
| Train | 14,336 | 224 |
| Validation | 1,024 | 16 |
| Confirmatory test | 1,024 | 16 |

Split-SHA-256: `da751db7853ddbb84f000464c2627d4880eb154aef2158fb958d9a3779117d33`.

## Recorded protocol

The architecture and induction rule remain substantively the same as ECP-5:

1. four independently initialized senders produce a factor-local permutation-slot code;
2. four receivers are trained over all sixteen sender-receiver links;
3. a new universal translator receives only labeled training messages;
4. the translator determines its factor-slot binding by comparing all `4! = 24` permutations on empirical mutual information and freezes the winner;
5. transfer is measured with 32, 128, 512, and 2,048 examples.

There is no new control arm: ECP-5 already tested the binding intervention directly in paired runs. ECP-6 is solely a preregistered scale replication of the successful intervention.

## Scale-safe measurements

Collisions, entropy, minimum pairs and exact task performance are calculated over all evaluated meanings. For topographic Spearman correlation, up to 1,000,000 unordered meaning pairs are sampled uniformly without replacement and with a fixed seed; smaller worlds use all pairs. This rule was implemented and tested before test unsealing because materializing all 134,209,536 pairs at once is not scalable.

Raw isolated message and prediction matrices continue to cover every evaluated meaning. Episode JSONL contains validation data and, only after unsealing, test data. The local channel audit checks every logged message for four symbols, factor-local alphabet boundaries, and exactly 14 bits.

## Predefined criteria

The five seeds are `11,23,37,53,71`. A seed is strong when existing ECP-5 thresholds are met: at least 97% average known exactness, at least 95% for the worst known pair, at least 80% average compositional test exactness, and at least 70% universal translation exactness.

ECP-6 is considered fully successful when:

1. at least four of five seeds are strong;
2. the average compositional population performance is at least 99%;
3. the average universal translation performance is at least 99%;
4. each sender encodes all 16,384 meanings collision-free;
5. each message demonstrably uses exactly 14 bits;
6. all artifact hashes, schemas, local alphabet boundaries, and test unsealing checks pass.

After freezing, no more model, split, measurement or threshold choices are adjusted based on ECP-6 test results.
