---
name: skill-workflow-manager
description: Use this skill when the user wants to create, update, adopt, diagnose, attach, or bootstrap a Codex skill. It manages both shared skills in $CODEX_HOME/skills and project-managed skills inside project _skill-library directories with consistent metadata and link handling.
---

# Skill Workflow Manager

## Purpose

Manage the lifecycle of two explicit kinds of Codex skills:

1. Shared skills in `$CODEX_HOME/skills`
2. Project-managed skills in `<project-root>/_skill-library`

Use this skill for skill lifecycle work only.

## Use This Skill When

- create or update a shared skill meant for reuse across projects
- create or update a project-managed skill that should live with one repository
- adopt a downloaded local skill into either the shared library or a project-managed library
- attach, detach, or exact-sync project discovery links
- run a health check for a skill directory or project link before risky changes
- bootstrap a standalone package into a project-managed layout

Do not use this skill for unrelated coding tasks.

## Operating Modes

### Shared Skill

- Canonical location: `$CODEX_HOME/skills/<skill-name>`
- Best when the skill should be reused across projects
- Project exposure is optional through `<project-root>/.agents/skills/<skill-name>`

### Project-Managed Skill

- Canonical location: `<project-root>/_skill-library/<skill-name>`
- Best when the skill is private, project-specific, or should evolve with one repository
- Project exposure still uses `<project-root>/.agents/skills/<skill-name>`

## Workflow

1. Choose the mode first: shared skill or project-managed skill.
2. Prefer the shared mode when the user wants reuse across projects.
3. Prefer the project-managed mode when the skill should stay versioned with one project.
4. Use `scripts/manage_skill.py` for deterministic filesystem work.
5. Use `--library-root <project-root>/_skill-library` for explicit project-managed create or adopt flows.
6. Use `--bootstrap-project-layout` only when converting a standalone package into a managed project layout.
7. Use `--doctor` / `--check`, `--inspect-import`, or `--dry-run` before risky changes.
8. Update `SKILL.md` and `agents/openai.yaml` together.
9. Report the chosen mode, canonical path, project links changed, and validation or doctor results.

## Rules

- Do not silently switch a skill from shared mode to project-managed mode, or the reverse.
- Never create duplicate canonical copies in the same mode unless the user explicitly wants a separate variant.
- Treat project links as opt-in. Link only the requested skills.
- Stop on name conflicts or non-symlink blockers; do not overwrite silently.
- Prefer incremental edits over rewriting a skill unless the user clearly wants a reset.

## Script Patterns

Use `scripts/manage_skill.py` with portable placeholders:

Shared create:

```bash
python3 <path-to-skill-workflow-manager>/scripts/manage_skill.py \
  <skill-name> \
  --purpose "<purpose>"
```

Project-managed create:

```bash
python3 <path-to-skill-workflow-manager>/scripts/manage_skill.py \
  <skill-name> \
  --library-root <project-root>/_skill-library \
  --project-root <project-root> \
  --purpose "<purpose>"
```

Shared adopt:

```bash
python3 <path-to-skill-workflow-manager>/scripts/manage_skill.py \
  --adopt <downloaded-skill>
```

Project-managed adopt:

```bash
python3 <path-to-skill-workflow-manager>/scripts/manage_skill.py \
  --adopt <downloaded-skill> \
  --library-root <project-root>/_skill-library \
  --project-root <project-root>
```

Attach shared skills to a project:

```bash
python3 <path-to-skill-workflow-manager>/scripts/manage_skill.py \
  --project-root <project-root> \
  --project-skills <skill-name>
```

Check before changing:

```bash
python3 <path-to-skill-workflow-manager>/scripts/manage_skill.py \
  <skill-name> \
  --project-root <project-root> \
  --doctor
```

Bootstrap a standalone package into a project-managed layout:

```bash
python3 <path-to-skill-workflow-manager>/scripts/manage_skill.py \
  --bootstrap-project-layout \
  --project-root <project-root>
```

Validate without writing:

```bash
python3 <path-to-skill-workflow-manager>/scripts/manage_skill.py \
  --validate-only
```

Key flags:

- `--adopt <downloaded-skill>`
- `--import-path <downloaded-skill>` as the explicit equivalent of `--adopt`
- `--doctor` / `--check`
- `--inspect-import`
- `--list-library-skills`
- `--list-project-skills --project-root <project-root>`
- `--project-skills skill-a,skill-b`
- `--unlink-skills skill-a`
- `--sync-project-skills skill-a,skill-b`
- `--library-root <project-root>/_skill-library` for explicit project-managed flows
- `--format json` for read-only modes
- `--dry-run`

## References

- Choose the reference file that matches the reader's language, and keep English and Chinese counterparts aligned when updating them.
- `references/use-cases.md` and `references/use-cases.zh-CN.md`: the main reader guides for mode selection, workflow choice, and CLI patterns
- `references/prompt-templates.en.md` and `references/prompt-templates.zh-CN.md`: slim prompt cheat sheets for direct reuse
