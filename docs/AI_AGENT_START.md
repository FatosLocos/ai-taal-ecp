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

Expected baseline: 136 passing tests and split sizes `14336/1024/1024`.

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

## 5. Preserve the completed ECP-7 series

Do not modify ECP-0 through ECP-6 or the completed ECP-7 Batch 1 through Batch 29
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
ECP7-B23-I restored joint replay gradients after the sender-only warmup. The
shared-error pool reached 1,414 during sender-only routing, then jumped to 1,984
at the first joint boundary and reached 2,085 at selection. The any-link pool
fell to 2,660, but validation remained 83.50%, train exactness and injectivity
still failed, and the confirmatory ECP-7 test remains sealed.
ECP7-B24-I made the post-warmup replay phase receiver-only. It set new ECP-7
bests of 84.69% mean train, 84.48% mean validation and 84.55% translator
validation, but worst-link validation remained 82.23%, sender injectivity
failed and the confirmatory ECP-7 test remains sealed.
ECP7-B25-I extended only that catch-up horizon to 45,000 steps. It improved to
85.26% mean train, 85.24% mean validation, 82.71% worst-link validation and
85.13% translator validation. The worst train link exactly matches its 82.81%
unique-code ceiling, so sender injectivity remains the structural blocker and
the confirmatory ECP-7 test remains sealed.
ECP7-B26-I inserted a second sender-only pulse followed by receiver-only
catch-up. It reached small new bests of 85.37% mean train and 85.38% validation
and translator validation, but its unique-message counts were effectively
unchanged. Shared failures fell while any-link failures rose, closing the
replay-routing family as an error-redistribution mechanism rather than an
injectivity solution. The confirmatory ECP-7 test remains sealed.
ECP7-B27-I added a late bounded direct collision-pair penalty. It reached
85.38% mean validation and reduced collision-pair multiplicity, but produced
exactly the same 13,440, 12,960, 12,720 and 13,440 unique-message counts as
Batch 25. Worst-link validation regressed to 82.13%, so the existing collision
loss is also closed as a capacity solution. The confirmatory test remains
sealed.
ECP7-B28-I added one zero-initialized shared residual sender interaction. Tests
prove an identical initial function and unchanged RNG state, but the trainable
branch still collapsed to 53.91% train, 9.65% validation, 11.62% translator
validation and only 7,928–8,333 messages. Generic sender depth active from the
first update is therefore rejected. The confirmatory test remains sealed.
ECP7-B29-I froze that residual branch at exact zero through step 30,000. All
151 shared history records matched Batch 25, but late activation reduced the
selected codebooks to 13,163, 12,960, 12,720 and 13,439 messages and worst-link
validation to 81.74%. This final permitted residual test failed. ECP-7
development is closed; no confirmatory configuration was frozen and the test
split was never opened.

Continue with this sequence:

1. Read `docs/research-design-ecp7.md` and `docs/development-log-ecp7.md`.
2. Read `docs/ecp7-development-conclusion.md`; do not create ECP7-B30.
3. Preserve every ECP-7 configuration and the still-sealed confirmatory split.
4. Define a new ECP-8 question before implementing another architecture or loss.
5. Create a fresh deterministic split and preregister its development gate.
6. Add tests for every new invariant.
7. Use only `smoke` and `develop` until one ECP-8 design passes development.
8. Freeze at most one design, its UTC time, hashes, seeds and thresholds.
9. Only then permit one confirmatory `experiment --unseal-test` execution.
10. Run integrity analysis and publish successes and failures.

## 6. Recommended next research phase

ECP-7 development is closed after 29 sealed variants. Do not continue a
residual schedule, collision coefficient, replay route or horizon search, and
do not open the unused ECP-7 confirmatory split.

ECP-8 Batch 1 is a separate preregistration that selects the learned-structure
direction through one narrow capacity question. Read
`docs/research-design-ecp8.md` and
`docs/development-log-ecp8.md`. Three seed-11 arms were registered before
training: a factorized 14-bit positive control, the strongest weak-structure
14-bit paired control, and the identical weak system with four unrestricted
16-symbol positions. Do not change their split, seed, architecture, training,
channel or gates, and never add `--unseal-test` during development.

After all three sealed runs, record the result even if it is negative. A passed
development gate only permits a later freeze decision; it does not itself
authorize confirmatory test access.

## 7. Definition of done for any contribution

- full tests pass;
- relevant configs validate;
- no generated checkpoint or episode log is staged;
- claims are backed by tracked evidence or reproducible commands;
- frozen experiments remain unchanged;
- limitations and any test access are stated explicitly.
