# Agent Workflow

This repository uses the long-task continuity suite as a set of narrow, composable skills.
Invoke the atomic skills directly when you need continuity support; this `AGENTS.md` file explains when each one should take over.

## Atomic Skills

### Refresh task state with `skill-context-keeper`

Use wording like:

- `Use $skill-context-keeper to refresh .agent-state/TASK_STATE.md before more edits.`
- `Rebuild the current task state, separate facts from assumptions, and update .agent-state/TASK_STATE.md.`

Reach for this when the thread is stale, the repo has changed since the last turn, or the next agent needs a current snapshot before acting.

### Gate meaningful changes with `skill-phase-gate`

Use wording like:

- `Use $skill-phase-gate for a preflight before this multi-file refactor.`
- `Run a postflight gate for the files I changed and record remaining risks.`

Use it only when the checkpoint itself adds value, such as before or after a risky edit, refactor, migration, or pre-commit review.

### Generate a handoff with `skill-handoff-summary`

Use wording like:

- `Use $skill-handoff-summary to write .agent-state/HANDOFF.md before we pause.`
- `Create a continuation-oriented handoff with the exact next action and a resume prompt.`

Use it when work is pausing, changing owners, or needs a trusted restart note for the next session.

## Recommended Long-Task Loop

1. Read `.agent-state/TASK_STATE.md`, `.agent-state/HANDOFF.md`, and any recent notes in `.agent-state/` before resuming work.
2. If the next change is meaningful or risky, run `skill-phase-gate` first so scope, non-goals, and validation stay explicit.
3. Execute the work, then refresh `.agent-state/TASK_STATE.md` with `skill-context-keeper` so the next turn inherits verified state.
4. Record durable choices in `.agent-state/DECISIONS.md` and append session-level evidence to `.agent-state/RUN_LOG.md` when it helps future resumes.
5. If work stops or ownership changes, use `skill-handoff-summary` to refresh `.agent-state/HANDOFF.md` with status, blockers, and the exact next action.

## Recommended Downstream Layout

```text
AGENTS.md
.agent-state/
  TASK_STATE.md
  HANDOFF.md
  DECISIONS.md
  RUN_LOG.md
```

These files are downstream consumer artifacts.
They are not meant to modify the public skill library itself.

## Optional Repo-Local Wrappers

You may add repo-local helper prompts or examples under `.agents/skills/` if they make invocation easier for your team.
That pattern is optional, not required.
Keep those wrappers thin: they should point back to the atomic skills above instead of replacing them.
