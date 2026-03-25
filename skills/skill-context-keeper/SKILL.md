---
name: skill-context-keeper
description: Use when the user needs to preserve or refresh structured long-task state for an ongoing coding task without running workflow gates or generating a final handoff.
---

# Skill Context Keeper

## Overview

Maintain structured working state for long-running coding tasks.
Use this skill when the thread needs trustworthy context reconstruction or a refreshed task-state artifact such as `.agent-state/TASK_STATE.md`, not phase planning or final transfer notes.

## Use This Skill When

- resuming a task after an interruption, stale summary, or context loss
- rebuilding the last known task state before new work continues
- refreshing TODOs, verified facts, decisions, or working assumptions for an ongoing task
- reconciling what changed since the last stable checkpoint
- updating a downstream state file such as `.agent-state/TASK_STATE.md`

## Do Not Use This Skill When

- the user needs workflow phases, checkpoints, or exit criteria
- the task is about deciding whether work should be gated before implementation
- the thread needs a final pause summary or transfer handoff
- the request is asking one package to coordinate the full continuity suite

## Core Rules

1. Keep the output focused on current task state, not future workflow control.
2. Distinguish verified facts from assumptions and from decisions already made.
3. Assume downstream path examples such as `.agent-state/TASK_STATE.md` unless the user specifies another target.
4. Do not run phase gates.
5. Do not generate final handoffs.

## References

- `README.md` and `README.zh-CN.md`: package overview, installation, and boundary guidance
- `references/use-cases.md` and `references/use-cases.zh-CN.md`: reader-facing trigger examples
- `references/prompt-templates.en.md` and `references/prompt-templates.zh-CN.md`: reusable refresh prompts
- `assets/TASK_STATE.template.md`: compact task-state artifact template
