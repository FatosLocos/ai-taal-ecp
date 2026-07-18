# Research Design ECP-7 — Weakening the Factor-Slot Bias

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026<br>
Intervention configuration: `config/ecp7-development.yaml`<br>
Positive-control configuration: `config/ecp7-positive-control-development.yaml`

The confirmatory ECP-7 test split has not been accessed. This document defines
the first development batch only. No frozen confirmatory configuration exists
yet.

## Question

Does exact, compositional and transferable communication survive when sender
and receiver architectures no longer encode a one-factor-per-slot binding,
while the world, four-slot wire capacity, population and training budget remain
fixed?

This is a narrower and more difficult question than whether a neural network
can reproduce the ECP-6 code. The intervention must learn how the four meaning
factors jointly determine a message, and a generic sequence receiver must learn
how the entire message determines every factor.

## Single intervention

ECP-7 changes one architectural assumption: factor-local processing.

The intervention sender:

1. embeds all four input factors into one joint context;
2. emits four symbols autoregressively with a GRU;
3. is constrained only by per-position alphabet sizes `[16,16,8,8]`;
4. has no factor-specific output heads, factor codebook or predefined
   factor-to-slot binding.

The intervention receiver and universal translator are generic GRU sequence
encoders with four classification heads. Slot-binding calibration and the
factor/atom consensus losses are disabled.

The unchanged ECP-6 factorized sender and receiver form a positive control on
the same new split. The positive control tests whether a failure comes from the
intervention rather than the split or execution pipeline.

## Capacity and remaining inductive bias

The world remains `16 × 16 × 8 × 8 = 16,384 = 2^14` equiprobable meanings. The
message has four categorical positions with alphabet sizes `[16,16,8,8]`, so
the nominal widths `[4,4,3,3]` occupy exactly 14 bits.

ECP-7 therefore removes factor-slot binding, but it is not an unconstrained or
natural language experiment. It retains:

- categorical, fully observed inputs;
- a synthetic product world;
- a fixed four-position message frame;
- position-specific alphabet capacities;
- supervised task rewards and a fixed training schedule.

Any conclusion must be limited to this setting.

## Sealed data split

Validation uses the unused cyclic color-shape matching with shift `+10`; the
confirmatory test uses shift `+11`. Both are disjoint from the ECP-6 validation
and test matchings (`+8` and `+9`).

| Split | Meanings | Color-shape pairs | Permitted during development |
|---|---:|---:|---|
| Train | 14,336 | 224 | yes |
| Validation | 1,024 | 16 | yes |
| Confirmatory test | 1,024 | 16 | **no** |

Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`.

## First development batch

The first batch contains exactly two runs, both with seed `11` and at most
5,000 population-training steps:

1. `ecp6_factorized_positive_control`;
2. `bounded_autoregressive_intervention`.

Only train and validation data may be evaluated. Smoke runs may precede the
full runs to verify mechanics, but may not be used to tune the intervention.
No alternative architecture or hyperparameter variant is admitted into this
batch.

The positive control validates the batch when both its mean and worst-link
validation exactness are at least 99%. If it misses that gate, the batch is
inconclusive rather than evidence against the intervention.

When the positive control is valid, the intervention passes the development
gate only if all of the following hold:

1. known population exactness is at least 97% on average and 95% for the worst
   sender-receiver link;
2. mean validation exactness is at least 80%;
3. universal-translator validation exactness is at least 70%;
4. every logged symbol respects its position-specific alphabet boundary;
5. each sender assigns a unique message to every accessible train and
   validation meaning;
6. artifact and split integrity checks pass and no confirmatory test episode or
   metric is written.

If the positive control passes and the intervention misses any gate, the first
ECP-7 architecture is recorded as a negative development result. The test stays
sealed. A later variant, if justified, must be numbered and preregistered before
training.

Passing the development gate is not confirmation. It only permits selection of
a single frozen ECP-7 design and confirmatory criteria in a later commit.

## Recorded configuration identities

| Arm | Raw file SHA-256 | Effective configuration SHA-256 |
|---|---|---|
| Intervention | `7863ffbb4fdfdf43d28fed897d75989153e72ed0c432eaadbddc835f27c77b8f` | `e5f6ea5042dc59b5b10c5860ce7a672274b6b3ba887656de6f56cb8192181561` |
| Positive control | `4d5904a894b5d854831049cb38331c2e42aabc5da844de3d95e665d941ca6c8f` | `db323732a1160859835c930f2ffa578df363ddf146537aa0d4ee2496e2b9744d` |
