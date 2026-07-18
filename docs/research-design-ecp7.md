# Research Design ECP-7 — Weakening the Factor-Slot Bias

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026<br>
Intervention configuration: `config/ecp7-development.yaml`<br>
Positive-control configuration: `config/ecp7-positive-control-development.yaml`

The confirmatory ECP-7 test split has not been accessed. This document defines
the first development batch only. No frozen confirmatory configuration exists
yet.

## Question

Does exact, compositional and transferable communication survive when sender
and receiver architectures no longer encode a one-factor-per-slot binding,
while the world, four-slot wire capacity, population and training budget remain
fixed?

This is a narrower and more difficult question than whether a neural network
can reproduce the ECP-6 code. The intervention must learn how the four meaning
factors jointly determine a message, and a generic sequence receiver must learn
how the entire message determines every factor.

## Single intervention

ECP-7 changes one architectural assumption: factor-local processing.

The intervention sender:

1. embeds all four input factors into one joint context;
2. emits four symbols autoregressively with a GRU;
3. is constrained only by per-position alphabet sizes `[16,16,8,8]`;
4. has no factor-specific output heads, factor codebook or predefined
   factor-to-slot binding.

The intervention receiver and universal translator are generic GRU sequence
encoders with four classification heads. Slot-binding calibration and the
factor/atom consensus losses are disabled.

The unchanged ECP-6 factorized sender and receiver form a positive control on
the same new split. The positive control tests whether a failure comes from the
intervention rather than the split or execution pipeline.

## Capacity and remaining inductive bias

The world remains `16 × 16 × 8 × 8 = 16,384 = 2^14` equiprobable meanings. The
message has four categorical positions with alphabet sizes `[16,16,8,8]`, so
the nominal widths `[4,4,3,3]` occupy exactly 14 bits.

ECP-7 therefore removes factor-slot binding, but it is not an unconstrained or
natural language experiment. It retains:

- categorical, fully observed inputs;
- a synthetic product world;
- a fixed four-position message frame;
- position-specific alphabet capacities;
- supervised task rewards and a fixed training schedule.

Any conclusion must be limited to this setting.

## Sealed data split

Validation uses the unused cyclic color-shape matching with shift `+10`; the
confirmatory test uses shift `+11`. Both are disjoint from the ECP-6 validation
and test matchings (`+8` and `+9`).

| Split | Meanings | Color-shape pairs | Permitted during development |
|---|---:|---:|---|
| Train | 14,336 | 224 | yes |
| Validation | 1,024 | 16 | yes |
| Confirmatory test | 1,024 | 16 | **no** |

Split-SHA-256: `4947058c75ab07cb43a87eb82776b12cb2a7e2eeba7114de110d3b852cbc64cd`.

## First development batch

The first batch contains exactly two runs, both with seed `11` and at most
5,000 population-training steps:

1. `ecp6_factorized_positive_control`;
2. `bounded_autoregressive_intervention`.

Only train and validation data may be evaluated. Smoke runs may precede the
full runs to verify mechanics, but may not be used to tune the intervention.
No alternative architecture or hyperparameter variant is admitted into this
batch.

The positive control validates the batch when both its mean and worst-link
validation exactness are at least 99%. If it misses that gate, the batch is
inconclusive rather than evidence against the intervention.

When the positive control is valid, the intervention passes the development
gate only if all of the following hold:

1. known population exactness is at least 97% on average and 95% for the worst
   sender-receiver link;
2. mean validation exactness is at least 80%;
3. universal-translator validation exactness is at least 70%;
4. every logged symbol respects its position-specific alphabet boundary;
5. each sender assigns a unique message to every accessible train and
   validation meaning;
6. artifact and split integrity checks pass and no confirmatory test episode or
   metric is written.

If the positive control passes and the intervention misses any gate, the first
ECP-7 architecture is recorded as a negative development result. The test stays
sealed. A later variant, if justified, must be numbered and preregistered before
training.

Passing the development gate is not confirmation. It only permits selection of
a single frozen ECP-7 design and confirmatory criteria in a later commit.

## Recorded configuration identities

| Arm | Raw file SHA-256 | Effective configuration SHA-256 |
|---|---|---|
| Intervention | `7863ffbb4fdfdf43d28fed897d75989153e72ed0c432eaadbddc835f27c77b8f` | `e5f6ea5042dc59b5b10c5860ce7a672274b6b3ba887656de6f56cb8192181561` |
| Positive control | `4d5904a894b5d854831049cb38331c2e42aabc5da844de3d95e665d941ca6c8f` | `db323732a1160859835c930f2ffa578df363ddf146537aa0d4ee2496e2b9744d` |

## Batch 2 preregistration — Factor-agnostic code utilization

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026<br>
Configuration: `config/ecp7-b2-development.yaml`<br>
Raw configuration SHA-256: `95f402cc9b5f151b017d2c92ad4954d463aa73e0a13e9e1df84393f12a570cfc`<br>
Effective configuration SHA-256: `fc419eff2065f6259553d7fb5bbbd7de396be055a66c860884fe1c193158ea0f`

