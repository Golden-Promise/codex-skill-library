# skill-phase-gate

[简体中文](README.zh-CN.md)

## Overview

`skill-phase-gate` adds compact preflight and postflight checkpoints around meaningful coding work.
If the checkpoint itself adds value, use this skill.

## Start Here In 30 Seconds

- Use this when: you are about to make a risky, multi-file, or otherwise meaningful change.
- You'll get: a compact checkpoint that makes scope, constraints, verification, and remaining risk explicit.
- Typical outputs: a preflight note shaped like `assets/PREFLIGHT.template.md` and a postflight note shaped like `assets/POSTFLIGHT.template.md`.

If you want to tell Codex exactly what to do:

Try this first:

- `Use skill-phase-gate to create a preflight gate before this risky multi-file change.`

## Install

You can ask Codex in natural language:

- `Use skill-installer to install skill-phase-gate from Golden-Promise/codex-skill-library at skills/skill-phase-gate.`
- `Use skill-installer to install skill-phase-gate from Golden-Promise/codex-skill-library at skills/skill-phase-gate using ref v0.6.1.`

If you want the exact shell command, jump to [Install Details](#install-details).

## What File Will This Create Or Update?

This package usually creates or refreshes a preflight checkpoint note, a postflight checkpoint note, or both.

Use the shipped templates as the starting shape:

- [assets/PREFLIGHT.template.md](assets/PREFLIGHT.template.md)
- [assets/POSTFLIGHT.template.md](assets/POSTFLIGHT.template.md)

## Don't Use This When

- the change is a trivial one-line edit
- the work is a pure explanation task
- the main problem is stale task state rather than checkpoint value
- you need a pause or transfer handoff instead of a workflow checkpoint

This package is not for trivial one-line edits and is not for pure explanation tasks.

## Related Skills

- `skill-context-keeper` for rebuilding task state before or after meaningful work
- `skill-handoff-summary` for pause and transfer notes
- `skill-task-continuity` for first-time setup and suite-level routing

## Documentation

- Trigger routing and package boundary: `SKILL.md`
- Reference index: [references/README.md](references/README.md)
- Use cases and trigger examples: [references/use-cases.md](references/use-cases.md)
- Chinese use cases: [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- Prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- Chinese prompt templates: [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- Preflight checklist: [assets/PREFLIGHT.template.md](assets/PREFLIGHT.template.md)
- Postflight checklist: [assets/POSTFLIGHT.template.md](assets/POSTFLIGHT.template.md)

## Install Details

Replace `/path/to/install-skill-from-github.py` with the actual path to your local `skill-installer` checkout.

```bash
python3 /path/to/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-phase-gate \
  --ref v0.6.1
```
