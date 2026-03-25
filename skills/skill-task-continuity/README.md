# skill-task-continuity

[简体中文](README.zh-CN.md)

## Overview

`skill-task-continuity` is the beginner entry package for the long-task continuity suite.
Start here if you are setting up the continuity workflow in a project for the first time.

## Start Here In 30 Seconds

- Use this when: you want to set up the continuity workflow in a repo, understand the suite, or decide which continuity skill to use next.
- You'll get: starter files for a downstream repo, a simple long-task loop, and a clear route to the atomic skills.
- Typical output: a downstream `AGENTS.md` plus `.agent-state/` starter files.

If you want to tell Codex exactly what to do:

Try this first:

- `Use skill-task-continuity to bootstrap the long-task continuity starter files into /path/to/downstream-repo. Preview the file operations first, then apply them if the preview looks correct. Do not overwrite existing files unless I explicitly ask.`

## Install

For most newcomers, natural-language installation is the easiest path.

You can ask Codex to install only this package:

- `Use skill-installer to install skill-task-continuity from Golden-Promise/codex-skill-library at skills/skill-task-continuity.`

You can also ask Codex to install the full suite:

- `Use skill-installer to install the full long-task continuity suite from Golden-Promise/codex-skill-library at skills/skill-context-keeper, skills/skill-phase-gate, skills/skill-handoff-summary, and skills/skill-task-continuity.`

Installing `skill-task-continuity` does not auto-install the atomic packages.
If you want all four packages at once, install the full suite in one command or use the full-suite natural-language prompt above.

If you want the exact shell commands, jump to [Install Details](#install-details).

## What Gets Created In Your Repo

The bootstrap helper prepares downstream starter files such as:

- `AGENTS.md`
- `.agent-state/TASK_STATE.md`
- `.agent-state/HANDOFF.md`
- `.agent-state/DECISIONS.md`
- `.agent-state/RUN_LOG.md`

`TASK_STATE.md` and `HANDOFF.md` are convenience copies of the atomic package templates so a downstream repo can start quickly.

## Fastest Setup

After installation, the fastest setup path is:

1. Ask Codex to bootstrap the starter files into your downstream repo.
2. Review the created `AGENTS.md` and `.agent-state/` files.
3. Start the first real task by calling the atomic package that owns the next action.

If you need exact CLI control instead, use `python3 skills/skill-task-continuity/scripts/bootstrap_suite.py --target /path/to/downstream-repo --dry-run` first, then rerun without `--dry-run` to apply.

## Which Skill To Use Next

- Use `skill-context-keeper` when the task is active but the state picture is stale.
- Use `skill-phase-gate` when the next step is a risky or multi-file change.
- Use `skill-handoff-summary` when you are about to pause or transfer the work.

## Don't Use This When

- you only need one atomic package for one immediate action
- you only need to refresh task state
- you only need a checkpoint around a meaningful change
- you only need a pause or transfer note

This package does not replace the three atomic skills and does not turn this public library checkout into a consumer repo.

## Related Skills

- `skill-context-keeper` for `.agent-state/TASK_STATE.md`
- `skill-phase-gate` for preflight and postflight checkpoints
- `skill-handoff-summary` for `.agent-state/HANDOFF.md`

## Documentation

- Trigger routing and package boundary: `SKILL.md`
- Composition guide: [references/composition-guide.md](references/composition-guide.md)
- Chinese composition guide: [references/composition-guide.zh-CN.md](references/composition-guide.zh-CN.md)
- Install playbook: [references/install-playbook.md](references/install-playbook.md)
- Chinese install playbook: [references/install-playbook.zh-CN.md](references/install-playbook.zh-CN.md)
- Downstream templates copied by the bootstrap helper: `assets/`

## Install Details

Replace `/path/to/install-skill-from-github.py` with the actual path to your local `skill-installer` checkout.

Install only this package:

```bash
python3 /path/to/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-task-continuity \
  --ref v0.6.1
```

Install the full suite in one command:

```bash
python3 /path/to/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path \
    skills/skill-context-keeper \
    skills/skill-phase-gate \
    skills/skill-handoff-summary \
    skills/skill-task-continuity \
  --ref v0.6.1
```
