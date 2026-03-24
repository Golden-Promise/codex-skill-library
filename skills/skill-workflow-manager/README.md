# skill-workflow-manager

[简体中文](README.zh-CN.md)

`skill-workflow-manager` is a lifecycle manager for Codex skills. Its product focus is now explicit:

- manage shared skills that live in `$CODEX_HOME/skills`
- manage project-managed skills that live in `<project-root>/_skill-library`
- move cleanly between standalone downloads, shared libraries, and project-contained layouts

It is not only a shared-library helper and not only a project bootstrap tool. It is the bridge between both models.

## Product Positioning

Use this package when you want one skill to handle:

- reusable cross-project skills
- private or project-specific skills that should stay versioned with one repository
- adoption of downloaded skills into a managed location
- project link maintenance through `.agents/skills`
- release checks, diagnostics, and cleanup before risky changes

## Choose A Mode First

| Mode | Best when | Canonical location | Project exposure |
| --- | --- | --- | --- |
| Shared skill | The skill should be reused across projects | `$CODEX_HOME/skills/<skill-name>` | Optional link in `<project-root>/.agents/skills/<skill-name>` |
| Project-managed skill | The skill is private, pinned, or evolves with one project | `<project-root>/_skill-library/<skill-name>` | Link in the same project's `.agents/skills/<skill-name>` |

If you are unsure, start with the shared mode. Reach for the project-managed mode only when the skill should clearly live with one repository.

## What This Package Can Do

- create a new shared skill
- create a new project-managed skill
- adopt a downloaded local skill into the shared library
- adopt a downloaded local skill into a project-managed library
- attach one or more shared skills to a project without copying them
- bootstrap a standalone package into a project-managed layout
- diagnose duplicates, broken links, missing files, and structural issues before cleanup or release

## Install

Install the latest version from `codex-skill-library`:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo <owner>/codex-skill-library \
  --path skills/skill-workflow-manager
```

Install the published `v0.2.0` release:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo <owner>/codex-skill-library \
  --path skills/skill-workflow-manager \
  --ref v0.2.0
```

Install from a GitHub tree URL:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --url https://github.com/<owner>/codex-skill-library/tree/main/skills/skill-workflow-manager
```

Install with Codex using the `skill-installer` skill:

- Ask Codex: `Use the skill-installer skill to install skill-workflow-manager from Golden-Promise/codex-skill-library at skills/skill-workflow-manager.`
- For the published release, ask: `Use the skill-installer skill to install skill-workflow-manager from Golden-Promise/codex-skill-library at skills/skill-workflow-manager using ref v0.2.0.`

For direct runtime use, the recommended destination is still the default Codex shared library in `$CODEX_HOME/skills`.

## Quick Start

### Shared Skill Path

1. Install `skill-workflow-manager` into the default Codex shared library.
2. Create or adopt one shared skill in `$CODEX_HOME/skills`.
3. Attach that shared skill to a project only if the project needs local discovery.
4. Run `--doctor` before cleanup, relinking, or release work.

### Project-Managed Skill Path

1. Choose one project that should own the skill.
2. Create or adopt the skill into `<project-root>/_skill-library`.
3. Link it through the same project's `.agents/skills`.
4. Use bootstrap only when converting a standalone package into that managed layout.

## Say This To Codex

- `Use $skill-workflow-manager to create or refresh <skill-name> as a shared skill in $CODEX_HOME/skills and validate it at the end.`
- `Use $skill-workflow-manager to create <skill-name> as a project-managed skill inside <project-root>/_skill-library and link it to that project.`
- `Use $skill-workflow-manager to adopt <import-path> into the shared library.`
- `Use $skill-workflow-manager to adopt <import-path> into <project-root>/_skill-library and link it to that project.`
- `Use $skill-workflow-manager to attach <skill-name> to <project-root> without copying the real skill.`
- `Use $skill-workflow-manager to check <skill-name> and its project link in <project-root> before making changes.`

## Common Commands

Create or refresh a shared skill:

```bash
python3 scripts/manage_skill.py \
  demo-skill \
  --purpose "Use this skill when the user wants help with demo-skill tasks."
```

Create or refresh a project-managed skill:

```bash
python3 scripts/manage_skill.py \
  demo-skill \
  --library-root <project-root>/_skill-library \
  --project-root <project-root> \
  --purpose "Use this skill when the user wants help with demo-skill tasks."
```

Adopt a downloaded local skill into the shared library:

```bash
python3 scripts/manage_skill.py \
  --adopt <import-path>
```

Adopt a downloaded local skill into a project-managed library:

```bash
python3 scripts/manage_skill.py \
  --adopt <import-path> \
  --library-root <project-root>/_skill-library \
  --project-root <project-root>
```

Attach an existing shared skill to a project:

```bash
python3 scripts/manage_skill.py \
  --project-root <project-root> \
  --project-skills demo-skill
```

Check one skill and its project link before changing anything:

```bash
python3 scripts/manage_skill.py \
  demo-skill \
  --project-root <project-root> \
  --doctor
```

Bootstrap a standalone package into a project-managed layout:

```bash
python3 scripts/manage_skill.py \
  --bootstrap-project-layout \
  --project-root <project-root>
```

Validate the current package without writing files:

```bash
python3 scripts/manage_skill.py --validate-only
```

## Platform Note

Project attachment depends on symlinks. On Windows or restricted filesystems, if link creation fails, check symlink permissions, developer mode, and whether the target filesystem supports symbolic links.

## What Is Inside

| Area | Purpose |
| --- | --- |
| `SKILL.md` | Runtime entry point for Codex |
| `agents/openai.yaml` | Metadata and default prompt wiring |
| `scripts/manage_skill.py` | Deterministic CLI for shared-mode and project-managed skill flows |
| `references/` | Reader-facing workflow guides and prompt references |
| `docs/` | Maintainer-oriented notes for publishing this package |
| `tests/` | Regression coverage for the management script |

## Start Here

1. Read the main workflow guide in [references/use-cases.md](references/use-cases.md).
2. Choose the mode first: shared skill or project-managed skill.
3. Use [references/prompt-templates.en.md](references/prompt-templates.en.md) when you only need copy-ready wording.
4. Use bootstrap only when you are converting a standalone package into a project-managed layout.

## Reader Guide

- Main workflow guide: [references/use-cases.md](references/use-cases.md)
- 中文工作流说明: [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- English prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- 中文提示词模板: [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- Package publishing notes: [docs/publishing-with-skill-installer.md](docs/publishing-with-skill-installer.md)
- 中文发布说明: [docs/publishing-with-skill-installer.zh-CN.md](docs/publishing-with-skill-installer.zh-CN.md)

## For Maintainers

- Repository home: [../../README.md](../../README.md)
- Repository publishing guide: [../../docs/publishing.md](../../docs/publishing.md)
- Run checks before release:

```bash
python3 scripts/manage_skill.py --validate-only
python3 -m unittest discover -s tests -p 'test_*.py' -v
```
