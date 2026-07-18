# Research Design ECP-4 — Theoretically Minimal 10-Bit Code

Status: **frozen before confirmatory test access**<br>
Frozen: July 18, 2026 at 06:11:20 UTC<br>
Intervention configuration: `config/ecp4.yaml`<br>
SHA-256: `c335483534248eda96094ceea7ff49cd3270256fdfff6e01824654a886bc6e17`<br>
Control configuration: `config/ecp4-control.yaml`<br>
SHA-256: `84c1024d49c9d2aff34fb56dbcabf41c9af76dc2ba478760e42d1098afa777c8`

## Question

Can the ECP protocol be compressed from 16 to exactly 10 bits — the source lower bound of the uniform world — without losing compositional generalization, population compatibility, or universal translation?

## Why 10 bits is the minimum

The world contains `8 × 8 × 4 × 4 = 1024 = 2^10` equiprobable meanings. Any unambiguous code therefore requires at least `log2(1024) = 10` bits.

ECP-4 uses four local factor alphabets:

| Factor | Values | Bits |
|---|---:|---:|
| Color | 8 | 3 |
| Shape | 8 | 3 |
| Size | 4 | 2 |
| Texture | 4 | 2 |
| **Total** | **1024 combinations** | **10** |

Each sender freely chooses a permutation from factor to slot and within each factor a free permutation from value to local symbol. The semantics of slots and symbols are therefore not stated in advance. However, the minimum factor structure has been imposed as an architectural bias.

## Factor-isolated receiver

ECP-3 had one outlier in which a generic GRU memorized color and shape as a joint contextual rule. ECP-4 allows each factor output to read exactly one freely learned slot. A change in another slot cannot affect that output by construction. Each receiver learns its own hard slot permutation and shares no parameters with senders or other receivers.

The universal translator and new transfer receivers use the same factor-isolated architecture, but are trained independently only after freezing the sender protocol.

## Last independent color-shape split

After ECP-0 through ECP-3, 48 of the 64 color-shape pairs were used as validation or testing. The remaining sixteen pairs form exactly two perfect matchings. They are explicitly divided, without sampling, between:

- eight development validation pairs;
- eight sealed confirmatory test pairs.

The split has SHA-256 `0f8b5505e1a3dceb0c87005a32d6bcffd39c66a6bb4246102617c92a8915b180`. After unsealing this test, all 64 color-shape pairs were used at least once as a validation or test; further research should therefore use a new world or an orthogonal holdout family.

## Paired 16-bit control

The control uses exactly the same split, five seeds, factor-isolated receivers, consensus losses, training budget, and evaluation. Only the sender code and channel differ:

- intervention: local alphabets `8,8,4,4`, exactly 10 bits;
- control: four global symbols of sixteen, 16 bits.

As a result, the comparison measures whether theoretically minimal compression causes performance degradation within the same enhanced decoder architecture.

## Predefined criteria

A seed is classified as strong evidence when it achieves:

- at least 97% known mean exact reconstruction;
- at least 95% for the worst known sender-receiver pair;
- at least 80% average exact reconstruction on new test pairs;
- at least 70% exact reconstruction by the universal translator.

ECP-4 is considered a successful minimum model when:

1. at least four of five intervention seeds are strong;
2. the intervention uses exactly 10 channel bits;
3. all sender codes are injective and collision-free;
4. all channel and integrity checks pass;
5. the average test accuracy is not more than one percentage point below the paired 16-bit check.

Five seeds (`11,23,37,53,71`) and an exact paired sign-flip test across 32 sign combinations are predefined. The ideal result is five error-free seeds, but the formal success rule remains four of five for consistency with ECP-3.
