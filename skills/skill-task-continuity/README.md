# skill-task-continuity

[简体中文](README.zh-CN.md)

## Overview

`skill-task-continuity` is the composition package for work that is explicitly about managing long-task continuity as a coordinated system.
It bootstraps or routes across context refresh, phase gating, and handoff writing while keeping the atomic package boundaries visible.

## Best For

- setting up the long-task continuity suite as a coherent package family
- coordinating which atomic continuity package should act first
- handling requests that truly span state refresh, staged execution, and handoff behavior
- keeping suite-level boundaries clear when prompts mention several continuity concerns at once

## What It Is Not For

- replacing `skill-context-keeper` for ordinary state refresh work
- replacing `skill-phase-gate` for a normal staged-plan decision
- replacing `skill-handoff-summary` for a simple pause or transfer note
- stealing one-package tasks just because the prompt contains many keywords

## Install

Install `skill-task-continuity` from this repository with the standard package path for published Codex skills.

You can ask Codex in natural language:

- `Use skill-installer to install skill-task-continuity from Golden-Promise/codex-skill-library at skills/skill-task-continuity.`
- `Use skill-installer to install skill-task-continuity from Golden-Promise/codex-skill-library at skills/skill-task-continuity using the release or ref I specify.`

## How To Use

Start here only when the task itself is about suite bootstrap or multi-package continuity coordination.
Describe which continuity problems are in play, which atomic packages are expected to cooperate, and what boundaries must stay narrow, then let the package route or scaffold the suite-level workflow.

## References

- `SKILL.md` for trigger routing and package boundaries
- `references/` for future public examples and prompt patterns
- `assets/` for future suite bootstrap and coordination templates
