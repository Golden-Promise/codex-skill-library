# skill-phase-gate

[简体中文](README.zh-CN.md)

## Overview

`skill-phase-gate` adds compact preflight and postflight checkpoints around meaningful coding work.
It keeps risky execution intentional without taking over long-term task state, generic planning, or final handoffs.

## Best For

- preflight before a refactor, migration, or other multi-file change
- postflight after a meaningful edit when you want to verify what actually changed
- risky edits where expected files, explicit non-goals, and a verification plan should be clear
- pre-commit checkpoints when the work deserves one more deliberate pass

## Meaningful Checkpoint Bar

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

Install `skill-phase-gate` from this repository with the standard package path for published Codex skills.

You can ask Codex in natural language:

- `Use skill-installer to install skill-phase-gate from Golden-Promise/codex-skill-library at skills/skill-phase-gate.`
- `Use skill-installer to install skill-phase-gate from Golden-Promise/codex-skill-library at skills/skill-phase-gate using the release or ref I specify.`

## How To Use

Use this package at a meaningful checkpoint before or after implementation work.
Describe the current goal, the key constraints, the expected files, the files you are explicitly not changing, and the verification plan for a preflight gate, or ask for a postflight gate that records actual changes, validations, remaining risks, and whether handoff is recommended.

If you also need current task state to persist across a long-running thread, keep that state in `skill-context-keeper`; this package only frames the immediate checkpoint.

## References

- `SKILL.md` for trigger routing and package boundaries
- [references/README.md](references/README.md) for the reader-facing reference index
- [references/use-cases.md](references/use-cases.md) for positive and negative trigger examples
- [references/prompt-templates.en.md](references/prompt-templates.en.md) for ready-to-paste prompts
- [assets/PREFLIGHT.template.md](assets/PREFLIGHT.template.md) for the preflight checklist
- [assets/POSTFLIGHT.template.md](assets/POSTFLIGHT.template.md) for the postflight checklist