Batch 1 showed severe code collapse: the intervention used only 130–139
messages and approximately 6.45 bits of entropy. Batch 2 asks whether one
factor-agnostic pressure for using the available code space can prevent that
collapse without restoring a factor-to-slot binding.

For each sender, the new loss observes only its relaxed message distributions.
It receives no factor labels, factor identity, target slot or desired code. For
each slot it minimizes normalized conditional entropy and maximizes normalized
marginal entropy. It also minimizes normalized pairwise mutual information
between slots, discouraging four balanced slots from carrying duplicate
information.

In compact form:

`L_util = mean(H(slot | input) - H(slot)) + mean(pairwise normalized MI)`

Each entropy is normalized by that slot's maximum entropy. The loss weight is
fixed at `1.0`, warms up linearly for 400 steps, uses relaxed temperature `1.0`,
and gives the independence term weight `1.0`. An ideal deterministic, balanced,
pairwise-independent code has loss `-1`; a deterministic collapsed code and a
fully uncertain uniform code both have loss `0`.

No architecture, task loss, population setting, data split, capacity, early
stopping rule or translator setting changes from ECP7-B1-I. This objective adds
a product-code utilization bias, but it does not specify which semantic factor
belongs in any slot.

The batch contains exactly two seed-11 runs:

1. the unchanged ECP-6 positive control;
2. ECP7-B2-I with factor-agnostic code utilization.

The positive-control validity gate and intervention development gate are
unchanged from Batch 1. In particular, B2 must reach the registered population,
validation and translator thresholds, produce an injective code over all 15,360
accessible meanings for every sender, respect every local slot boundary, and
write no confirmatory test metric or episode. Failure is recorded without
opening the test split. No weight, warmup, temperature or independence variant
may be tried inside Batch 2.

## Batch 3 preregistration — Straight-through hard utilization

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026<br>
Configuration: `config/ecp7-b3-development.yaml`<br>
Raw configuration SHA-256: `8a1fb70caeb16ee2e9f912fe37508d02c25d2b00e4ec887546d143fdc099ad39`<br>
Effective configuration SHA-256: `62cb6965f619a72905af2ba652e1feea3e718cad1201cdd4066063de4aef7756`

Batch 2 improved its loss on relaxed distributions while the evaluated hard
code collapsed further. Batch 3 tests whether that relaxation gap closes when
the unchanged utilization formula receives the same straight-through one-hot
messages already consumed by the receivers during task training.

This is the only Batch 3 change. The forward values used to calculate entropy
and pairwise mutual information are discrete one-hot symbols. Gradients still
flow through the straight-through Gumbel estimator. The architecture, factor
inputs, loss weight `1.0`, 400-step warmup, temperature `1.0`, independence
weight `1.0`, task loss, population, split, capacity, training duration, early
stopping and translator remain unchanged from Batch 2.

The utilization loss still receives no factor labels, factor identities or
desired slot mapping. It does add an explicit pressure on the empirical hard
symbol marginals and pairwise slot dependence of each training batch.

The batch contains exactly two seed-11 runs:

1. the unchanged ECP-6 positive control;
2. ECP7-B3-I with straight-through hard code utilization.

The positive-control validity gate and intervention development gate remain
unchanged. B3 must pass population, validation, translator, injectivity, channel
and sealed-test checks together. A failure remains a development result and
does not authorize confirmatory test access. No alternative estimator, weight
or training schedule may be tried inside Batch 3.

## Batch 4 preregistration — Direct joint-message collisions

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026<br>
Configuration: `config/ecp7-b4-development.yaml`<br>
Raw configuration SHA-256: `6229c5cd13c796a9ce297b9c38cc2ff1a2090a2a22a5678ec7afe38aa0bd6955`<br>
Effective configuration SHA-256: `4cffdb040ba358d7416e0643595c4e11fadc0fdffd5c0120761c4890a8c3f10e`

Batch 3 improved marginal hard utilization but retained thousands of complete
message collisions. Batch 4 asks whether directly penalizing those joint
collisions produces an injective and compositional code without a semantic
factor-to-slot binding.

For every sender and minibatch, the new loss is the average number of other
distinct inputs with the same complete straight-through message:

`L_joint = (1/B) × sum_i sum_j!=i 1[x_i != x_j] × product_s <m_i,s, m_j,s>`

Because the forward messages are one-hot, the slot dot product is one exactly
when both symbols match, and the product is one exactly when the full messages
match. Identical sampled inputs are excluded; no factor label, factor identity
or desired code is provided. Straight-through gradients flow back through the
hard messages.

The joint-collision weight is fixed at `1.0` with a 400-step linear warmup. This
is the only Batch 4 addition. The complete Batch 3 utilization objective,
architecture, task loss, population, split, 14-bit channel, 5,000-step limit,
early stopping and translator remain unchanged.

