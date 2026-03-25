# skill-handoff-summary

[简体中文](README.zh-CN.md)

## Overview

`skill-handoff-summary` is the package for writing a clean pause or transfer summary when long-running coding work needs to stop and resume later.
It packages status, blockers, and next steps so the next agent does not have to reconstruct intent from scattered thread history.

## Best For

- pausing work at the end of a session with open tasks still pending
- transferring a task to another agent that needs a trusted restart note
- capturing blockers, decisions, and next actions before context goes stale
- reducing the cost of resuming a thread after a handoff

## What It Is Not For

- rebuilding the current task state before work continues
- deciding whether a task needs staged phases or checkpoints
- coordinating the atomic packages as one suite-level workflow
- replacing the final user-facing answer when no handoff is needed

## Install

Install `skill-handoff-summary` from this repository with the standard package path for published Codex skills.

You can ask Codex in natural language:

- `Use skill-installer to install skill-handoff-summary from Golden-Promise/codex-skill-library at skills/skill-handoff-summary.`
- `Use skill-installer to install skill-handoff-summary from Golden-Promise/codex-skill-library at skills/skill-handoff-summary using the release or ref I specify.`

## How To Use

Reach for this package when execution is about to pause or move to another owner.
Describe the current status, unresolved questions, blockers, and the very next actions, then have the skill turn that into a concise transfer note rather than a full re-plan.

## References

- `SKILL.md` for trigger routing and package boundaries
- [references/README.md](references/README.md) for the package boundary and the planned reader-facing reference scope
- `assets/` for future handoff, blocker, and next-step templates
