# Agent Workflow

This repository uses the long-task continuity suite as a set of narrow, composable skills.
Invoke the atomic skills directly when you need continuity support; this `AGENTS.md` file explains when each one should take over.

## Entry Point

Start from `.agent-state/INDEX.md`.
Read the root packet or a subtask packet before loading a full state file.
Treat packets as the default injection surface and state files as the deeper source of truth.

## Atomic Skills

### Refresh task state with `skill-context-keeper`

Use wording like:

- `Use $skill-context-keeper to refresh .agent-state/root/TASK_STATE.md before more edits.`
- `Rebuild the current root task state, separate facts from assumptions, and update .agent-state/root/TASK_STATE.md.`

Reach for this when the root thread is stale, the repo has changed since the last turn, or the next agent needs a current snapshot before acting.

### Open or refresh a child task with `skill-subtask-context`

Use wording like:

- `Use $skill-subtask-context to open .agent-state/subtasks/parser-cleanup/TASK_STATE.md for this bounded child task.`
- `Refresh the local state for the parser-cleanup subtask without restating the whole parent task.`

Use it when a child task deserves its own owner, its own narrow scope, or a local note set that should not bloat the root task state.

### Compress the next turn with `skill-context-packet`

Use wording like:

- `Use $skill-context-packet to compress the next root turn into .agent-state/root/PACKET.md.`
- `Write the minimum packet for the parser-cleanup subtask before handing it off.`

Use it when the next agent only needs the minimum facts, constraints, and next action, not a full state refresh.

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

1. Read `.agent-state/INDEX.md`, then open the root packet or the active subtask packet before touching broader state files.
2. If the packet is not enough, open the matching root or subtask state file.
3. If the next change is meaningful or risky, run `skill-phase-gate` first so scope, non-goals, and validation stay explicit.
4. Execute the work, then refresh the matching root or subtask state file so the next turn inherits verified state.
5. Compress the next action back into a packet with `skill-context-packet`.
6. Record durable choices in `.agent-state/root/DECISIONS.md` and append session-level evidence to `.agent-state/root/RUN_LOG.md` only when it helps future resumes.
7. If work stops or ownership changes, use `skill-handoff-summary` to refresh the matching handoff with status, blockers, and the exact next action.

## Recommended Downstream Layout

```text
AGENTS.md
.agent-state/
  INDEX.md
  root/
    TASK_STATE.md
    PACKET.md
    HANDOFF.md
    DECISIONS.md
    RUN_LOG.md
  subtasks/
  archive/
    root/
    subtasks/
    packets/
```

These files are downstream consumer artifacts.
Beginner mode uses `INDEX.md` and `root/` only.
Expanded mode opens real child-task folders inside `subtasks/`.
These files are not meant to modify the public skill library itself.

## Optional Repo-Local Wrappers

You may add repo-local helper prompts or examples under `.agents/skills/` if they make invocation easier for your team.
That pattern is optional, not required.
Keep those wrappers thin: they should point back to the atomic skills above instead of replacing them.
