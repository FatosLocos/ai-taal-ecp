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

Reproduce the development arms with:

```bash
.venv/bin/ecp7 --config config/ecp7-positive-control-development.yaml develop --seed 11
.venv/bin/ecp7 --config config/ecp7-development.yaml develop --seed 11
```

Exact run identities, metrics and hashes are in `manifest.json`.
