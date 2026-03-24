# skill-governance command reference

Chinese version: [use-cases.zh-CN.md](use-cases.zh-CN.md)

This page is the command reference for `skill-governance`. It collects install commands, task entry points, command patterns, automatic behavior, governance checks, and repository configuration.

If you are new to the package, start with [../README.md](../README.md) and [prompt-templates.en.md](prompt-templates.en.md). The README stays natural-language-first, so the install commands live here.

## Install Commands

Install the latest package from this repository:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-governance
```

Install a specific tagged release:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-governance \
  --ref v0.5.0
```

## Task Entry Points

- `manage`: inspect a project directory, discover local skills, and adopt them into `skill-governance`
- `setup`: create the project folders used for governance
- `add`: create a new skill or import a local package
- `enable`: expose a managed skill in one project
- `doctor`: check health and overlap before cleanup, relinking, upgrade, or release
- `repair`: apply only safe automatic fixes
- `audit`: write or verify the registry and dependency graph for CI or release checks
- `document`: fill missing `SKILL.md` sections; use `--overwrite-skill-md` to rewrite the file
- `upgrade`: refresh a managed skill from a local source package
- `retire`: remove a skill from one project without deleting the shared copy

## Command Patterns

Take over skill management for a project directory:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  manage <project-root>
```

Set up the project folders for skill governance:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  setup <project-root>
```

Add a reusable shared skill:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  add <skill-name> \
  --purpose "<purpose>"
```

Bring a local package into one project:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  add <import-path> \
  --project <project-root>
```

Make an existing skill available in a project:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  enable <skill-name> \
  --project <project-root>
```

Check a skill before cleanup, relinking, or release:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  doctor <skill-name> \
  --project <project-root>
```

Apply safe automatic fixes:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  repair <skill-name> \
  --workspace-root <workspace-root>
```

Refresh missing `SKILL.md` sections:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  document <skill-name> \
  --library-root <library-root>
```

Rewrite the whole `SKILL.md` file:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  document <skill-name> \
  --library-root <library-root> \
  --overwrite-skill-md
```

Write or verify platform state:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  audit \
  --workspace-root <workspace-root> \
  --sync-platform-state
```

## Automatic Decisions

- `manage` finds local skill packages and organizes them.
- `setup` creates the project skill folders and governance state folders.
- Without `--project`, `add` uses the shared library.
- With `--project`, `add` keeps the skill with that project.
- `auto` mode chooses `manifest` in CI, `copy` on Windows, and `symlink` on Linux or macOS.
- `enable`, `doctor`, `repair`, and `retire` can infer the project root from the current working directory.
- `document` preserves existing sections unless you explicitly ask for `--overwrite-skill-md`.

## Governance Outputs and Checks

`doctor` reports:

- health score and quality dimensions
- similar or overlapping skills
- impacted projects and workspace reference graph
- governance suggestions and next actions
- `repair_plan`, `work_queue`, and `batch_repair_preview`

`repair` applies only `safe_auto_fix`.

`audit` writes or checks:

- `.skill-platform/registry.json`
- `.skill-platform/dependency-graph.json`

`audit` also enforces governance metadata for CI and release checks:

- `active`, `review`, `deprecated`, and `blocked` skills should carry an `owner`
- `active`, `review`, `deprecated`, and `blocked` skills should carry a semver-like `version`
- `review` skills should also carry a `reviewer`
- `active` and `review` skills should usually carry a `team`

Example:

```bash
python3 scripts/manage_skill.py \
  add demo-skill \
  --purpose "Use this skill when the user wants help with demo skill tasks." \
  --owner "platform@example.com" \
  --team "core-platform" \
  --version "1.2.0"
```

## Repository Configuration

Use `skill-governance.toml` when you want custom paths:

```toml
[skill_registry]
shared_root = ".platform/skills/shared"
project_root = ".platform/skills/project"
exposure_root = ".agents/skills"
exposure_mode = "auto"
workspace_root = ".."
platform_root = ".skill-platform"
```

The older filename `skill-workflow.toml` is still accepted.

## Related Documentation

- [README.md](../README.md): start here if you are new
- [prompt-templates.en.md](prompt-templates.en.md): copy-ready requests
- [prompt-templates.zh-CN.md](prompt-templates.zh-CN.md): Chinese copy-ready requests
