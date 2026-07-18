# AI Language — Emergent Communication Research

This project investigates whether independently trained AI agents can develop a communication protocol that is more compact, less ambiguous and more portable than human language for a defined task.

The first version is called **ECP-0**: *Emergent Communication Protocol, experiment 0*. ECP-0 does not use words or pre-assigned symbol meanings. A sender and receiver must reconstruct a meaning from an artificial world via four discrete symbols.

## Research question

> Can independent AI agents themselves develop a communication protocol that is efficient, generalizable, translatable and portable given the same task performance?

Within this research, a protocol only counts as a serious new form of communication when it:

1. is not semantically pre-programmed by humans;
2. can express unknown combinations;
3. can be accessed by an independent translator;
4. can be learned by new agents;
5. is demonstrably efficient compared to fixed baselines;
6. only uses the allowed and fully logged channel.

## Current status

**ECP-6 remains the latest confirmed result and successful scale replication of the fully efficient protocol.** All five seeds reconstruct known and completely new factor combinations for 100%. The universal translator and the worst agent pair also achieve 100%. The predetermined classification is **strong evidence**.

The protocol uses no words or alphabet, but four meaning-free local symbols. For `16 × 16 × 8 × 8 = 16,384` uniform meanings it uses exactly `4+4+3+3=14` bits: the information-theoretic lower bound. For this defined task, this is on average 23.9 times more compact than the Dutch text template.

See [`docs/results-ecp6.md`](docs/results-ecp6.md) for the conclusion, [`docs/protocol-specification-ecp6.md`](docs/protocol-specification-ecp6.md) for the wire format and [`evidence/ecp6/report.md`](evidence/ecp6/report.md) for the compact confirmatory evidence.

ECP-7 development now tests how much of that result depends on the explicit
one-factor-per-slot architecture. Its first twenty sealed batches are valid
development results but none passes the full gate. Batch 15 established the
strong position-aware base: at 30,000 optimization steps it reaches 83.46% train
exactness, 82.59% validation and 83.37% translator validation while using
12,585–13,200 hard messages per sender. Validation and translator thresholds pass
together, but the registered train and injectivity thresholds do not. Batch 16
added late worst-factor pressure and regressed to 76.46% validation. Batch 17
replayed globally mined training collisions and modestly improved code use, but
still regressed to 77.09% validation. Batch 18 reduced replay to task-loss scale,
recovering 80.71% validation and a new-best 84.06% translator score, but train
exactness and injectivity still failed. Batch 19 bounded replay to a pulse and
reached 82.04% validation plus a new-best 80.57% worst-link validation, but
again failed train exactness and injectivity. The ECP-6 positive controls remain
perfect. Batch 20 replayed population-hard training meanings and established
new-best 83.45% mean and 82.13% worst-link validation, but again failed train
exactness and injectivity. The ECP-7 confirmatory test remains sealed. See
[`docs/development-log-ecp7.md`](docs/development-log-ecp7.md).

## Build on this work

A new developer or fresh AI agent can start with no previous chat context. First read [`AGENTS.md`](AGENTS.md) for the binding research rules and then follow [`docs/AI_AGENT_START.md`](docs/AI_AGENT_START.md) for installation, architecture overview, reproduction and proper setup of ECP-7.

Contributions are welcome via [`CONTRIBUTING.md`](CONTRIBUTING.md). Large generated runs stay local; compact verifiable results come under [`evidence/`](evidence/).

## Language and frozen provenance

All reader-facing documentation, schemas, command-line output, and source commentary are in English. Two reproducibility artifacts intentionally retain original Dutch literals:

- the Dutch UTF-8 baseline sentence in `src/ai_taal/baselines.py`, because its byte length is a measured comparison;
- descriptive metadata and comments inside existing ECP-0 through ECP-6 YAML configurations, because their exact bytes are preregistered and referenced by published SHA-256 hashes.

Do not translate those artifacts in place. New experiment configurations and all new public documentation must be written in English.

## Files

