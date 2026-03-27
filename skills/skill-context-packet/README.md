# skill-context-packet

[简体中文](README.zh-CN.md)

## Overview

`skill-context-packet` is the narrow package for writing the minimum context object needed for the next root or subtask turn.
Use it when a full state file would waste context budget and the next step only needs a compact execution packet.

## Start Here In 30 Seconds

- Use this when: the next turn needs the smallest useful context object instead of a full state refresh.
- You'll get: a packet with the exact objective, scope, inputs, facts, constraints, risks, exit criteria, and next command.
- Typical output: updates `.agent-state/root/PACKET.md` or `.agent-state/subtasks/<slug>/PACKET.md`.

If you want to tell Codex exactly what to do:

Try this first:

- `Use skill-context-packet to compress the next turn into .agent-state/root/PACKET.md and keep only the minimum facts and constraints we still need.`

## Install

You can ask Codex in natural language:

- `Use skill-installer to install skill-context-packet from Golden-Promise/codex-skill-library at skills/skill-context-packet.`
- `Use skill-installer to install skill-context-packet from Golden-Promise/codex-skill-library at skills/skill-context-packet using ref <tag-or-commit>.`

If you want the exact shell command, jump to [Install Details](#install-details).

## What File Will This Create Or Update?

The typical downstream files are `.agent-state/root/PACKET.md` and `.agent-state/subtasks/<slug>/PACKET.md`.

Use this package when you want to compress the next turn into a minimum context object that preserves:

- the exact objective for this turn
- the narrow scope and explicit non-goals
- the minimal files or inputs worth loading
- the facts and constraints that still matter
- the exit criteria and exact next command

## Don't Use This When

- you need to rebuild root task state or subtask state in full
- you need a risky-change checkpoint or workflow gate
- you need a pause or transfer handoff
- you are bootstrapping the suite for the first time

This package owns the minimum context object, does not own root task state, and does not own workflow gates.

## Related Skills

- `skill-context-keeper` for `.agent-state/root/TASK_STATE.md`
- `skill-subtask-context` for `.agent-state/subtasks/<slug>/TASK_STATE.md`
- `skill-phase-gate` for meaningful preflight and postflight checkpoints
- `skill-handoff-summary` for pause and transfer notes
- `skill-task-continuity` for suite-level bootstrap and routing

## Documentation

- Trigger routing and package boundary: `SKILL.md`
- Use cases and trigger examples: [references/use-cases.md](references/use-cases.md)
- Chinese use cases: [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- Prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- Chinese prompt templates: [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- Packet template: [assets/PACKET.template.md](assets/PACKET.template.md)

## Install Details

Replace `/path/to/install-skill-from-github.py` with the actual path to your local `skill-installer` checkout.

```bash
python3 /path/to/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-context-packet \
  --ref <tag-or-commit>
```
