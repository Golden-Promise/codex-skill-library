---
name: skill-handoff-summary
description: Use when an ongoing coding task needs a compact root-task or subtask handoff before pausing or transferring ownership, without turning it into full-project documentation, root-state refresh, or workflow control.
---

# Skill Handoff Summary

## Overview

Capture a concise continuation-oriented handoff for a coding task that will resume later in the same thread or a new one.
This package specializes in compact handoff creation only.
It can target downstream artifacts such as `.agent-state/root/HANDOFF.md` or `.agent-state/subtasks/<slug>/HANDOFF.md`, but it does not own root-state refresh and it does not own workflow gating.

## Use This Skill When

- pausing work and needing a clean continuation note for later resumption
- transferring a task to another agent with open questions, constraints, and an exact next action
- writing or refreshing a compact artifact such as `.agent-state/root/HANDOFF.md`
- writing or refreshing a compact artifact such as `.agent-state/subtasks/<slug>/HANDOFF.md`
- reducing restart cost after a stop point in a long thread

## Do Not Use This Skill When

- the main need is rebuilding root-task state before more work continues
- the main need is creating subtask-local state instead of a pause artifact
- the main need is packet compression for the next live turn
- the request is asking for a workflow gate rather than a continuation handoff

## References

- `README.md` and `README.zh-CN.md`: package overview, boundary guidance, and install notes
- `references/use-cases.md` and `references/use-cases.zh-CN.md`: positive and negative trigger examples
- `references/prompt-templates.en.md` and `references/prompt-templates.zh-CN.md`: reusable pause and resume wording
- `assets/HANDOFF.template.md`: compact template for root or subtask handoffs
