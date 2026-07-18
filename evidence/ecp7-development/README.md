# ECP-7 Sealed Development Evidence

This directory records the compact evidence for ECP-7 Batch 1. It is a
development result, not a confirmatory experiment.

The batch used seed `11` and split SHA-256
`4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`.
The ECP-6 positive control achieved 100% exact validation accuracy. The
weak-structure intervention achieved 0.6287% mean validation exactness, created
only 130–139 unique messages per sender, and failed the preregistered gate.

The confirmatory test stayed sealed: both runs have `test_unsealed=false`, no
test metrics, and validation-only episode logs. The complete generated runs,
checkpoints and raw episode logs remain local under `runs/` and are not tracked.

Batch 2 added a factor-agnostic soft code-utilization loss. The positive control
again achieved 100%, but the intervention used only 85–104 hard messages and
failed the same registered gate. Its improved soft utilization objective did
not transfer to the discrete protocol. Exact Batch 2 identities and hashes are
in `batch2-manifest.json`.

Batch 3 applied the unchanged objective to straight-through one-hot messages.
It remained below the gate but improved to 585–972 hard messages, 8.20–8.73
bits of entropy and 1.92% validation. Exact identities and hashes are in
`batch3-manifest.json`.

Batch 4 added direct minibatch full-message collision pressure. It regressed to
426–579 messages and 0.42% validation, showing that the sparse local signal was
not a useful proxy for global codebook occupancy. Exact identities and hashes
are in `batch4-manifest.json`.

Batch 5 aligned straight-through symbols across independent senders on the
Batch 3 base. Exact complete-message agreement rose from 2.47% to 44.02%, but
the shared protocol collapsed to 169–231 messages and 0.48% validation. Exact
identities and hashes are in `batch5-manifest.json`.

Batch 6 emphasized the worst normalized factor-reconstruction loss. Color and
shape remained near chance, and the protocol used only 313–542 messages with
0.46% validation. Exact identities and hashes are in `batch6-manifest.json`.

Batch 7 replaced autoregressive generation with a joint-context parallel
sender. It reached 3,118–3,415 messages, 9.60% train exactness and 45.64% color
accuracy, but shape remained below chance and validation stayed at 0.51%. Exact
identities and hashes are in `batch7-manifest.json`.

Batch 8 added algebraic context invariance to Batch 7. The relaxed surrogate
improved, but the discrete protocol regressed to 857–1,135 messages and 0.32%
validation. Exact identities and hashes are in `batch8-manifest.json`.

Batch 9 replaced the recurrent decoder with a generic position-aware MLP. It
reached 71.27% train exactness, 52.39% validation, 54.81% translator validation
and 10,834–11,017 messages, but still missed every registered performance and
injectivity gate. Exact identities and hashes are in `batch9-manifest.json`.

Batch 10 preserved Batch 9's first 5,000 temperature steps and extended only
population optimization to 15,000 steps. It reached 82.08% train exactness,
72.98% validation and 75.15% translator validation. The translator gate passed,
but train, validation and injectivity still failed. Exact identities and hashes
are in `batch10-manifest.json`.

Batch 11 decayed code-utilization weight after step 5,000. It regressed to
79.09% train exactness, 72.22% validation, 72.41% translator validation and
11,893–12,323 messages. Batch 10 therefore remains the strongest base. Exact
identities and hashes are in `batch11-manifest.json`.

Batch 12 added one generic shared hidden layer to the receiver and translator.
It regressed sharply to 71.53% train exactness, 47.98% validation and 63.04%
translator validation. Decoder depth is therefore rejected as the B10
bottleneck. Exact identities and hashes are in `batch12-manifest.json`.

Batch 13 added the symmetric shared sender layer. It collapsed to 1.32% train
exactness, 0.32% validation, 0.61% translator validation and only 694–831
messages. Sender depth is therefore also rejected. Exact identities and hashes
are in `batch13-manifest.json`.

Batch 14 decayed learning rate after step 5,000. It regressed to 79.13% train
exactness, 65.49% validation and 71.02% translator validation. Constant late
learning rate is therefore retained. Exact identities and hashes are in
`batch14-manifest.json`.

Batch 15 extended the constant-rate horizon to 30,000 steps. It reached 83.46%
train exactness, 82.59% validation and 83.37% translator validation. Validation
and translator gates passed together, but train exactness and injectivity still
failed. Exact identities and hashes are in `batch15-manifest.json`.

