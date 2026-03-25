---
name: skill-task-continuity
description: Use when the user is explicitly bootstrapping or coordinating the long-task continuity suite across context refresh, phase gating, and handoff boundaries for an ongoing coding effort.
---

# Skill Task Continuity

## Overview

Coordinate the long-task continuity suite when the task is about the continuity workflow itself rather than a single atomic continuity action.
Use this package as the suite entry point and downstream bootstrap helper while keeping the atomic package boundaries clear.

## Use This Skill When

- bootstrapping the long-task continuity suite in a downstream repository
- explaining how context refresh, phase gates, and handoff behavior fit together
- deciding which atomic package should trigger first in a suite-shaped request
- protecting package boundaries when a prompt mentions multiple continuity concerns

## Do Not Use This Skill When

- the task only needs `skill-context-keeper` to refresh state
- the task only needs `skill-phase-gate` for a meaningful checkpoint
- the task only needs `skill-handoff-summary` for a pause or transfer note
- the user is asking this package to replace the atomic skills instead of composing them

## Composition Boundary

This package explains the suite and bootstraps downstream templates.
It does not replace the three atomic skills:

- `skill-context-keeper` owns ongoing task state such as `.agent-state/TASK_STATE.md`
- `skill-phase-gate` owns meaningful preflight and postflight checkpoints
- `skill-handoff-summary` owns `.agent-state/HANDOFF.md` and continuation-oriented handoffs

Use `skill-task-continuity` to route into the right atomic package or to install the downstream starter files that make the suite easy to adopt.

## Downstream Templates

The templates in `assets/` are for downstream consumer repositories only.
They are duplicated here so a consumer repo can bootstrap the suite from one package.
Do not use this package to mutate the public library root into a consumer repo.

## References

- `README.md` and `README.zh-CN.md`: package overview, bootstrap command, and suite entry guidance
- `references/composition-guide.md`: how the suite pieces fit together and when to invoke each atomic skill
- `references/install-playbook.md`: downstream bootstrap walkthrough and recommended layout
- `assets/`: downstream-only templates copied by `scripts/bootstrap_suite.py`
