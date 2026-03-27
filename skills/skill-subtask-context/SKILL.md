---
name: skill-subtask-context
description: Use when a bounded child task needs its own local context, scope, and restart state without inflating the root task summary.
---

# Skill Subtask Context

## Overview

Use this package when a long-running task needs a child task with its own local state.
Keep the package boundary narrow: open, refresh, or close subtask state without taking over root state, packet compression, workflow gates, or final handoffs.

## Use This Skill When

- a child task needs its own `.agent-state/subtasks/<slug>/TASK_STATE.md`
- the parent task is getting noisy and should hand a bounded slice to a separate owner
- a subtask needs local facts, local risks, and local exit criteria
- a child task is closing and its merge notes need to be made explicit

## Do Not Use This Skill When

- the root task state itself needs a refresh
- the next step only needs a compressed packet rather than a full local state refresh
- the task needs a risky-change checkpoint or formal gate
- the task is pausing and needs a handoff summary instead of active subtask state

## Package Boundary

This package owns local child-task state such as `.agent-state/subtasks/<slug>/TASK_STATE.md`.
It does not own root task state, does not own packet compression, does not own workflow gates, and does not own final handoffs.

## References

- `README.md` and `README.zh-CN.md`: entry docs and direct invocation wording
- `references/use-cases.md`: positive and negative trigger examples
- `references/prompt-templates.en.md`: reusable prompt patterns
- `assets/TASK_STATE.template.md`: subtask-state template
