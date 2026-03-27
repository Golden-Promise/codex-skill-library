---
name: skill-context-keeper
description: Use when the user needs to refresh or compress trusted root-task state for an ongoing coding task without creating subtask-local state, workflow gates, or final handoffs.
---

# Skill Context Keeper

## Overview

Maintain trusted root-task state for long-running coding tasks.
Use this skill when the thread needs root-state refresh or compression for an artifact such as `.agent-state/root/TASK_STATE.md`, not subtask-local state, packet compression, phase gates, or final transfer notes.

## Use This Skill When

- resuming a task after an interruption, stale summary, or context loss at the root-task level
- rebuilding the last known root task state before new work continues
- refreshing verified facts, decisions, assumptions, or next actions in `.agent-state/root/TASK_STATE.md`
- compressing stale root-task detail into archive-minded notes instead of letting the active summary grow indefinitely
- reconciling root-state changes since the last stable checkpoint

## Do Not Use This Skill When

- the user needs a bounded child task with its own local state
- the next step only needs a packet-sized context object
- the user needs workflow phases, checkpoints, or exit criteria
- the thread needs a final pause summary or transfer handoff
- the request is asking one package to coordinate the full continuity suite

## Core Rules

1. Keep the output focused on root-state refresh and compression, not future workflow control.
2. Distinguish verified facts from assumptions and from decisions already made.
3. Assume downstream path examples such as `.agent-state/root/TASK_STATE.md` unless the user specifies another target.
4. Move stale detail into compression or archive notes instead of inflating the active summary.
5. Do not create subtask-local state.
6. Do not run phase gates.
7. Do not generate final handoffs.

## References

- `README.md` and `README.zh-CN.md`: package overview, installation, and boundary guidance
- `references/use-cases.md` and `references/use-cases.zh-CN.md`: reader-facing trigger examples
- `references/prompt-templates.en.md` and `references/prompt-templates.zh-CN.md`: reusable root-state refresh prompts
- `assets/TASK_STATE.template.md`: compact root task-state artifact template
