---
name: skill-workflow-manager
description: Use this skill when the user wants to create, update, standardize, import, or relink a Codex skill with a shared-library workflow. It treats $CODEX_HOME/skills as the default shared library, manages optional project discovery links, and updates skill metadata consistently.
---

# Skill Workflow Manager

## Purpose

Manage skills in the default Codex shared library plus optional project discovery links.
Use this skill for skill lifecycle work only.

## Use This Skill When

- create or update a managed skill
- inspect or import a downloaded local skill into the library
- attach, detach, or exact-sync selected skills for a project
- repair project discovery links
- bootstrap a project-local managed layout when the user explicitly wants project-contained skill management
- register a staged package for direct Codex discovery

Do not use this skill for unrelated coding tasks.

## Working Model

1. Treat `$CODEX_HOME/skills/<skill-name>` as the default canonical shared-library location unless the user explicitly chooses another library root.
2. Expose a shared-library skill to projects through `<project-root>/.agents/skills/<skill-name>` only when project discovery is needed.
3. Use `<project-root>/_skill-library/<skill-name>` only when the user explicitly wants a project-contained managed layout.
4. Update `SKILL.md` and `agents/openai.yaml` together.
5. Keep `SKILL.md` concise and move longer examples or policy details into `references/`.
6. Validate after create or update work unless the user explicitly asks to skip it.

## Workflow

1. Classify the request as create/update, inspect/import, project link management, project-local bootstrap, or runtime registration.
2. Use `scripts/manage_skill.py` for deterministic filesystem work.
3. Prefer `--dry-run` or `--inspect-import` before risky changes.
4. Prefer the global shared-library flow in `$CODEX_HOME/skills`; use project-local bootstrap only when the user explicitly wants vendored project management.
5. Default to `--import-mode copy`; use `move` only when the shared-library copy should become the sole source.
6. Report the canonical path, any links changed, and the validation result or remaining manual follow-up.

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
  --purpose "<purpose>"
```

```bash
python3 <path-to-skill-workflow-manager>/scripts/manage_skill.py \
  --inspect-import \
  --import-path <downloaded-skill>
```

```bash
python3 <path-to-skill-workflow-manager>/scripts/manage_skill.py \
  --project-root <project-root> \
  --project-skills <skill-name>
```

```bash
python3 <path-to-skill-workflow-manager>/scripts/manage_skill.py \
  --bootstrap-project-layout \
  --project-root <project-root>
```

```bash
python3 <path-to-skill-workflow-manager>/scripts/manage_skill.py \
  --register-runtime-skill
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
- `--register-runtime-skill`
- `--runtime-skills-root <runtime-skills-root>`
- `--overwrite-skill-md`
- `--overwrite-openai`
- `--validate-only`
- `--skip-validate`
- `--dry-run`

## References

- Choose the reference file that matches the reader's language, and keep English and Chinese counterparts aligned when updating them.
- `references/use-cases.md` and `references/use-cases.zh-CN.md`: the main reader guides for workflow selection, task coverage, and CLI patterns
- `references/prompt-templates.en.md` and `references/prompt-templates.zh-CN.md`: slim prompt cheat sheets for direct reuse
