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
| ECP7-B4-I | Intervention | B3 plus direct full-message collision loss | Generic sequence encoder | completed; gate failed |
| ECP7-B5-I | Intervention | B3 plus straight-through sender consensus | Generic sequence encoder | completed; gate failed |
| ECP7-B6-I | Intervention | B3 plus normalized factor minimax | Generic sequence encoder | completed; gate failed |
| ECP7-B7-I | Intervention | Bounded parallel joint-context sender | Generic sequence encoder | completed; gate failed |
| ECP7-B8-I | Intervention | B7 plus algebraic context invariance | Generic sequence encoder | completed; gate failed |
| ECP7-B9-I | Intervention | B7 sender and position-aware MLP decoder | Position-aware MLP | completed; gate failed |
| ECP7-B10-I | Intervention | B9 with 15,000-step optimization | Position-aware MLP | completed; gate failed |
| ECP7-B11-I | Intervention | B10 with late utilization decay | Position-aware MLP | completed; gate failed |
| ECP7-B12-I | Intervention | B10 with deeper shared decoder | Deep position-aware MLP | completed; gate failed |
| ECP7-B13-I | Intervention | B10 with deeper shared sender | Position-aware MLP | completed; gate failed |
| ECP7-B14-I | Intervention | B10 with late learning-rate decay | Position-aware MLP | completed; gate failed |
| ECP7-B15-I | Intervention | B10 with 30,000-step optimization | Position-aware MLP | completed; gate failed |
| ECP7-B16-I | Intervention | B15 with late normalized factor minimax | Position-aware MLP | completed; gate failed |
| ECP7-B17-I | Intervention | B15 with late global collision-pair replay | Position-aware MLP | completed; gate failed |
| ECP7-B18-I | Intervention | B17 replay with final weight 0.1 | Position-aware MLP | completed; gate failed |
| ECP7-B19-I | Intervention | B18 with replay decayed to zero after step 20,000 | Position-aware MLP | valid negative; validation 82.04%, train and injectivity fail |
| ECP7-B20-I | Intervention | Late global replay of population-hard training meanings | Position-aware MLP | valid negative; new-best validation 83.45%, train and injectivity fail |

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

## Batch 4 preregistration

Date: July 18, 2026<br>
Seed: `11`<br>
Maximum population steps: `5,000`<br>
Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`<br>
Test unsealed: **no**

ECP7-B4-I retains all Batch 3 settings and adds one factor-agnostic loss: the
average number of distinct minibatch inputs sharing the same complete
straight-through message. Its exact formula, weight and warmup are recorded in
`docs/research-design-ecp7.md`. The unchanged positive control is rerun. Smoke
cannot authorize tuning.

## Batch 4 results

Positive-control run: `runs/ecp7-batch4-control-development/20260718T111008Z-ecp7-development`<br>
Intervention run: `runs/ecp7-batch4-intervention-development/20260718T111141Z-ecp7-development`<br>
Test unsealed: **no**

| Metric | Positive control | ECP7-B4-I |
|---|---:|---:|
| Population train, mean | 100% | 0.3204% |
| Population train, worst link | 100% | 0.2860% |
| Population validation, mean | 100% | 0.4211% |
| Population validation, worst link | 100% | 0.2930% |
| Universal translator, validation | 100% | 0.6104% |
| Unique messages per sender | 15,360 | 426–579 |
| Collision meanings per sender | 0 | 14,781–14,934 |
| Message entropy | 13.91 bits | 7.46–7.84 bits |
| Development gate | pass | **fail** |

The positive control again validated the batch at 100%. ECP7-B4-I failed every
performance and injectivity gate and regressed relative to Batch 3.

At the selected step 800 checkpoint, the average number of distinct colliding
partners in the current minibatch was `0.03125`, while the retained hard
utilization loss was `-0.7213`. Despite that low local collision count, global
evaluation found only 426–579 messages across 15,360 accessible meanings. The
minibatch signal was therefore too sparse and local to represent global
codebook occupancy.

Population validation dropped from Batch 3's 1.9226% to 0.4211%; message entropy
dropped from 8.20–8.73 to 7.46–7.84 bits. Factor accuracies were approximately
`[6.48%, 6.41%, 92.13%, 83.79%]`, so the added loss also disrupted the two
factors previously learned almost exactly. Changing its weight after seeing
this outcome is not permitted inside Batch 4.

Both sealed analyses report 65 matching artifact hashes, 16,384 validation-only
episodes, no confirmatory-test keys, valid local alphabets, and exactly 14
declared bits for every logged message.

## Batch 4 decision

ECP7-B4-I is recorded as a negative development result and is not retained. The
confirmatory split remains sealed. The strongest weak-structure variant remains
ECP7-B3-I. A future ECP7-B5 may add one straight-through sender-consensus loss
to B3, testing whether a shared factor-agnostic convention helps receivers
without restoring semantic slot assignments.

## Batch 5 preregistration

Date: July 18, 2026<br>
Seed: `11`<br>
Maximum population steps: `5,000`<br>
Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`<br>
Test unsealed: **no**

ECP7-B5-I returns to the Batch 3 configuration and adds exactly one
factor-agnostic loss: mean straight-through symbol disagreement between every
sender pair on the same minibatch. Its fixed formula, weight and warmup are
recorded in `docs/research-design-ecp7.md`. The Batch 4 collision loss is not
retained. The unchanged positive control is rerun. Smoke is mechanical only
and cannot authorize tuning.

## Batch 5 results

Positive-control run: `runs/ecp7-batch5-control-development/20260718T112234Z-ecp7-development`<br>
Intervention run: `runs/ecp7-batch5-intervention-development/20260718T112234Z-ecp7-development`<br>
Test unsealed: **no**

| Metric | Positive control | ECP7-B5-I |
|---|---:|---:|
| Population train, mean | 100% | 0.1818% |
| Population train, worst link | 100% | 0.1256% |
| Population validation, mean | 100% | 0.4761% |
| Population validation, worst link | 100% | 0.1953% |
| Universal translator, validation | 100% | 0.5859% |
| Exact sender-message agreement | 100% | 44.02% |
| Unique messages per sender | 15,360 | 169–231 |
| Collision meanings per sender | 0 | 15,129–15,191 |
| Message entropy | 13.91 bits | 6.02–6.13 bits |
| Development gate | pass | **fail** |

The positive control again validated the batch at 100%. ECP7-B5-I failed the
population, validation, translator and injectivity gates. It stopped at step
2,000 under the unchanged early-stopping rule, with step 400 selected.

The intervention answered its narrow question: exact complete-message
agreement between sender pairs increased from Batch 3's 2.47% to 44.02%.
However, the shared convention was mostly a shared collapse. Unique messages
fell from Batch 3's 585–972 to 169–231 and entropy fell from 8.20–8.73 to
6.02–6.13 bits. At the selected checkpoint, sender-consensus loss was `0.2673`
and hard-utilization loss was only `-0.5350`, compared with Batch 3's selected
hard-utilization value of approximately `-0.7075`.

Population validation factor accuracies were approximately
`[6.43%, 6.31%, 64.42%, 78.00%]`. Consensus therefore did not recover color or
shape and also weakened size and texture. Population validation fell from
Batch 3's 1.9226% to 0.4761%; translator validation fell from 2.2705% to
0.5859%.

Both sealed analyses report 65 matching artifact hashes, 16,384 validation-only
episodes, no confirmatory-test keys, valid local alphabets, and exactly 14
declared bits for every logged message.

## Batch 5 decision

ECP7-B5-I is recorded as a negative development result and is not retained. It
shows that inter-sender agreement is not sufficient: without a stronger
semantic pressure, independent senders can agree by discarding distinctions.
The confirmatory split remains sealed and ECP7-B3-I remains the strongest
weak-structure variant.

Across B3–B5, color and especially shape remain the persistent bottleneck while
size and texture are easier to learn. A future ECP7-B6 may return to B3 and add
one minimax factor-reconstruction objective that emphasizes the currently
worst decoded factor without assigning any factor to a channel slot. It must
not retain the rejected B4 or B5 losses or change the architecture at the same
time.

## Batch 6 preregistration

