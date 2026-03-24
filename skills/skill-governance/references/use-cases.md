# skill-governance task guide

Chinese version: [use-cases.zh-CN.md](use-cases.zh-CN.md)

Use this page when you want quick command patterns for the most common tasks.

## The Short Version

- `manage`: inspect a project directory, adopt local skills, and build the managed layout
- `setup`: create the project management skeleton
- `add`: create or adopt a skill
- `enable`: expose a skill to one project
- `doctor`: inspect health and governance state
- `repair`: apply only safe automatic fixes
- `audit`: write or verify platform state for CI
- `document`: fill missing `SKILL.md` sections
- `upgrade`: refresh a managed skill from a local package
- `retire`: remove a project exposure

## Most Common Flows

Take over skill management for a project directory:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  manage <project-root>
```

Set up a clean project management skeleton:

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

Adopt a downloaded local package into one project:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  add <import-path> \
  --project <project-root>
```

Enable an existing skill for a project:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  enable <skill-name> \
  --project <project-root>
```

Check before cleanup, relinking, or release:

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

Force a full `SKILL.md` rewrite:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  document <skill-name> \
  --library-root <library-root> \
  --overwrite-skill-md
```

Persist or verify platform state:

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  audit \
  --workspace-root <workspace-root> \
  --sync-platform-state
```

## Automatic Decisions

- `manage` discovers local skill packages and adopts them into the managed project structure.
- `setup` creates the project-owned library, exposure root, and platform state directories.
- No `--project`: default to the shared library.
- With `--project`: `add` prefers project-owned storage.
- `auto` exposure mode chooses `manifest` in CI, `copy` on Windows, and `symlink` on Linux/macOS.
- `enable`, `doctor`, `repair`, and `retire` can infer the project root from the current working directory.
- `document` preserves existing sections unless you explicitly request `--overwrite-skill-md`.

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

- [prompt-templates.en.md](prompt-templates.en.md): copy-ready prompts
- [prompt-templates.zh-CN.md](prompt-templates.zh-CN.md): Chinese prompt templates
