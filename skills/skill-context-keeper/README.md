# skill-context-keeper

[简体中文](README.zh-CN.md)

## Overview

`skill-context-keeper` is the narrow package for recovering and refreshing structured task state during a long coding thread.
It helps the next turn start from the best known picture of the work without expanding into phase control or end-of-task handoff writing.

## Best For

- resuming a paused task after the working context has drifted
- rebuilding the current state before making more code changes
- refreshing open TODOs, assumptions, and recent changes in one place
- reconciling what the thread believes with what the repository now shows

## What It Is Not For

- breaking a task into staged execution phases
- deciding checkpoint rules or phase exit criteria
- writing a final pause or transfer handoff for another agent
- bootstrapping the full long-task continuity suite

## Install

Install `skill-context-keeper` from this repository with the standard package path for published Codex skills.

You can ask Codex in natural language:

- `Use skill-installer to install skill-context-keeper from Golden-Promise/codex-skill-library at skills/skill-context-keeper.`
- `Use skill-installer to install skill-context-keeper from Golden-Promise/codex-skill-library at skills/skill-context-keeper using the release or ref I specify.`

## How To Use

Start when the task needs a reliable state refresh before execution continues.
Describe what looks stale or missing, then ask the skill to reconstruct the current task picture, carry forward unresolved work, and keep the summary narrow to ongoing state.

## References

- `SKILL.md` for trigger routing and package boundaries
- `references/` for future public examples and prompt patterns
- `assets/` for future state snapshot and continuity note templates
