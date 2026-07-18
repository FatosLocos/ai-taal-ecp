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
and size remained the residual errors.

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
