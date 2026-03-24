# skill-governance

[简体中文](README.zh-CN.md)

## Overview

`skill-governance` is the project skill governance tool for taking over an existing codebase and bringing its skills under clear, repeatable control.
It helps you organize local skills, decide what should stay enabled, and keep a project ready for cleanup, release, or ongoing maintenance.

## Core Capabilities

`skill-governance` focuses on the practical work that comes with owning project skills:

- take over an existing project and organize the skills already present
- establish a clean governance flow for a new project
- add, enable, or document a skill with project-specific context
- check for safe cleanup, relinking, upgrade, or release readiness
- prepare skill metadata for CI and publishing workflows

## Best For

It is a strong fit when you are:

- stepping into a project that already has local skills
- setting up skill governance for a new project
- adding a reusable skill you want to keep and reuse later
- enabling one skill for one project without affecting everything else
- checking health before cleanup, relinking, upgrade, or release
- preparing skill metadata for CI or release checks

If you are new to the tool, start with project takeover, project setup, or a pre-release health check.

## Install

Installation is documented in the style of the rest of the package: start with the standard project path, then choose whether you want the latest published release or a specific ref.

For the copy-ready command patterns and advanced installation notes, see [references/use-cases.md](references/use-cases.md).

## Quick Start

Most people start with one of these three actions:

1. Take over an existing project directory.
2. Set up skill governance for a new project.
3. Check the project before cleanup or release.

If you want the exact prompts for each path, use [references/use-cases.md](references/use-cases.md).

## What You Can Do Next

Once the basics are in place, `skill-governance` can also help with:

- adding a new skill
- enabling a skill in one project
- repairing safe issues
- auditing registry or dependency state
- documenting an existing skill
- upgrading or retiring a skill

For more detailed examples and direct command patterns, see [references/use-cases.md](references/use-cases.md).

## Documentation

- Command reference and advanced usage: [references/use-cases.md](references/use-cases.md)
- 中文任务说明: [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- Copy-ready prompts: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- 中文提示词模板: [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- Maintainer publishing notes: [docs/publishing-with-skill-installer.md](docs/publishing-with-skill-installer.md)
