# skill-context-keeper

[简体中文](README.zh-CN.md)

## Overview

`skill-context-keeper` is the narrow package for recovering and refreshing structured task state during a long coding thread.
It helps the next turn start from the best known picture of the work without expanding into phase control or end-of-task handoff writing.
This package maintains structured long-task state only.
It assumes downstream state files can live at paths such as `.agent-state/TASK_STATE.md`, but it does not own workflow gating and it does not own final handoffs.

## Best For

- resuming a paused task after the working context has drifted
- rebuilding the current state before making more code changes
- refreshing open TODOs, assumptions, and recent changes in one place
- reconciling what the thread believes with what the repository now shows

## What It Is Not For

- breaking a task into staged execution phases
- deciding checkpoint rules or phase exit criteria
- writing a final pause or transfer handoff for another agent
- bootstrapping the full long-task continuity suite

## Package Boundary

Use this package when the task needs a current-state refresh.
It is responsible for reconstructing verified codebase facts, preserving open issues, and updating a compact task-state artifact for downstream work.

Keep the boundary narrow:

- maintain structured state for an ongoing task
- refresh or rewrite artifacts such as `.agent-state/TASK_STATE.md`
- separate facts, assumptions, and decisions clearly

This package does not run phase gates, does not own workflow gating, and does not own final handoffs.

## Install

Install `skill-context-keeper` from this repository with the standard package path for published Codex skills.

You can ask Codex in natural language:

- `Use skill-installer to install skill-context-keeper from Golden-Promise/codex-skill-library at skills/skill-context-keeper.`
- `Use skill-installer to install skill-context-keeper from Golden-Promise/codex-skill-library at skills/skill-context-keeper using the release or ref I specify.`

## How To Use

Start when the task needs a reliable state refresh before execution continues.
Describe what looks stale or missing, then ask the skill to reconstruct the current task picture, carry forward unresolved work, and keep the summary narrow to ongoing state.
If you want a concrete downstream artifact, say so explicitly, for example: `Refresh the current task state and update .agent-state/TASK_STATE.md.`

## References

- `SKILL.md` for trigger routing and package boundaries
- [references/use-cases.md](references/use-cases.md) for positive and negative trigger examples
- [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md) for Chinese trigger examples
- [references/prompt-templates.en.md](references/prompt-templates.en.md) for reusable refresh prompts
- [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md) for Chinese refresh prompts
- [assets/TASK_STATE.template.md](assets/TASK_STATE.template.md) for the compact task-state artifact template
