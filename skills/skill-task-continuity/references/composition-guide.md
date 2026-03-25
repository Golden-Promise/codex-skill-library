# Composition Guide

`skill-task-continuity` is the suite entry point for downstream teams that want the long-task continuity workflow to feel coherent without collapsing the atomic package boundaries.
Use it to explain how the pieces fit together and to bootstrap downstream files, not to replace the atomic skills.

## How The Suite Fits Together

- `skill-context-keeper` refreshes current task state and keeps facts, assumptions, and decisions separated.
- `skill-phase-gate` adds meaningful preflight or postflight checkpoints around substantial edits.
- `skill-handoff-summary` writes the continuation-oriented handoff when work pauses or changes owners.

The suite package exists so a downstream repository can install one entry point, learn the system from one place, and copy starter files into its own repo.

## Explicit Invocation Wording

Use the atomic skills with direct prompts like these:

- `Use $skill-context-keeper to refresh .agent-state/TASK_STATE.md before more implementation work.`
- `Use $skill-phase-gate for a preflight before this risky multi-file change.`
- `Use $skill-phase-gate for a postflight gate now that the refactor is done.`
- `Use $skill-handoff-summary to write .agent-state/HANDOFF.md before we pause.`

If the request is about the suite itself, start with `skill-task-continuity` and then route into the atomic skill that owns the next action.

## Recommended Downstream Layout

```text
AGENTS.md
.agent-state/
  TASK_STATE.md
  HANDOFF.md
  DECISIONS.md
  RUN_LOG.md
```

This layout is intentionally small.
The suite ships templates for these files so the downstream repo can standardize how agents resume work.

## Recommended Long-Task Loop

1. Read `.agent-state/TASK_STATE.md` and `.agent-state/HANDOFF.md` before taking over the task.
2. If the next edit is substantial or risky, run a `skill-phase-gate` preflight.
3. Implement the change.
4. Refresh `.agent-state/TASK_STATE.md` with `skill-context-keeper`.
5. Update `.agent-state/DECISIONS.md` or `.agent-state/RUN_LOG.md` if you made a durable choice or ran checks worth preserving.
6. If work stops, refresh `.agent-state/HANDOFF.md` with `skill-handoff-summary`.

## Optional Repo-Local Wrapper Pattern

Some teams like to add repo-local helper prompts or examples under `.agents/skills/`.
That can be useful, but it is optional.
Keep wrappers thin and explicit, for example:

- `.agents/skills/refresh-task-state.md` that says to invoke `skill-context-keeper` for `.agent-state/TASK_STATE.md`
- `.agents/skills/preflight-risky-change.md` that says to invoke `skill-phase-gate`
- `.agents/skills/write-handoff.md` that says to invoke `skill-handoff-summary`

Those wrappers should help local adoption without forking the public skill behavior.