- [`docs/research-design.md`](docs/research-design.md) — complete research question, phasing, measurements and stopping criteria.
- [`docs/experiment-template.md`](docs/experiment-template.md) — fixed report format per experimental run.
- [`docs/results-ecp0.md`](docs/results-ecp0.md) — outcomes, hypothesis testing and recommendation for step 2.
- [`docs/research-design-ecp1.md`](docs/research-design-ecp1.md) — predefined population experiment and decision criteria.
- [`docs/development-log-ecp1.md`](docs/development-log-ecp1.md) — development that occurred while the ECP-1 test set remained sealed.
- [`docs/results-ecp1.md`](docs/results-ecp1.md) — confirmatory results, comparison with ECP-0 and recommendation for ECP-2.
- [`docs/results-ecp2.md`](docs/results-ecp2.md) — permutation slots, paired consensus trial, and residual symbol collisions.
- [`docs/research-design-ecp3.md`](docs/research-design-ecp3.md) — pre-frozen hypothesis, split and decision rules for the injective protocol.
- [`docs/development-log-ecp3.md`](docs/development-log-ecp3.md) — development while the ECP-3 test split remained sealed.
- [`docs/results-ecp3.md`](docs/results-ecp3.md) — strong evidence, protocol example, efficiency and limits of the base model.
- [`docs/results-ecp4.md`](docs/results-ecp4.md) — perfect 10-bit population and the isolated translator error.
- [`docs/research-design-ecp5.md`](docs/research-design-ecp5.md) — prefrozen calibration experiment and orthogonal holdout.
- [`docs/development-log-ecp5.md`](docs/development-log-ecp5.md) — sealed development of exact binding induction.
- [`docs/results-ecp5.md`](docs/results-ecp5.md) — 5/5 error-free seeds and full efficiency analysis.
- [`docs/protocol-specification-ecp5.md`](docs/protocol-specification-ecp5.md) — logical message, 10-bit wire format and decoder procedure.
- [`docs/research-design-ecp6.md`](docs/research-design-ecp6.md) — pre-frozen scale test for 16,384 meanings.
- [`docs/development-log-ecp6.md`](docs/development-log-ecp6.md) — scale invariants and sealed 14-bit development.
- [`docs/results-ecp6.md`](docs/results-ecp6.md) — 5/5 error-free scale replications and integrity analysis.
- [`docs/protocol-specification-ecp6.md`](docs/protocol-specification-ecp6.md) — machine code, 14-bit wire format and induction procedure.
- [`docs/research-design-ecp7.md`](docs/research-design-ecp7.md) — preregistered weak-structure question, paired control and sealed split.
- [`docs/development-log-ecp7.md`](docs/development-log-ecp7.md) — the first negative weak-structure batch and integrity checks.
- [`config/ecp7-development.yaml`](config/ecp7-development.yaml) — sealed weak-structure intervention configuration.
- [`config/ecp7-b2-development.yaml`](config/ecp7-b2-development.yaml) — factor-agnostic soft code-utilization intervention.
- [`config/ecp7-b3-development.yaml`](config/ecp7-b3-development.yaml) — the same utilization formula on straight-through hard messages.
- [`config/ecp7-b4-development.yaml`](config/ecp7-b4-development.yaml) — direct joint-message collision pressure on top of Batch 3.
- [`config/ecp7-b5-development.yaml`](config/ecp7-b5-development.yaml) — straight-through sender consensus on the Batch 3 base.
- [`config/ecp7-b6-development.yaml`](config/ecp7-b6-development.yaml) — normalized minimax factor reconstruction on the Batch 3 base.
- [`config/ecp7-b7-development.yaml`](config/ecp7-b7-development.yaml) — bounded parallel generation from one shared joint context.
- [`config/ecp7-b8-development.yaml`](config/ecp7-b8-development.yaml) — algebraic context invariance on the parallel sender.
- [`config/ecp7-b9-development.yaml`](config/ecp7-b9-development.yaml) — generic position-aware MLP decoding on the parallel sender.
- [`config/ecp7-b10-development.yaml`](config/ecp7-b10-development.yaml) — the Batch 9 design with an isolated extended optimization horizon.
- [`config/ecp7-b11-development.yaml`](config/ecp7-b11-development.yaml) — late utilization-weight decay on the Batch 10 base.
- [`config/ecp7-b12-development.yaml`](config/ecp7-b12-development.yaml) — one additional generic shared decoder layer on the Batch 10 base.
- [`config/ecp7-b13-development.yaml`](config/ecp7-b13-development.yaml) — one additional generic shared sender layer on the Batch 10 base.
- [`config/ecp7-b14-development.yaml`](config/ecp7-b14-development.yaml) — late learning-rate decay on the Batch 10 base.
- [`config/ecp7-b15-development.yaml`](config/ecp7-b15-development.yaml) — the Batch 10 design with a 30,000-step population horizon.
- [`config/ecp7-b16-development.yaml`](config/ecp7-b16-development.yaml) — late normalized factor-minimax pressure on the Batch 15 base.
- [`config/ecp7-b17-development.yaml`](config/ecp7-b17-development.yaml) — late training-only global collision-pair replay on the Batch 15 base.
- [`config/ecp7-b18-development.yaml`](config/ecp7-b18-development.yaml) — the Batch 17 replay mechanism with final weight reduced to 0.1.
- [`config/ecp7-b19-development.yaml`](config/ecp7-b19-development.yaml) — the Batch 18 replay mechanism decayed back to zero after step 20,000.
- [`config/ecp7-b20-development.yaml`](config/ecp7-b20-development.yaml) — late ordinary task replay on population-hard training meanings.
- [`config/ecp7-positive-control-development.yaml`](config/ecp7-positive-control-development.yaml) — ECP-6 positive control on the ECP-7 split.
- [`config/ecp0.yaml`](config/ecp0.yaml) — machine-readable configuration from step 1.
- [`config/ecp1.yaml`](config/ecp1.yaml) — frozen configuration of the population trial.
- [`config/ecp3.yaml`](config/ecp3.yaml) — frozen configuration of the first successful base model.
- [`config/ecp5.yaml`](config/ecp5.yaml) — frozen configuration of the fully efficient end model.
- [`config/ecp6.yaml`](config/ecp6.yaml) — frozen configuration of the 16× scale replication.
- [`AGENTS.md`](AGENTS.md) — binding research and change rules for AI agents.
- [`docs/AI_AGENT_START.md`](docs/AI_AGENT_START.md) — full onboarding for a fresh AI agent.
- [`evidence/ecp6/manifest.json`](evidence/ecp6/manifest.json) — compact machine-readable confirmatory evidence.
- [`schemas/meaning.schema.json`](schemas/meaning.schema.json) — format of a meaning.
- [`schemas/message.schema.json`](schemas/message.schema.json) — format of an agent message.
- [`schemas/episode.schema.json`](schemas/episode.schema.json) — format of an evaluated episode.

