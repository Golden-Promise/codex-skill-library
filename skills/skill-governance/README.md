# skill-governance

[简体中文](README.zh-CN.md)

`skill-governance` is a task-first governance tool for Codex skills.
Use it to add, enable, check, repair, audit, document, upgrade, or retire skills without manually managing storage paths, project exposure, or platform state.

## What It Is Best For

- taking over skill management for an existing project directory
- setting up a clean skill governance skeleton for one project
- adding a new reusable skill
- adopting a downloaded local skill package
- enabling a skill inside one project
- checking skill health before cleanup, relinking, upgrade, or release
- repairing safe project exposure issues
- keeping registry, lifecycle, and dependency state ready for CI

If you are unsure where to start, use `manage`, `setup`, and `doctor`.

## Install

Install the latest package from this repository:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-governance
```

Install the current release:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-governance \
  --ref v0.5.0
```

Natural-language install request inside Codex:

```text
Use skill-installer to install skill-governance from Golden-Promise/codex-skill-library at skills/skill-governance.
```

## Quick Start

If you have just installed `skill-governance`, start with one of these two requests inside Codex:

- `Take over skill management for this directory and organize any local skills into the managed project structure.`
- `Set up skill governance for this project and create the management skeleton.`

That is the fastest path for most users.

If you already know which managed skill you want to work on next, then ask for:

- `Run doctor for this project before I clean up or relink skills.`
- `Enable <skill-name> for this project.`
- `Add a new reusable skill to the shared library.`

If you prefer direct command patterns, use [references/use-cases.md](references/use-cases.md).

## Main Tasks

| Task | What it does |
| --- | --- |
| `manage` | Inspect one project directory, discover local skill packages, adopt them into managed storage, and build the project structure |
| `setup` | Create the project skill governance skeleton without taking over local skill packages |
| `add` | Create a new skill or adopt a downloaded local package |
| `enable` | Expose an existing skill to one project |
| `doctor` | Score health, detect overlap, analyze impact, and produce repair suggestions |
| `repair` | Apply only the current `safe_auto_fix` queue |
| `audit` | Persist or verify registry, lifecycle, and dependency state for CI or release checks |
| `document` | Fill missing `SKILL.md` sections by default; use `--overwrite-skill-md` for a full rewrite |
| `upgrade` | Refresh a managed skill from a local source package |
| `retire` | Remove a managed project exposure without deleting the canonical skill |

## What The Tool Decides Automatically

- `manage` inspects the target directory, discovers local skill packages, and builds the managed project layout for you.
- `setup` creates the project-owned library, exposure root, and platform state layout for you.
- Without `--project`, skills default to the shared library.
- With `--project`, `add` prefers project-owned storage.
- Exposure mode `auto` currently chooses:
  - `manifest` in CI
  - `copy` on Windows
  - `symlink` on Linux and macOS
- `enable`, `doctor`, `repair`, and `retire` can infer the project root when you run them inside the target project.
- `document` preserves existing sections and only fills missing ones unless you explicitly ask for a full rewrite.

## Governance Output

`doctor` reports:

- health score and quality dimensions
- similar or overlapping skills
- impacted projects and workspace reference graph
- governance suggestions and action suggestions
- `repair_plan`, `work_queue`, and `batch_repair_preview`

`repair` only applies `safe_auto_fix`. It does not auto-run manual cleanup or governance review actions.

`audit` writes or checks:

- `.skill-platform/registry.json`
- `.skill-platform/dependency-graph.json`

`audit` also acts as a CI gate for governance metadata:

- `active`, `review`, `deprecated`, and `blocked` skills should carry an `owner`
- `active`, `review`, `deprecated`, and `blocked` skills should carry a semver-like `version`
- `review` skills should also carry a `reviewer`
- `active` and `review` skills should usually carry a `team`

You can set these fields during task flows such as `add`, `enable`, or `upgrade`:

```bash
python3 scripts/manage_skill.py \
  add demo-skill \
  --purpose "Use this skill when the user wants help with demo skill tasks." \
  --owner "platform@example.com" \
  --team "core-platform" \
  --version "1.2.0"
```

## Optional Repo Config

Use `skill-governance.toml` in the project root when you want custom paths:

```toml
[skill_registry]
shared_root = ".platform/skills/shared"
project_root = ".platform/skills/project"
exposure_root = ".agents/skills"
exposure_mode = "auto"
workspace_root = ".."
platform_root = ".skill-platform"
```

The older filename `skill-workflow.toml` is still accepted for compatibility.

## Read More

- Task guide: [references/use-cases.md](references/use-cases.md)
- 中文任务说明: [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- Prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- 中文提示词模板: [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- Maintainer publishing notes: [docs/publishing-with-skill-installer.md](docs/publishing-with-skill-installer.md)
