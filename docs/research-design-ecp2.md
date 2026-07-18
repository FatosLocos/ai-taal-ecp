# Research Design ECP-2 — Algebraically Consistent Emergent Protocol

Status: Frozen for confirmatory execution on July 18, 2026 at 01:31:00 UTC<br>
Parent experiment: ECP-1<br>
Intervention configuration: `config/ecp2.yaml`<br>
Control configuration: `config/ecp2-control.yaml`

## Rationale

ECP-1 showed that four independent senders and four independent receivers can stabilize a shared protocol. Nevertheless, population generalization decreased from 15.9% in ECP-0 to 10.1%. Simply providing multiple communication partners is therefore insufficient.

This result is consistent with existing research. Lee likewise found that having one sender broadcast to multiple receivers does not automatically produce greater compositionality ([EMNLP 2024](https://aclanthology.org/2024.emnlp-main.1157/)). Rita et al. attribute poor emergent generalization partly to overfitting through co-adaptation ([NeurIPS 2022](https://openreview.net/forum?id=qqHMvHbfu6)). Chaabouni et al. show that more compositional protocols are easier to transfer, but that ordinary generalization pressures do not necessarily create compositionality ([ACL 2020](https://aclanthology.org/2020.acl-main.407/)).

## Central hypothesis

> A protocol generalizes better when the same atomic change in meaning in different contexts causes a similar change in the internal message distribution.

For a factor change `A → A'` and the same change in a different context `B → B'`, ECP-2 minimizes:

`||(M(A') − M(A)) − (M(B') − M(B))||²`

`M` is the distribution over the four positions and sixteen symbols learned by the sender. The final communication remains exactly the same hard 16-bit channel as in ECP-1.

## What is not pre-programmed

- No symbol is given a meaning in advance.
- No message position is assigned to color, shape, size, or texture.
- The four channels do not share any parameters or embeddings.
- The regularization does not prescribe which message represents a meaning.
- The receivers only see the symbols produced and not the algebraic tetrads.

The experimental pressure does use the known factor structure of the artificial world. This is an explicit inductive bias and must be taken into account in the interpretation. The experiment therefore tests whether agents discover a useful discrete protocol within such a general consistency pressure, not whether compositionality arises without any environmental structure.

## Algebraic training quads

Each quad contains `A`, `B`, `A'` and `B'`:

1. `A → A'` changes exactly one factor value;
2. `B → B'` changes exactly the same source value to the same target value;
3. the other factors form different contexts;
4. all four meanings must be in the training set;
5. validation and test meanings are never used as regularization input.

This allows the sender to learn, for example, that one color change behaves context-invariant, without having to determine in advance which symbol or which position carries that change.

## Two independent compositional holdouts

ECP-2 corrects a methodological weakness in ECP-0 and ECP-1. The old validation sets contained separate meanings whose color-shape pairs already occurred in training. They therefore mainly measured interpolation.

ECP-2 reserves two complete and mutually disjoint matchings:

- 128 meanings from eight color-shape pairs form the compositional validation set;
- 128 meanings from eight other pairs form the sealed compositional test set;
- the remaining 768 meanings constitute the training;
- all sixteen previously opened ECP-0 and ECP-1 test pairs have been excluded from both new matchings.

The validation set may be used for model selection. The test set is not coded, decoded, or evaluated during development.

## Development comparison

With seed 11, up to four preselected weights are compared:

| Variant | Algebraic weight |
|---|---:|
| Control | 0 |
| Light | 0.25 |
| Medium | 1.0 |
| Strong | 4.0 |

The chosen variant is the variant with the highest exact compositional validation performance, provided that known meanings achieve at least 97% on average and at least 95% for the worst pair. With a difference of less than two percentage points, the lower weight wins.

After this choice, architecture, weight, training duration, five seeds and outcome thresholds are frozen. The control and intervention use exactly the same split, seeds, population architecture and training budget in the confirmatory phase.

## Confirmatory requirements for a developed ECP-2 model

Strong evidence required in at least four of five intervention runs:

- at least 97% known reconstruction on average;
- at least 95% for the worst known sender-receiver pair;
- at least 80% exact reconstruction on the sealed compositional test;
- at least 70% for one independent universal translator;
- passed channel isolation, shuffling and symbol permutation checks.

In addition, the intervention mean must exceed the paired-control mean on the same test split. A score above the ECP-1 reference alone is insufficient.

## Continue in case of a negative development outcome

If no algebraic weight clearly improves the compositional validation, the test set is not opened. The next development variant will then be generation transmission: agents are replaced periodically and new agents are given a limited transmission bottleneck. This follows the positive results on iterative and generational learning from [Guo et al.](https://arxiv.org/abs/1910.05291) and [Cogswell et al.](https://openreview.net/forum?id=r1gzoaNtvr&noteId=SJl3j-ScjB).

## Frozen final variant

The algebraic intervention failed and cultural transmission improved compositional validation to 19.9%, but not to the preselected performance threshold. The final candidate therefore uses the transparently registered permutation slot architecture with meaning-free binding consensus:

- each sender internally chooses one of 24 factor slot permutations;
- no concrete permutation, symbol meaning, or symbol code is specified in advance;
- four independent channels are given consensus weight 5.0 on their soft binding matrices;
- the control group uses exactly the same slot architecture without consensus pressure;
- both arms use the same five seeds, split, training budget, translator and transfer curve;
- the sealed test will not be opened until both effective configurations have been captured.

The strong development variant achieved 100% known, 97.0% compositional validation and 95.3% universal translator validation. This development performance is not a confirmatory result.
