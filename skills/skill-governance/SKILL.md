---
name: skill-governance
description: Use when the user wants to take over project skill governance, set it up, add or enable a skill, check, audit, or repair it, or document, upgrade, or retire Codex skills.
---

# Skill Governance

## Overview

Project skill governance for taking over, setting up, and maintaining Codex skills in a project.
Use this skill for project skill work when you want to start from the task instead of the layout.

## Use This Skill When

- taking over project skill management
- setting up project skill management
- adding a reusable skill
- bringing a local skill into a project
- making a skill available in a project
- checking, auditing, or repairing skills
- documenting, upgrading, or retiring skills

## Core Rules

1. Start with the user’s task, not the underlying layout.
2. Prefer `doctor` before cleanup, relinking, upgrade, or release.
3. Prefer `audit` for CI or release checks.
4. Use `document` to fill missing `SKILL.md` sections; use `--overwrite-skill-md` only for a full rewrite.
5. Keep the main interaction short and task-first.

## References

- `references/use-cases.md` and `references/use-cases.zh-CN.md`: command reference and advanced usage
- `references/prompt-templates.en.md` and `references/prompt-templates.zh-CN.md`: copy-ready requests
