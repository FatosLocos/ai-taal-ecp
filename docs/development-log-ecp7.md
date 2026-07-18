# Development Log ECP-7

The ECP-7 confirmatory test set remains sealed throughout all work recorded in
this log.

## Variant register

| Variant | Arm | Sender | Receiver | Status |
|---|---|---|---|---|
| ECP7-B1-C | Positive control | ECP-6 factor-local permutation slots | Factor-local classifier | completed; gate passed |
| ECP7-B1-I | Intervention | Joint-context bounded autoregressive | Generic sequence encoder | completed; gate failed |
| ECP7-B2-I | Intervention | B1 sender plus factor-agnostic code utilization | Generic sequence encoder | completed; gate failed |
| ECP7-B3-I | Intervention | B2 loss on straight-through hard messages | Generic sequence encoder | completed; gate failed |

No other ECP-7 variant has been trained.

## Batch 1 preregistration

Date: July 18, 2026<br>
Seed: `11`<br>
Maximum population steps: `5,000`<br>
Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`<br>
Test unsealed: **no**

The batch compares the weak-structure intervention against the frozen ECP-6
architecture on the same new validation matching. The decision rules are fixed
in `docs/research-design-ecp7.md`. Smoke runs are mechanical checks only and do
not authorize tuning.

## Batch 1 results

Positive-control run: `runs/ecp7-batch1-control-development/20260718T100308Z-ecp7-development`<br>
Intervention run: `runs/ecp7-batch1-intervention-development/20260718T100549Z-ecp7-development`<br>
Test unsealed: **no**

| Metric | Positive control | Intervention |
|---|---:|---:|
| Population train, mean | 100% | 0.4312% |
| Population train, worst link | 100% | 0.3906% |
| Population validation, mean | 100% | 0.6287% |
| Population validation, worst link | 100% | 0.4883% |
| Universal translator, validation | 100% | 0.5371% |
| Unique messages per sender | 15,360 | 130–139 |
| Collision meanings per sender | 0 | 15,221–15,230 |
| Development gate | pass | **fail** |

The positive control passed its 99% batch-validity threshold for every link, so
the intervention failure cannot be attributed to the new split or execution
pipeline.

The intervention learned the two smaller factors but not the held-out pair
factors. Its population validation factor accuracies were approximately
`[6.80%, 6.58%, 100%, 100%]` for color, shape, size and texture. The universal
translator showed the same pattern: `[6.35%, 6.69%, 100%, 99.95%]`. Color and
shape are therefore near their 6.25% chance level, while size and texture are
almost exact.

All four intervention senders collapsed most of the 14-bit channel to only
130–139 distinct messages. Their message entropy was 6.43–6.47 bits over the
15,360 accessible meanings, versus 13.91 bits for the collision-free control.
The result is a failure of code utilization and compositional reconstruction,
not a wire-capacity violation.

## Integrity

Both analyses report:

- all 65 captured artifact hashes match;
- all 16,384 episode rows contain validation data only;
- no `compositional_test` metric or episode exists;
- every logged message declares exactly 14 bits;
- all symbols respect their local slot alphabet;
- isolated sender and receiver workers completed successfully.

The first intervention smoke attempt stopped during isolated checkpoint loading
because the worker's runtime sender-type allowlist did not yet include the new
class. No result or test data was produced. The allowlist was fixed, a
regression test was added, and the repeated mechanical smoke completed before
the full batch. No model setting changed.

## Decision

ECP7-B1-I is recorded as a negative development result. The confirmatory split
remains sealed and no `config/ecp7.yaml` is created. A second development batch
may test one preregistered intervention aimed at code utilization without
restoring a factor-to-slot binding; it must receive a new variant identifier
before any training run.

## Batch 2 preregistration

Date: July 18, 2026<br>
Seed: `11`<br>
Maximum population steps: `5,000`<br>
Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`<br>
Test unsealed: **no**

ECP7-B2-I adds exactly one factor-agnostic code-utilization loss to the Batch 1
intervention. Its fixed formula and hyperparameters are recorded in
`docs/research-design-ecp7.md`. The unchanged ECP-6 control is rerun on the same
seed and split. Mechanical smoke runs cannot authorize tuning.

## Batch 2 results

Positive-control run: `runs/ecp7-batch2-control-development/20260718T102740Z-ecp7-development`<br>
Intervention run: `runs/ecp7-batch2-intervention-development/20260718T103041Z-ecp7-development`<br>
Test unsealed: **no**