The batch contains exactly two seed-11 runs:

1. the unchanged ECP-6 positive control;
2. ECP7-B4-I with the added direct joint-collision loss.

All existing validity and development gates remain unchanged. Failure is
recorded without confirmatory test access. No alternative collision weight,
batch size, architecture or duration may be tried inside Batch 4.

## Batch 5 preregistration — Straight-through sender consensus

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026<br>
Configuration: `config/ecp7-b5-development.yaml`<br>
Raw configuration SHA-256: `3333e3e150e242b0984e79a2923ffe94d68cee7d004ae51f4914097917503db7`<br>
Effective configuration SHA-256: `4c2648efa2719d1cd3e0bdf96a2cbea21ea697280b74bbce82ba45371bbc0ed9`

Batch 4 regressed relative to Batch 3, so Batch 5 returns to the stronger
ECP7-B3-I base and does not retain the joint-collision loss. Batch 3's four
senders used substantially more of the hard code space than earlier batches,
but their complete-message agreement on the accessible meanings was only
approximately 2.47%. Batch 5 asks whether one shared factor-agnostic convention
helps generic receivers learn the protocol.

For the same training minibatch, the new objective compares each unordered
pair of senders. It averages their straight-through one-hot symbol disagreement
over inputs and message slots, then averages over all sender pairs:

`L_sender = mean_(a<b,x,s) [1 - <m_a(x,s), m_b(x,s)>]`

The forward value is zero when two senders emit the same hard symbol and one
when they differ. Gradients flow through the straight-through Gumbel estimator.
The objective receives no factor labels, factor identities, target slots,
desired symbols or privileged codebook. Per-sender hard utilization from Batch
3 remains active to oppose agreement through collapse.

The sender-consensus weight is fixed at `1.0` with a 400-step linear warmup.
This is the only Batch 5 addition. Architecture, task loss, Batch 3 hard
utilization, population, split, 14-bit channel, 5,000-step limit, early
stopping and translator remain unchanged. The rejected Batch 4 collision loss
is absent.

The batch contains exactly two seed-11 runs:

1. the unchanged ECP-6 positive control;
2. ECP7-B5-I with straight-through sender consensus on the Batch 3 base.

All existing validity and development gates remain unchanged. Failure is
recorded without confirmatory test access. No alternative consensus weight,
warmup, reduction, architecture or duration may be tried inside Batch 5.

## Batch 6 preregistration — Normalized factor minimax

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026<br>
Configuration: `config/ecp7-b6-development.yaml`<br>
Raw configuration SHA-256: `29fffcbfbc81c96e5765594ba67eea8143ff6d45f77defc8ce3acaf1a628b6f9`<br>
Effective configuration SHA-256: `3e54202ce906426a2a576c54ba9a8a4d7d65711dd8bc9376c2d6551244db046a`

Batch 5 increased sender agreement by creating a shared collapse, so Batch 6
returns to ECP7-B3-I and retains neither the Batch 4 collision loss nor the
Batch 5 sender-consensus loss. Across B3–B5, color and especially shape remain
the weak factors while size and texture are much easier. Batch 6 asks whether
the mean task objective lets the system neglect its hardest semantic dimension.

For every sender-receiver pair and training minibatch, let `CE_f` be the
cross-entropy for output factor `f` and `K_f` its number of values. The new
objective is:

`L_minimax = max_f [CE_f / log(K_f)]`

Dividing by the uniform-guess cross-entropy makes difficulty comparable across
16-way and 8-way factors. The original mean factor-reconstruction loss remains
active; the minimax term adds gradient pressure from the currently worst
relative factor. It uses the same supervised output factors already present in
the task, but receives no channel-slot identity, factor-to-slot assignment,
desired symbol or privileged codebook.

The minimax weight is fixed at `1.0` with a 400-step linear warmup. This is the
only Batch 6 addition. The Batch 3 straight-through utilization objective,
architecture, population, split, 14-bit channel, 5,000-step limit, early
stopping and translator remain unchanged.

The batch contains exactly two seed-11 runs:

1. the unchanged ECP-6 positive control;
2. ECP7-B6-I with normalized factor minimax on the Batch 3 base.

All existing validity and development gates remain unchanged. Failure is
recorded without confirmatory test access. No alternative minimax weight,
normalization, reduction, architecture or duration may be tried inside Batch 6.

## Batch 7 preregistration — Bounded parallel sender

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026<br>
Configuration: `config/ecp7-b7-development.yaml`<br>
Raw configuration SHA-256: `e885c6892b9da0b4af89dce96c00037a3813881499f20dd1b21e7a06ca4cf41d`<br>
Effective configuration SHA-256: `1ca8b5c618bc9193b60745040fa7f8a91e31a92e5786d2eab0597874938dee9e`

