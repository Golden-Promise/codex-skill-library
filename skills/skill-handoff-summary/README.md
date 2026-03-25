# skill-handoff-summary

[简体中文](README.zh-CN.md)

## Overview

`skill-handoff-summary` is the narrow package for writing continuation-oriented pause or transfer summaries when long-running coding work needs to stop and resume later.
It packages status, blockers, preserved constraints, and the exact next action so the next session does not have to reconstruct intent from scattered thread history.
It is for compact handoffs such as `.agent-state/HANDOFF.md`, not whole-project documentation.

## Best For

- pausing work at the end of a session with open tasks still pending
- transferring a task to another agent that needs a trusted restart note
- capturing blockers, decisions, and next actions before context goes stale
- reducing the cost of resuming a thread after a handoff

## What It Is Not For

- rebuilding the current task state before work continues
- deciding whether a task needs staged phases or checkpoints
- coordinating the atomic packages as one suite-level workflow
- maintaining long-term state across the whole task
- producing whole-project documentation or repository tours
- replacing the final user-facing answer when no handoff is needed

## Package Boundary

Use this package when the work is pausing or changing hands and the next session needs a fast restart note.
Keep the output continuation-oriented, compact, and immediately actionable.

This package specializes in handoff creation only:

- write or refresh a concise artifact such as `.agent-state/HANDOFF.md`
- preserve the task summary, current status, hard constraints, open problems, and the exact next action
- include a reusable resume prompt for the next session

This package does not own long-term state, does not own workflow gating, and should not expand into whole-project documentation.

## Install

Install `skill-handoff-summary` from this repository with the standard package path for published Codex skills.

You can ask Codex in natural language:

- `Use skill-installer to install skill-handoff-summary from Golden-Promise/codex-skill-library at skills/skill-handoff-summary.`
- `Use skill-installer to install skill-handoff-summary from Golden-Promise/codex-skill-library at skills/skill-handoff-summary using the release or ref I specify.`

Or run `skill-installer` directly:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-handoff-summary
```

Pin the planned continuity-suite release:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-handoff-summary \
  --ref v0.6.0
```

## How To Use

Reach for this package when execution is about to pause or move to another owner.
Describe the current status, unresolved questions, blockers, hard constraints, and the very next action, then have the skill turn that into a concise continuation-oriented transfer note rather than a full re-plan.
If you want a concrete downstream artifact, say so explicitly, for example: `Write the handoff to .agent-state/HANDOFF.md and end with a resume prompt for the next session.`

## References

- `SKILL.md` for trigger routing and package boundaries
- [references/README.md](references/README.md) for the reader-facing reference index
- [references/use-cases.md](references/use-cases.md) for positive and negative trigger examples
- [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md) for Chinese trigger examples
- [references/prompt-templates.en.md](references/prompt-templates.en.md) for reusable handoff and resume prompts
- [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md) for reusable Chinese handoff and resume prompts
- [assets/HANDOFF.template.md](assets/HANDOFF.template.md) for the compact handoff artifact template
