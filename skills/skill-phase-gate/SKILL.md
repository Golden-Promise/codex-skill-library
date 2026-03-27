---
name: skill-phase-gate
description: Use when a meaningful coding checkpoint is needed before or after risky execution, such as a multi-file refactor, migration, or pre-commit pause.
---

# Skill Phase Gate

## Overview

Use `skill-phase-gate` to add an optional operational checkpoint around meaningful coding work.
It is for risky edits before or after execution, not for root-state refresh, packet compression, suite bootstrap, generic planning, or final handoff writing.

## Use This Skill When

- you are about to start a refactor, migration, or multi-file change and want a brief preflight gate
- you have finished a meaningful edit and need a postflight checkpoint before commit or handoff
- the task is risky enough that expected files, explicit non-goals, and a verification plan should be stated out loud
- you want a pre-commit checkpoint for work that is substantial enough to deserve one more deliberate review pass

## Do Not Use This Skill When

- the request is a typo fix, tiny one-line edit, or similarly trivial change
- the user only wants an explanation, walkthrough, or analysis with no checkpoint artifact
- the main need is reconstructing current task state or preserving long-running state ownership
- the main need is packet compression for the next live turn
- the main need is suite bootstrap or routing
- the main need is generating a full transfer packet or final handoff summary

## Meaningful Checkpoint Bar

This package is a good fit when the checkpoint serves a meaningful workflow boundary:

- good fit: refactors, multi-file changes, risky edits, migration checkpoints, or pre-commit review passes
- bad fit: typo fixes, tiny one-line changes, pure explanation tasks, or generic up-front planning

## Package Boundary

- `skill-phase-gate` can mention current task state only to support the immediate checkpoint
- `skill-context-keeper` remains the owner of root-state refresh and compression
- `skill-subtask-context` remains the owner of local child-task state
- `skill-context-packet` remains the owner of packet-sized next-turn context
- this package does not replace suite bootstrap, planning packages, or handoff generation

## References

- `README.md` and `README.zh-CN.md`: install guidance, trigger boundaries, and non-goals
- `assets/PREFLIGHT.template.md`: compact pre-execution gate
- `assets/POSTFLIGHT.template.md`: compact post-execution gate
- `references/use-cases.md` and `references/use-cases.zh-CN.md`: reader-facing positive and negative examples
- `references/prompt-templates.en.md` and `references/prompt-templates.zh-CN.md`: ready-to-paste prompt patterns
