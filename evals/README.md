# Long-Task Continuity Evals

This directory contains the static, repo-driven evaluation harness for the long-task continuity suite.
It uses `evals/cases.csv` as the seed matrix and checks the published repository shape rather than executing a model.

## What It Checks

- CSV parsing and normalization
- should-trigger vs should-not-trigger coverage from prompt polarity
- expected artifact templates for each package, with strict token-to-template mapping
- routing hints in `SKILL.md` and package READMEs
- boundary language and non-overlap guidance in package READMEs
- expected event tokens by package namespace and case polarity
- suite-level downstream templates and assets for `skill-task-continuity`
- optional command-count or verbosity guardrails when future cases add them

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
If the case needs optional guardrails later, add the relevant CSV columns and the runner will normalize them without changing the API.
For polarity-sensitive cases, make sure the prompt cues, expected events, and artifact tokens all match the package’s routing boundary.
