# skill-workflow-manager

[简体中文](README.zh-CN.md)

Maintain Codex skills with one canonical source, optional project discovery links, and a shared-library workflow that stays consistent over time.

## What This Package Helps With

- creating or refreshing a canonical skill package
- importing a downloaded local skill into a managed library
- attaching, detaching, or syncing project discovery links
- bootstrapping a managed project layout for skills without leaving a duplicate source folder behind
- validating an existing skill package without writing files

## Best For

This package is especially useful when you want one source of truth for a skill while still exposing it to one or more projects through lightweight links.

## Install

Install the latest version from `codex-skill-library`:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo <owner>/codex-skill-library \
  --path skills/skill-workflow-manager
```

Install the published `v0.1.0` release:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo <owner>/codex-skill-library \
  --path skills/skill-workflow-manager \
  --ref v0.1.0
```

Install from a GitHub tree URL:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --url https://github.com/<owner>/codex-skill-library/tree/main/skills/skill-workflow-manager
```

Install with Codex using the `skill-installer` skill:

- Ask Codex: `Use the skill-installer skill to install skill-workflow-manager from Golden-Promise/codex-skill-library at skills/skill-workflow-manager.`
- For the published release, ask: `Use the skill-installer skill to install skill-workflow-manager from Golden-Promise/codex-skill-library at skills/skill-workflow-manager using ref v0.1.0.`

## Start Here

1. Read the main workflow guide in [references/use-cases.md](references/use-cases.md).
2. Use [references/prompt-templates.en.md](references/prompt-templates.en.md) when you want copy-ready prompt wording.
3. Use the CLI patterns below when you already know which mode you need.

## Common Commands

Create or refresh a managed skill:

```bash
python3 scripts/manage_skill.py \
  demo-skill \
  --project-root <project-root> \
  --purpose "Use this skill when the user wants help with demo-skill tasks."
```

Inspect a downloaded local skill before import:

```bash
python3 scripts/manage_skill.py \
  --inspect-import \
  --import-path <import-path> \
  --project-root <project-root>
```

Validate the current package without writing files:

```bash
python3 scripts/manage_skill.py --validate-only
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
| `scripts/manage_skill.py` | Deterministic CLI for create, import, link, and validate flows |
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