| Metric | Positive control | ECP7-B2-I |
|---|---:|---:|
| Population train, mean | 100% | 0.3967% |
| Population train, worst link | 100% | 0.3697% |
| Population validation, mean | 100% | 0.6165% |
| Population validation, worst link | 100% | 0.1953% |
| Universal translator, validation | 100% | 0.6592% |
| Unique messages per sender | 15,360 | 85–104 |
| Collision meanings per sender | 0 | 15,256–15,275 |
| Message entropy | 13.91 bits | 6.13–6.31 bits |
| Development gate | pass | **fail** |

The positive control again validated the batch with 100% for every registered
performance measure. ECP7-B2-I failed the population, validation, translator
and injectivity gates.

At its selected checkpoint (step 400), the differentiable utilization loss had
improved to `-0.5605`, substantially closer to its ideal value of `-1` than a
collapsed soft code's value of `0`. The hard argmax protocol nevertheless used
only 85–104 messages. This is a relaxation gap: balanced and independent soft
message distributions did not become a balanced and independent discrete
protocol.

The semantic failure remained the same as Batch 1. Population validation factor
accuracies were approximately `[6.43%, 6.31%, 99.93%, 100%]`; color and shape
stayed near their 6.25% chance level while size and texture were almost exact.
Compared with Batch 1, hard code utilization became worse rather than better:
unique messages fell from 130–139 to 85–104 and entropy fell from 6.43–6.47 to
6.13–6.31 bits.

Both sealed analyses report 65 matching artifact hashes, 16,384 validation-only
episodes, no confirmatory-test keys, valid local alphabets, and exactly 14
declared bits for every logged message.

## Batch 2 decision

ECP7-B2-I is recorded as a negative development result. The confirmatory split
remains sealed and no frozen ECP-7 configuration is created. A future ECP7-B3
may test one preregistered utilization signal calculated from straight-through
hard messages, directly addressing the observed relaxation gap. It must not
simultaneously change architecture, training duration or loss weight.

## Batch 3 preregistration

Date: July 18, 2026<br>
Seed: `11`<br>
Maximum population steps: `5,000`<br>
Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`<br>
Test unsealed: **no**

ECP7-B3-I changes only the Batch 2 utilization-loss input from relaxed messages
to the straight-through one-hot messages already used for receiver training.
The exact identity and unchanged hyperparameters are recorded in
`docs/research-design-ecp7.md`. The ECP-6 positive control is rerun on the same
seed and split. Smoke is mechanical only and cannot authorize tuning.

## Batch 3 results

Positive-control run: `runs/ecp7-batch3-control-development/20260718T104735Z-ecp7-development`<br>
Intervention run: `runs/ecp7-batch3-intervention-development/20260718T105006Z-ecp7-development`<br>
Test unsealed: **no**

| Metric | Positive control | ECP7-B3-I |
|---|---:|---:|
| Population train, mean | 100% | 1.1911% |
| Population train, worst link | 100% | 1.0184% |
| Population validation, mean | 100% | 1.9226% |
| Population validation, worst link | 100% | 1.2695% |
| Universal translator, validation | 100% | 2.2705% |
| Unique messages per sender | 15,360 | 585–972 |
| Collision meanings per sender | 0 | 14,388–14,775 |
| Message entropy | 13.91 bits | 8.20–8.73 bits |
| Development gate | pass | **fail** |

The positive control again validated the batch at 100%. ECP7-B3-I failed the
population, validation, translator and injectivity gates, but it materially
improved every hard-utilization measure relative to Batch 2.

At the selected step 3,400 checkpoint, the straight-through utilization loss
was `-0.7075`. Unique hard messages increased from Batch 2's 85–104 to 585–972,
entropy increased from 6.13–6.31 to 8.20–8.73 bits, population validation rose
from 0.6165% to 1.9226%, and translator validation rose from 0.6592% to 2.2705%.
The run reached the fixed 5,000-step limit; later checkpoints improved training
accuracy but generalized worse, so the preregistered selector retained step
3,400.

Population validation factor accuracies were approximately
`[17.67%, 6.17%, 99.93%, 99.88%]`. Hard utilization therefore helped color but
shape remained at its 6.25% chance level. Marginal balance and pairwise slot
independence still allowed extensive higher-order full-message collisions.

Both sealed analyses report 65 matching artifact hashes, 16,384 validation-only
episodes, no confirmatory-test keys, valid local alphabets, and exactly 14
declared bits for every logged message.

## Batch 3 decision

ECP7-B3-I is a negative development result with a clear directional gain. The
confirmatory split remains sealed and no frozen ECP-7 configuration is created.
A future ECP7-B4 may add one direct straight-through full-message collision
penalty while retaining all Batch 3 settings. This targets joint collisions
without assigning semantic factors to slots.