Date: July 18, 2026<br>
Seed: `11`<br>
Maximum population steps: `5,000`<br>
Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`<br>
Test unsealed: **no**

ECP7-B6-I returns to Batch 3 and adds exactly one normalized minimax
factor-reconstruction term. For each sender-receiver pair it selects the
largest factor cross-entropy after division by that factor's uniform-guess
entropy. Its fixed formula, weight and warmup are recorded in
`docs/research-design-ecp7.md`. The rejected Batch 4 and Batch 5 losses are
absent. The unchanged positive control is rerun. Smoke is mechanical only and
cannot authorize tuning.

## Batch 6 results

Positive-control run: `runs/ecp7-batch6-control-development/20260718T113533Z-ecp7-development`<br>
Intervention run: `runs/ecp7-batch6-intervention-development/20260718T113533Z-ecp7-development`<br>
Test unsealed: **no**

| Metric | Positive control | ECP7-B6-I |
|---|---:|---:|
| Population train, mean | 100% | 0.4486% |
| Population train, worst link | 100% | 0.3836% |
| Population validation, mean | 100% | 0.4639% |
| Population validation, worst link | 100% | 0.1953% |
| Universal translator, validation | 100% | 0.5859% |
| Exact sender-message agreement | 100% | 2.75% |
| Unique messages per sender | 15,360 | 313–542 |
| Collision meanings per sender | 0 | 14,818–15,047 |
| Message entropy | 13.91 bits | 7.14–7.50 bits |
| Development gate | pass | **fail** |

The positive control again validated the batch at 100%. ECP7-B6-I failed the
population, validation, translator and injectivity gates. It stopped at step
3,000 under the unchanged early-stopping rule, with step 1,400 selected.

At that checkpoint, the normalized minimax loss was `1.0014`: the worst factor
remained essentially at uniform-guess cross-entropy despite receiving the full
additional weight. The hard-utilization loss was `-0.7024`. Population
validation factor accuracies were approximately
`[6.65%, 6.49%, 99.48%, 99.62%]`. The intervention therefore did not redistribute
semantic learning toward color or shape; it preserved the same easy-factor
solution.

Compared with Batch 3, unique messages fell from 585–972 to 313–542, entropy
fell from 8.20–8.73 to 7.14–7.50 bits, population validation fell from 1.9226%
to 0.4639%, and translator validation fell from 2.2705% to 0.5859%. The mean
training exactness was higher than Batch 5, but it did not generalize to the
held-out color-shape combinations.

Both sealed analyses report 65 matching artifact hashes, 16,384 validation-only
episodes, no confirmatory-test keys, valid local alphabets, and exactly 14
declared bits for every logged message.

## Batch 6 decision

ECP7-B6-I is recorded as a negative development result and is not retained. It
shows that emphasizing the worst decoded factor is insufficient when the
generic sender still converges to a code dominated by the easier factors. The
confirmatory split remains sealed and ECP7-B3-I remains the strongest
weak-structure variant.

B4–B6 added three distinct training pressures to the same autoregressive base;
all reduced its strongest result. A future ECP7-B7 may instead change exactly
one architectural assumption: replace autoregressive symbol generation with a
generic parallel sender whose every slot reads the same joint meaning context.
This removes sequential optimization while still providing no factor-specific
input path, factor-to-slot assignment or semantic codebook. It must return to
the Batch 3 loss set and leave the generic receiver unchanged.

## Batch 7 preregistration

Date: July 18, 2026<br>
Seed: `11`<br>
Maximum population steps: `5,000`<br>
Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`<br>
Test unsealed: **no**

ECP7-B7-I returns to the complete Batch 3 loss set and changes exactly one
sender property: the four locally bounded symbols are generated in parallel
from one shared joint meaning context instead of autoregressively. The receiver,
translator, hard-utilization objective and every training rule remain
unchanged. The exact architecture and exclusions are recorded in
`docs/research-design-ecp7.md`. The unchanged positive control is rerun. Smoke
is mechanical only and cannot authorize tuning.

## Batch 7 results

Positive-control run: `runs/ecp7-batch7-control-development/20260718T114952Z-ecp7-development`<br>
Intervention run: `runs/ecp7-batch7-intervention-development/20260718T114952Z-ecp7-development`<br>
Test unsealed: **no**

| Metric | Positive control | ECP7-B7-I |
|---|---:|---:|
| Population train, mean | 100% | 9.5965% |
| Population train, worst link | 100% | 9.2494% |
| Population validation, mean | 100% | 0.5066% |
| Population validation, worst link | 100% | 0% |
| Universal translator, validation | 100% | 2.7588% |
| Exact sender-message agreement | 100% | 27.90% |
| Unique messages per sender | 15,360 | 3,118–3,415 |
| Collision meanings per sender | 0 | 11,945–12,242 |
| Message entropy | 13.91 bits | 11.11–11.25 bits |
| Development gate | pass | **fail** |

The positive control again validated the batch at 100%. ECP7-B7-I failed the
population, validation, translator and injectivity gates. It stopped at step
4,800 under the unchanged early-stopping rule, with step 3,200 selected.

Parallel generation produced the largest optimization gain in ECP-7 so far.
Compared with autoregressive Batch 3, mean training exactness rose from 1.1911%
to 9.5965%, unique messages rose from 585–972 to 3,118–3,415, entropy rose from
8.20–8.73 to 11.11–11.25 bits, and universal-translator validation rose from
2.2705% to 2.7588%. The selected hard-utilization loss was `-0.7229`.

Those gains did not compose across the held-out color-shape matching.
Population validation remained 0.5066%, below Batch 3's 1.9226%, and its worst
sender-receiver link reconstructed none of the 1,024 validation meanings.
Population validation factor accuracies were approximately
`[45.64%, 4.84%, 94.67%, 95.04%]`. Parallelization substantially improved color
but shape remained below its 6.25% chance level. The universal translator
reached 12.40% on shape, suggesting that the sender messages contain some shape
signal that the jointly trained receiver population does not use reliably.

The first intervention smoke reached isolated evaluation but stopped because
the worker's sender-type guard did not yet list the new checkpoint class. No
test data was accessed. The guard and worker-route regression test were added;
the repeated smoke completed without changing the registered config or model.

Both sealed analyses report 65 matching artifact hashes, 16,384 validation-only
episodes, no confirmatory-test keys, valid local alphabets, and exactly 14
declared bits for every logged message.

## Batch 7 decision

ECP7-B7-I is a negative development result, but it establishes that
autoregressive generation was a major optimization bottleneck. The
confirmatory split remains sealed. Batch 3 still has the highest population
validation exactness, while Batch 7 has the strongest train exactness,
code-space use, color learning and translator result among the weak-structure
variants.

A future ECP7-B8 may retain the B7 parallel sender and add exactly one
context-invariance objective: the existing algebraic consistency loss for the
same atomic factor transition in two different training contexts. This directly
targets composition rather than memorization and assigns no factor to a message
slot. It must not restore B4–B6 losses or change the receiver simultaneously.

## Batch 8 preregistration

