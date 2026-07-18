# Runs

The simulator writes here immutable output files from ECP experiments. Each run gets its own directory containing at minimum:

- the effective configuration and hash;
- dataset manifest and hashes;
- model and software versions;
- raw messages and reconstructions;
- metrics and controls;
- a filled-in experiment report.

Run directories can grow hundreds of megabytes in size and are therefore listed in `.gitignore`. Do not commit checkpoints, isolated matrices, or episode files. Publish a compact, controlled results snapshot under `evidence/` and record the reproduction instruction.
