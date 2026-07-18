# Instructions for AI agents

This repository is a reproducible research project, not a generic chat application. Preserve the distinction between development evidence and confirmatory evidence.

## Start here

Read these files in order before changing code:

1. `README.md`
2. `docs/results-ecp6.md`
3. `docs/protocol-specification-ecp6.md`
4. `docs/research-design-ecp6.md`
5. `docs/AI_AGENT_START.md`

Then run:

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/pytest
.venv/bin/ecp6 --config config/ecp6.yaml validate
```

## Non-negotiable research rules

- Never tune a model, split, threshold, metric or seed after reading its confirmatory test result.
- Never edit a frozen `config/ecpN.yaml` in place. Create `config/ecpN+1-development.yaml` for new work.
- Use `smoke` and `develop` while the new test split is sealed. Only a frozen config may use `experiment --unseal-test`.
- Record the config SHA-256, split SHA-256 and freeze time before unsealing a new test.
- Keep train, validation and confirmatory test meanings disjoint and deterministic.
- Preserve channel isolation: receivers may receive symbol matrices only, never meaning IDs, sender parameters or hidden state.
- Preserve hard-symbol evaluation. Continuous relaxations may be used for training only.
- Report negative and partial results. Do not silently discard failed seeds or variants.
- Do not commit generated `runs/*/` directories, checkpoints or episode logs. Put compact, reviewed evidence under `evidence/`.
- Do not claim that ECP is a general replacement for human language. Every conclusion must state the synthetic-world and architectural limits.

## Change discipline

- Add or update tests for every invariant or behavior change.
- Run the full test suite and the relevant config validation before committing.
- Keep existing ECP-0 through ECP-6 configurations reproducible.
- Document new experiments in three stages: preregistration, sealed development log, confirmatory results.
- Write new configurations, documentation, reports and user-facing output in English.
- Preserve the completed ECP-8 Batch 1 capacity isolation and its sealed confirmatory split. Any Batch 2 must keep the 16-bit arm fixed and preregister exactly one structure-induction mechanism.

ECP-8 Batch 1 found that surplus capacity nearly removes collisions but does not reach injectivity or compositional validation. Do not continue a channel-size search.
