---
name: skill-context-packet
description: Use when the next turn needs a minimum context packet rather than a full root or subtask state refresh.
---

# Skill Context Packet

## Overview

Use this package when the next root or subtask turn needs a compact packet instead of a full state file.
Keep the package boundary narrow: compress the minimum context object for the next turn without taking over root-state refresh, subtask-state refresh, workflow gates, or handoffs.

## Use This Skill When

- the next turn only needs a small packet of facts, constraints, and exact next action
- a root or subtask state file is getting too large to inject directly
- you want to hand a bounded task slice to another owner without copying the full history
- you need a packet-first workflow that protects context budget

## Do Not Use This Skill When

- the root task or subtask state itself needs a full refresh
- the task needs a risky-change checkpoint or phase gate
- the work is pausing and needs a handoff summary
- the repo needs suite bootstrap or routing guidance

## Package Boundary

This package owns packet compression such as `.agent-state/root/PACKET.md` or `.agent-state/subtasks/<slug>/PACKET.md`.
It does not own root task state, does not own workflow gates, and does not own final handoffs.

## References

- `README.md` and `README.zh-CN.md`: entry docs and direct invocation wording
- `references/use-cases.md`: positive and negative trigger examples
- `references/prompt-templates.en.md`: reusable packet-writing prompts
- `assets/PACKET.template.md`: packet template
