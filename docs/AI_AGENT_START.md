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

Expected baseline: 114 passing tests and split sizes `14336/1024/1024`.

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

Do not modify ECP-0 through ECP-6 or the completed ECP-7 Batch 1 through Batch 22
configs. ECP7-B1-I collapsed to 130–139 hard messages. ECP7-B2-I improved its
soft objective but collapsed further to 85–104 hard messages. ECP7-B3-I applied
that loss to straight-through hard messages and improved to 585–972 messages,
but still reached only 1.92% validation. ECP7-B4-I added direct minibatch
collision pressure and regressed to 426–579 messages and 0.42% validation.
ECP7-B5-I raised exact inter-sender agreement from 2.47% to 44.02%, but did so
through a shared collapse to 169–231 messages and 0.48% validation.
ECP7-B6-I emphasized the worst normalized factor loss, but color and shape
remained near chance and validation reached only 0.46%. All paired ECP-6
positive controls stayed perfect. ECP7-B7-I replaced autoregression with a
parallel joint-context sender. It increased train exactness to 9.60% and used
3,118–3,415 messages, but shape stayed below chance and validation reached only
0.51%. ECP7-B8-I added context-invariant atomic transitions, but regressed to
857–1,135 messages and 0.32% validation. ECP7-B9-I replaced the recurrent
final-state decoder with a generic position-aware MLP. It is the first major
weak-structure result: 71.27% train exactness, 52.39% validation, 54.81%
translator validation and 10,834–11,017 messages. It still failed all joint
performance and injectivity gates. ECP7-B10-I kept B9's original temperature
schedule and extended population optimization to 15,000 steps. It reached
82.08% train exactness, 72.98% validation, 75.15% translator validation and
12,358–12,906 messages. The translator gate passed, but train, validation and
injectivity did not. ECP7-B11-I decayed late utilization pressure and regressed
to 79.09% train, 72.22% validation and 72.41% translator validation. B10 remains
the strongest base. ECP7-B12-I added one shared decoder layer and regressed
further to 71.53% train, 47.98% validation and 63.04% translator validation.
ECP7-B13-I added the symmetric sender layer and collapsed to 1.32% train, 0.32%
validation and 0.61% translator validation. ECP7-B14-I decayed late learning
rate and regressed to 79.13% train, 65.49% validation and 71.02% translator
validation. ECP7-B15-I extended constant-rate training to 30,000 steps and is
now strongest at 83.46% train, 82.59% validation and 83.37% translator
validation. Its validation and translator gates pass, but train and injectivity
do not. ECP7-B16-I added late normalized factor-minimax pressure. It slightly
improved texture but disrupted color, regressing to 82.80% train, 76.46%
validation and 77.76% translator validation without solving injectivity. Batch
15 remains strongest. ECP7-B17-I replayed globally mined training collisions.
It modestly improved unique-message use but regressed to 83.15% train, 77.09%
validation and 83.01% translator validation without becoming injective. The
confirmatory ECP-7 test is still sealed.
ECP7-B18-I reduced replay weight to `0.1` and recovered 84.08% train, 80.71%
validation and a new-best 84.06% translator validation. Validation and
translator gates pass, but train and injectivity do not. Batch 15 retained the
best validation result at that stage, and the confirmatory ECP-7 test remains
sealed.
ECP7-B19-I decayed replay back to zero from steps 20,000–25,000. It reached
83.74% train, 82.04% validation, a new-best 80.57% worst-link validation and
83.50% translator validation. The bounded pulse improved cross-link balance but
still failed train thresholds and injectivity. Batch 15 retained the best mean
validation result at that stage, and the confirmatory ECP-7 test remains
sealed.
ECP7-B20-I replayed ordinary task updates on training meanings failed by any
population link. It reached 83.77% train, a new-best 83.45% mean and 82.13%
worst-link validation, and 83.96% translator validation. The pool shrank but its
remaining errors became more population-wide, so train thresholds and
injectivity still failed. The confirmatory ECP-7 test remains sealed.
ECP7-B21-I restricted the same replay budget to meanings failed by all 16
population links. It reached a new-best 83.63% mean and 82.62% worst-link
validation and 92.96% sender agreement, but mean train remained 83.71% and the
target shared-error pool grew. The confirmatory ECP-7 test remains sealed.
ECP7-B22-I blocked receiver-parameter gradients only for the additional replay
loss. Its shared-error pool fell from 1,745 to 1,513 at selection, but the total
any-link pool grew to 3,197, sender agreement fell to 92.06% and validation
regressed to 83.51%. Train thresholds and injectivity still failed, and the
confirmatory ECP-7 test remains sealed.

Continue with this sequence:

1. Read `docs/research-design-ecp7.md` and `docs/development-log-ecp7.md`.
2. Define exactly one ECP7-B23 intervention and its failure criterion.
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

Batch 22 confirms that sender-only replay reduces shared errors, but receivers
cannot follow the moving codes quickly enough: any-link failures rise and
agreement falls. Batch 21 shows the opposite joint-routing behavior. The clean
next question is whether routing should be phased rather than permanent. A clean
ECP7-B23 progression is:

- inherit the complete Batch 22 implementation, Batch 21 predicate and Batch 15
  base;
- keep replay sender-only only during its registered steps 15,000–20,000
  warmup, then restore receiver-parameter replay gradients after step 20,000;
- keep ordinary base-task updates to both senders and receivers unchanged;
- keep weight `0.25`, the 64-meaning replay batch, 200-step refresh,
  seed-derived sampler, predicate, temperature and horizon unchanged;
- continue to mine and replay training meanings only;
- measure shared and any-link pool sizes, train exactness, injectivity,
  validation and new-reader induction, and rerun the frozen ECP-6 control.

Do not combine the routing schedule with another predicate, coefficient, graded
sampling, collision pressure, a new architecture, factor-specific weights,
optimizer changes, longer training, variable-length messages or negotiation.

## 7. Definition of done for any contribution

- full tests pass;
- relevant configs validate;
- no generated checkpoint or episode log is staged;
- claims are backed by tracked evidence or reproducible commands;
- frozen experiments remain unchanged;
- limitations and any test access are stated explicitly.
