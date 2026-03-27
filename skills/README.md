# Skills

[简体中文](README.zh-CN.md)

This directory contains the installable skill packages published by `codex-skill-library`.

## Pick the Right Continuity Skill

Use this quick guide first:

- I paused a task and need to rebuild the current picture.
  Start with `skill-context-keeper`.
- I am splitting work into a bounded child task with its own local context.
  Start with `skill-subtask-context`.
- I need the smallest possible context object for the next turn.
  Start with `skill-context-packet`.
- I am about to make a risky or multi-file change.
  Start with `skill-phase-gate`.
- I need to stop now and leave a durable restart note.
  Start with `skill-handoff-summary`.
- I want to set up the whole continuity workflow in a repo for the first time.
  Start with `skill-task-continuity`.

## How To Use This Index

1. Start with the quick picker above if you are working on continuity setup or continuity workflow tasks.
2. Scan the table below to find the package that matches your next action.
3. Open the package README in your preferred language.
4. Use the package reference pages for examples, prompt wording, and deeper boundary notes when needed.

## Published Packages

| Skill | Best For | Docs |
| --- | --- | --- |
| `skill-governance` | Governing Codex skill assets with add, enable, doctor, repair, audit, and document tasks | [EN](skill-governance/README.md) / [中文](skill-governance/README.zh-CN.md) |
| `skill-context-keeper` | Refreshing and compressing trusted root-task state without taking over child-task state or handoffs | [EN](skill-context-keeper/README.md) / [中文](skill-context-keeper/README.zh-CN.md) |
| `skill-subtask-context` | Opening, refreshing, and closing child-task state without bloating root task context | [EN](skill-subtask-context/README.md) / [中文](skill-subtask-context/README.zh-CN.md) |
| `skill-context-packet` | Compressing the minimum context needed for the next root or subtask turn | [EN](skill-context-packet/README.md) / [中文](skill-context-packet/README.zh-CN.md) |
| `skill-phase-gate` | Adding optional operational checkpoints around risky edits without taking over state ownership | [EN](skill-phase-gate/README.md) / [中文](skill-phase-gate/README.zh-CN.md) |
| `skill-handoff-summary` | Producing compact continuation handoffs for root tasks or subtasks with status, blockers, and exact next steps | [EN](skill-handoff-summary/README.md) / [中文](skill-handoff-summary/README.zh-CN.md) |
| `skill-task-continuity` | Bootstrapping `INDEX.md`, root packets, subtask folders, and suite composition guidance | [EN](skill-task-continuity/README.md) / [中文](skill-task-continuity/README.zh-CN.md) |

## Package Conventions

- Each published package lives in `skills/<skill-name>/`.
- The directory name should match the `name` field in `SKILL.md`.
- Package `README.md` files are the main entry point for users.
- `references/` is for reader-facing material; `docs/` is for maintainer notes when needed.
- For the long-task continuity workflow, start with `skill-task-continuity` only when you need suite bootstrap or composition guidance; otherwise install the atomic package that owns the next action or the packet you need next.
