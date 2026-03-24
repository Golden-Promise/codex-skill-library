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

If you are new to the tool, start by taking over a project, setting up a project, or checking a project before cleanup or release.

## Install

In Codex, the simplest way to ask is just:

“Use skill-installer to install skill-governance from Golden-Promise/codex-skill-library at skills/skill-governance.”

If you want a specific release, add the version you want:

“Use skill-installer to install skill-governance from Golden-Promise/codex-skill-library at skills/skill-governance using ref v0.5.0.”

If you want exact install commands and advanced usage, use [references/use-cases.md](references/use-cases.md).

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

## Read More

- Command reference and advanced usage: [references/use-cases.md](references/use-cases.md)
- 中文任务说明: [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- Copy-ready prompts: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- 中文提示词模板: [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- Maintainer publishing notes: [docs/publishing-with-skill-installer.md](docs/publishing-with-skill-installer.md)
