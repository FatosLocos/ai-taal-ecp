# Development log ECP-4

The confirmatory ECP-4 test split remained technically sealed throughout development.

## Implementation

ECP-4 adds two prespecified components:

1. `MinimalPermutationSlotSender`: a freely learned hard permutation for each factor within a local alphabet of exactly the required size;
2. `FactorizedPermutationSlotReceiver`: a freely learned but hard-isolated message slot for each factor output.

The transport metadata, configuration validation, and episode schemas now support protocol-specific bit lengths. Each episode is also checked against the active configuration for exact message length, bit length, and symbol range.

## Technical verification

The tests verify that:

- the four local codebooks exactly `8×8`, `8×8`, `4×4` and `4×4` are hard permutations;
- each symbol actually sent falls within the local factor alphabet;
- a factor output remains unchanged when an unselected slot changes;
- minimum sender and factor receiver run separately through checkpoints and isolated processes;
- `3+3+2+2 = 10` bits exactly equals the source entropy;
- the explicit validation and test splits use exactly the final sixteen unused pairs.

All 34 tests pass.

## Sealed development

Develop run: `runs/ecp4-development/20260718T060943Z-ecp4-development`<br>
Seed: 11

| Metric | Outcome |
|---|---:|
| Known mean | 100.0% |
| Worst known sender-receiver pair | 100.0% |
| Fully new validation pairs | 100.0% |
| Worst validation pair | 100.0% |
| Universal translator on validation | 100.0% |
| New receiver, 32 examples | 100.0% |
| New receiver, 128 examples | 100.0% |
| New receiver, 512 examples | 100.0% |
| New receiver, 768 examples | 100.0% |

All four channels chose the same internally determined slot order `[size, texture, color, shape]`. Message agreement between every sender pair is 100%. Across the 896 training and validation meanings, each sender uses 896 unique messages without collisions and has topographic similarity 1.0.

The best condition was already selected at step 400. No 12-bit intermediate variant is therefore required: the direct 10-bit variant meets every sealed-development criterion.

## Conclusion

The 10-bit variant is frozen without further modification. The paired control retains the same factorized receiver but uses the 16-bit injective ECP-3 channel. No confirmatory test pair was evaluated before this choice.