Date: July 18, 2026<br>
Seed: `11`<br>
Maximum population steps: `5,000`<br>
Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`<br>
Test unsealed: **no**

ECP7-B8-I retains the complete Batch 7 architecture and loss set, then activates
one context-invariance term. It matches two training-only instances of the same
atomic factor transition and minimizes the squared difference between their
relaxed message displacements. Its fixed construction and hyperparameters are
recorded in `docs/research-design-ecp7.md`. No factor is assigned to a channel
slot. The unchanged positive control is rerun. Smoke is mechanical only and
cannot authorize tuning.

## Batch 8 results

Positive-control run: `runs/ecp7-batch8-control-development/20260718T120358Z-ecp7-development`<br>
Intervention run: `runs/ecp7-batch8-intervention-development/20260718T120358Z-ecp7-development`<br>
Test unsealed: **no**

| Metric | Positive control | ECP7-B8-I |
|---|---:|---:|
| Population train, mean | 100% | 0.5349% |
| Population train, worst link | 100% | 0.4464% |
| Population validation, mean | 100% | 0.3235% |
| Population validation, worst link | 100% | 0.0977% |
| Universal translator, validation | 100% | 0.6836% |
| Exact sender-message agreement | 100% | 1.18% |
| Unique messages per sender | 15,360 | 857–1,135 |
| Collision meanings per sender | 0 | 14,225–14,503 |
| Message entropy | 13.91 bits | 8.23–8.92 bits |
| Development gate | pass | **fail** |

The positive control again validated the batch at 100%. ECP7-B8-I failed the
population, validation, translator and injectivity gates. It stopped at step
2,200 under the unchanged early-stopping rule, with step 600 selected.

At that checkpoint, algebraic consistency loss was `0.05265` at its scheduled
weight of `0.75`, and the hard-utilization loss was `-0.7321`. The surrogate
could be reduced, but it did not create a useful discrete compositional code.
Compared with B7, training exactness fell from 9.5965% to 0.5349%, unique
messages fell from 3,118–3,415 to 857–1,135, population validation fell from
0.5066% to 0.3235%, and translator validation fell from 2.7588% to 0.6836%.

Population validation factor accuracies were approximately
`[7.63%, 6.57%, 89.04%, 96.64%]`. The context objective therefore suppressed
the strong B7 color signal and left shape near chance. Universal-translator
factor accuracies of `[14.60%, 10.30%, 98.12%, 99.02%]` again show that a fresh
decoder extracts more color and shape information than the jointly trained
population receivers, but far below the registered gate.

Both sealed analyses report 65 matching artifact hashes, 16,384 validation-only
episodes, no confirmatory-test keys, valid local alphabets, and exactly 14
declared bits for every logged message.

## Batch 8 decision

ECP7-B8-I is recorded as a negative development result and is not retained.
Relaxed transition invariance competed with the discrete task and utilization
objectives instead of converting B7's distinctions into composition. The
confirmatory split remains sealed.

B7 remains the strongest optimization base. Its shape minimal pairs change
approximately 1.11–1.13 message positions and concentrate about 64% of that
change in one position, while its post-hoc universal translator decodes shape
better than the jointly trained receivers. A future ECP7-B9 may keep the B7
sender and losses but replace the recurrent final-state receiver with one
generic position-aware MLP over all four embedded slots. This tests decoder
access without factor-to-slot binding and must not add another loss.

## Batch 9 preregistration

Date: July 18, 2026<br>
Seed: `11`<br>
Maximum population steps: `5,000`<br>
Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`<br>
Test unsealed: **no**

ECP7-B9-I returns to the Batch 7 parallel sender and loss set, then changes one
shared decoder family. The receiver and post-freeze translator concatenate all
four embedded message positions and decode every factor from one generic MLP
representation instead of a recurrent final state. They have no binding matrix
or factor-specific slot input. The exact architecture and exclusions are
recorded in `docs/research-design-ecp7.md`. The unchanged positive control is
rerun. Smoke is mechanical only and cannot authorize tuning.

## Batch 9 results

Positive-control run: `runs/ecp7-batch9-control-development/20260718T121559Z-ecp7-development`<br>
Intervention run: `runs/ecp7-batch9-intervention-development/20260718T121559Z-ecp7-development`<br>
Test unsealed: **no**

| Metric | Positive control | ECP7-B9-I |
|---|---:|---:|
| Population train, mean | 100% | 71.2734% |
| Population train, worst link | 100% | 70.1521% |
| Population validation, mean | 100% | 52.3865% |
| Population validation, worst link | 100% | 50.8789% |
| Universal translator, validation | 100% | 54.8096% |
| Exact sender-message agreement | 100% | 89.51% |
| Unique messages per sender | 15,360 | 10,834–11,017 |
| Collision meanings per sender | 0 | 4,343–4,526 |
| Message entropy | 13.91 bits | 13.25–13.28 bits |
| Development gate | pass | **fail** |

The positive control again validated the batch at 100%. ECP7-B9-I still failed
the population, validation, translator and injectivity gates, so it does not
authorize confirmatory access. It nevertheless produced the first large
weak-structure result in ECP-7.

The position-aware decoder raised mean population train exactness from B7's
9.5965% to 71.2734%, validation from 0.5066% to 52.3865%, worst-link validation
from 0% to 50.8789%, and universal-translator validation from 2.7588% to
54.8096%. Sender exact-message agreement rose from 27.90% to 89.51%, even
without an explicit sender-consensus loss.

Population validation factor accuracies were approximately
`[84.17%, 76.09%, 98.45%, 86.10%]`; the decoder therefore recovered the shape
signal that the recurrent population ignored. Universal-translator factor
accuracies were `[86.08%, 83.50%, 97.85%, 81.98%]`. No factor remains near
chance.

The selected checkpoint was the final registered step 5,000. Its task loss was
`0.1724`, hard-utilization loss was `-0.7357`, and exactness was still improving.
Each sender used 10,834–11,017 messages with 13.25–13.28 bits of entropy; the
largest collision bucket contained only 8–9 meanings. These observations
indicate unfinished optimization rather than the previous semantic collapse.

Both sealed analyses report 65 matching artifact hashes, 16,384 validation-only
episodes, no confirmatory-test keys, valid local alphabets, and exactly 14
declared bits for every logged message.

## Batch 9 decision

ECP7-B9-I is a negative development result because every registered threshold
must pass together. It is also the new strongest weak-structure design and the
first result that justifies an isolated optimization-budget test. The
confirmatory split remains sealed.

A future ECP7-B10 may keep the complete B9 architecture and loss set, preserve
its original 5,000-step temperature annealing, and extend only the population
optimization horizon to 15,000 steps with a preregistered longer selection
window. No architecture, decoder, loss, data, translator or threshold may
change in that batch.

## Batch 10 preregistration

Date: July 18, 2026<br>
Seed: `11`<br>
Maximum population steps: `15,000`<br>
Temperature schedule steps: `5,000`, then hold at `0.8`<br>
Minimum selection steps: `5,000`<br>
Early-stopping patience: `3,000` steps<br>
Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`<br>
Test unsealed: **no**

ECP7-B10-I keeps the complete Batch 9 model, loss, optimizer, data, translator
and gate definitions. It extends only population optimization and its selection
window. The temperature at every step through 5,000 is identical to B9 and
holds the B9 endpoint thereafter, avoiding a second annealing-rate change. The
unchanged positive control is rerun. No alternative horizon or accompanying
intervention is admitted into this batch.

## Batch 10 results

Positive-control run: `runs/ecp7-batch10-control-development/20260718T122855Z-ecp7-development`<br>
Intervention run: `runs/ecp7-batch10-intervention-development/20260718T122855Z-ecp7-development`<br>
Test unsealed: **no**

| Metric | Positive control | ECP7-B10-I |
|---|---:|---:|
| Population train, mean | 100% | 82.0836% |
| Population train, worst link | 100% | 80.5455% |
| Population validation, mean | 100% | 72.9797% |
| Population validation, worst link | 100% | 71.4844% |
| Universal translator, validation | 100% | 75.1465% |
| Exact sender-message agreement | 100% | 92.31% |
| Unique messages per sender | 15,360 | 12,358–12,906 |
| Collision meanings per sender | 0 | 2,454–3,002 |
| Message entropy | 13.91 bits | 13.48–13.57 bits |
| Development gate | pass | **fail** |

The unchanged positive control passed every gate at 100%. ECP7-B10-I passed
the universal-translator threshold for the first time, but missed the train,
validation and injectivity requirements. Because every threshold must pass
together, the batch remains a negative development result and does not
authorize confirmatory access.

The isolated longer horizon raised train exactness from B9's 71.2734% to
82.0836%, validation from 52.3865% to 72.9797%, worst-link validation from
50.8789% to 71.4844%, and translator validation from 54.8096% to 75.1465%.
Sender agreement rose from 89.51% to 92.31%, and collisions fell substantially.

Population validation factor accuracies were
`[87.24%, 99.93%, 98.44%, 86.18%]`; universal-translator factor accuracies were
`[94.41%, 100%, 97.73%, 81.69%]`. Shape became essentially perfect while color
and texture remained the residual errors.

The selected checkpoint was again the final registered step, now 15,000. Its
task loss was `0.0765` and its full-weight code-utilization term was `-0.7548`.
Validation plateaued near 73% after step 12,000 even as train exactness continued
to improve slowly. Each sender still used 12,358–12,906 messages at 13.48–13.57
bits of entropy, and no collision bucket contained more than four meanings.

Both sealed analyses report 65 matching artifact hashes, 16,384 validation-only
episodes, no confirmatory-test keys, valid local alphabets, and exactly 14
declared bits for every logged message.

## Batch 10 decision

ECP7-B10-I is retained as the new strongest weak-structure base but is not a
passing ECP-7 design. Its large improvement establishes that B9 was
underoptimized, while the late plateau makes another duration-only extension a
weak next test. The confirmatory split remains sealed.

A future ECP7-B11 may keep the complete B10 design and alter only the
code-utilization coefficient after the already reproduced B9 horizon. It may
hold weight `1.0` through step 5,000, then decay linearly to `0.1` at step
15,000. This keeps anti-collapse pressure while bringing the surrogate's final
weighted magnitude close to the remaining task loss. No other loss,
architecture, duration, annealing, data, translator or threshold may change.

## Batch 11 preregistration

Date: July 18, 2026<br>
Seed: `11`<br>
Maximum population steps: `15,000`<br>
Temperature schedule steps: `5,000`, then hold at `0.8`<br>
Code-utilization weight: `1.0` through step `5,000`, then linear to `0.1` at step `15,000`<br>
Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`<br>
Test unsealed: **no**

