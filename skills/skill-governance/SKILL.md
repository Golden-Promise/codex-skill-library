---
name: skill-governance
description: Use this skill when the user wants to set up skill management for a project, take over an existing project directory, or add, enable, inspect, repair, audit, document, upgrade, or retire Codex skills. It chooses storage paths from context, manages project exposure, and keeps governance state consistent.
---

# Skill Governance

## Purpose

Manage Codex skills as governed assets through task-style commands.

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

1. Prefer task verbs: `manage`, `setup`, `add`, `enable`, `doctor`, `repair`, `audit`, `document`, `upgrade`, `retire`.
2. Let the tool choose shared versus project-owned storage from context and config.
3. When the user points at a project directory and wants a quick start, prefer `manage` or `setup` instead of lower-level commands.
4. Prefer `doctor` before risky changes.
5. Prefer `audit` for CI or release checks.
6. `document` fills missing sections by default; use `--overwrite-skill-md` only when you want a full rewrite.

## Core Commands

```bash
python3 <path-to-skill-governance>/scripts/manage_skill.py manage <project-root>
python3 <path-to-skill-governance>/scripts/manage_skill.py setup <project-root>
python3 <path-to-skill-governance>/scripts/manage_skill.py add <skill-name> --purpose "<purpose>"
python3 <path-to-skill-governance>/scripts/manage_skill.py add <import-path> --project <project-root>
python3 <path-to-skill-governance>/scripts/manage_skill.py enable <skill-name> --project <project-root>
python3 <path-to-skill-governance>/scripts/manage_skill.py doctor <skill-name> --project <project-root>
python3 <path-to-skill-governance>/scripts/manage_skill.py repair <skill-name> --workspace-root <workspace-root>
python3 <path-to-skill-governance>/scripts/manage_skill.py audit --workspace-root <workspace-root> --sync-platform-state
python3 <path-to-skill-governance>/scripts/manage_skill.py document <skill-name> --library-root <library-root>
```

## References

- `references/use-cases.md` and `references/use-cases.zh-CN.md`: quick task guide
- `references/prompt-templates.en.md` and `references/prompt-templates.zh-CN.md`: copy-ready prompts
