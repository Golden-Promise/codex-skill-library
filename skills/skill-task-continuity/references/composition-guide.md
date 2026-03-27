# Composition Guide

`skill-task-continuity` is the suite entry point for downstream teams that want the long-task continuity workflow to feel coherent without collapsing the atomic package boundaries.
Use it to explain how packets, root state, subtasks, gates, and handoffs fit together and to bootstrap downstream files, not to replace the atomic skills.

## How The Suite Fits Together

- `skill-context-keeper` refreshes current task state and keeps facts, assumptions, and decisions separated.
- `skill-subtask-context` owns bounded child-task state so subtask reasoning stays isolated from the root task.
- `skill-context-packet` compresses the minimum context needed for the next root or subtask turn.
- `skill-phase-gate` adds meaningful preflight or postflight checkpoints around substantial edits.
- `skill-handoff-summary` writes the continuation-oriented handoff when work pauses or changes owners.

The suite package exists so a downstream repository can install one entry point, learn the system from one place, and copy starter files into its own repo.
If the team wants all four packages available immediately, the suite can also be installed together with the three atomic packages in one `skill-installer` command.

## Install Choices

- install `skill-task-continuity` only when you want the suite entry point first
- install the full suite in one command when you want all six packages available right away

The suite package stays explicit: it does not auto-install the atomic skills for you.
Instead, it documents the existing multi-path `skill-installer` flow so users can choose one command without hidden side effects.

## Explicit Invocation Wording

Use the atomic skills with direct prompts like these:

- `Use $skill-context-keeper to refresh .agent-state/root/TASK_STATE.md before more implementation work.`
- `Use $skill-subtask-context to open or refresh .agent-state/subtasks/api-migration/TASK_STATE.md for this child task.`
- `Use $skill-context-packet to compress the next turn into .agent-state/root/PACKET.md before we continue.`
- `Use $skill-phase-gate for a preflight before this risky multi-file change.`
- `Use $skill-phase-gate for a postflight gate now that the refactor is done.`
- `Use $skill-handoff-summary to write the root or subtask handoff before we pause.`

If the request is about the suite itself, start with `skill-task-continuity` and then route into the atomic skill that owns the next action.

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

Beginner mode is the subset that only uses `INDEX.md` and `root/`.
Expanded mode starts when the repo opens real child-task folders under `subtasks/`.

## Recommended Long-Task Loop

1. Read `.agent-state/INDEX.md` first.
2. Start with `.agent-state/root/PACKET.md` or a subtask packet instead of loading full state by default.
3. If the packet is not enough, open the matching root or subtask task-state file.
4. If the next edit is substantial or risky, run a `skill-phase-gate` preflight.
5. Implement the change.
6. Refresh the matching root or subtask state file, then compress the next turn back into a packet.
7. Update the decisions log or run log only when the evidence is worth preserving.
8. If work stops, refresh the root or subtask handoff.

## Optional Repo-Local Wrapper Pattern

Some teams like to add repo-local helper prompts or examples under `.agents/skills/`.
That can be useful, but it is optional.
Keep wrappers thin and explicit, for example:

- `.agents/skills/refresh-task-state.md` that says to invoke `skill-context-keeper` for `.agent-state/root/TASK_STATE.md`
- `.agents/skills/open-subtask.md` that says to invoke `skill-subtask-context`
- `.agents/skills/compress-next-turn.md` that says to invoke `skill-context-packet`
- `.agents/skills/preflight-risky-change.md` that says to invoke `skill-phase-gate`
- `.agents/skills/write-handoff.md` that says to invoke `skill-handoff-summary`

Those wrappers should help local adoption without forking the public skill behavior.
