# codex-skill-library

[简体中文](README.zh-CN.md)

A curated repository of installable Codex skills.

## What This Repo Is For

This repository is designed for people who want to:

- install ready-to-use Codex skills from one shared place
- browse skills before deciding what to use
- maintain a clean, publishable collection of reusable skill packages

## What You Will Find Here

| Area | Purpose |
| --- | --- |
| `skills/` | Published skill packages that can be installed individually |
| Package `README.md` | The best entry point for users of a specific skill |
| Package `references/` | Reader-facing examples, guides, and bilingual reference material |
| Package `docs/` | Maintainer-oriented notes when a package needs release guidance |

## Available Skills

| Skill | Best For | Docs |
| --- | --- | --- |
| `skill-governance` | Governing skill assets with task-first add, enable, doctor, repair, audit, and document flows | [EN](skills/skill-governance/README.md) / [中文](skills/skill-governance/README.zh-CN.md) |
| `skill-context-keeper` | Refreshing and compressing trusted root-task state | [EN](skills/skill-context-keeper/README.md) / [中文](skills/skill-context-keeper/README.zh-CN.md) |
| `skill-subtask-context` | Opening and maintaining bounded child-task state without bloating the root summary | [EN](skills/skill-subtask-context/README.md) / [中文](skills/skill-subtask-context/README.zh-CN.md) |
| `skill-context-packet` | Writing the minimum next-turn context packet for root or subtask work | [EN](skills/skill-context-packet/README.md) / [中文](skills/skill-context-packet/README.zh-CN.md) |
| `skill-phase-gate` | Adding preflight and postflight checkpoints around meaningful edits | [EN](skills/skill-phase-gate/README.md) / [中文](skills/skill-phase-gate/README.zh-CN.md) |
| `skill-handoff-summary` | Writing compact continuation handoffs when work pauses or changes owners | [EN](skills/skill-handoff-summary/README.md) / [中文](skills/skill-handoff-summary/README.zh-CN.md) |
| `skill-task-continuity` | Bootstrapping and composing the continuity suite without replacing the atomic packages | [EN](skills/skill-task-continuity/README.md) / [中文](skills/skill-task-continuity/README.zh-CN.md) |

## Quick Start

1. Open the package list in [skills/README.md](skills/README.md).
2. Choose a skill and read its package `README.md`.
3. Follow the installation guidance in that package README.
4. For the continuity workflow, start with `skill-task-continuity` when you need suite bootstrap or composition guidance, or jump directly to `skill-context-keeper`, `skill-subtask-context`, `skill-context-packet`, `skill-phase-gate`, or `skill-handoff-summary` when the next action is already clear.
5. Use the package reference pages for boundary notes now, and later for examples, prompts, and deeper guidance.

## Reading Guide

- English skill index: [skills/README.md](skills/README.md)
- 中文技能索引: [skills/README.zh-CN.md](skills/README.zh-CN.md)
- `skill-governance` package: [EN](skills/skill-governance/README.md) / [中文](skills/skill-governance/README.zh-CN.md)
- `skill-context-keeper` package: [EN](skills/skill-context-keeper/README.md) / [中文](skills/skill-context-keeper/README.zh-CN.md)
- `skill-subtask-context` package: [EN](skills/skill-subtask-context/README.md) / [中文](skills/skill-subtask-context/README.zh-CN.md)
- `skill-context-packet` package: [EN](skills/skill-context-packet/README.md) / [中文](skills/skill-context-packet/README.zh-CN.md)
- `skill-phase-gate` package: [EN](skills/skill-phase-gate/README.md) / [中文](skills/skill-phase-gate/README.zh-CN.md)
- `skill-handoff-summary` package: [EN](skills/skill-handoff-summary/README.md) / [中文](skills/skill-handoff-summary/README.zh-CN.md)
- `skill-task-continuity` package: [EN](skills/skill-task-continuity/README.md) / [中文](skills/skill-task-continuity/README.zh-CN.md)
- Context protocol migration guide: [docs/context-protocol-migration.md](docs/context-protocol-migration.md)
- 中文迁移说明: [docs/context-protocol-migration.zh-CN.md](docs/context-protocol-migration.zh-CN.md)
- Continuity suite overview: [docs/long-task-suite.md](docs/long-task-suite.md)
- 中文连续性套件总览: [docs/long-task-suite.zh-CN.md](docs/long-task-suite.zh-CN.md)
- Repository publishing guide: [docs/publishing.md](docs/publishing.md)
- 中文发布说明: [docs/publishing.zh-CN.md](docs/publishing.zh-CN.md)
- Release checklist for the continuity suite: [docs/release-checklist-long-task-suite.md](docs/release-checklist-long-task-suite.md)
- 中文连续性套件发布清单: [docs/release-checklist-long-task-suite.zh-CN.md](docs/release-checklist-long-task-suite.zh-CN.md)

## Repository Layout

```text
codex-skill-library/
  README.md
  README.zh-CN.md
  CHANGELOG.md
  docs/
  skills/
    README.md
    README.zh-CN.md
    skill-governance/
    skill-context-keeper/
    skill-subtask-context/
    skill-context-packet/
    skill-phase-gate/
    skill-handoff-summary/
    skill-task-continuity/
```

## For Maintainers

Repository versioning, release flow, and validation steps are documented in [docs/publishing.md](docs/publishing.md).
The continuity-suite release checklist lives in [docs/release-checklist-long-task-suite.md](docs/release-checklist-long-task-suite.md).
Protocol migration and overview docs live in [docs/context-protocol-migration.md](docs/context-protocol-migration.md) and [docs/long-task-suite.md](docs/long-task-suite.md).
Package-level install guidance stays in each package README.
If you are publishing this repository for the first time, start with those maintainer docs instead of the package runtime docs.
