# Development log ECP-3

The confirmatory ECP-3 test split remained sealed throughout all work described below.

## Failure mode in ECP-2

ECP-2 learned a shared factor-slot binding within each seed, but only two of five seeds met every threshold. The weak seeds no longer had a structural slot-binding problem; they remained stuck with non-unique or insufficiently stable symbols for individual factor values. As a result, even known meanings in seeds 37 and 53 could not be fully distinguished.

## Preselected repair

ECP-3 replaces the neural slot heads with a freely learned injective symbol allocation for each factor. The sender may still choose any symbol for each value, but two values within the same factor may not coincide. The existing free factor-slot permutation is retained. In addition to binding consensus, the same meaning-free population consensus is applied to the soft atomic codebooks.

One development seed has been used: seed 11. The training budget, population size, receiver architecture and channel capacity are kept equal to ECP-2.

## Result on training and compositional validation

| Metric | Outcome |
|---|---:|
| Known mean | 100.0% |
| Worst known sender-receiver pair | 100.0% |
| Fully new validation pairs | 100.0% |
| Worst validation pair | 100.0% |
| Universal translator on validation | 100.0% |
| New receiver with 128 examples | 94.3% |
| New receiver with 512 examples | 99.8% |
| New receiver with 768 examples | 100.0% |

All four channels chose the same slot order `[shape, texture, size, color]`. Their exact atomic codebooks did not match everywhere, but every code remained injective and all sixteen sender-receiver links decoded both dialect variants flawlessly.

For each of the four channels, across the 896 training and validation meanings:

- 896 unique messages and zero collisions;
- message entropy of `9.807` bits, equal to the source entropy of this subset;
- mean message distance of exactly one for a one-factor meaning change;
- full concentration of such a change in one position;
- topographic Spearman correlation of `1.0`.

The technical smoke test, checkpoint cycle, isolated processes, shuffled-message control, and consistent symbol permutation all passed. All 29 tests passed.

## Conclusion

No further refinement is allowed before the confirmatory test. The development variant achieves every goal without opening the sealed split and is therefore frozen unchanged as the ECP-3 intervention. An otherwise identical control disables only slot-binding and atomic-code consensus.

Development run: `runs/ecp3-development/20260718T020325Z-ecp3-development`.
