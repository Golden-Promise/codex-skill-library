---
name: skill-governance
description: Use when the user wants to take over skill management for a project, set up skill management for a project, or check, repair, audit, document, upgrade, or retire Codex skills.
---

# Skill Governance

## Overview

Manage Codex skills through task-first requests.
Use this skill when the user wants project skill onboarding, quick health checks, or governance actions without having to sort out the underlying layout manually.

## Use This Skill When

- taking over skill management for an existing project directory
- setting up a skill management skeleton for one project
- adding or adopting a skill
- enabling a skill for one project
- checking health before cleanup, relinking, upgrade, or release
- repairing safe exposure problems
- auditing registry, lifecycle, or dependency state
- filling missing `SKILL.md` sections for an existing package

## Core Rules

1. For project onboarding, start with `manage` or `setup`.
2. Prefer `doctor` before cleanup, relinking, upgrade, or release.
3. Prefer `audit` for CI or release checks.
4. Use `document` to fill missing `SKILL.md` sections; use `--overwrite-skill-md` only for a full rewrite.
5. Keep command details in the reference guides and keep the main interaction task-first.

## References

- `references/use-cases.md` and `references/use-cases.zh-CN.md`: quick task guide
- `references/prompt-templates.en.md` and `references/prompt-templates.zh-CN.md`: copy-ready prompts