Batches 4–6 added three different training pressures to the autoregressive
Batch 3 sender, and every addition reduced its strongest result. Batch 7
therefore returns to the exact Batch 3 loss set and changes one architectural
assumption: symbols no longer depend sequentially on earlier symbols.

The bounded parallel sender embeds all four meaning factors, concatenates them,
and projects them into one shared joint context. Four independent output heads
read that same context simultaneously and are limited only by the registered
slot alphabet sizes `[16,16,8,8]`. Straight-through Gumbel sampling and the
Batch 3 hard-utilization loss remain unchanged.

The heads identify channel positions, not semantic factors. There is no
factor-specific projection, factor-local message head, recurrent state,
factor-to-slot binding, binding matrix, desired symbol or semantic codebook.
The generic sequence receiver and universal translator are unchanged. This
tests whether sequential generation itself was an optimization bottleneck;
it does not remove the fixed four-position channel frame.

The batch contains exactly two seed-11 runs:

1. the unchanged ECP-6 positive control;
2. ECP7-B7-I with bounded parallel generation and the Batch 3 loss set.

All existing validity and development gates remain unchanged. Failure is
recorded without confirmatory test access. No receiver change, hidden-size
change, extra loss, longer duration or alternative parallel architecture may be
tried inside Batch 7.

## Batch 8 preregistration — Algebraic context invariance

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026<br>
Configuration: `config/ecp7-b8-development.yaml`<br>
Raw configuration SHA-256: `3eac0d25bf636d4a1aeb6161ad479a4a78f0a3e88788a0274c154c21ff192829`<br>
Effective configuration SHA-256: `6e8f9ea0e968693bd9f67a4ca1180ab447c6e2d6c2fbc6b9f9a66582aa02fa3c`

Batch 7 greatly improved training exactness and code-space use, but those
distinctions did not compose across the held-out color-shape matching. Batch 8
retains the entire B7 architecture and loss set, then activates one existing
context-invariance objective that was previously disabled.

Every training quadruple contains meanings `A`, `B`, `A'`, and `B'`. The
transitions `A→A'` and `B→B'` change the same factor value in two different
contexts, and all four meanings belong to the training split. For relaxed
message distributions `m`, the objective is:

`L_alg = mean ||(m(A') - m(A)) - (m(B') - m(B))||²`

This encourages the same atomic semantic change to produce the same message
displacement regardless of the other factor values. It uses factor identities
only to construct matching transitions. It does not specify a target message,
symbol, channel slot, factor-to-slot binding or codebook.

The loss weight is fixed at `1.0` with an 800-step linear warmup, relaxed
temperature `1.0`, 32 quadruples per update and a deterministic pool of 8,192
training-only quadruples. These values match the dormant inherited settings;
only `enabled` and `weight` change from B7. The parallel sender, generic
receiver, hard-utilization loss, channel, split, training duration, selection
and translator remain unchanged.

The batch contains exactly two seed-11 runs:

1. the unchanged ECP-6 positive control;
2. ECP7-B8-I with algebraic context invariance on the B7 parallel sender.

All existing validity and development gates remain unchanged. Failure is
recorded without confirmatory test access. No alternative quadruple sampling,
weight, warmup, receiver, architecture or duration may be tried inside Batch 8.

## Batch 9 preregistration — Position-aware MLP decoder

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026<br>
Configuration: `config/ecp7-b9-development.yaml`<br>
Raw configuration SHA-256: `1ceeb80a3657078167d6d2ebacc1d57546d41ce53860148b9dfe7941b855c3fc`<br>
Effective configuration SHA-256: `d76fd03cfdffc97cdc4ded755868db93c6d77df62c14fb9fda3627fc2a3ad591`

Batch 7 messages changed when shape changed, and a fresh translator extracted
more shape information than the jointly trained receiver population. Batch 8's
sender-side context loss suppressed the stronger Batch 7 code. Batch 9 returns
to the complete B7 sender and loss set, then changes one shared decoder-family
assumption: messages are no longer compressed into a GRU final state.

The position-aware MLP decoder embeds each of the four received symbols with
one shared symbol embedding, concatenates the four embeddings in channel order,
projects that complete vector into one hidden representation, and applies four
factor-classification heads. Every factor head reads the same representation of
all message positions.

The decoder preserves positional information but has no recurrent order bias,
factor-specific input path, binding matrix, hard slot selection or
factor-to-slot assignment. The post-freeze universal translator uses the same
decoder family so transfer is evaluated without giving it a different
architectural advantage. Its isolation metadata is unchanged.

This decoder-family replacement is the only Batch 9 change. The B7 parallel
sender, Batch 3 hard-utilization loss, task loss, population, channel, split,
duration, selection and transfer training remain unchanged. The rejected Batch
8 algebraic objective is disabled as in B7.

The batch contains exactly two seed-11 runs:

