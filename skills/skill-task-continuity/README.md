# skill-task-continuity

[简体中文](README.zh-CN.md)

## Overview

`skill-task-continuity` is the suite entry point for long-task continuity.
It explains how the continuity packages fit together and ships a bootstrap helper that copies downstream templates into a consumer repository.
It does not replace the atomic skills.

## Core Capabilities

`skill-task-continuity` focuses on composition and downstream setup.

- explain how `skill-context-keeper`, `skill-phase-gate`, and `skill-handoff-summary` fit together
- bootstrap downstream files such as `AGENTS.md` and `.agent-state/*.md`
- route suite-shaped requests to the atomic package that owns the next action
- keep the public-package boundary explicit so templates remain downstream assets, not live repo-root runtime files

## Best For

- adopting the continuity workflow in a downstream repository for the first time
- setting up downstream templates before long-running work starts
- deciding which atomic package should own the next action
- teaching maintainers or downstream users how the suite composes without blurring package boundaries

## What It Is Not For

- replacing `skill-context-keeper` for ordinary state refresh work
- replacing `skill-phase-gate` for a normal checkpoint
- replacing `skill-handoff-summary` for a simple pause or transfer note
- turning this public library checkout into a consumer repo

## Install

To install `skill-task-continuity`, use the standard published package path in this repository and choose the release or ref that fits your workflow.

You can ask Codex in natural language:

- `Use skill-installer to install skill-task-continuity from Golden-Promise/codex-skill-library at skills/skill-task-continuity.`
- `Use skill-installer to install skill-task-continuity from Golden-Promise/codex-skill-library at skills/skill-task-continuity using ref v0.6.0.`

For downstream bootstrap walkthroughs and prompt wording, see [references/install-playbook.md](references/install-playbook.md).

## Recommended Downstream Layout

```text
AGENTS.md
.agent-state/
  TASK_STATE.md
  HANDOFF.md
  DECISIONS.md
  RUN_LOG.md
```

`TASK_STATE.md` and `HANDOFF.md` are duplicated copies of the atomic package templates for downstream convenience.
The atomic packages remain the source of truth for their behavior and wording.

## Common Paths

Start with one of these three paths:

1. Bootstrap a downstream repository with `AGENTS.md` and `.agent-state/` templates.
2. Read the composition guide and decide which atomic package owns the next action.
3. Add thin repo-local wrappers only when a downstream repository truly needs them.

The bootstrap helper requires an explicit target and refuses to bootstrap inside this public skill library checkout.
Use `python3 skills/skill-task-continuity/scripts/bootstrap_suite.py --target /path/to/downstream-repo --dry-run` to preview changes, then rerun without `--dry-run` to apply them.

## How The Suite Composes

Use the atomic skills directly in downstream work:

- `Use $skill-context-keeper to refresh .agent-state/TASK_STATE.md before more implementation work.`
- `Use $skill-phase-gate for a preflight before this risky multi-file change.`
- `Use $skill-handoff-summary to write .agent-state/HANDOFF.md before we pause.`

The recommended long-task loop is:

1. Read the state files before resuming.
2. Gate meaningful changes when the checkpoint adds value.
3. Refresh task state after meaningful work.
4. Write a handoff when pausing or transferring ownership.

Repo-local `.agents/skills/` wrappers or examples are optional.
If you add them, keep them thin and point back to the atomic skills instead of replacing them.

## Documentation

- Trigger routing and package boundary: `SKILL.md`
- Composition guide: [references/composition-guide.md](references/composition-guide.md)
- Chinese composition guide: [references/composition-guide.zh-CN.md](references/composition-guide.zh-CN.md)
- Install playbook: [references/install-playbook.md](references/install-playbook.md)
- Chinese install playbook: [references/install-playbook.zh-CN.md](references/install-playbook.zh-CN.md)
- Downstream templates copied by the bootstrap helper: `assets/`
