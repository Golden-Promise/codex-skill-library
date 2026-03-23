# Skill Workflow Manager Use Cases

Chinese version: [use-cases.zh-CN.md](use-cases.zh-CN.md)

This is the main reader guide for `skill-workflow-manager`.
Use it to understand the workflow, choose the right mode, and find the matching CLI pattern.

## Start Here

- If you already know the workflow and only need copy-ready wording, open [prompt-templates.en.md](prompt-templates.en.md).
- Treat `$CODEX_HOME/skills` as the default shared library unless the user explicitly wants a project-local managed layout.
- If you need to choose the correct operation, start with the decision map below.
- Read-only modes can add `--format json` when you need machine-readable output for CI or automation.

## Decision Map

| Goal | Use this mode | Core flags |
| --- | --- | --- |
| Create or refresh one shared-library skill | Create or update | `<skill-name> --purpose "<purpose>"` |
| Preview risky changes first | Dry run | `--dry-run` |
| See what already exists | Inventory | `--list-library-skills` or `--list-project-skills` |
| Attach or repair project links | Project link | `--project-skills ...` or `<skill-name> --project-root ...` |
| Remove or exact-sync project links | Project cleanup | `--unlink-skills ...` or `--sync-project-skills ...` |
| Inspect a local skill before import | Import inspection | `--inspect-import --import-path <import-path>` |
| Adopt a downloaded local skill | Import | `--import-path <import-path>` |
| Turn a standalone package into a managed layout | Bootstrap | `--bootstrap-project-layout` |
| Validate an existing skill without writing files | Validation | `--validate-only` |

## Shared Placeholders

| Placeholder | Meaning |
| --- | --- |
| `<skill-dir>` | The directory that contains this skill package |
| `<skill-name>` | The canonical hyphen-case skill name |
| `<library-root>` | The canonical shared-library root, usually `$CODEX_HOME/skills` |
| `<project-root>` | The target project root |
| `<import-path>` | A downloaded local skill directory outside the library |
| `<purpose>` | The frontmatter description for the target skill |

## Working Rules

- Use create or update mode when the user wants to edit one canonical skill.
- Use inventory mode when the user wants to list library skills or project links.
- Use project-link mode when the skill already exists and the user only wants attachment changes.
- Use `--inspect-import` before importing an unfamiliar downloaded skill.
- Treat `$CODEX_HOME/skills` as the default canonical library and add project links only when needed.
- Use project-local bootstrap only when the user explicitly wants a skill to live inside one project.
- Use `copy` import mode by default. Use `move` only when the shared-library copy should become the sole source.

## 1. Create Or Refresh A Managed Skill

Use when:

- the user wants a new canonical skill scaffold
- the user wants to update metadata or regenerate one of the default files

Command pattern:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  <skill-name> \
  --purpose "<purpose>"
```

Notes:

- This is the default path for skills that should live in the shared Codex library.
- Add `--overwrite-skill-md` only when the user explicitly wants to rewrite the main template.
- Add `--overwrite-openai` only when `agents/openai.yaml` should be regenerated.
- Add `--project-root` only when the same request should also ensure a project link.
- For copy-ready request wording, see [prompt-templates.en.md](prompt-templates.en.md).

## 2. Preview Risky Changes

Use when:

- the task involves deletes, sync operations, relinking, or imports
- the user wants a preview before writing files

Command pattern:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  <skill-name> \
  --project-root <project-root> \
  --purpose "<purpose>" \
  --dry-run
```

Notes:

- Use `--dry-run` before bulk project cleanup or unfamiliar imports.
- For copy-ready request wording, see [prompt-templates.en.md](prompt-templates.en.md).

## 3. List Library Skills Or Project Links

Use when:

- the user wants to see which canonical skills already exist
- the user wants to audit one project's current links

Command patterns:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --list-library-skills
```

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --project-root <project-root> \
  --list-project-skills
```

Notes:

- Use the library listing before onboarding a project to existing skills.
- Use the project listing before cleanup, repair, or exact sync work.

## 4. Attach Or Repair Selected Project Links

Use when:

- the canonical skill already exists
- the project should discover one or more skills without copying them
- a project link is missing or stale

Command patterns:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --project-root <project-root> \
  --project-skills skill-workflow-manager,linux-command-coach
```

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  <skill-name> \
  --project-root <project-root>
```

Notes:

- Use `--project-skills` when attaching multiple existing skills.
- Use `<skill-name> --project-root ...` when the main need is to refresh one canonical skill and ensure its project link.

## 5. Remove Or Exact-Sync Project Links

Use when:

- the user wants to detach one or more skills from a project
- the user wants the project links to match an exact set

Command patterns:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --project-root <project-root> \
  --unlink-skills linux-command-coach
```

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --project-root <project-root> \
  --sync-project-skills skill-workflow-manager,git-commit-coach
```

Notes:

- `--unlink-skills` removes selected project links without deleting the canonical skill.
- `--sync-project-skills` is stronger: it makes the project match the exact chosen set.

## 6. Inspect A Downloaded Skill Before Import

Use when:

- the user wants to check structure, metadata, and conflict status first
- the user is unsure whether the import should use `copy` or `move`

Command pattern:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --inspect-import \
  --import-path <import-path> \
  --project-root <project-root>
```

Notes:

- This is the safest first step for an unfamiliar downloaded skill.
- If the source name conflicts, the script will suggest alternative canonical names.

## 7. Import A Downloaded Skill Into The Shared Library

Use when:

- the user already has a local skill directory outside the library
- the shared library should become the canonical source

Command pattern:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --import-path <import-path>
```

Notes:

- This is the default adoption path for a downloaded skill that should become part of the shared Codex library.
- Use `--import-mode move` only when the original download directory should stop being the source of truth.
- If the imported name conflicts, retry with an explicit positional `<skill-name>`.
- Add `--project-root <project-root>` only when the same request should also attach the imported skill to one project.
- When the import source lives outside the project root, the script records it in `.agents/skill-workflow-manager/external-sources.json`.

## 8. Bootstrap A Standalone Download Into A Managed Project Layout

Use when:

- the current directory contains a standalone downloaded skill package
- the project still needs `_skill-library` and `.agents/skills`

Command pattern:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --bootstrap-project-layout \
  --project-root <project-root>
```

Notes:

- This is not the default way to manage globally shared skills.
- If the script can infer the project root safely, `--project-root` may be omitted.
- This is the bridge from a standalone package to a project-local managed layout.
- When bootstrap adopts a standalone in-project package, it removes the original source folder after validation so the project does not keep two `skill-workflow-manager` directories.

## 9. Validate An Existing Skill Without Writing Files

Use when:

- you want a release check or CI-friendly validation pass
- you want to validate the current package, a canonical skill, or an import candidate without modifying anything

Command patterns:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --validate-only
```

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  <skill-name> \
  --library-root <library-root> \
  --validate-only
```

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --import-path <import-path> \
  --validate-only
```

Notes:

- With no explicit target, the script validates the package that contains `manage_skill.py`.
- With `<skill-name>`, the script validates the canonical skill under `<library-root>/<skill-name>`.
- With `--import-path`, the script validates that directory directly.
