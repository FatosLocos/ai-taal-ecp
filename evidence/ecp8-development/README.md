# ECP-8 sealed development evidence

ECP-8 Batch 1 tests whether two surplus, semantically unallocated channel bits
solve the hard-code bottleneck of the strongest weak-structure ECP-7 system.
The factorized 14-bit positive control, weak-structure 14-bit paired control and
weak-structure 16-bit intervention use one fresh deterministic split and seed
11. The confirmatory split was never opened.

The positive control is perfect. The 16-bit intervention raises mean train
exactness from 79.55% to 98.76%, mean validation from 70.27% to 74.46% and
worst-link validation from 64.84% to 73.34%. It also raises the minimum sender
codebook from 12,048 to 15,095 of 15,360 accessible meanings. However, every
sender still has 225–265 hard-code collisions and validation remains below the
registered 80% mean and worst-link thresholds. Batch 1 is therefore a valid
negative development result.

`batch1-manifest.json` records the preregistration commit, configuration and
split identities, compact metrics, gate checks and hashes of the local run
artifacts. The large checkpoints, message matrices and episode logs remain
under ignored local `runs/` directories.
