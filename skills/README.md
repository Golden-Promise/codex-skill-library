# Skills

[简体中文](README.zh-CN.md)

This directory contains the installable skill packages published by `codex-skill-library`.

## Pick the Right Continuity Skill

Use this quick guide first:

- I paused a task and need to rebuild the current picture.
  Start with `skill-context-keeper`.
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
| `skill-context-keeper` | Refreshing current task state without taking over checkpoints or handoffs | [EN](skill-context-keeper/README.md) / [中文](skill-context-keeper/README.zh-CN.md) |
| `skill-phase-gate` | Adding preflight and postflight checkpoints around substantial edits | [EN](skill-phase-gate/README.md) / [中文](skill-phase-gate/README.zh-CN.md) |
| `skill-handoff-summary` | Producing compact continuation handoffs with status, blockers, and exact next steps | [EN](skill-handoff-summary/README.md) / [中文](skill-handoff-summary/README.zh-CN.md) |
| `skill-task-continuity` | Bootstrapping and composing the continuity suite while preserving atomic package boundaries | [EN](skill-task-continuity/README.md) / [中文](skill-task-continuity/README.zh-CN.md) |

## Package Conventions

- Each published package lives in `skills/<skill-name>/`.
- The directory name should match the `name` field in `SKILL.md`.
- Package `README.md` files are the main entry point for users.
- `references/` is for reader-facing material; `docs/` is for maintainer notes when needed.
- For the long-task continuity workflow, start with `skill-task-continuity` only when you need suite bootstrap or composition guidance; otherwise install the atomic package that owns the next action.
