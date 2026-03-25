# skill-phase-gate

[简体中文](README.zh-CN.md)

## Overview

`skill-phase-gate` is the package for deciding when a coding task needs explicit phases, checkpoints, and exit criteria before execution continues.
It keeps staged work intentional so a complex thread does not blur into an unreviewed one-shot run.

## Best For

- splitting a multi-step task before implementation starts
- adding checkpoints to risky refactors or migrations
- making phase boundaries visible when several changes depend on each other
- deciding whether a task is small enough to proceed directly or large enough to gate

## What It Is Not For

- reconstructing stale or missing task context
- summarizing the current state after an interruption
- writing a pause note or transfer package for another agent
- orchestrating the whole long-task continuity suite

## Install

Install `skill-phase-gate` from this repository with the standard package path for published Codex skills.

You can ask Codex in natural language:

- `Use skill-installer to install skill-phase-gate from Golden-Promise/codex-skill-library at skills/skill-phase-gate.`
- `Use skill-installer to install skill-phase-gate from Golden-Promise/codex-skill-library at skills/skill-phase-gate using the release or ref I specify.`

## How To Use

Use this package before the task drifts into implementation.
Describe the multi-step goal, the points that need review or verification, and where the work should pause before moving forward, then have the skill turn that into a narrow staged plan.

## References

- `SKILL.md` for trigger routing and package boundaries
- `references/` for future public examples and prompt patterns
- `assets/` for future phase-plan, checkpoint, and exit-criteria templates
