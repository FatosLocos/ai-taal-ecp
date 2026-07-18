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

Reproduce the development arms with:

```bash
.venv/bin/ecp7 --config config/ecp7-positive-control-development.yaml develop --seed 11
.venv/bin/ecp7 --config config/ecp7-development.yaml develop --seed 11
```

Exact run identities, metrics and hashes are in `manifest.json`.
