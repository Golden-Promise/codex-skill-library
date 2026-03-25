# skill-task-continuity

[简体中文](README.zh-CN.md)

## Overview

`skill-task-continuity` is the suite entry point for long-task continuity.
It explains how the continuity packages fit together and ships a bootstrap helper that copies downstream templates into a consumer repository.
It does not replace the atomic skills.

## Package Role

- explain the composition of `skill-context-keeper`, `skill-phase-gate`, and `skill-handoff-summary`
- bootstrap downstream files such as `AGENTS.md` and `.agent-state/*.md`
- route suite-shaped requests to the atomic package that owns the next action
- keep the package boundary explicit: templates are for downstream consumers only

## What It Is Not For

- replacing `skill-context-keeper` for ordinary state refresh work
- replacing `skill-phase-gate` for a normal checkpoint
- replacing `skill-handoff-summary` for a simple pause or transfer note
- turning this public library checkout into a consumer repo

## Install

Install `skill-task-continuity` from this repository with the standard package path for published Codex skills.

You can ask Codex in natural language:

- `Use skill-installer to install skill-task-continuity from Golden-Promise/codex-skill-library at skills/skill-task-continuity.`
- `Use skill-installer to install skill-task-continuity from Golden-Promise/codex-skill-library at skills/skill-task-continuity using the release or ref I specify.`

Or run `skill-installer` directly:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-task-continuity
```

Pin the planned continuity-suite release:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-task-continuity \
  --ref v0.6.0
```

## Bootstrap A Downstream Repo

Preview the downstream file operations first:

```bash
python3 skills/skill-task-continuity/scripts/bootstrap_suite.py --target /path/to/downstream-repo --dry-run
```

Then copy the templates for real:

```bash
python3 skills/skill-task-continuity/scripts/bootstrap_suite.py --target /path/to/downstream-repo
```

Use `--force` only when you intentionally want to overwrite an existing downstream file.
The script requires an explicit `--target` and refuses to bootstrap inside this public skill library checkout.

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

## References

- `SKILL.md` for trigger routing and package boundaries
- [references/composition-guide.md](references/composition-guide.md) for suite composition and explicit invocation wording
- [references/install-playbook.md](references/install-playbook.md) for a downstream bootstrap walkthrough
- `assets/` for downstream-only templates copied by the bootstrap helper
