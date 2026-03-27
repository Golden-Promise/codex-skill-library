# Context Protocol Evals

This directory contains the static, repo-driven evaluation harness for the context-protocol continuity suite.
It uses `evals/cases.csv` as the seed matrix and validates the published repository shape rather than executing a model.

## What It Checks

- CSV parsing and normalization for the protocol-era seed matrix
- six-package routing coverage across:
  - `skill-context-keeper`
  - `skill-subtask-context`
  - `skill-context-packet`
  - `skill-phase-gate`
  - `skill-handoff-summary`
  - `skill-task-continuity`
- root / subtask / packet artifact mapping with strict token-to-template validation
- routing hints in `SKILL.md`, package READMEs, and prompt polarity
- boundary language and non-overlap guidance in package docs
- exact workflow-event namespaces by package and polarity contract
- suite-level bootstrap assets for `AGENTS.md`, `.agent-state/INDEX.md`, root artifacts, and subtask artifacts
- static guardrail metadata validation when optional columns are present

## Matrix Conventions

The seed matrix uses normalized artifact tokens instead of raw downstream paths.
Current token families include:

- `root/task_state`
- `root/packet`
- `root/handoff`
- `subtask/task_state`
- `subtask/packet`
- `subtask/handoff`
- `phase/preflight`
- `phase/postflight`
- `suite/agents`
- `suite/index`

This keeps the eval surface stable even when multiple packages point to the same downstream file shape.

## Run It

```bash
python3 evals/run_evals.py
```

For machine-readable output:

```bash
python3 evals/run_evals.py --format json
```

Run the tests directly when you change the harness:

```bash
python3 -m unittest discover -s evals -p 'test_*.py' -v
```

## Adding Cases

Add a new row to `evals/cases.csv`, then rerun the harness.

Prefer cases that add real routing pressure instead of paraphrasing an existing row:

- root-state refresh vs packet compression
- root vs subtask ownership
- packet-only continuation vs full-state refresh
- risky checkpoint vs trivial edit
- handoff vs in-thread status chatter
- suite bootstrap vs a single atomic action

If a case needs optional guardrails later, add the relevant CSV columns and the runner will validate `max_commands > 0` and `max_verbosity` in `low|medium|high`.
