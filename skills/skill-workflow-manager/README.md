# skill-workflow-manager

[简体中文](README.zh-CN.md)

Maintain Codex skills with a global-first shared-library workflow built around `$CODEX_HOME/skills`, plus optional project discovery links when a project needs them.

## What This Package Helps With

- creating or refreshing a canonical skill package in the default Codex shared library
- importing a downloaded local skill into that shared library
- attaching, detaching, or syncing project discovery links
- bootstrapping a project-local managed layout when you intentionally want project-contained skill management
- registering a staged skill package into the runtime skills root for direct Codex discovery
- validating an existing skill package without writing files

## Best For

This package works best when you treat `$CODEX_HOME/skills` as the natural shared skill library and add project links only when a project needs local discovery.

## Recommended Model

Use this package in two layers:

- Default shared library: keep canonical skills in `$CODEX_HOME/skills`
- Optional project links: expose selected skills through `<project-root>/.agents/skills`
- Project-local bootstrap: use `<project-root>/_skill-library` only when you explicitly want a project-contained managed layout

## Install

Install the latest version from `codex-skill-library`:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo <owner>/codex-skill-library \
  --path skills/skill-workflow-manager
```

Install the published `v0.1.1` release:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo <owner>/codex-skill-library \
  --path skills/skill-workflow-manager \
  --ref v0.1.1
```

Install from a GitHub tree URL:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --url https://github.com/<owner>/codex-skill-library/tree/main/skills/skill-workflow-manager
```

Install with Codex using the `skill-installer` skill:

- Ask Codex: `Use the skill-installer skill to install skill-workflow-manager from Golden-Promise/codex-skill-library at skills/skill-workflow-manager.`
- For the published release, ask: `Use the skill-installer skill to install skill-workflow-manager from Golden-Promise/codex-skill-library at skills/skill-workflow-manager using ref v0.1.1.`
- To stage it in another directory, ask: `Use the skill-installer skill to install skill-workflow-manager from Golden-Promise/codex-skill-library at skills/skill-workflow-manager, and install it to <target-root>.`
- More precisely, `<target-root>` is the install root, and the staged directory will be `<target-root>/skill-workflow-manager`.
- A staged install is not automatically discoverable as a Codex skill. To use it as a skill, either install to `$CODEX_HOME/skills` or link `<target-root>/skill-workflow-manager` into `$CODEX_HOME/skills/skill-workflow-manager` or `<project-root>/.agents/skills/skill-workflow-manager`.

After a staged install, register it for direct Codex use:

```bash
python3 <target-root>/skill-workflow-manager/scripts/manage_skill.py \
  --register-runtime-skill
```

## Start Here

1. Read the main workflow guide in [references/use-cases.md](references/use-cases.md).
2. Default to the global shared-library flow in `$CODEX_HOME/skills`.
3. Use [references/prompt-templates.en.md](references/prompt-templates.en.md) when you want copy-ready prompt wording.
4. Reach for project-local bootstrap only when the skill should live under one project rather than the global shared library.

## Common Commands

Create or refresh a shared-library skill:

```bash
python3 scripts/manage_skill.py \
  demo-skill \
  --purpose "Use this skill when the user wants help with demo-skill tasks."
```

Import a downloaded local skill into the shared library:

```bash
python3 scripts/manage_skill.py \
  --import-path <import-path>
```

Attach an existing shared-library skill to a project:

```bash
python3 scripts/manage_skill.py \
  --project-root <project-root> \
  --project-skills demo-skill
```

Validate the current package without writing files:

```bash
python3 scripts/manage_skill.py --validate-only
```

Register the current package into the runtime skills root:

```bash
python3 scripts/manage_skill.py --register-runtime-skill
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
