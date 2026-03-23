---
name: skill-workflow-manager
description: Use this skill when the user wants to create, update, standardize, import, or relink a Codex skill with a shared-library workflow. It maintains one canonical source, manages project discovery links, and updates skill metadata consistently.
---

# Skill Workflow Manager

## Purpose

Manage a skill as one canonical source plus optional project discovery links.
Use this skill for skill lifecycle work only.

## Use This Skill When

- create or update a managed skill
- inspect or import a downloaded local skill into the library
- attach, detach, or exact-sync selected skills for a project
- repair project discovery links or bootstrap a managed project layout

Do not use this skill for unrelated coding tasks.

## Working Model

1. Keep exactly one canonical source at `<library-root>/<skill-name>`.
2. Expose that skill to projects through `<project-root>/.agents/skills/<skill-name>`.
3. Update `SKILL.md` and `agents/openai.yaml` together.
4. Keep `SKILL.md` concise and move longer examples or policy details into `references/`.
5. Validate after create or update work unless the user explicitly asks to skip it.

## Workflow

1. Classify the request as create/update, inspect/import, project link management, or bootstrap.
2. Use `scripts/manage_skill.py` for deterministic filesystem work.
3. Prefer `--dry-run` or `--inspect-import` before risky changes.
4. Default to `--import-mode copy`; use `move` only when the shared-library copy should become the sole source.
5. Report the canonical path, any links changed, and the validation result or remaining manual follow-up.

## Rules

- Never create duplicate canonical copies unless the user explicitly wants a separate version.
- Stop on name conflicts or non-symlink blockers; do not overwrite silently.
- Treat project links as opt-in. Link only the requested skills.
- Prefer incremental edits over rewriting a skill unless the user clearly wants a reset.

## Script Patterns

Use `scripts/manage_skill.py` with portable placeholders:

```bash
python3 <path-to-skill-workflow-manager>/scripts/manage_skill.py \
  <skill-name> \
  --project-root <project-root> \
  --purpose "<purpose>"
```

```bash
python3 <path-to-skill-workflow-manager>/scripts/manage_skill.py \
  --inspect-import \
  --import-path <downloaded-skill> \
  --project-root <project-root>
```

```bash
python3 <path-to-skill-workflow-manager>/scripts/manage_skill.py \
  --bootstrap-project-layout \
  --project-root <project-root>
```

```bash
python3 <path-to-skill-workflow-manager>/scripts/manage_skill.py \
  --validate-only
```

Key flags:

- `--list-library-skills`
- `--list-project-skills --project-root <project-root>`
- `--format json` for read-only modes
- `--project-skills skill-a,skill-b`
- `--unlink-skills skill-a`
- `--sync-project-skills skill-a,skill-b`
- `--overwrite-skill-md`
- `--overwrite-openai`
- `--validate-only`
- `--skip-validate`
- `--dry-run`

## References

- Choose the reference file that matches the reader's language, and keep English and Chinese counterparts aligned when updating them.
- `references/use-cases.md` and `references/use-cases.zh-CN.md`: the main reader guides for workflow selection, task coverage, and CLI patterns
- `references/prompt-templates.en.md` and `references/prompt-templates.zh-CN.md`: slim prompt cheat sheets for direct reuse
