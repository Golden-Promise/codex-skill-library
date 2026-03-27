# skill-handoff-summary

[简体中文](README.zh-CN.md)

## Overview

`skill-handoff-summary` is the focused package for writing continuation-oriented pause or transfer notes.
It is for compact downstream artifacts such as `.agent-state/root/HANDOFF.md` or `.agent-state/subtasks/<slug>/HANDOFF.md`, not whole-project documentation.

## Start Here In 30 Seconds

- Use this when: work is about to pause, switch owners, or cross into a new session.
- You'll get: a compact restart note with current status, hard constraints, open problems, and the exact next action.
- Typical output: updates `.agent-state/root/HANDOFF.md` or `.agent-state/subtasks/<slug>/HANDOFF.md`.

Need a durable restart note? Use this.
Just need a quick status update in chat? Don't use this.

If you want to tell Codex exactly what to do:

Try this first:

- `Use skill-handoff-summary to write a compact continuation-oriented handoff for the root task or a subtask before we pause.`

## Install

You can ask Codex in natural language:

- `Use skill-installer to install skill-handoff-summary from Golden-Promise/codex-skill-library at skills/skill-handoff-summary.`
- `Use skill-installer to install skill-handoff-summary from Golden-Promise/codex-skill-library at skills/skill-handoff-summary using ref <tag-or-commit>.`

If you want the exact shell command, jump to [Install Details](#install-details).

## What File Will This Create Or Update?

The typical downstream files are `.agent-state/root/HANDOFF.md` and `.agent-state/subtasks/<slug>/HANDOFF.md`.

Use this package when you want one of those files to preserve:

- task summary
- current status
- what changed in the current session
- hard constraints to preserve
- open problems
- the exact next action
- a reusable resume prompt

## Don't Use This When

- you need to rebuild the current task state before more work continues
- you need a root-state refresh instead of a pause artifact
- you need a checkpoint around a risky or multi-file change
- you only need a quick status note inside the current chat
- you want whole-project documentation instead of a continuation-oriented handoff

This package is continuation-oriented, does not own root-state refresh, and does not own workflow gates.

## Related Skills

- `skill-context-keeper` for refreshing `.agent-state/root/TASK_STATE.md`
- `skill-subtask-context` for `.agent-state/subtasks/<slug>/TASK_STATE.md`
- `skill-context-packet` for packet-sized next-turn context
- `skill-phase-gate` for preflight and postflight checkpoints
- `skill-task-continuity` for first-time continuity setup and routing

## Documentation

- Trigger routing and package boundary: `SKILL.md`
- Reference index: [references/README.md](references/README.md)
- Use cases and trigger examples: [references/use-cases.md](references/use-cases.md)
- Chinese use cases: [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- Prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- Chinese prompt templates: [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- Handoff template: [assets/HANDOFF.template.md](assets/HANDOFF.template.md)

## Install Details

Replace `/path/to/install-skill-from-github.py` with the actual path to your local `skill-installer` checkout.

```bash
python3 /path/to/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-handoff-summary \
  --ref <tag-or-commit>
```