1. the unchanged ECP-6 positive control;
2. ECP7-B9-I with the shared position-aware MLP decoder on the B7 sender.

All existing validity and development gates remain unchanged. Failure is
recorded without confirmatory test access. No sender, loss, hidden-size,
duration or alternative decoder variant may be tried inside Batch 9.

## Batch 10 preregistration — Extended optimization horizon

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026<br>
Configuration: `config/ecp7-b10-development.yaml`<br>
Raw configuration SHA-256: `ac1faed6538fcd7bcdd5dfe16a952ec317286629dcb3ecee7e9ec94e73939a2d`<br>
Effective configuration SHA-256: `415092b9215f7544f7a54f4b3d954a3a1e69ad90c43781c93dbcf8d3892cc76b`

Batch 9 selected its final registered checkpoint at step 5,000 while task loss
and exactness were still improving. It used about 11,000 high-entropy messages,
its largest collision bucket contained only 8–9 meanings, and no factor remained
near chance. Batch 10 therefore tests one explanation: the B9 design was
underoptimized at the registered stopping horizon.

ECP7-B10-I keeps the complete B9 architecture, sender, position-aware receiver,
translator, losses, optimizer, batch size, learning rate, data, evaluation
interval, channel, thresholds and seed. It changes only the population
optimization horizon and its associated checkpoint-selection window:

- maximum population steps increase from 5,000 to 15,000;
- minimum selection steps increase from 2,000 to 5,000;
- early-stopping patience increases from 1,600 to 3,000 steps;
- the original geometric temperature schedule remains exactly unchanged from
  steps 1 through 5,000, then holds its registered final value of `0.8`.

Translator training remains unchanged. The schedule hold prevents the longer
horizon from also becoming a slower-annealing intervention. Smoke runs are
mechanical only and may not authorize tuning.

The batch contains exactly two seed-11 runs:

1. the unchanged ECP-6 positive control;
2. ECP7-B10-I with the extended B9 population optimization horizon.

All existing validity and development gates remain unchanged. Failure is
recorded without confirmatory test access. No alternative horizon, patience,
annealing schedule, architecture, loss, optimizer or seed may be tried inside
Batch 10.

## Batch 11 preregistration — Code-utilization weight decay

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026<br>
Configuration: `config/ecp7-b11-development.yaml`<br>
Raw configuration SHA-256: `6316b7361a7c4947089b7e33d189a80c4e37739650c75e961fcec7628b812c70`<br>
Effective configuration SHA-256: `db05737365381f73afada0462de1f6ae111b92b96589364e29f05befac701519`

Batch 10 passed the translator threshold and reached 72.98% validation, but
validation plateaued after approximately step 12,000. At the selected final
checkpoint, the unweighted utilization term had magnitude `0.7548` while task
loss was `0.0765`. The code nevertheless retained 12,358–12,906 unique messages,
13.48–13.57 bits of entropy, sender agreement above 92%, and collision buckets
of at most four meanings.

Batch 11 tests one explanation: after the high-entropy code is established,
full utilization pressure dominates the remaining task objective and prevents
the last color and texture distinctions from resolving.

ECP7-B11-I keeps the complete B10 model, data, optimizer, duration, checkpoint
selection, temperature schedule, translator, task loss and utilization formula.
It changes only the coefficient applied to that existing utilization term:

- the original warmup and weight `1.0` are unchanged through step 5,000;
- the coefficient then decays linearly from `1.0` at step 5,000 to `0.1` at
  step 15,000;
- the final nonzero coefficient preserves an anti-collapse signal while making
  its expected weighted magnitude comparable to B10's remaining task loss.

This schedule reproduces every B10 optimization setting and weight through the
original B9 horizon. Smoke runs are mechanical only and may not authorize
tuning.

The batch contains exactly two seed-11 runs:

1. the unchanged ECP-6 positive control;
2. ECP7-B11-I with utilization-weight decay on the B10 base.

All existing validity and development gates remain unchanged. Failure is
recorded without confirmatory test access. No alternative final weight, decay
shape, decay boundary, duration, architecture, loss, optimizer or seed may be
tried inside Batch 11.

## Batch 12 preregistration — Deep position-aware decoder

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026<br>
Configuration: `config/ecp7-b12-development.yaml`<br>
Raw configuration SHA-256: `4cc37488453b756fb43b4782d0e3e93cf051815a367d1852047fcc34fa29d5ce`<br>
Effective configuration SHA-256: `798a6380ab144e5db63c8177d3dd70edf76e66b660b3cbb355f5beabe86b27b2`

Batch 11 showed that reducing late utilization pressure worsened task accuracy,
code use and sender agreement. Batch 10 therefore remains the base. Its shared
one-hidden-layer decoder and independently trained translator both retained a
texture weakness, while color was the other residual population error. Batch 12
tests whether the generic decoder is still too shallow for the entangled code.