ECP7-B11-I keeps every Batch 10 setting except the coefficient schedule on the
existing code-utilization term. The coefficient remains identical to B10
through the original 5,000-step horizon, then decays to a nonzero anti-collapse
weight. The unchanged positive control is rerun. No alternative weight or
accompanying intervention is admitted into this batch.

## Batch 11 results

Positive-control run: `runs/ecp7-batch11-control-development/20260718T124421Z-ecp7-development`<br>
Intervention run: `runs/ecp7-batch11-intervention-development/20260718T124421Z-ecp7-development`<br>
Test unsealed: **no**

| Metric | Positive control | ECP7-B11-I |
|---|---:|---:|
| Population train, mean | 100% | 79.0911% |
| Population train, worst link | 100% | 77.8530% |
| Population validation, mean | 100% | 72.2229% |
| Population validation, worst link | 100% | 70.8008% |
| Universal translator, validation | 100% | 72.4121% |
| Exact sender-message agreement | 100% | 89.14% |
| Unique messages per sender | 15,360 | 11,893–12,323 |
| Collision meanings per sender | 0 | 3,037–3,467 |
| Message entropy | 13.91 bits | 13.41–13.48 bits |
| Development gate | pass | **fail** |

The positive control again passed every gate at 100%. ECP7-B11-I retained a
passing translator score, but missed train, validation and injectivity. It does
not authorize confirmatory access.

Relative to B10, decaying utilization pressure reduced train exactness from
82.0836% to 79.0911%, validation from 72.9797% to 72.2229%, translator validation
from 75.1465% to 72.4121%, and sender agreement from 92.31% to 89.14%. It also
lost roughly 300–1,000 unique messages per sender and introduced more collision
meanings. The isolated change therefore moved every principal code and task
measure in the wrong direction.

Population validation factor accuracies were
`[87.21%, 99.96%, 98.54%, 85.45%]`; universal-translator factor accuracies were
`[87.50%, 100%, 98.54%, 85.28%]`. Color and texture remain the residual errors.

The selected checkpoint was step 14,800. Its task loss was `0.0805`, utilization
loss was `-0.7275`, and scheduled utilization weight was `0.118`. Every setting
and recorded metric through step 5,000 matched the B10 trajectory before the
registered coefficient schedules diverged.

Both sealed analyses report 65 matching artifact hashes, 16,384 validation-only
episodes, no confirmatory-test keys, valid local alphabets, and exactly 14
declared bits for every logged message.

## Batch 11 decision

ECP7-B11-I is rejected. The result falsifies the proposed explanation that
full late utilization pressure was the primary B10 bottleneck. B10 remains the
strongest weak-structure base, and the confirmatory split remains sealed.

The residual error now appears decoder-limited rather than loss-weight-limited:
B10's shared one-hidden-layer decoder plateaued on color and texture, and its
fresh translator showed the same texture weakness. A future ECP7-B12 may return to the
complete B10 schedule and add exactly one second generic shared hidden layer to
both the position-aware receiver and isolated translator. It must preserve the
same flattened positional input and must not add factor-specific paths, binding,
loss, duration, data or threshold changes.

## Batch 12 preregistration

Date: July 18, 2026<br>
Seed: `11`<br>
Maximum population steps: `15,000`<br>
Temperature schedule steps: `5,000`, then hold at `0.8`<br>
Decoder change: one additional shared `hidden_dim × hidden_dim` layer<br>
Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`<br>
Test unsealed: **no**

ECP7-B12-I returns to every Batch 10 training and loss setting, then changes
only the receiver and translator depth. The four factor heads still consume one
shared representation of all four embedded positions. There is no binding or
factor-specific input path. The unchanged positive control is rerun, and no
alternative decoder variant is admitted into this batch.

## Batch 12 results

Positive-control run: `runs/ecp7-batch12-control-development/20260718T130109Z-ecp7-development`<br>
Intervention run: `runs/ecp7-batch12-intervention-development/20260718T130109Z-ecp7-development`<br>
Test unsealed: **no**

| Metric | Positive control | ECP7-B12-I |
|---|---:|---:|
| Population train, mean | 100% | 71.5297% |
| Population train, worst link | 100% | 66.6016% |
| Population validation, mean | 100% | 47.9797% |
| Population validation, worst link | 100% | 39.7461% |
| Universal translator, validation | 100% | 63.0371% |
| Exact sender-message agreement | 100% | 88.64% |
| Unique messages per sender | 15,360 | 10,119–11,404 |
| Collision meanings per sender | 0 | 3,956–5,241 |
| Message entropy | 13.91 bits | 13.11–13.33 bits |
| Development gate | pass | **fail** |

The positive control passed every gate at 100%. ECP7-B12-I failed train,
validation, translator and injectivity. It does not authorize confirmatory
access.

Relative to B10, the second decoder layer reduced train exactness from 82.0836%
to 71.5297%, validation from 72.9797% to 47.9797%, and translator validation from
75.1465% to 63.0371%. Code use and sender agreement also fell. The added generic
decoder depth therefore made the emergent protocol harder, not easier, to learn.

Population validation factor accuracies were
`[77.07%, 86.05%, 100%, 77.05%]`; universal-translator factor accuracies were
`[97.17%, 87.50%, 100%, 75.90%]`. The deeper shared representation did not
resolve the residual factors consistently across receivers and a new reader.

The selected checkpoint was step 10,000 with task loss `0.1539` and utilization
loss `-0.7153`. Validation subsequently regressed, so the registered patience
rule stopped population training at step 13,000.

Both sealed analyses report 65 matching artifact hashes, 16,384 validation-only
episodes, no confirmatory-test keys, valid local alphabets, and exactly 14
declared bits for every logged message.

## Batch 12 decision

ECP7-B12-I is rejected. Decoder depth is not the B10 bottleneck. Batch 10 remains
the strongest weak-structure base, and the confirmatory split remains sealed.

The remaining capacity hypothesis is sender-side: B10 generates all four slots
from one shallow shared context, and receiver depth has now been ruled out. A
future ECP7-B13 may return to the complete B10 model and add exactly one second
generic shared hidden layer to the bounded parallel sender before all four slot
heads. It must retain the B10 one-layer receiver and translator and must not add
factor-specific sender paths, loss, width, duration, data or threshold changes.

## Batch 13 preregistration

Date: July 18, 2026<br>
Seed: `11`<br>
Maximum population steps: `15,000`<br>
Temperature schedule steps: `5,000`, then hold at `0.8`<br>
Sender change: one additional shared `hidden_dim × hidden_dim` layer<br>
Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`<br>
Test unsealed: **no**

ECP7-B13-I returns to every Batch 10 model, training and loss setting, then
changes only sender depth. All four slot heads still consume one shared context
of the complete meaning. There is no binding or factor-specific hidden path.
The unchanged positive control is rerun, and no alternative sender variant is
admitted into this batch.

## Batch 13 results

Positive-control run: `runs/ecp7-batch13-control-development/20260718T131611Z-ecp7-development`<br>
Intervention run: `runs/ecp7-batch13-intervention-development/20260718T131611Z-ecp7-development`<br>
Test unsealed: **no**

| Metric | Positive control | ECP7-B13-I |
|---|---:|---:|
| Population train, mean | 100% | 1.3218% |
| Population train, worst link | 100% | 1.0672% |
| Population validation, mean | 100% | 0.3174% |
| Population validation, worst link | 100% | 0% |
| Universal translator, validation | 100% | 0.6104% |
| Exact sender-message agreement | 100% | 19.06% |
| Unique messages per sender | 15,360 | 694–831 |
| Collision meanings per sender | 0 | 14,529–14,666 |
| Message entropy | 13.91 bits | 8.44–8.77 bits |
| Development gate | pass | **fail** |

