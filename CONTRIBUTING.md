# Contributing

Contributions are welcome: new agent architectures, alternative inductive biases, stronger controls, additional metrics, documentation and independent replications.

## Development setup

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/pytest
```

## Pull requests

Keep each pull request focused on one research or engineering question. Include:

- the hypothesis or problem being addressed;
- the files and experiment stage affected;
- whether any confirmatory test data was accessed;
- tests and config validation performed;
- expected scientific interpretation and limitations.

Generated run directories are intentionally ignored. If a result is important, add a compact reviewed manifest under `evidence/` and document the exact reproduction command.

Never rewrite a frozen experiment configuration. New hypotheses require a new numbered development configuration and a new sealed test decision.

See `AGENTS.md` and `docs/AI_AGENT_START.md` for the complete workflow.
