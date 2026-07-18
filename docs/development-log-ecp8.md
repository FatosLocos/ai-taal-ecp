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