The positive control passed every gate at 100%. ECP7-B13-I failed every
performance and injectivity requirement and does not authorize confirmatory
access.

The second sender layer caused a renewed semantic collapse. Population
validation factor accuracies were only
`[4.28%, 18.58%, 98.49%, 99.84%]`; the protocol preserved texture and size but
failed to encode color and shape. Universal-translator validation was similarly
`[4.71%, 21.41%, 98.58%, 99.85%]`.

The selected checkpoint was step 600 with task loss `1.3516` and utilization
loss `-0.6994`. The registered minimum-step rule kept training through step
5,000, but no later checkpoint surpassed the early validation score. At that
point each sender used only 694–831 messages and collision buckets contained up
to 161–170 meanings.

Both sealed analyses report 65 matching artifact hashes, 16,384 validation-only
episodes, no confirmatory-test keys, valid local alphabets, and exactly 14
declared bits for every logged message.

## Batch 13 decision

ECP7-B13-I is rejected. Additional generic sender depth is strongly harmful,
just as additional decoder depth was harmful in Batch 12. Batch 10 remains the
strongest weak-structure base, and the confirmatory split remains sealed.

The next clean refinement hypothesis is optimization stability rather than
capacity or loss removal. B10 continued improving late but fluctuated around its
validation plateau at the unchanged learning rate `0.001`. A future ECP7-B14 may
keep the complete B10 design and learning rate through step 5,000, then decay
only that rate linearly to `0.0001` at step 15,000. Temperature, utilization,
architecture, duration, data, translator and thresholds must remain unchanged.

## Batch 14 preregistration

Date: July 18, 2026<br>
Seed: `11`<br>
Maximum population steps: `15,000`<br>
Temperature schedule steps: `5,000`, then hold at `0.8`<br>
Learning rate: `0.001` through step `5,000`, then linear to `0.0001` at step `15,000`<br>
Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`<br>
Test unsealed: **no**

ECP7-B14-I keeps every Batch 10 model, loss and training setting except the late
learning-rate schedule. The optimizer rate remains identical through the
original 5,000-step horizon, then decays tenfold. The unchanged positive control
is rerun, and no alternative schedule or accompanying intervention is admitted
into this batch.

## Batch 14 results

Positive-control run: `runs/ecp7-batch14-control-development/20260718T132929Z-ecp7-development`<br>
Intervention run: `runs/ecp7-batch14-intervention-development/20260718T132929Z-ecp7-development`<br>
Test unsealed: **no**

| Metric | Positive control | ECP7-B14-I |
|---|---:|---:|
| Population train, mean | 100% | 79.1321% |
| Population train, worst link | 100% | 77.7902% |
| Population validation, mean | 100% | 65.4907% |
| Population validation, worst link | 100% | 63.1836% |
| Universal translator, validation | 100% | 71.0205% |
| Exact sender-message agreement | 100% | 89.04% |
| Unique messages per sender | 15,360 | 11,961–12,280 |
| Collision meanings per sender | 0 | 3,080–3,399 |
| Message entropy | 13.91 bits | 13.43–13.48 bits |
| Development gate | pass | **fail** |

The positive control passed every gate at 100%. ECP7-B14-I retained a passing
translator score, but failed train, validation and injectivity. It does not
authorize confirmatory access.

Relative to B10, late learning-rate decay reduced train exactness from 82.0836%
to 79.1321%, validation from 72.9797% to 65.4907%, and translator validation from
75.1465% to 71.0205%. Sender agreement and code use also fell. Smaller late
updates therefore did not stabilize the B10 refinement trajectory.

Population validation factor accuracies were
`[87.10%, 91.46%, 98.44%, 86.36%]`; universal-translator factor accuracies were
`[87.21%, 98.34%, 98.44%, 85.35%]`.

The selected checkpoint was step 14,800, where learning rate had decayed to
`0.000118`. Task loss was `0.0868` and utilization loss was `-0.7330`. The final
step at learning rate `0.0001` was slightly worse on validation.

Both sealed analyses report 65 matching artifact hashes, 16,384 validation-only
episodes, no confirmatory-test keys, valid local alphabets, and exactly 14
declared bits for every logged message.

## Batch 14 decision

ECP7-B14-I is rejected. Constant late learning rate is beneficial relative to
decay, and Batch 10 remains the strongest weak-structure base. The confirmatory
split remains sealed.

B10 selected its final 15,000-step checkpoint and B14 shows that shrinking late
updates is harmful. A future ECP7-B15 may therefore keep the exact B10
architecture, losses, constant learning rate and temperature endpoint, then
extend only the maximum population horizon to 30,000 steps with minimum
selection step 15,000 and patience 5,000. No other setting may change.

## Batch 15 preregistration

Date: July 18, 2026<br>
Seed: `11`<br>
Maximum population steps: `30,000`<br>
Minimum selection steps: `15,000`<br>
Early-stopping patience: `5,000` steps<br>
Learning rate: constant `0.001`<br>
Temperature schedule steps: `5,000`, then hold at `0.8`<br>
Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`<br>
Test unsealed: **no**

ECP7-B15-I keeps every Batch 10 architecture, loss, optimizer, data and
translator setting. It extends only population optimization and its selection
window. The unchanged positive control is rerun, and no alternative horizon or
accompanying intervention is admitted into this batch.

## Batch 15 results

Positive-control run: `runs/ecp7-batch15-control-development/20260718T134437Z-ecp7-development`<br>
Intervention run: `runs/ecp7-batch15-intervention-development/20260718T134437Z-ecp7-development`<br>
Test unsealed: **no**

| Metric | Positive control | ECP7-B15-I |
|---|---:|---:|
| Population train, mean | 100% | 83.4612% |
| Population train, worst link | 100% | 81.9336% |
| Population validation, mean | 100% | **82.5867%** |
| Population validation, worst link | 100% | 79.7852% |
| Universal translator, validation | 100% | **83.3740%** |
| Exact sender-message agreement | 100% | 92.33% |
| Unique messages per sender | 15,360 | 12,585–13,200 |
| Collision meanings per sender | 0 | 2,160–2,775 |
| Message entropy | 13.91 bits | 13.52–13.61 bits |
| Development gate | pass | **fail** |

The positive control passed every gate at 100%. ECP7-B15-I passed the registered
mean validation and universal-translator thresholds for the first time in one
batch. It still failed known-meaning train exactness and sender injectivity, so
the joint gate fails and confirmatory access remains unauthorized.

Relative to B10, the longer constant-rate horizon raised validation from
72.9797% to 82.5867% and translator validation from 75.1465% to 83.3740%.
Population train exactness increased only from 82.0836% to 83.4612%, indicating
that residual hard-message collisions, not held-out composition, are now the
principal gate failure.

Population validation factor accuracies were
`[98.86%, 99.75%, 98.44%, 85.05%]`; universal-translator factor accuracies were
`[100%, 100%, 98.44%, 84.94%]`. Color and shape became essentially perfect.
Texture is now the dominant residual factor. The fixed 98.44% size accuracy
adds a smaller exact-match ceiling.

The selected checkpoint was step 28,800 with task loss `0.0675` and utilization
loss `-0.7399`. Validation first crossed 80% between steps 24,000 and 26,000 and
remained above it through the final step. Every sender used at least 12,585
messages, and no collision bucket contained more than three meanings.

Both sealed analyses report 65 matching artifact hashes, 16,384 validation-only
episodes, no confirmatory-test keys, valid local alphabets, and exactly 14
declared bits for every logged message.

## Batch 15 decision

ECP7-B15-I is a negative result under the joint gate but becomes the new
strongest weak-structure base. It passes composition and new-reader induction;
only known-meaning exactness and injectivity remain below their registered
thresholds. The confirmatory split remains sealed.

The residual error is concentrated in texture after the shared code is already
established. A future ECP7-B16 may keep the complete B15 design and introduce
only late normalized worst-factor emphasis: factor-minimax weight `0` through
step 15,000, linearly warm to `1.0` over 5,000 steps, then hold. This revisits the
Batch 6 objective only after the high-entropy B15 protocol exists and must not
change architecture, utilization, duration, data, translator or thresholds.

