# skill-governance

[简体中文](README.zh-CN.md)

`skill-governance` is a task-first governance tool for Codex skills.
Use it to add, enable, check, repair, audit, document, upgrade, or retire skills without manually managing storage paths, project exposure, or platform state.

## What It Is Best For

- adding a new reusable skill
- adopting a downloaded local skill package
- enabling a skill inside one project
- checking skill health before cleanup, relinking, upgrade, or release
- repairing safe project exposure issues
- keeping registry, lifecycle, and dependency state ready for CI

If you are unsure where to start, use `add`, `enable`, and `doctor`.

## Install

Install the latest package from this repository:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo <owner>/codex-skill-library \
  --path skills/skill-governance
```

Install the current release:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo <owner>/codex-skill-library \
  --path skills/skill-governance \
  --ref v0.3.0
```

Natural-language install request inside Codex:

```text
Use skill-installer to install skill-governance from <owner>/codex-skill-library at skills/skill-governance.
```

## Quick Start

Add a reusable shared skill:

```bash
python3 scripts/manage_skill.py \
  add demo-skill \
  --purpose "Use this skill when the user wants help with demo-skill tasks."
```

Adopt a downloaded skill into one project:

```bash
python3 scripts/manage_skill.py \
  add <import-path> \
  --project <project-root>
```

Enable a skill for a project:

```bash
python3 scripts/manage_skill.py \
  enable demo-skill \
  --project <project-root>
```

Check health before you change anything:

```bash
python3 scripts/manage_skill.py \
  doctor demo-skill \
  --project <project-root>
```

## Main Tasks

| Task | What it does |
| --- | --- |
| `add` | Create a new skill or adopt a downloaded local package |
| `enable` | Expose an existing skill to one project |
| `doctor` | Score health, detect overlap, analyze impact, and produce repair suggestions |
| `repair` | Apply only the current `safe_auto_fix` queue |
| `audit` | Persist or verify registry, lifecycle, and dependency state for CI or release checks |
| `document` | Fill missing `SKILL.md` sections by default; use `--overwrite-skill-md` for a full rewrite |
| `upgrade` | Refresh a managed skill from a local source package |
| `retire` | Remove a managed project exposure without deleting the canonical skill |

## What The Tool Decides Automatically

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
