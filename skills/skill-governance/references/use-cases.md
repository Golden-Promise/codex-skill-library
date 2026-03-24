# skill-governance command reference

Chinese version: [use-cases.zh-CN.md](use-cases.zh-CN.md)

Use this page for command syntax and advanced usage. If you are new, start with [../README.md](../README.md) and [prompt-templates.en.md](prompt-templates.en.md).

## Common Commands

- `manage`: inspect a project directory, find local skills, and bring them under `skill-governance`
- `setup`: create the project folders needed for skill governance
- `add`: create a new skill or bring in a local package
- `enable`: make a managed skill available in one project
- `doctor`: check health and overlap before cleanup, relinking, upgrade, or release
- `repair`: apply only safe automatic fixes
- `audit`: write or verify registry and dependency graph for CI or release checks
- `document`: fill missing `SKILL.md` sections; use `--overwrite-skill-md` to rewrite the whole file
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

## What The Command Decides For You

- `manage` finds local skill packages and organizes them for you.
- `setup` creates the project skill folders and platform state folders.
- Without `--project`, `add` uses the shared library.
- With `--project`, `add` keeps the skill with that project.
- `auto` mode chooses `manifest` in CI, `copy` on Windows, and `symlink` on Linux/macOS.
- `enable`, `doctor`, `repair`, and `retire` can infer the project root from the current working directory.
- `document` preserves existing sections unless you explicitly ask for `--overwrite-skill-md`.

## Optional Repo Config

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

## Related Files

- [README.md](../README.md): start here if you are new
- [prompt-templates.en.md](prompt-templates.en.md): copy-ready requests
- [prompt-templates.zh-CN.md](prompt-templates.zh-CN.md): Chinese copy-ready requests
