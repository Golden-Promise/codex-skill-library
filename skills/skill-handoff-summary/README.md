# skill-handoff-summary

[简体中文](README.zh-CN.md)

## Overview

`skill-handoff-summary` is the focused package for writing continuation-oriented pause or transfer summaries when long-running coding work needs to stop and resume later.
It turns status, blockers, preserved constraints, and the exact next action into a compact restart note so the next session does not have to reconstruct intent from scattered thread history.
It is for compact downstream artifacts such as `.agent-state/HANDOFF.md`, not whole-project documentation.

## Core Capabilities

`skill-handoff-summary` specializes in one narrow outcome: a handoff that is short, trusted, and immediately reusable.

- write concise downstream artifacts such as `.agent-state/HANDOFF.md`
- preserve current status, open problems, hard constraints, and the exact next action
- include a reusable resume prompt for the next thread or session
- stay focused on continuation instead of expanding into whole-project documentation

## Best For

- pausing work at the end of a session with open tasks still pending
- transferring a task to another agent that needs a trusted restart note
- capturing blockers, decisions, and next actions before context goes stale
- reducing the cost of resuming a thread after a handoff

If you already know the work is about to pause or change hands, this package is the right starting point.

## What It Is Not For

- rebuilding the current task state before work continues
- deciding whether a task needs staged phases or checkpoints
- coordinating the atomic packages as one suite-level workflow
- maintaining long-term state across the whole task
- producing whole-project documentation or repository tours
- replacing the final user-facing answer when no handoff is needed

## Install

To install `skill-handoff-summary`, use the standard published package path in this repository and choose the release or ref that fits your workflow.

You can ask Codex in natural language:

- `Use skill-installer to install skill-handoff-summary from Golden-Promise/codex-skill-library at skills/skill-handoff-summary.`
- `Use skill-installer to install skill-handoff-summary from Golden-Promise/codex-skill-library at skills/skill-handoff-summary using ref v0.6.1.`

For direct trigger examples and prompt wording, see [references/use-cases.md](references/use-cases.md).

## Common Paths

Start with one of these three paths:

1. Pause a session while important work is still open.
2. Transfer a task to another agent and preserve the restart context.
3. Write `.agent-state/HANDOFF.md` with the exact next action and a reusable resume prompt.

If you want ready-to-paste prompts, see [references/prompt-templates.en.md](references/prompt-templates.en.md).

## Documentation

- Trigger routing and package boundary: `SKILL.md`
- Reference index: [references/README.md](references/README.md)
- Use cases and trigger examples: [references/use-cases.md](references/use-cases.md)
- Chinese use cases: [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- Prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- Chinese prompt templates: [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- Handoff template: [assets/HANDOFF.template.md](assets/HANDOFF.template.md)
