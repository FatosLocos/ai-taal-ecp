# Research Design ECP-3

Status: **frozen before confirmatory test access**<br>
Frozen: July 18, 2026 02:07:44 UTC<br>
Intervention configuration: `config/ecp3.yaml`<br>
SHA-256: `2cab56d55a0364a218755d8815a7efaf36292896a125fdc4c593150c19b93f6e`<br>
Control configuration: `config/ecp3-control.yaml`<br>
SHA-256: `9569c5f5cef10681f4fd02ba0c70907910246d14802836ffe5bf0d2c5f0edcfa`

## Question

Does a hard injectivity condition for atomic factor codes remove the local symbol collisions of ECP-2 and thereby create a robust compositional population protocol?

## Model

Four independent senders communicate with four independent receivers using exactly four symbols from a vocabulary of sixteen. Each sender learns two types of arbitrary discrete assignments:

1. a free one-to-one permutation from the four factors to the four message slots;
2. per factor a free injective assignment of factor values to symbols.

A Sinkhorn approach provides the gradients; transmission and evaluation use only a hard factor-slot permutation and hard unique symbols. The intervention aligns the soft slot and atomic assignments across channels. The paired control has exactly the same injective architecture, split, seeds, and training budget, but both consensus losses are disabled.

No slot or symbol is assigned a meaning in advance. It is, however, specified in advance that each factor uses one position and that two values of the same factor may not share a symbol. ECP-3 therefore uses an explicit factorized inductive bias; it is not evidence of unconstrained language emergence.

## New sealed split

The world remains `8 × 8 × 4 × 4 = 1,024` meanings. ECP-3 uses:

- 768 training meanings;
- 128 meanings from one fully withheld color-shape matching for selection;
- 128 meanings from a second fully withheld matching for the one-time confirmatory test.

All ECP-0, ECP-1, and ECP-2 test pairs are excluded. Out of extra caution, the eight ECP-2 validation pairs were also excluded because they influenced the architecture choice. The new split has SHA-256 `91d6439fada82b1384a8d03f7cc1f5602091f794477be31c179c5a26e1b0464b`.

## Predefined criteria

A seed is classified as strong evidence when it achieves:

- at least 97% known mean exact reconstruction;
- at least 95% for the worst known sender-receiver pair;
- at least 80% average exact reconstruction on new test pairs;
- at least 70% exact reconstruction by the universal translator.

The population outcome is strong when at least four of five seeds are strong. Five predefined seeds (`11, 23, 37, 53, 71`) are used. Results are also reported as paired differences from the control, including the exact one-sided sign-flip test across all `2^5 = 32` sign combinations.

The model is considered a usable ECP base model if the intervention produces at least four strong seeds, passes all channel checks and contains no artifact integrity error. A control effect is informative about consensus, but not an additional condition for the usefulness of the model itself.

## Integrity checks

- The test split is not used for training, early stopping, or selection.
- Senders and receivers do not share parameters, embeddings or state.
- Final evaluation runs in separate processes; receivers receive only symbol matrices.
- All messages and reconstructions are schema-validated and logged.
- Shuffling must remain within 1% exact.
- Consistent symbol renaming should preserve all predictions.
- All prewritten artifacts are hashed and rechecked upon completion.
