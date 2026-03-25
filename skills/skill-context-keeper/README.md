# skill-context-keeper

[简体中文](README.zh-CN.md)

## Overview

`skill-context-keeper` is the focused package for recovering and refreshing structured task state during long-running coding work.
It helps the next turn start from the best verified picture of the task without expanding into checkpoints, workflow control, or final handoff writing.

## Core Capabilities

`skill-context-keeper` is designed for one job: keeping ongoing task state trustworthy and resumable.

- rebuild the current task picture from verified repository facts
- keep facts, assumptions, decisions, risks, and next actions clearly separated
- refresh compact downstream state files such as `.agent-state/TASK_STATE.md`
- preserve just enough continuity for the next turn without turning into a full workflow package

Use this skill when the main problem is stale or scattered task context rather than workflow control.

## Best For

- resuming a paused task after the working context has drifted
- resuming a task after an interruption or stale summary
- rebuilding the current state before making more code changes
- rebuilding the last known task state before new work continues
- refreshing open TODOs, assumptions, and recent changes in one place
- reconciling what the thread believes with what the repository now shows

If you are picking an entry point, start here when the main problem is stale or scattered task context.

## What It Is Not For

- breaking a task into staged execution phases
- deciding checkpoint rules or phase exit criteria
- writing a final pause or transfer handoff for another agent
- bootstrapping the full long-task continuity suite

This package does not own workflow gating and does not own final handoffs.

## Install

To install `skill-context-keeper`, use the standard published package path in this repository and choose the release or ref that fits your workflow.

You can ask Codex in natural language:

- `Use skill-installer to install skill-context-keeper from Golden-Promise/codex-skill-library at skills/skill-context-keeper.`
- `Use skill-installer to install skill-context-keeper from Golden-Promise/codex-skill-library at skills/skill-context-keeper using ref v0.6.1.`

For trigger examples and prompt wording, see [references/use-cases.md](references/use-cases.md).

## Common Paths

Start with one of these three paths:

1. Resume a paused task after the working picture has drifted.
2. Refresh task state before more implementation work.
3. Reconcile facts, open issues, and the next action in `.agent-state/TASK_STATE.md`.

If you want ready-to-paste prompts, see [references/prompt-templates.en.md](references/prompt-templates.en.md).

## Documentation

- Trigger routing and package boundary: `SKILL.md`
- Use cases and trigger examples: [references/use-cases.md](references/use-cases.md)
- Chinese use cases: [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- Prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- Chinese prompt templates: [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- Task-state template: [assets/TASK_STATE.template.md](assets/TASK_STATE.template.md)