## Batch 16 preregistration

Preregistered: July 18, 2026 at 14:07:11 UTC<br>
Seed: `11`<br>
Maximum population steps: `30,000`<br>
Minimum selection steps: `15,000`<br>
Early-stopping patience: `5,000` steps<br>
Factor-minimax weight: `0` through step `15,000`, linear to `1.0` at step `20,000`, then hold<br>
Raw configuration SHA-256: `caef16ec93d0a9424fd3c4af46a987aad63118f24e57e77e9d51cc2eb77e073b`<br>
Effective configuration SHA-256: `b40f35ab2f03fa8450805908713b4b9a59bbc060c38a4e68e4e3c5be2d2b4efb`<br>
Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`<br>
Test unsealed: **no**

ECP7-B16-I keeps every Batch 15 architecture, base loss, optimizer, data,
temperature, duration, selection and translator setting. It adds only the
existing normalized factor-minimax loss with a delayed coefficient: no minimax
gradient through step 15,000, a 5,000-step linear warmup, then full weight.
The unchanged positive control is rerun. No alternative schedule or accompanying
intervention is admitted into this batch, and smoke remains mechanical only.

## Batch 16 results

Positive-control run: `runs/ecp7-batch16-control-development/20260718T140854Z-ecp7-development`<br>
Intervention run: `runs/ecp7-batch16-intervention-development/20260718T140854Z-ecp7-development`<br>
Test unsealed: **no**

| Metric | Positive control | ECP7-B16-I |
|---|---:|---:|
| Population train, mean | 100% | 82.8033% |
| Population train, worst link | 100% | 81.4104% |
| Population validation, mean | 100% | 76.4648% |
| Population validation, worst link | 100% | 74.5117% |
| Universal translator, validation | 100% | 77.7588% |
| Exact sender-message agreement | 100% | 92.59% |
| Unique messages per sender | 15,360 | 12,487–13,044 |
| Collision meanings per sender | 0 | 2,316–2,873 |
| Message entropy | 13.91 bits | 13.50–13.59 bits |
| Development gate | pass | **fail** |

The positive control passed every gate at 100%. ECP7-B16-I retained a passing
universal-translator score, but failed known-meaning train exactness, validation
and injectivity. It therefore remains a negative sealed-development result and
does not authorize confirmatory access.

The trajectory through step 15,000 matches B15 exactly, including task loss
`0.076486`, train exactness `82.0836%` and validation `72.9797%`. This verifies
that the delayed schedule isolated the intended late intervention. Minimax
weight then rose to `0.2` at step 16,000, `0.6` at step 18,000 and `1.0` at step
20,000.

At the selected step 28,000 checkpoint, the minimax loss was `0.11384` at full
weight, task loss was `0.07254`, and utilization loss was `-0.75143`. Relative
to B15, validation fell from 82.5867% to 76.4648% and translator validation fell
from 83.3740% to 77.7588%. The intervention did not reduce collision meanings or
make any sender injective.

Population validation factor accuracies were
`[90.74%, 99.90%, 98.44%, 86.34%]`; universal-translator factor accuracies were
`[93.65%, 100%, 98.44%, 84.62%]`. Late minimax slightly improved the weakest
texture score relative to B15 but disrupted the previously near-perfect color
generalization. The largest collision bucket also increased from three meanings
in B15 to four meanings in B16.

Both sealed analyses report 65 matching artifact hashes, 16,384 validation-only
episodes, no confirmatory-test keys, valid local alphabets, and exactly 14
declared bits for every logged message.

## Batch 16 decision

ECP7-B16-I is rejected. Generic worst-factor pressure after protocol formation
trades texture improvement for a larger color regression and does not solve
injectivity. Batch 15 remains the strongest weak-structure base, and the
confirmatory split remains sealed.

The next intervention should target the remaining hard-message collisions
without reweighting semantic factors. A future ECP7-B17 may return to B15 and
add one late, training-only global collision-pair replay objective. It would
mine colliding meaning pairs from each sender's complete training codebook,
then penalize their relaxed full-message collision probability. This directly
addresses the sparse-minibatch limitation observed in Batch 4 while assigning
no semantic factor to any channel slot. Architecture, base losses, duration,
data, translator and thresholds must remain unchanged.

## Batch 17 preregistration

Preregistered: July 18, 2026 at 14:35:00 UTC<br>
Seed: `11`<br>
Maximum population steps: `30,000`<br>
Minimum selection steps: `15,000`<br>
Early-stopping patience: `5,000` steps<br>
Replay start: step `15,000`<br>
Replay weight: `0` through step `15,000`, linear to `1.0` at step `20,000`, then hold<br>
Replay pairs per sender and update: `32`<br>
Training-codebook refresh interval: `200` steps<br>
Relaxed replay temperature: `1.0`<br>
Raw configuration SHA-256: `81bc1c36f7fd19afdecd61eb917fe41925db8266d8ac8b2bc96e70178e39c412`<br>
Effective configuration SHA-256: `70921261774f38f5ca22f122d05a2b9f1f0bc7c9ca6ea4c327097b7619715d5b`<br>
Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`<br>
Test unsealed: **no**

ECP7-B17-I returns to every Batch 15 setting and adds exactly one late
factor-agnostic collision-replay intervention. At registered evaluation
boundaries from step 15,000 onward, each sender's hard code over training
meanings is mined for every unordered colliding pair. A deterministic separate
sampler replays 32 pairs per sender and update; their relaxed full-message
collision probability is penalized. Validation and confirmatory meanings never
enter the replay bank. The unchanged positive control is rerun, and no
alternative replay or accompanying intervention is admitted into this batch.

## Batch 17 results

Positive-control run: `runs/ecp7-batch17-control-development/20260718T143730Z-ecp7-development`<br>
Intervention run: `runs/ecp7-batch17-intervention-development/20260718T143730Z-ecp7-development`<br>
Test unsealed: **no**

| Metric | Positive control | ECP7-B17-I |
|---|---:|---:|
| Population train, mean | 100% | 83.1456% |
| Population train, worst link | 100% | 82.5753% |
| Population validation, mean | 100% | 77.0935% |
| Population validation, worst link | 100% | 76.3672% |
| Universal translator, validation | 100% | 83.0078% |
| Exact sender-message agreement | 100% | 89.42% |
| Unique messages per sender | 15,360 | 12,944–13,259 |
| Collision meanings per sender | 0 | 2,101–2,416 |
| Message entropy | 13.91 bits | 13.58–13.61 bits |
| Development gate | pass | **fail** |

The positive control passed every gate at 100%. ECP7-B17-I retained a passing
universal-translator score, but failed known-meaning train exactness, validation
and injectivity. It remains a negative sealed-development result and does not
authorize confirmatory access.

The trajectory through step 15,000 matches B15 exactly. The first global mining
pass found 3,015, 3,005, 3,434 and 2,644 unordered colliding training pairs for
the four senders. At step 15,200, replay weight was `0.04` and the relaxed
collision probability was still `0.9977`, confirming that the hard-collision
pairs also had nearly identical soft codes.

The selected checkpoint was step 16,200. Replay weight was `0.24`, replay loss
was `0.83844`, task loss was `0.07453`, and utilization loss was `-0.74019`.
The weighted replay term was therefore approximately `0.201`, substantially
larger than the remaining task loss. The mined pair banks had fallen to
2,564, 2,255, 2,248 and 2,407 pairs, so the intervention did separate many
targeted collisions.

That benefit did not remain stable. As replay reached full weight, old pairs
separated but new collisions formed. At the final step 21,200, pair-bank sizes
were 3,493, 3,956, 2,215 and 1,194; validation had fallen to 71.60%. The
registered patience rule then stopped training 5,000 steps after the best
checkpoint.

Compared with B15, every selected sender used more unique messages and fewer
collision meanings, but no sender became injective. Sender agreement fell from
92.33% to 89.42%, while validation fell from 82.5867% to 77.0935%. Population
validation factor accuracies were
`[92.24%, 99.85%, 98.44%, 84.52%]`; universal-translator factor accuracies were
`[99.73%, 100%, 98.44%, 84.69%]`.

Both sealed analyses report 65 matching artifact hashes, 16,384 validation-only
episodes, no confirmatory-test keys, valid local alphabets, and exactly 14
declared bits for every logged message.

## Batch 17 decision

