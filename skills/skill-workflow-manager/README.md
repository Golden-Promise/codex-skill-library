# skill-workflow-manager

[简体中文](README.zh-CN.md)

Manage Codex skills with a global-first workflow: keep canonical skills in `$CODEX_HOME/skills`, then expose selected ones to projects only when a project needs local discovery.

## The 3 Main Paths

- Create or refresh one shared skill in `$CODEX_HOME/skills`
- Adopt a downloaded local skill into that shared library
- Attach shared skills to a project through `<project-root>/.agents/skills`

## Advanced Paths

- Run `--doctor` / `--check` when you want a health check before changing anything
- Use `--validate-only` for release checks and CI
- Use `--list-library-skills` or `--list-project-skills` to inventory what already exists
- Use `--bootstrap-project-layout` only when you explicitly want a project-contained `_skill-library`

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

If you install it to another target root for manual inspection, Codex will not auto-discover it as a runtime skill. The recommended path for direct use is still the default install into `$CODEX_HOME/skills`.

## Quick Start In 5 Minutes

1. Install `skill-workflow-manager` into the default Codex shared library.
2. Create or adopt one shared skill in `$CODEX_HOME/skills`.
3. Attach that shared skill to one project through `.agents/skills`.
4. Run `--doctor` before cleanup, relinking, or release work.

## Platform Note

Project attachment depends on symlinks. On Windows or restricted filesystems, if link creation fails, check symlink permissions, developer mode, and whether the target filesystem supports symbolic links.

## Say This To Codex

- `Use $skill-workflow-manager to create or refresh <skill-name> in the shared library and validate it at the end.`
- `Use $skill-workflow-manager to adopt <import-path> into the shared library.`
- `Use $skill-workflow-manager to attach <skill-name> to <project-root>.`
- `Use $skill-workflow-manager to check <skill-name> and its project link in <project-root> before making changes.`

## Start Here

1. Read the main workflow guide in [references/use-cases.md](references/use-cases.md).
2. If you are new, follow the 5-minute quick start first.
3. Use [references/prompt-templates.en.md](references/prompt-templates.en.md) when you only need copy-ready wording.
4. Reach for project-local bootstrap only when the skill should live under one project rather than the global shared library.

## Common Commands

Create or refresh a shared-library skill:

```bash
python3 scripts/manage_skill.py \
  demo-skill \
  --purpose "Use this skill when the user wants help with demo-skill tasks."
```

Adopt a downloaded local skill into the shared library:

```bash
python3 scripts/manage_skill.py \
  --adopt <import-path>
```

Attach an existing shared-library skill to a project:

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

Validate the current package without writing files:

```bash
python3 scripts/manage_skill.py --validate-only
```

Bootstrap a project-local managed layout only when the skill should live inside one project:

```bash
python3 scripts/manage_skill.py \
  --bootstrap-project-layout \
  --project-root <project-root>
```

List library skills in machine-readable form:

```bash
python3 scripts/manage_skill.py \
  --list-library-skills \
  --format json
```

## What Is Inside

| Area | Purpose |
| --- | --- |
| `SKILL.md` | Runtime entry point for Codex |
| `agents/openai.yaml` | Metadata and default prompt wiring |
| `scripts/manage_skill.py` | Deterministic CLI for create, adopt, check, link, bootstrap, and validate flows |
| `references/` | Reader-facing workflow guides and prompt references |
| `docs/` | Maintainer-oriented notes for publishing this package |
| `tests/` | Regression coverage for the management script |

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