## ECP-0 in one minute

- The world contains `8 × 8 × 4 × 4 = 1024` possible meanings.
- Each meaning consists of four independent factors: color, shape, size and texture.
- The agents only see numerical categories, not human labels.
- The channel has 16 possible symbols and exactly 4 positions: 16 bits per message.
- The sender and receiver do not share weights, embeddings or state.
- 128 meanings are completely excluded from training as unknown color-shape combinations.
- After training, the protocol is frozen and translated by a third model.
- Five independent training runs prevent conclusions based on one random code.

The theoretical lower limit for exactly distinguishing 1024 uniform meanings is 10 bits. ECP-0 deliberately uses 16 bits: more than enough to first test learnability, compositionality and translatability. Compression to 12 bits and then towards the 10-bit lower limit is part of step 2.

## Simulator

The reproducible simulator includes:

1. deterministic dataset generation;
2. separate sender, receiver and translation models;
3. discrete evaluation without hidden side channel;
4. automatic baselines, checks, measurements and run reports.

## Execute

Required: Python 3.12.

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/ecp0 validate
.venv/bin/pytest
```

The three output modes deliberately access the data differently:

```bash
# 25 steps: verify that the complete technical pipeline works
.venv/bin/ecp0 smoke --seed 11

# Full training on train and validation; the test split remains sealed
.venv/bin/ecp0 develop --seed 11

# Confirmatory run: all preregistered seeds and one-time test unsealing
.venv/bin/ecp0 experiment --unseal-test

# Verify hashes and compare protocol structure with random assignments
.venv/bin/ecp0 analyze runs/<run-id> --permutations 100

# ECP-1 uses the same interface with the population configuration
.venv/bin/ecp1 --config config/ecp1.yaml validate
.venv/bin/ecp1 --config config/ecp1.yaml analyze runs/<ecp1-run-id> --permutations 100

# ECP-3: injective atomic codes and learned protocol consensus
.venv/bin/ecp3 --config config/ecp3.yaml validate
.venv/bin/ecp3 --config config/ecp3.yaml analyze runs/<ecp3-run-id> --permutations 100

# ECP-5: theoretically minimal 10-bit code with a calibrated reader
.venv/bin/ecp5 --config config/ecp5.yaml validate
.venv/bin/ecp5 --config config/ecp5.yaml analyze runs/<ecp5-run-id> --permutations 100

# ECP-6: 16,384 meanings at the exact 14-bit lower bound
.venv/bin/ecp6 --config config/ecp6.yaml validate
.venv/bin/ecp6 --config config/ecp6.yaml analyze runs/<ecp6-run-id> --permutations 100

# ECP-7 sealed development; never add --unseal-test to these configs
.venv/bin/ecp7 --config config/ecp7-development.yaml validate
.venv/bin/ecp7 --config config/ecp7-development.yaml develop --seed 11
.venv/bin/ecp7 --config config/ecp7-development.yaml analyze runs/<ecp7-development-run-id> --permutations 100
```

Each run writes configuration, environment, checkpoints, raw messages, checks, hashes, metrics, and a report to a new folder under `runs/`.
