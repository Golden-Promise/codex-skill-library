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
| `skill-context-keeper` | Refreshing or reconstructing long-task state without turning it into phase planning or a final handoff | [EN](skills/skill-context-keeper/README.md) / [中文](skills/skill-context-keeper/README.zh-CN.md) |
| `skill-phase-gate` | Splitting multi-step coding work into explicit phases, checkpoints, and exit criteria | [EN](skills/skill-phase-gate/README.md) / [中文](skills/skill-phase-gate/README.zh-CN.md) |
| `skill-handoff-summary` | Writing pause or transfer summaries with status, blockers, and next steps | [EN](skills/skill-handoff-summary/README.md) / [中文](skills/skill-handoff-summary/README.zh-CN.md) |
| `skill-task-continuity` | Coordinating the long-task continuity suite across the three narrower continuity packages | [EN](skills/skill-task-continuity/README.md) / [中文](skills/skill-task-continuity/README.zh-CN.md) |

## Quick Start

1. Open the package list in [skills/README.md](skills/README.md).
2. Choose a skill and read its package `README.md`.
3. Install it with `skill-installer`, usually into the default Codex shared library.
4. Use the package reference pages for boundary notes now, and later for examples, prompts, and deeper guidance.

## Install Example

Install `skill-governance` from this repository:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-governance
```

Install the current release:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-governance \
  --ref v0.5.1
```

Install from a GitHub tree URL:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --url https://github.com/Golden-Promise/codex-skill-library/tree/main/skills/skill-governance
```

## Reading Guide

- English skill index: [skills/README.md](skills/README.md)
- 中文技能索引: [skills/README.zh-CN.md](skills/README.zh-CN.md)
- `skill-governance` package: [EN](skills/skill-governance/README.md) / [中文](skills/skill-governance/README.zh-CN.md)
- `skill-context-keeper` package: [EN](skills/skill-context-keeper/README.md) / [中文](skills/skill-context-keeper/README.zh-CN.md)
- `skill-phase-gate` package: [EN](skills/skill-phase-gate/README.md) / [中文](skills/skill-phase-gate/README.zh-CN.md)
- `skill-handoff-summary` package: [EN](skills/skill-handoff-summary/README.md) / [中文](skills/skill-handoff-summary/README.zh-CN.md)
- `skill-task-continuity` package: [EN](skills/skill-task-continuity/README.md) / [中文](skills/skill-task-continuity/README.zh-CN.md)
- Repository publishing guide: [docs/publishing.md](docs/publishing.md)
- 中文发布说明: [docs/publishing.zh-CN.md](docs/publishing.zh-CN.md)

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
    skill-phase-gate/
    skill-handoff-summary/
    skill-task-continuity/
```

## For Maintainers

Repository versioning, release flow, and validation steps are documented in [docs/publishing.md](docs/publishing.md).
If you are publishing this repository for the first time, start there instead of the package runtime docs.
