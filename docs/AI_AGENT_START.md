# Fresh AI-agent start guide

This guide lets a new AI coding agent continue the project without relying on prior chat history.

## 1. What this repository contains

The project studies an Emergent Communication Protocol (ECP) between independently initialized sender and receiver agents. A meaning is a tuple of four categorical factors. Agents communicate through discrete, fixed-length messages and are evaluated on combinations excluded from training.

ECP-6 is the current confirmed result. It encodes `16 × 16 × 8 × 8 = 16,384` meanings with four factor-local symbols occupying exactly 14 wire bits. Five preregistered seeds achieved 100% population, worst-pair and universal-translator accuracy on the sealed test split.

The strongest justified conclusion is narrow: the learned protocol is lossless, compositional, transferable and information-theoretically minimal inside this synthetic product world. The factorization and factor-local receiver are architectural biases.

## 2. Repository map

| Path | Purpose |
|---|---|
| `config/` | Inheritable development, control and frozen experiment configurations |
| `src/ai_taal/world.py` | World enumeration and deterministic holdout construction |
| `src/ai_taal/models.py` | Sender and receiver architectures |
| `src/ai_taal/training.py` | Population, translator and binding-calibration training |
| `src/ai_taal/population_experiment.py` | Multi-agent execution, isolation and artifact writing |
| `src/ai_taal/metrics.py` | Accuracy, entropy, minimal-pair and topographic metrics |
| `src/ai_taal/analysis.py` | Hash checking and post-run confirmatory analysis |
| `schemas/` | JSON Schemas for meanings, messages and episodes |
| `tests/` | Unit and invariant tests |
| `docs/` | Preregistrations, sealed development logs, results and protocol specs |
| `evidence/` | Compact tracked snapshots of important results |
| `runs/` | Generated local artifacts; ignored by Git except its README |

## 3. Bootstrap and verify

The supported runtime is Python 3.12.

```bash
git clone https://github.com/FatosLocos/ai-taal-ecp.git
cd ai-taal-ecp
python3.12 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -e '.[dev]'
.venv/bin/pytest
.venv/bin/ecp6 --config config/ecp6.yaml validate
```

Expected baseline: 51 passing tests and split sizes `14336/1024/1024`.

## 4. Reproduce ECP-6

Start with a technical smoke run:

```bash
.venv/bin/ecp6 --config config/ecp6.yaml smoke --seed 11
```

To reproduce the already published confirmatory experiment, write to a fresh local output directory:

```bash
.venv/bin/ecp6 --config config/ecp6.yaml experiment \
  --unseal-test \
  --output-root runs/reproduction
```

Then verify hashes, channel constraints and topographic null models:

```bash
.venv/bin/ecp6 --config config/ecp6.yaml analyze \
  runs/reproduction/<generated-ecp6-experiment-directory> \
  --permutations 100
```

This reruns a known experiment. It must not be presented as a new independent confirmatory test.

## 5. Continue ECP-7 scientifically

Do not modify ECP-0 through ECP-6 or the completed ECP-7 Batch 1 and Batch 2
configs. ECP7-B1-I collapsed to 130–139 hard messages. ECP7-B2-I added a
factor-agnostic utilization loss that improved its soft objective but collapsed
further to 85–104 hard messages. Both paired ECP-6 positive controls stayed
perfect. The confirmatory ECP-7 test is still sealed.

Continue with this sequence:

1. Read `docs/research-design-ecp7.md` and `docs/development-log-ecp7.md`.
2. Define exactly one ECP7-B3 intervention and its failure criterion.
3. Register the variant and immutable configuration hashes before training.
4. Add tests for every new invariant.
5. Use only `smoke` and `develop`; keep the ECP-7 test split sealed.
6. Append every attempted variant and negative result to the development log.
7. Select at most one final design using train and validation only.
8. Create `config/ecp7.yaml` only after a design passes its development gate.
9. Freeze its UTC time, config hash, split hash, seeds and thresholds.
10. Only then run those seeds once with `experiment --unseal-test`.
11. Run integrity analysis and publish successes and failures.

## 6. Recommended next experiment

The first two attempts showed both severe code collapse and a soft-to-hard
relaxation gap. The most informative next step is one utilization objective
calculated from straight-through hard messages. A clean ECP7-B3 progression is:

- keep the same world and bit budget;
- keep the joint autoregressive sender and generic isolated receiver;
- retain the Batch 2 formula and replace only its soft message input with the
  straight-through hard message used by the task;
- measure injectivity, validation composition and new-reader induction;
- rerun the ECP-6 architecture as the frozen positive control.

Do not combine this with architectural resizing, a new loss weight, longer
training, variable-length messages or negotiation. That would make any change
from Batch 2 uninterpretable.

## 7. Definition of done for any contribution

- full tests pass;
- relevant configs validate;
- no generated checkpoint or episode log is staged;
- claims are backed by tracked evidence or reproducible commands;
- frozen experiments remain unchanged;
- limitations and any test access are stated explicitly.
