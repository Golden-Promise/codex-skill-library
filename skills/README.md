# Skills

[简体中文](README.zh-CN.md)

This directory contains the installable skill packages published by `codex-skill-library`.

## How To Use This Index

1. Scan the table below to find the skill that matches your task.
2. Open the package README in your preferred language.
3. Use the package references when you need examples or prompt wording.

## Published Packages

| Skill | Best For | Docs |
| --- | --- | --- |
| `skill-governance` | Governing Codex skill assets with add, enable, doctor, repair, audit, and document tasks | [EN](skill-governance/README.md) / [中文](skill-governance/README.zh-CN.md) |
| `skill-context-keeper` | Refreshing or reconstructing long-task state without drifting into phase planning or handoff writing | [EN](skill-context-keeper/README.md) / [中文](skill-context-keeper/README.zh-CN.md) |
| `skill-phase-gate` | Adding phase boundaries, checkpoints, and exit criteria to multi-step coding work | [EN](skill-phase-gate/README.md) / [中文](skill-phase-gate/README.zh-CN.md) |
| `skill-handoff-summary` | Producing pause and transfer summaries with status, blockers, and next steps | [EN](skill-handoff-summary/README.md) / [中文](skill-handoff-summary/README.zh-CN.md) |
| `skill-task-continuity` | Coordinating the continuity suite when context, phases, and handoff concerns must stay aligned | [EN](skill-task-continuity/README.md) / [中文](skill-task-continuity/README.zh-CN.md) |

## Package Conventions

- Each published package lives in `skills/<skill-name>/`.
- The directory name should match the `name` field in `SKILL.md`.
- Package `README.md` files are the main entry point for users.
- `references/` is for reader-facing material; `docs/` is for maintainer notes when needed.