ECP7-B12-I returns to the complete B10 training and loss schedule. It keeps the
shared symbol embedding, flattened four-position input and first generic hidden
projection, then adds exactly one second `hidden_dim × hidden_dim` projection
with `tanh`. All four factor heads read that same second shared representation.
The isolated translator uses the identical deeper family.

The decoder still has no factor-specific input path, factor-specific hidden
projection, binding matrix, slot selector or hard factor-to-slot assignment.
Hidden width, sender, losses, optimizer, data, 15,000-step duration, original
5,000-step temperature annealing, selection window and thresholds remain
unchanged from B10. Smoke runs are mechanical only and may not authorize
tuning.

The batch contains exactly two seed-11 runs:

1. the unchanged ECP-6 positive control;
2. ECP7-B12-I with the deeper shared position-aware receiver and translator.

All existing validity and development gates remain unchanged. Failure is
recorded without confirmatory test access. No alternative depth, activation,
width, residual connection, sender, loss, duration, optimizer or seed may be
tried inside Batch 12.

## Batch 13 preregistration — Deep bounded-parallel sender

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026<br>
Configuration: `config/ecp7-b13-development.yaml`<br>
Raw configuration SHA-256: `9b57b1ae0387483594a8171a1535c0e9a82fc988708d74d0300a775747ea7210`<br>
Effective configuration SHA-256: `661a0e286eb986a1b907df5e30dc416a1aefd5e5263056ccc12092c6beb3002d`

Batch 12 rejected extra receiver and translator depth. Batch 10 remains the
base, but its bounded parallel sender still constructs all four message slots
from one shallow shared context. Batch 13 tests the symmetric remaining capacity
hypothesis: the sender context is too shallow to construct the residual color
and texture distinctions.

ECP7-B13-I returns to the complete B10 model, receiver, translator, training and
loss schedule. It keeps the shared factor embeddings and first generic context
projection, then adds exactly one second `hidden_dim × hidden_dim` projection
with `tanh`. All four slot heads read that same second shared context.

The sender still has no factor-specific hidden path, binding matrix, hard slot
selector or factor-to-slot assignment. Hidden width, receiver, translator,
losses, optimizer, data, 15,000-step duration, original 5,000-step temperature
annealing, selection window and thresholds remain unchanged from B10. Smoke
runs are mechanical only and may not authorize tuning.

The batch contains exactly two seed-11 runs:

1. the unchanged ECP-6 positive control;
2. ECP7-B13-I with the deeper shared bounded-parallel sender.

All existing validity and development gates remain unchanged. Failure is
recorded without confirmatory test access. No alternative sender depth,
activation, width, residual connection, decoder, loss, duration, optimizer or
seed may be tried inside Batch 13.

## Batch 14 preregistration — Late learning-rate decay

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026<br>
Configuration: `config/ecp7-b14-development.yaml`<br>
Raw configuration SHA-256: `867e42a0a8c530a4bd1d42be68f2846b66ce368644e993be67f82b39c8caec04`<br>
Effective configuration SHA-256: `f44a36695c59bd532d7372c6cb3fb5b6eeed06b5bc10f04e96603926f7a9f37e`

Batches 12 and 13 rejected additional generic decoder and sender depth. Batch
11 rejected reducing late utilization pressure. Batch 10 remains the base: it
continued to improve late, but its validation score fluctuated around a plateau
while AdamW retained learning rate `0.001` through step 15,000.

Batch 14 tests one optimization-stability hypothesis: smaller late parameter
updates can refine the established high-entropy code without changing its
architecture, temperature or objective balance.

ECP7-B14-I keeps the complete B10 model, losses, optimizer type, data,
temperature schedule, duration, selection window and translator. Learning rate
remains exactly `0.001` through step 5,000, then decays linearly to `0.0001` at
step 15,000. No other AdamW or training setting changes.

This reproduces the full B9 trajectory before the learning-rate schedules
diverge. Smoke runs are mechanical only and may not authorize tuning.

The batch contains exactly two seed-11 runs:

1. the unchanged ECP-6 positive control;
2. ECP7-B14-I with late learning-rate decay on the B10 base.

All existing validity and development gates remain unchanged. Failure is
recorded without confirmatory test access. No alternative final rate, decay
shape, decay boundary, architecture, loss, duration, optimizer or seed may be
tried inside Batch 14.

## Batch 15 preregistration — 30,000-step optimization horizon

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026<br>
Configuration: `config/ecp7-b15-development.yaml`<br>
Raw configuration SHA-256: `2b4ed0979cb1f6a6aac0409e2624bf982fd020306492706f4aa0e6b3a8c9d15d`<br>
Effective configuration SHA-256: `d60b8a9aebe75514560b35790a3de9674990724fff0a9c52283c91ff429a487b`

Batch 10 selected its final 15,000-step checkpoint. Batch 14 showed that
decaying late learning rate harms validation, while Batches 11–13 rejected loss
removal and added capacity. Batch 15 therefore tests one remaining optimization
hypothesis: the constant-rate B10 trajectory needs more time.

