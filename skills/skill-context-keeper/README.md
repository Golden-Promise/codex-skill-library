# skill-context-keeper

[简体中文](README.zh-CN.md)

## Overview

`skill-context-keeper` is the focused package for refreshing structured task state during long-running coding work.
Use it when the task is still ongoing, but the working context is stale.

## Start Here In 30 Seconds

- Use this when: the task is still active, but the current picture is stale, scattered, or partially trusted.
- You'll get: a compact, verified task snapshot that separates facts, assumptions, decisions, risks, and next actions.
- Typical output: updates `.agent-state/TASK_STATE.md`.

If you want to tell Codex exactly what to do:

Try this first:

- `Use skill-context-keeper to refresh the current task state from the repository before we continue.`

## Install

You can ask Codex in natural language:

- `Use skill-installer to install skill-context-keeper from Golden-Promise/codex-skill-library at skills/skill-context-keeper.`
- `Use skill-installer to install skill-context-keeper from Golden-Promise/codex-skill-library at skills/skill-context-keeper using ref v0.6.1.`

If you want the exact shell command, jump to [Install Details](#install-details).

## What File Will This Create Or Update?

The typical downstream file is `.agent-state/TASK_STATE.md`.

Use this package when you want to refresh or rewrite that task-state file so the next turn can resume from a trusted summary of:

- the current objective
- current repository facts
- completed work
- open issues and risks
- the next recommended action

## Don't Use This When

- you need a preflight or postflight checkpoint around a risky change
- you need a durable pause or transfer handoff
- you are setting up the full continuity workflow in a repo for the first time
- you want generic workflow control instead of state refresh

This package does not own workflow gating and does not own final handoffs.

## Related Skills

- `skill-phase-gate` for meaningful preflight and postflight checkpoints
- `skill-handoff-summary` for pause and transfer notes
- `skill-task-continuity` for first-time continuity setup and suite-level guidance

## Documentation

- Trigger routing and package boundary: `SKILL.md`
- Use cases and trigger examples: [references/use-cases.md](references/use-cases.md)
- Chinese use cases: [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- Prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- Chinese prompt templates: [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- Task-state template: [assets/TASK_STATE.template.md](assets/TASK_STATE.template.md)

## Install Details

Replace `/path/to/install-skill-from-github.py` with the actual path to your local `skill-installer` checkout.

```bash
python3 /path/to/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-context-keeper \
  --ref v0.6.1
```
