# Skill Workflow Manager Use Cases

Chinese version: [use-cases.zh-CN.md](use-cases.zh-CN.md)

This is the main reader guide for `skill-workflow-manager`.
Use it to choose a mode first, then choose the right operation inside that mode.

## Start Here

- `skill-workflow-manager` supports two explicit modes: shared skills and project-managed skills.
- If you already know the workflow and only need copy-ready wording, open [prompt-templates.en.md](prompt-templates.en.md).
- If you are unsure which mode to use, start with the mode selector below.
- Read-only modes can add `--format json` when you need machine-readable output for CI or automation.

## Mode Selector

| Mode | Choose it when | Canonical location | Typical follow-up |
| --- | --- | --- | --- |
| Shared skill | The skill should be reused across projects | `$CODEX_HOME/skills/<skill-name>` | Optionally link it into one or more projects |
| Project-managed skill | The skill is private, pinned, or should evolve with one repository | `<project-root>/_skill-library/<skill-name>` | Link it inside the same project |

## Most Common Paths

| Goal | Best first move | Typical command |
| --- | --- | --- |
| Create a reusable shared skill | Shared create | `<skill-name> --purpose "<purpose>"` |
| Create a project-specific skill | Project-managed create | `<skill-name> --library-root <project-root>/_skill-library --project-root <project-root>` |
| Adopt a downloaded skill into the shared library | Shared adopt | `--adopt <import-path>` |
| Adopt a downloaded skill into a project-managed library | Project-managed adopt | `--adopt <import-path> --library-root <project-root>/_skill-library --project-root <project-root>` |
| Expose an existing shared skill to one project | Project link | `--project-skills ... --project-root <project-root>` |
| Diagnose a skill or project link before changing anything | Doctor | `--doctor` |

## Shared Placeholders

| Placeholder | Meaning |
| --- | --- |
| `<skill-dir>` | The directory that contains this skill package |
| `<skill-name>` | The canonical hyphen-case skill name |
| `<library-root>` | The chosen canonical library root |
| `<project-root>` | The target project root |
| `<import-path>` | A downloaded local skill directory outside the chosen library |
| `<purpose>` | The frontmatter description for the target skill |

## Working Rules

- Choose the mode first. Do not blur shared and project-managed flows together.
- Prefer the shared mode when the skill should survive beyond one repository.
- Prefer the project-managed mode when the skill should stay private or versioned with one project.
- Use `--inspect-import`, `--doctor`, or `--dry-run` before risky changes.
- Use `copy` import mode by default. Use `move` only when the adopted copy should become the sole source.
- Treat project links as exposure paths, not as the canonical source of truth.

## 1. Create Or Refresh A Shared Skill

Use when:

- the skill should live in `$CODEX_HOME/skills`
- the user wants one canonical copy reused across projects

Command pattern:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  <skill-name> \
  --purpose "<purpose>"
```

Notes:

- This is the default mode for reusable skills.
- Add `--project-root` only when the same request should also ensure a project link.
- Add `--overwrite-skill-md` or `--overwrite-openai` only when the user explicitly wants template regeneration.

## 2. Create Or Refresh A Project-Managed Skill

Use when:

- the skill should stay inside one repository
- the project should own the canonical copy

Command pattern:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  <skill-name> \
  --library-root <project-root>/_skill-library \
  --project-root <project-root> \
  --purpose "<purpose>"
```

Notes:

- This creates the canonical copy inside the project rather than in `$CODEX_HOME/skills`.
- The project link is still maintained through `.agents/skills`.
- Use this mode for private, pinned, or repository-specific skills.

## 3. Adopt A Downloaded Skill Into The Shared Library

Use when:

- the user already has a local skill directory outside the shared library
- the shared library should become the canonical source

Command pattern:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --adopt <import-path>
```

Notes:

- This is the default adoption path for a downloaded skill that should become reusable across projects.
- `--import-path <import-path>` remains available as the explicit equivalent of `--adopt <import-path>`.
- Add `--project-root <project-root>` only when the same request should also attach the adopted skill to one project.

## 4. Adopt A Downloaded Skill Into A Project-Managed Library

Use when:

- the user already has a local skill directory outside the target project
- that project should own the canonical copy

Command pattern:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --adopt <import-path> \
  --library-root <project-root>/_skill-library \
  --project-root <project-root>
```

Notes:

- This is the project-managed equivalent of the shared adopt flow.
- Use this when the project should vendor the skill instead of reusing a global copy.
- If the import name conflicts, retry with an explicit positional `<skill-name>`.

## 5. Inspect A Downloaded Skill Before Adoption

Use when:

- the user wants to check structure, metadata, and name conflicts before adopting
- the user is unsure whether the target should be shared or project-managed

Command patterns:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --inspect-import \
  --adopt <import-path>
```

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --inspect-import \
  --adopt <import-path> \
  --project-root <project-root>
```

Notes:

- This is the safest first step for an unfamiliar downloaded skill.
- The inspection tells you whether the structure is valid and whether the canonical name conflicts.

## 6. Attach Or Repair Project Links

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
- This operation works with both shared skills and project-managed skills, as long as the chosen canonical library root is correct.

## 7. Remove Or Exact-Sync Project Links

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

## 8. Check A Skill Before Changing It

Use when:

- the user wants to know whether one skill is structurally healthy before editing, adopting, or linking it
- the user wants to check whether a project link is missing, broken, blocked, or pointing to the wrong place

Command patterns:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --doctor
```

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  <skill-name> \
  --project-root <project-root> \
  --doctor
```

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --adopt <import-path> \
  --doctor
```

Notes:

- `--doctor` is the fastest read-only way to answer "is this skill healthy and discoverable?"
- It supports `--format json` for automation.
- It exits non-zero when it finds blocking issues.

## 9. Bootstrap A Standalone Package Into A Project-Managed Layout

Use when:

- the current directory contains a standalone downloaded skill package
- the end state should be a project-managed layout

Command pattern:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --bootstrap-project-layout \
  --project-root <project-root>
```

Notes:

- This is not the default way to create shared skills.
- This is the bridge from a standalone package to a project-managed layout.
- When bootstrap adopts a standalone in-project package, it removes the original source folder after validation so the project does not keep two copies.

## 10. Inventory Existing Skills

Use when:

- the user wants to see which canonical skills already exist
- the user wants to audit one project's current links before cleanup or repair

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

## 11. Validate Without Writing Files

Use when:

- you want a release check or CI-friendly validation pass
- you want to validate the current package, a canonical skill, or an adoption candidate without modifying anything

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
  --adopt <import-path> \
  --validate-only
```

Notes:

- With no explicit target, the script validates the package that contains `manage_skill.py`.
- With `<skill-name>`, the script validates the canonical skill under `<library-root>/<skill-name>`.
- With `--adopt` or `--import-path`, the script validates that directory directly.