ECP7-B15-I keeps the complete B10 architecture, sender, receiver, translator,
losses, AdamW settings, data, temperature schedule, evaluation cadence and
thresholds. It changes only the population optimization horizon and associated
selection window:

- maximum population steps increase from 15,000 to 30,000;
- minimum selection steps increase from 5,000 to 15,000;
- early-stopping patience increases from 3,000 to 5,000 steps;
- learning rate remains constant at `0.001`;
- temperature still reaches `0.8` at step 5,000 and holds thereafter.

Translator training remains unchanged. Smoke runs are mechanical only and may
not authorize tuning.

The batch contains exactly two seed-11 runs:

1. the unchanged ECP-6 positive control;
2. ECP7-B15-I with the extended B10 population optimization horizon.

All existing validity and development gates remain unchanged. Failure is
recorded without confirmatory test access. No alternative horizon, patience,
learning rate, architecture, loss, temperature, optimizer or seed may be tried
inside Batch 15.

## Batch 16 preregistration — Late normalized factor minimax

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026 at 14:07:11 UTC<br>
Configuration: `config/ecp7-b16-development.yaml`<br>
Raw configuration SHA-256: `caef16ec93d0a9424fd3c4af46a987aad63118f24e57e77e9d51cc2eb77e073b`<br>
Effective configuration SHA-256: `b40f35ab2f03fa8450805908713b4b9a59bbc060c38a4e68e4e3c5be2d2b4efb`

Batch 15 established the first weak-structure protocol to pass validation and
universal-translator thresholds together. Its remaining exact-match errors are
concentrated in the weakest decoded factor after a high-entropy protocol is
already established. Batch 16 tests whether late worst-factor emphasis can
resolve those residual collisions without disrupting the successful early
trajectory.

ECP7-B16-I keeps the complete Batch 15 architecture, base task and utilization
losses, AdamW settings, data, temperature schedule, 30,000-step horizon,
selection window, translator and thresholds. It adds the existing normalized
factor-minimax term with one delayed coefficient schedule:

- weight is exactly `0` through step `15,000`;
- weight increases linearly from `0` to `1.0` over steps `15,000–20,000`;
- weight remains `1.0` from step `20,000` through step `30,000`.

The minimax formula is unchanged from Batch 6: it selects the largest factor
cross-entropy after normalization by the uniform-guess entropy for that factor.
Unlike Batch 6, no minimax gradient is present while the base high-entropy code
is forming. The original mean task loss remains active throughout.

The batch contains exactly two seed-11 runs:

1. the unchanged ECP-6 positive control;
2. ECP7-B16-I with late normalized factor minimax on the complete B15 base.

All existing validity and development gates remain unchanged. The intervention
fails if any train, validation, translator, injectivity, channel-integrity or
sealed-test requirement fails. No alternative start step, warmup, weight,
normalization, duration, architecture, utilization, optimizer, data, translator
or seed may be tried inside Batch 16. Failure is recorded without confirmatory
test access.

## Batch 17 preregistration — Late global collision-pair replay

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026 at 14:35:00 UTC<br>
Configuration: `config/ecp7-b17-development.yaml`<br>
Raw configuration SHA-256: `81bc1c36f7fd19afdecd61eb917fe41925db8266d8ac8b2bc96e70178e39c412`<br>
Effective configuration SHA-256: `70921261774f38f5ca22f122d05a2b9f1f0bc7c9ca6ea4c327097b7619715d5b`

Batch 16 showed that late semantic factor reweighting slightly improves
texture but disrupts color generalization and does not make the code injective.
Batch 17 therefore returns to the complete Batch 15 base and targets only the
remaining complete-message collisions. It revisits the Batch 4 question after
a mature high-entropy protocol exists, but replaces Batch 4's sparse random
minibatch signal with deterministic training-codebook mining.

At step 15,000 and every 200-step registered evaluation boundary thereafter,
each sender encodes all 14,336 training meanings with hard argmax symbols. For
each complete message, every unordered pair of distinct training meanings that
shares that message enters that sender's replay bank. Validation meanings,
factor labels, factor identities and validation outcomes never enter mining.

For every subsequent population update, a separate seed-derived generator
samples 32 mined pairs with replacement per sender. The sender produces relaxed
message distributions at temperature `1.0`. For pair `(x,y)`, the new loss is
the probability that all four relaxed symbols agree:

`L_replay(x,y) = product_s <p_s(x), p_s(y)>`

The loss averages over sampled pairs and senders. It specifies no desired
symbol, target slot, semantic codebook or factor-to-slot binding. Reducing it
requires at least one message position to distinguish each replayed pair.

