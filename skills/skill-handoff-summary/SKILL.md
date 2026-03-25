---
name: skill-handoff-summary
description: Use when an ongoing coding task needs a compact continuation-oriented handoff summary, especially before pausing or transferring ownership, without turning it into full-project documentation or workflow control.
---

# Skill Handoff Summary

## Overview

Capture a concise continuation-oriented handoff for a coding task that will resume later in the same thread or a new one.
This package specializes in compact handoff creation only.
It can target downstream artifacts such as `.agent-state/HANDOFF.md`, but it does not own long-term state and it does not own workflow gating.

## Use This Skill When

- pausing work and needing a clean continuation note for later resumption
- transferring a task to another agent with open questions, constraints, and an exact next action
- writing or refreshing a compact artifact such as `.agent-state/HANDOFF.md`
- reducing restart cost after a stop point in a long thread

## References

- `README.md` and `README.zh-CN.md`: package overview, boundary guidance, and install notes
- `references/use-cases.md` and `references/use-cases.zh-CN.md`: positive and negative trigger examples
- `references/prompt-templates.en.md` and `references/prompt-templates.zh-CN.md`: reusable pause and resume wording
- `assets/HANDOFF.template.md`: compact template for `.agent-state/HANDOFF.md`
