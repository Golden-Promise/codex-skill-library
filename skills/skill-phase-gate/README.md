# skill-phase-gate

[简体中文](README.zh-CN.md)

## Overview

`skill-phase-gate` adds compact preflight and postflight checkpoints around meaningful coding work.
It keeps risky execution intentional without taking over long-term task state, generic planning, or final handoffs.

## Core Capabilities

`skill-phase-gate` focuses on making high-value checkpoints crisp and repeatable.

- define a preflight checkpoint around goal, constraints, scope, and verification
- capture a postflight checkpoint around actual changes, validations, and remaining risks
- make checkpoint use explicit for meaningful edits instead of every small action
- leave long-term state to `skill-context-keeper` and handoffs to `skill-handoff-summary`

## Best For

- preflight before a refactor, migration, or other multi-file change
- postflight after a meaningful edit when you want to verify what actually changed
- risky edits where expected files, explicit non-goals, and a verification plan should be clear
- pre-commit checkpoints when the work deserves one more deliberate pass

If the value comes from pausing to confirm scope and validation, this package is the right fit.

## Checkpoint Bar

Use this package when the checkpoint itself is valuable:

- good fit: refactors, multi-file changes, risky edits, or pre-commit checkpoints
- bad fit: typo fixes, tiny one-line changes, pure explanation tasks, or generic planning requests

## What It Is Not For

- not for trivial one-line edits
- not for pure explanation tasks
- reconstructing stale or missing task context
- summarizing the current state after an interruption
- writing a pause note or transfer package for another agent
- owning long-term state that belongs to `skill-context-keeper`
- orchestrating the whole long-task continuity suite

## Install

To install `skill-phase-gate`, use the standard published package path in this repository and choose the release or ref that fits your workflow.

You can ask Codex in natural language:

- `Use skill-installer to install skill-phase-gate from Golden-Promise/codex-skill-library at skills/skill-phase-gate.`
- `Use skill-installer to install skill-phase-gate from Golden-Promise/codex-skill-library at skills/skill-phase-gate using ref v0.6.1.`

For direct trigger examples and prompt wording, see [references/use-cases.md](references/use-cases.md).

## Common Paths

Start with one of these three paths:

1. Run a preflight before a refactor, migration, or risky multi-file change.
2. Run a postflight after meaningful implementation work.
3. Add a deliberate pre-commit checkpoint when the change deserves one.

If you want ready-to-paste prompts, see [references/prompt-templates.en.md](references/prompt-templates.en.md).

## Documentation

- Trigger routing and package boundary: `SKILL.md`
- Reference index: [references/README.md](references/README.md)
- Use cases and trigger examples: [references/use-cases.md](references/use-cases.md)
- Chinese use cases: [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- Prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- Chinese prompt templates: [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- Preflight checklist: [assets/PREFLIGHT.template.md](assets/PREFLIGHT.template.md)
- Postflight checklist: [assets/POSTFLIGHT.template.md](assets/POSTFLIGHT.template.md)