ECP7-B17-I keeps every Batch 15 architecture, task and utilization loss,
optimizer, data, temperature schedule, 30,000-step duration, selection window,
translator and threshold. Collision-replay weight is exactly `0` through step
15,000, rises linearly to `1.0` over steps 15,000–20,000, and then holds. The
separate replay sampler does not alter the registered task-batch sampler. The
trajectory through step 15,000 must therefore match Batch 15 exactly.

The batch contains exactly two seed-11 runs:

1. the unchanged ECP-6 positive control;
2. ECP7-B17-I with late global collision-pair replay on the complete B15 base.

All existing validity and development gates remain unchanged. The intervention
fails if any train, validation, translator, injectivity, channel-integrity or
sealed-test requirement fails. No alternative mining source, refresh interval,
pair batch size, temperature, weight, warmup, architecture, duration, optimizer,
data, translator or seed may be tried inside Batch 17. Failure is recorded
without confirmatory test access.

## Batch 18 preregistration — Attenuated collision replay

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026 at 14:53:31 UTC<br>
Configuration: `config/ecp7-b18-development.yaml`<br>
Raw configuration SHA-256: `a9da48a2c76fd01a9f2889050c347ed9fcf616389297424f156e9f2d8489e59f`<br>
Effective configuration SHA-256: `21d76380640738ee98ddbdb7ae88c6a1d3185add860b96f1fe9c5c83a782d757`

Batch 17 established that global training-codebook mining produces a usable
collision signal and modestly improves hard code use. Its replay weight rose to
`0.24` at the selected checkpoint, where replay loss `0.83844` contributed
approximately `0.201` to the objective versus task loss `0.07453`. Higher
weights then caused collision churn, validation regression and early stopping.

Batch 18 tests only whether coefficient scale caused that failure. ECP7-B18-I
inherits the complete B17 mining algorithm, training-only pair source,
seed-derived sampler, 32-pair sender batches, 200-step refresh interval, relaxed
temperature `1.0`, architecture, base losses, optimizer, data, 30,000-step
duration, selection window, translator and thresholds. The sole change is:

- replay weight remains `0` through step `15,000`;
- replay weight rises linearly to `0.1` over steps `15,000–20,000`;
- replay weight remains `0.1` through step `30,000`.

For an initially near-one replay loss, full weight `0.1` is comparable to the
remaining B15 task-loss scale instead of several times larger. The task-batch
trajectory and all random sampling through step 15,000 must again match B15
exactly.

The batch contains exactly two seed-11 runs:

1. the unchanged ECP-6 positive control;
2. ECP7-B18-I with attenuated late global collision-pair replay.

All existing validity and development gates remain unchanged. The intervention
fails if any train, validation, translator, injectivity, channel-integrity or
sealed-test requirement fails. No alternative coefficient, schedule, mining
source, pair sampler, refresh, temperature, architecture, duration, optimizer,
data, translator or seed may be tried inside Batch 18. Failure is recorded
without confirmatory test access.

## Batch 19 preregistration — Bounded collision-replay pulse

Status: **preregistered for sealed development**<br>
Preregistered: July 18, 2026 at 15:15:36 UTC<br>
Configuration: `config/ecp7-b19-development.yaml`<br>
Raw configuration SHA-256: `dab2cd0dadbadb47a10e2c45a720611dc91d140d3783f0ca1a537e4e8a8549c0`<br>
Effective configuration SHA-256: `cbd144a5fce451315a7d5fb322a11f2f29c32514fc22fbe06f46285aef677d13`

Batch 18 confirmed that replay at task-loss scale avoids B17's early collapse,
but validation peaked at step 22,400 and then regressed while weight `0.1`
remained active. Batch 19 tests whether replay is useful as a bounded codebook
diversification pulse rather than a permanent late objective.

ECP7-B19-I inherits the complete Batch 18 architecture, training-only mining,
seed-derived pair sampler, 32-pair sender batches, 200-step refresh interval,
relaxed temperature, base losses, optimizer, data, duration, selection,
translator and thresholds. It is identical to B18 through step 20,000. The sole
change is a coefficient decay:

- replay weight remains `0` through step `15,000`;
- replay weight rises linearly to `0.1` at step `20,000`;
- replay weight falls linearly to `0` over steps `20,000–25,000`;
- replay weight remains `0` through step `30,000`.

Training-codebook collision mining continues at evaluation boundaries after
step 25,000 for diagnostics, but contributes no gradient and consumes no replay
sampler draws. The final optimization phase therefore contains only the B15
task and utilization objectives. The complete trajectory through step 20,000
must match B18 exactly.

The batch contains exactly two seed-11 runs:

1. the unchanged ECP-6 positive control;
2. ECP7-B19-I with one bounded global collision-replay pulse.

All existing validity and development gates remain unchanged. The intervention
fails if any train, validation, translator, injectivity, channel-integrity or
sealed-test requirement fails. No alternative decay, endpoint, mining, pair
sampler, architecture, base loss, optimizer, duration, data, translator or seed
may be tried inside Batch 19. Failure is recorded without confirmatory test
access.