ECP7-B17-I is rejected under the joint gate. Global collision mining fixed the
sparse-signal problem from Batch 4 and modestly improved hard code use, but its
registered coefficient overpowered the remaining task objective and caused
collision churn rather than injectivity. Batch 15 remains the strongest base,
and the confirmatory split remains sealed.

A future ECP7-B18 may keep the complete B17 mining and replay mechanism while
returning to B15 and changing only the final replay coefficient from `1.0` to
`0.1`. Weight would remain `0` through step 15,000, warm linearly to `0.1` at
step 20,000 and then hold. This makes an initially near-one replay loss
comparable to the remaining task loss instead of several times larger. No
mining, pair batch, refresh, architecture, base loss, duration, data, translator
or threshold change may accompany that coefficient test.

## Batch 18 preregistration

Preregistered: July 18, 2026 at 14:53:31 UTC<br>
Seed: `11`<br>
Maximum population steps: `30,000`<br>
Minimum selection steps: `15,000`<br>
Early-stopping patience: `5,000` steps<br>
Replay start: step `15,000`<br>
Replay weight: `0` through step `15,000`, linear to `0.1` at step `20,000`, then hold<br>
Replay pairs per sender and update: `32`<br>
Training-codebook refresh interval: `200` steps<br>
Relaxed replay temperature: `1.0`<br>
Raw configuration SHA-256: `a9da48a2c76fd01a9f2889050c347ed9fcf616389297424f156e9f2d8489e59f`<br>
Effective configuration SHA-256: `21d76380640738ee98ddbdb7ae88c6a1d3185add860b96f1fe9c5c83a782d757`<br>
Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`<br>
Test unsealed: **no**

ECP7-B18-I keeps the entire Batch 17 mechanism and every Batch 15 model,
training and evaluation setting. It changes only the replay coefficient from
`1.0` to `0.1`, preserving the same start and 5,000-step linear warmup. This
tests whether replay can retain its code-use improvement when its weighted
magnitude remains comparable to the task loss. The unchanged positive control
is rerun, and no alternative coefficient or accompanying intervention is
admitted into this batch.

## Batch 18 results

Positive-control run: `runs/ecp7-batch18-control-development/20260718T145534Z-ecp7-development`<br>
Intervention run: `runs/ecp7-batch18-intervention-development/20260718T145534Z-ecp7-development`<br>
Test unsealed: **no**

| Metric | Positive control | ECP7-B18-I |
|---|---:|---:|
| Population train, mean | 100% | **84.0777%** |
| Population train, worst link | 100% | 82.1429% |
| Population validation, mean | 100% | **80.7129%** |
| Population validation, worst link | 100% | 78.6133% |
| Universal translator, validation | 100% | **84.0576%** |
| Exact sender-message agreement | 100% | 90.13% |
| Unique messages per sender | 15,360 | 12,720–13,442 |
| Collision meanings per sender | 0 | 1,918–2,640 |
| Message entropy | 13.91 bits | 13.55–13.64 bits |
| Development gate | pass | **fail** |

The positive control passed every gate at 100%. ECP7-B18-I passed validation
and universal-translator thresholds together. It set the strongest ECP-7 train
and translator scores so far, but still failed both known-meaning train
thresholds and sender injectivity. The joint gate therefore fails and
confirmatory access remains unauthorized.

The trajectory through step 15,000 again matches B15 exactly. At step 18,000,
replay weight was `0.06`, train exactness was 83.61% and validation was 79.52%.
At step 20,000 the coefficient reached its registered maximum `0.1` and
validation crossed 80%.

The selected checkpoint was step 22,400. Replay loss was `0.80354`, so its
weighted contribution was approximately `0.0804`, close to task loss `0.06669`
and far below B17's selected `0.201` contribution. Utilization loss was
`-0.75717`. The mined collision-pair banks contained 2,688, 2,240, 2,777 and
2,135 pairs.

The lower coefficient prevented B17's early collapse but did not make replayed
pairs stably separable: replay loss returned near one at several later
checkpoints while pair banks continued changing. Validation declined after the
selected checkpoint. The registered patience rule stopped at step 27,400, where
train exactness had risen to 84.49% but validation had fallen to 78.97%.

Compared with B15, three senders had fewer collision meanings and the fourth
was unchanged, but none became injective. Sender agreement remained below B15
at 90.13%. Population validation factor accuracies were
`[95.97%, 99.77%, 98.44%, 85.59%]`; universal-translator factor accuracies were
`[100%, 100%, 98.44%, 85.62%]`. The replay tradeoff again slightly improved
texture and code use while weakening population color generalization.

Both sealed analyses report 65 matching artifact hashes, 16,384 validation-only
episodes, no confirmatory-test keys, valid local alphabets, and exactly 14
declared bits for every logged message.

## Batch 18 decision

ECP7-B18-I is a valid partial improvement but remains negative under the joint
gate. Coefficient attenuation recovers validation and creates new-best train
and translator scores, confirming that B17's principal failure was objective
scale. It still does not approach the train thresholds or injectivity, and
Batch 15 retains the highest validation score. The confirmatory split remains
sealed.

A future ECP7-B19 may keep B18 exactly through step 20,000, then decay only the
replay coefficient linearly from `0.1` to `0` over steps 20,000–25,000 and hold
it at zero thereafter. This tests whether a bounded replay pulse can preserve
the early collision reduction while returning the final phase to pure B15 task
and utilization refinement. Mining, pair batch, refresh, architecture, base
losses, optimizer, duration, data, translator and thresholds must not change.

## Batch 19 preregistration

Preregistered: July 18, 2026 at 15:15:36 UTC<br>
Seed: `11`<br>
Maximum population steps: `30,000`<br>
Minimum selection steps: `15,000`<br>
Early-stopping patience: `5,000` steps<br>
Replay weight: `0` through step `15,000`, linear to `0.1` at step `20,000`, linear to `0` at step `25,000`, then hold<br>
Replay pairs per sender and update: `32`<br>
Training-codebook refresh interval: `200` steps<br>
Relaxed replay temperature: `1.0`<br>
Raw configuration SHA-256: `dab2cd0dadbadb47a10e2c45a720611dc91d140d3783f0ca1a537e4e8a8549c0`<br>
Effective configuration SHA-256: `cbd144a5fce451315a7d5fb322a11f2f29c32514fc22fbe06f46285aef677d13`<br>
Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`<br>
Test unsealed: **no**

ECP7-B19-I is identical to Batch 18 through step 20,000. It then changes only
the replay coefficient, decaying from `0.1` to zero by step 25,000. Mining
continues for diagnostics, but the final 5,000 steps receive no replay gradient
or sampler draws. This directly tests whether the early code-use gain can be
retained while the final phase returns to the unchanged B15 objectives. The
positive control is rerun, and no alternative pulse or accompanying
intervention is admitted into this batch.

## Batch 19 results

Positive-control run: `runs/ecp7-batch19-control-development/20260718T151853Z-ecp7-development`<br>
Intervention run: `runs/ecp7-batch19-intervention-development/20260718T151853Z-ecp7-development`<br>
Test unsealed: **no**

| Metric | Positive control | ECP7-B19-I |
|---|---:|---:|
| Population train, mean | 100% | **83.7385%** |
| Population train, worst link | 100% | 82.7148% |
| Population validation, mean | 100% | **82.0435%** |
| Population validation, worst link | 100% | **80.5664%** |
| Universal translator, validation | 100% | **83.4961%** |
| Exact sender-message agreement | 100% | 91.81% |
| Unique messages per sender | 15,360 | 12,709–13,200 |
| Collision meanings per sender | 0 | 2,160–2,651 |
| Message entropy | 13.91 bits | 13.54–13.61 bits |
| Development gate | pass | **fail** |

The positive control again passed every gate at 100%. ECP7-B19-I passed the
validation and universal-translator thresholds, and its 80.57% worst-link
validation is the strongest ECP-7 worst-link result so far. It still failed
both known-meaning train thresholds and every sender remained non-injective.
The joint gate therefore fails and confirmatory access remains unauthorized.

All 101 logged trajectory records through step 20,000 match Batch 18 exactly.
Replay then decayed as registered: weight was `0.06` at step 22,000, `0.02` at
step 24,000 and zero from step 25,000 onward. At zero weight the logged replay
loss is also zero and the sampler consumes no draws; deterministic full-codebook
mining remains visible only through diagnostic collision-pair counts.

