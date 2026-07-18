# Development log ECP-5

The ECP-5 test set remained sealed during development.

## Cause analysis ECP-4

All five 10-bit populations communicated without error. However, four universal translators remained at 9.4–12.5%. Their symbol heads were not the problem: the hard receiver binding assigned factors to the wrong slots. The same error also occurred twice in the 16-bit control.

## Exact calibration

The new procedure calculates a `4×4` matrix of empirical mutual information and scores all 24 permutations. A test with a hidden synthetic slot order recovers the exact inverse binding and freezes it. All 35 tests pass.

## Sealed development run

Run: `runs/ecp5-development-final/20260718T062526Z-ecp5-development`<br>
Seed: 11

| Metric | Outcome |
|---|---:|
| Population known | 100% |
| Worst known pair | 100% |
| New size-texture validation | 100% |
| Worst validation pair | 100% |
| Calibrated universal translator | 100% |
| New receiver with 32 examples | 100% |
| New receiver with 128 examples | 100% |
| New receiver with 256 examples | 100% |
| New receiver with 512 examples | 100% |

The chosen slot order by factor was `[2,3,0,1]`. The total mutual-information score was exactly 10.0 bits; the runner-up scored 8.0 bits. The choice is therefore not marginal. Even with only 32 examples, the correct permutation remained the clear winner.

## Conclusion

Calibration was frozen without further variants. With `binding_calibration.enabled`, no ECP-5 test pair was evaluated before this choice.
