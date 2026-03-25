# skill-governance

[简体中文](README.zh-CN.md)

## Overview

`skill-governance` is the project skill governance tool for organizing local skills, deciding what stays enabled, and keeping a project release-ready.
It helps you bring project skills under clear, repeatable control for cleanup, release, or ongoing maintenance.

## Core Capabilities

`skill-governance` focuses on the practical work that comes with owning project skills:

- project takeover and organization for existing skills
- governance setup for a new project
- skill context, enablement, and documentation
- safe cleanup, relinking, upgrade, and release checks
- metadata for CI and publishing workflows

## Best For

It is a strong fit when you are:

- stepping into a project that already has local skills
- setting up skill governance for a new project
- adding a reusable skill you want to keep and reuse later
- enabling one skill for one project without affecting everything else
- checking health before cleanup, relinking, upgrade, or release
- preparing skill metadata for CI or release checks

If you are starting fresh, begin with project takeover, project setup, or a pre-release health check.

## Install

To install `skill-governance`, use the standard package path in your Codex workspace, then choose the release or ref that fits your workflow.

You can ask Codex in natural language:

- `Use skill-installer to install skill-governance from Golden-Promise/codex-skill-library at skills/skill-governance.`
- `Use skill-installer to install skill-governance from Golden-Promise/codex-skill-library at skills/skill-governance using ref v0.6.1.`

For command patterns and advanced installation notes, see [references/use-cases.md](references/use-cases.md).

## Common Paths

Start with one of these three actions:

1. Take over an existing project directory.
2. Set up skill governance for a new project.
3. Check the project before cleanup or release.

If you want the prompt templates for each path, see [references/prompt-templates.en.md](references/prompt-templates.en.md).

## What You Can Do Next

Once the basics are in place, `skill-governance` can also help with:

- adding a new skill
- enabling a skill in one project
- applying safe fixes
- auditing registry or dependency state
- documenting an existing skill
- upgrading or retiring a skill

For more detailed examples and direct command patterns, see [references/use-cases.md](references/use-cases.md).

## Documentation

- Command reference and advanced usage: [references/use-cases.md](references/use-cases.md)
- Chinese command reference and usage: [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- Prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- Chinese prompt templates: [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- Maintainer publishing notes: [docs/publishing-with-skill-installer.md](docs/publishing-with-skill-installer.md)
