# Research Design ECP-5 — Robust Protocol Induction

Status: **frozen before confirmatory test access**<br>
Frozen: July 18, 2026 at 06:27:09 UTC<br>
Intervention configuration: `config/ecp5.yaml`<br>
SHA-256: `5e4bf30517e0edbe96d5f0b5c666b9b03f6fe8366fd80bcc5ab455d615d11b8b`<br>
Control configuration: `config/ecp5-control.yaml`<br>
SHA-256: `4ee2f8ff314acd6f042c66fd4e81b6beb0c360b979f585f5d00b0e9df6ed2582`

## Question

Can a new universal reader reliably induce the arbitrary slot grammar of the perfect 10-bit protocol by precisely calibrating the discrete factor-slot permutation from labeled training messages?

## Intervention

The empirical mutual information is calculated for each combination of four factors and four slots. There are only `4! = 24` valid one-to-one permutations. The intervention exhaustively chooses the permutation with the highest total information and freezes that binding before training the four symbol decoders.

The procedure:

- only reads messages and meaning labels from the allowed training set;
- does not open validation or test meanings;
- does not read sender parameters, codebooks, or hidden state;
- does not prescribe symbol meanings;
- only determines which message position statistically belongs to which factor.

The paired control relearns the same binding with the existing straight-through gradients. All other code, data, seeds, and training budgets are identical.

## Orthogonal sealed test

Because all color-shape pairs had been used for validation or testing by the end of ECP-4, ECP-5 preregisters a size-texture holdout instead:

- 512 training meanings;
- 256 meanings from four fully withheld validation pairs;
- 256 meanings from four other sealed test pairs.

Color and shape vary completely within each retained pair. The split SHA-256 is `cc487fd9042c5190bee93278c4be5180363f46a46d0e8af2f9d7d75a4f173140`.

## Criteria

The ECP-3/4 thresholds continue to apply per seed: 97% known average, 95% for the worst known pair, 80% compositional test accuracy and 70% universal translation accuracy.

ECP-5 is passed when:

1. at least four of five intervention seeds are strong;
2. the average population and translation accuracy are each at least 95%;
3. each message uses exactly 10 bits and all codes are collision-free;
4. all channel and artifact checks pass;
5. the calibrated translator performs better than the uncalibrated control in at least four of five seeds or ends up equal at 100%.

Seeds `11,23,37,53,71` and the exact paired sign-flip test were recorded before test access.
