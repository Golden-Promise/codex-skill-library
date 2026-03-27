# skill-subtask-context

[简体中文](README.zh-CN.md)

## Overview

`skill-subtask-context` is the narrow package for opening, refreshing, and closing local child-task state during a larger long-running task.
Use it when a bounded workstream deserves its own state file instead of polluting the root task summary.

## Start Here In 30 Seconds

- Use this when: a child task needs its own local context, scope, and exit criteria.
- You'll get: a focused subtask state file with parent links, local facts, local risks, and merge notes.
- Typical output: updates `.agent-state/subtasks/<slug>/TASK_STATE.md`.

If you want to tell Codex exactly what to do:

Try this first:

- `Use skill-subtask-context to open or refresh a child task at .agent-state/subtasks/<slug>/TASK_STATE.md and keep the parent context minimal.`

## Install

You can ask Codex in natural language:

- `Use skill-installer to install skill-subtask-context from Golden-Promise/codex-skill-library at skills/skill-subtask-context.`
- `Use skill-installer to install skill-subtask-context from Golden-Promise/codex-skill-library at skills/skill-subtask-context using ref <tag-or-commit>.`

If you want the exact shell command, jump to [Install Details](#install-details).

## What File Will This Create Or Update?

The typical downstream file is `.agent-state/subtasks/<slug>/TASK_STATE.md`.

Use this package when you want to open or refresh that local subtask state so the next turn can resume from a trusted summary of:

- the subtask objective
- the parent facts that still matter locally
- local files and inputs worth loading
- local risks, blockers, and exit criteria
- merge notes for the parent task

## Don't Use This When

- you need to refresh the root task state instead of a child task
- you need packet compression instead of a local state refresh
- you need a preflight or postflight checkpoint around a risky change
- you need a pause or transfer handoff rather than active local state

This package owns local child-task state, does not own root task state, and does not own packet compression.

## Related Skills

- `skill-context-keeper` for `.agent-state/root/TASK_STATE.md`
- `skill-context-packet` for root or subtask packet compression
- `skill-phase-gate` for meaningful preflight and postflight checkpoints
- `skill-handoff-summary` for pause and transfer notes
- `skill-task-continuity` for suite-level bootstrap and routing

## Documentation

- Trigger routing and package boundary: `SKILL.md`
- Use cases and trigger examples: [references/use-cases.md](references/use-cases.md)
- Chinese use cases: [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- Prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- Chinese prompt templates: [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- Subtask-state template: [assets/TASK_STATE.template.md](assets/TASK_STATE.template.md)

## Install Details

Replace `/path/to/install-skill-from-github.py` with the actual path to your local `skill-installer` checkout.

```bash
python3 /path/to/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-subtask-context \
  --ref <tag-or-commit>
```
