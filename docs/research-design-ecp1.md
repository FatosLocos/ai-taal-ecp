# Research Design ECP-1 — Population and Transmissibility

Status: Frozen for confirmatory execution on July 18, 2026 at 00:17:09 UTC<br>
Parent experiment: ECP-0.2

## Rationale

ECP-0 developed near-injective protocols with provable semantic geometry, but only 15.9% average exact generalization to fully withheld color-shape pairs. The large differences between seeds indicate co-adaptation: one sender and one receiver can together stabilize a usable but poorly transferable code.

## Central hypothesis

> If each sender has to communicate with multiple independently parameterized receivers and vice versa during training, there is more pressure towards a shared, systematic and portable protocol.

ECP-1 therefore changes one primary mechanism: one pair is replaced by four senders and four receivers. Channel, world, models and reconstruction task remain the same as ECP-0.2.

## New and independent test set

The eight ECP-0 test pairs are explicitly excluded. ECP-1 uses a new data-split seed and accepts only a one-to-one matching that contains no old test pair. The new test set remains sealed during development and model selection.

Because the ECP-0 test set is known, it may not be reused as a confirmatory ECP-1 test.

## Population training

- Four senders and four receivers start with independent initializations.
- No weights, embeddings, gradients outside the chosen pair, or hidden states are shared.
- Per step, all four senders each produce one message for the same random batch.
- All four receivers reconstruct each sender message; the sixteen losses are averaged.
- Each step therefore contains all sixteen sender-receiver interactions, without a leader or preferred dialect.
- Over 7,000 steps, each pair receives the same number of direct learning interactions as an ECP-0 pair.
- Model selection uses only train and validation.
- A checkpoint is only primarily selectable if it has at least 99% average known accuracy and at least 95% for the worst pair.

## Universal translator and new receiver

After freezing the population, one new receiver is trained on messages from all four senders. This receiver does not have access to the original receivers and simultaneously acts as a universal translator.

A transfer curve additionally trains fresh receivers with 32, 128, 512, and 768 unique training meanings. All four senders deliver messages for the same selected meanings. The curve measures whether the population protocol can be adopted with few examples.

## Primary outcome measures

1. average exact accuracy over all sixteen pairs;
2. worst pair accuracy;
3. mean accuracy on the new held-out color-shape pairs;
4. accuracy of the universal translator on those pairs.

Strong evidence required in at least four of five valid seeds:

- at least 99% average on known meanings;
- minimum 95% for the worst known pair;
- at least 60% average on the compositional test;
- at least 50% for the universal translator on the compositional test.

## Controls

- Final sender and receiver evaluations run in separate processes.
- Receivers receive only the symbol matrix.
- Messages are shuffled within each channel; the accuracy should drop to a maximum of 1%.
- A consistent vocabulary permutation is applied to all messages and receiver embeddings; predictions must remain identical.
- Results are stored per pair and as a population average, so that a good average does not hide a failing pair.

## Interpretation

An improvement over ECP-0 supports the hypothesis that communicative diversity reduces co-adaptation. No improvement is also informative: then population pressure alone is insufficient and ECP-2 must isolate iterative learning, progressive reconstruction or more explicit context pressure.

Compression to 12 bits is deliberately not tested in ECP-1. First, the semantic transfer must become more stable.

The five seeds may run simultaneously in separate processes. This does not change any data, model interaction or random generator within a seed and only serves to reduce wall clock time.
