# skill-governance

[简体中文](README.zh-CN.md)

## What It Is

`skill-governance` helps you manage Codex skills with less guesswork.
Use it when you want to take over an existing project, set up a clean skill workflow, add or enable a skill, or check everything is safe before cleanup or release.

## Best For

It is especially useful when you are:

- stepping into a project that already has local skills
- setting up skill governance for a new project
- adding a reusable skill you want to keep and reuse later
- enabling one skill for one project without touching everything else
- checking health before cleanup, relinking, upgrade, or release
- preparing skill metadata for CI or release checks

If you are new to the tool, start with `manage`, `setup`, and `doctor`.

## Install

In Codex, the simplest way to ask is just:

“Use skill-installer to install skill-governance from Golden-Promise/codex-skill-library at skills/skill-governance.”

If you want a specific release, add the version you want:

“Use skill-installer to install skill-governance from Golden-Promise/codex-skill-library at skills/skill-governance using ref v0.5.0.”

If you prefer exact command patterns, use [references/use-cases.md](references/use-cases.md).

## Quick Start

Your first three moves are usually:

1. Take over an existing project directory: `Take over skill management for this directory and organize any local skills for me.`
2. Set up a project from scratch: `Set up skill governance for this project.`
3. Check before cleanup or release: `Check this project before I clean up or relink skills.`

## What You Can Ask Next

Once the basics are in place, you can ask `skill-governance` to help with:

- adding a new skill
- enabling a skill in one project
- repairing safe issues
- auditing registry or dependency state
- documenting an existing skill
- upgrading or retiring a skill

If you want direct command patterns and more detailed examples, use [references/use-cases.md](references/use-cases.md).

## Main Tasks

| Task | What it does |
| --- | --- |
| `manage` | Review a project directory, find local skill packages, and bring them under managed skill governance |
| `setup` | Create a clean skill-management skeleton for one project |
| `add` | Create a new skill or bring an existing local package into management |
| `enable` | Make one managed skill available to one project |
| `doctor` | Score health, detect overlap, analyze impact, and produce repair suggestions |
| `repair` | Apply only the current `safe_auto_fix` queue |
| `audit` | Persist or verify registry, lifecycle, and dependency state for CI or release checks |
| `document` | Fill missing `SKILL.md` sections by default; use `--overwrite-skill-md` for a full rewrite |
| `upgrade` | Refresh a managed skill from a local source package |
| `retire` | Remove a skill from one project without deleting the shared copy |

## What the Tool Decides Automatically

- `manage` inspects the target directory, discovers local skill packages, and organizes them into the project's managed layout for you.
- `setup` creates the project skill folders and governance state folders for you.
- Without `--project`, new skills default to the shared library.
- With `--project`, `add` prefers to keep the skill with that project.
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
- governance suggestions and next actions
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

## Advanced Setup

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