Batch 16 added normalized factor-minimax pressure only after step 15,000. It
regressed to 82.80% train exactness, 76.46% validation and 77.76% translator
validation, while injectivity still failed. Batch 15 remains strongest. Exact
identities and hashes are in `batch16-manifest.json`.

Batch 17 replayed globally mined training-code collisions after step 15,000.
It improved hard code use modestly but regressed to 83.15% train exactness,
77.09% validation and 83.01% translator validation without reaching
injectivity. Exact identities and hashes are in `batch17-manifest.json`.

Batch 18 reduced final replay weight to 0.1. It recovered 84.08% train
exactness, 80.71% validation and a new-best 84.06% translator validation, but
still failed train thresholds and injectivity. Exact identities and hashes are
in `batch18-manifest.json`.

Batch 19 decayed that replay weight back to zero after step 20,000. It reached
83.74% train exactness, 82.04% validation, a new-best 80.57% worst-link
validation and 83.50% translator validation. The bounded pulse improved
cross-link balance but still failed train thresholds and injectivity. Exact
identities and hashes are in `batch19-manifest.json`.

Batch 20 replayed ordinary task updates on training meanings failed by any
population link. It reached 83.77% train exactness, a new-best 83.45% mean and
82.13% worst-link validation, and 83.96% translator validation. The hard pool
shrunk but concentrated into population-wide failures, so train thresholds and
injectivity still failed. Exact identities and hashes are in
`batch20-manifest.json`.

Batch 21 restricted the unchanged replay budget to meanings failed by all 16
population links. It reached a new-best 83.63% mean and 82.62% worst-link
validation plus 92.96% sender agreement, but mean train remained 83.71% and the
target shared-error pool grew. Exact identities and hashes are in
`batch21-manifest.json`.

Batch 22 blocked receiver-parameter gradients only on the additional all-link
replay loss. Shared errors fell from 1,745 to 1,513 at selection, but the total
any-link pool grew to 3,197 and validation regressed to 83.51%. Sender-only
routing therefore trades shared ambiguity for cross-link fragmentation. Exact
identities and hashes are in `batch22-manifest.json`.

Batch 23 kept the Batch 22 sender-only warmup through step 20,000 and then
restored joint replay gradients. The shared-error pool fell to 1,414 during the
sender-only phase but jumped to 1,984 at the first joint phase boundary and
reached 2,085 at selection. The any-link pool improved to 2,660, but validation
remained 83.50% and injectivity still failed. Exact identities and hashes are in
`batch23-manifest.json`.

Batch 24 changed the second replay phase from joint to receiver-only. It reached
new-best means of 84.69% train, 84.48% validation and 84.55% translator
validation. The selected error pool contains 1,690 shared failures and 3,142
any-link failures, so worst-link accuracy and injectivity still fail. Exact
identities and hashes are in `batch24-manifest.json`.

Batch 25 extended only the receiver-only catch-up ceiling to 45,000 steps. It
set new-best means of 85.26% train, 85.24% validation and 85.13% translator
validation, but the observed worst train link exactly reached its sender's
82.81% unique-code ceiling. The remaining failure is sender injectivity, not
receiver training time. Exact identities and hashes are in
`batch25-manifest.json`.

Batch 26 inserted one second sender-only pulse followed by receiver-only
catch-up. It reached small new-best means of 85.37% train and 85.38% validation
and translator validation, but its unique-message counts were effectively
unchanged. Shared failures fell from 1,677 to 1,330 while any-link failures
rose from 2,967 to 3,262, confirming that route cycling redistributes errors
without fixing sender collisions. Exact identities and hashes are in
`batch26-manifest.json`.

Batch 27 added a late bounded direct penalty on globally mined sender
collisions. It reduced unordered collision-pair multiplicity and increased
message entropy, but produced exactly the same unique-message counts as Batch
25 while worst-link validation fell to 82.13%. The existing collision loss
therefore reshapes occupied codes without creating new ones. Exact identities
and hashes are in `batch27-manifest.json`.

Reproduce the development arms with:

```bash
.venv/bin/ecp7 --config config/ecp7-positive-control-development.yaml develop --seed 11
.venv/bin/ecp7 --config config/ecp7-development.yaml develop --seed 11
```

Exact run identities, metrics and hashes are in `manifest.json`.