Validation rose from 81.59% at the end of the decay to the selected 82.04% at
step 26,200, with replay fully inactive. It later fluctuated and finished at
81.20% at step 30,000. The selected checkpoint had task loss `0.06103`,
utilization loss `-0.72858`, and mined collision-pair counts of 2,674, 2,645,
2,921 and 2,352. The run reached the registered maximum horizon rather than an
early stop.

Compared with Batch 18, mean validation improved by 1.33 percentage points and
sender agreement improved from 90.13% to 91.81%. Train exactness fell by 0.34
points, translator validation fell by 0.56 points, and three of four senders
had more collision meanings. Compared with Batch 15, the pulse slightly reduced
collisions for three senders and produced a stronger worst validation link, but
mean validation remained 0.54 points lower and train exactness remained lower.
The selected sender codebooks contain 12,855, 12,886, 12,709 and 13,200 unique
messages, with 2,505, 2,474, 2,651 and 2,160 collision meanings.

Population validation factor accuracies were
`[97.93%, 99.73%, 98.44%, 85.30%]`; universal-translator factor accuracies were
`[100%, 100%, 98.44%, 85.06%]`. The bounded pulse therefore improves population
color generalization and cross-link balance after replay is removed, but does
not resolve the persistent texture errors or hard-code collisions.

Both sealed analyses report 65 matching artifact hashes, 16,384 validation-only
episodes, no confirmatory-test keys, valid local alphabets, and exactly 14
declared bits for every logged message.

## Batch 19 decision

ECP7-B19-I is a valid negative result under the joint gate. A bounded replay
pulse is less disruptive to validation than persistent replay, and its
replay-free tail improves the worst population link, but the collision benefit
does not persist and the train bottleneck remains essentially unchanged. Batch
15 retains the strongest mean validation, while Batch 18 retains the strongest
train and translator values. The confirmatory split remains sealed.

A future ECP7-B20 should stop tuning collision-replay schedules. A clean next
causal test is deterministic global hard-meaning task replay on the unchanged
Batch 15 base: mine only training meanings that the current population
reconstructs incorrectly, then add ordinary sender-receiver reconstruction
updates on a registered bounded sample. This directly tests whether the
remaining train error is a sparse hard-example problem without adding a
meaning-to-slot binding or a code-distance surrogate. Collision replay, factor
reweighting, architecture, optimizer, horizon, data, translator and thresholds
must remain unchanged or absent as appropriate.

## Batch 20 preregistration

Preregistered: July 18, 2026 at 15:42:06 UTC<br>
Seed: `11`<br>
Maximum population steps: `30,000`<br>
Minimum selection steps: `15,000`<br>
Early-stopping patience: `5,000` steps<br>
Hard-meaning predicate: any incorrect factor from any of 16 current population links<br>
Replay weight: `0` through step `15,000`, linear to `0.25` at step `20,000`, then hold<br>
Replay batch size: `64` meanings, uniform with replacement<br>
Training-only pool refresh interval: `200` steps<br>
Replay sampler seed offset: `+1211`<br>
Raw configuration SHA-256: `01afcad913222db6a6ef858919664cc50bfac9269f8405eb8cae0dd9832c7319`<br>
Effective configuration SHA-256: `44b1dbd8b767e4b3e58e88e7f1645e6dc1578b04fd30fa174777dffaf96c3b75`<br>
Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`<br>
Test unsealed: **no**

A selected-checkpoint diagnostic on completed Batch 15 found 3,406 training
meanings with at least one population-link error. They fail for 11.14 of 16
links on average. Their ordinary reconstruction loss is `0.20870`, compared
with `0.06442` on the full training set, so the registered coefficient gives an
estimated task-scale contribution of `0.0522`.

ECP7-B20-I is identical to Batch 15 through step 15,000. The first pool is then
mined from hard training predictions only. Each subsequent replay update uses
the same all-senders/all-receivers factor reconstruction loss and current
straight-through temperature as the ordinary task batch. The independent
sampler prevents replay-index draws from changing the base batch sequence. No
validation meaning participates in mining or replay. The positive control is
rerun, and no alternative hard predicate, coefficient, sampler or accompanying
intervention is admitted into this batch.

## Batch 20 results

Positive-control run: `runs/ecp7-batch20-control-development/20260718T154331Z-ecp7-development`<br>
Intervention run: `runs/ecp7-batch20-intervention-development/20260718T154331Z-ecp7-development`<br>
Test unsealed: **no**

| Metric | Positive control | ECP7-B20-I |
|---|---:|---:|
| Population train, mean | 100% | **83.7721%** |
| Population train, worst link | 100% | 82.7148% |
| Population validation, mean | 100% | **83.4473%** |
| Population validation, worst link | 100% | **82.1289%** |
| Universal translator, validation | 100% | **83.9600%** |
| Exact sender-message agreement | 100% | **92.40%** |
| Unique messages per sender | 15,360 | 12,795–13,304 |
| Collision meanings per sender | 0 | 2,056–2,565 |
| Message entropy | 13.91 bits | 13.56–13.62 bits |
| Development gate | pass | **fail** |

The positive control passed every gate at 100%. ECP7-B20-I establishes the
strongest ECP-7 mean validation, worst-link validation and sender agreement so
far. It passes the validation and universal-translator thresholds, but still
fails both known-meaning train thresholds and sender injectivity. The joint gate
therefore fails and confirmatory access remains unauthorized.

All 76 logged records through step 15,000 match Batch 15 exactly on every 25
shared trajectory field. The first registered mining pass found 3,452 hard
training meanings. Replay weight rose from zero to `0.25` by step 20,000, where
the pool had fallen to 2,862. Its minimum was 2,705 at step 27,400; it then
continued to fluctuate rather than converging to zero.

The selected checkpoint was step 29,800 with a 2,848-meaning pool. Task loss was
`0.06719`, hard-meaning replay loss `0.14823`, replay weight `0.25`, and
utilization loss `-0.73711`. The weighted replay contribution was approximately
`0.0371`, below the ordinary task loss. The run reached the registered 30,000
step horizon. Its final checkpoint had 3,084 hard meanings and 82.84%
validation, so selection correctly retained step 29,800 using validation only.

Compared with Batch 15, train exactness improved by 0.31 percentage points,
mean validation by 0.86 points, worst-link validation by 2.34 points, translator
validation by 0.59 points and sender agreement by 0.07 points. Batch 20 now
holds the strongest ECP-7 validation result; Batch 18 retains the strongest
train and translator results.

The hard pool did shrink, but its remaining errors became more population-wide.
At the selected Batch 15 checkpoint, 3,406 meanings fail for at least one link,
1,469 fail for all 16 links, and a hard meaning fails for 11.14 links on
average. At the selected Batch 20 checkpoint, those values are 2,848, 1,937 and
13.07. Uniform any-link replay therefore repairs many link-specific errors while
leaving a smaller set of more consistently wrong meanings. Its hard-pool loss
rose from the diagnostic `0.20870` to `0.25880` despite the smaller pool.

Selected sender codebooks contain 12,795, 12,960, 12,898 and 13,304 unique
messages, with 2,565, 2,400, 2,462 and 2,056 collision meanings. Population
validation factor accuracies were `[99.58%, 99.96%, 98.44%, 85.35%]`;
universal-translator factor accuracies were
`[100%, 100%, 98.44%, 85.52%]`. The generalization gain comes primarily from
near-complete population color and shape recovery, while size and especially
texture remain fixed bottlenecks.

Both sealed analyses report 65 matching artifact hashes, 16,384 validation-only
episodes, no confirmatory-test keys, valid local alphabets, and exactly 14
declared bits for every logged message.

## Batch 20 decision

ECP7-B20-I is a valid and informative negative result. Ordinary task replay on
any-link failures improves cross-link consistency and establishes the strongest
weak-structure validation result, but it does not materially lift train
exactness or reach injectivity. The confirmatory split remains sealed.

A future ECP7-B21 may keep the complete Batch 20 mechanism and parameters while
changing only the mining predicate from “at least one of 16 links fails” to
“all 16 links fail.” This tests the observed concentration directly by spending
the same registered replay budget exclusively on population-shared errors. No
coefficient, replay batch, refresh, schedule, architecture, base loss,
optimizer, horizon, data, translator or threshold change may accompany that
predicate test.
