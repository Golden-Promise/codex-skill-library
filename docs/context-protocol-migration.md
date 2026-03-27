# Context Protocol Migration Guide

## Who This Is For

Use this guide if you already know the older long-task continuity suite and need to understand what changed.

You can ignore this guide if:

- you are starting fresh with the current six-package suite
- you only need one atomic package and do not care about the broader workflow
- you are reading package docs directly and do not need the historical bridge

## Why The Model Changed

The older continuity framing was useful, but it still treated too much work as “state vs gate vs handoff.”
That left two important jobs under-modeled:

- isolated child-task context
- minimum next-turn context injection

The context protocol makes both of those first-class.

## Old Model vs New Model

| Older Mental Model | Context Protocol Replacement |
| --- | --- |
| One task state that keeps growing | Separate `root/` state from `subtasks/` state |
| Summaries are the main continuity object | Packets become the default next-turn injection object |
| `skill-phase-gate` often feels central | `skill-phase-gate` is now an optional checkpoint only |
| Handoff is mostly a flat `.agent-state/HANDOFF.md` | Handoff can target root or subtask scope |
| Orchestration is mainly about four packages | Suite routing now spans six packages and a layered repo layout |

## Package Mapping

### Still The Same In Spirit

- `skill-context-keeper`
  - still owns trusted root-task refresh
  - now explicitly owns root-state compression too
- `skill-handoff-summary`
  - still owns continuation-oriented pause artifacts
  - now works for both root and subtask scope
- `skill-task-continuity`
  - still owns bootstrap and package routing
  - now boots a layered protocol layout instead of a flat one

### Newly First-Class

- `skill-subtask-context`
  - owns bounded child-task state under `.agent-state/subtasks/<slug>/`
- `skill-context-packet`
  - owns minimum next-turn packets under `.agent-state/root/PACKET.md` or `.agent-state/subtasks/<slug>/PACKET.md`

### Narrowed On Purpose

- `skill-phase-gate`
  - no longer acts like the center of continuity
  - only adds an optional operational checkpoint around risky work

## How To Adopt The New Workflow

### Recommended Path

1. Start in beginner mode.
2. Bootstrap `AGENTS.md`, `.agent-state/INDEX.md`, and `.agent-state/root/`.
3. Keep using `skill-context-keeper` for root-state refresh.
4. When the root summary gets noisy, split one bounded child task with `skill-subtask-context`.
5. When the next turn does not need the whole state file, create a packet with `skill-context-packet`.
6. Use `skill-phase-gate` only when the checkpoint itself adds value.
7. Use `skill-handoff-summary` whenever work pauses or ownership changes.

### Beginner Mode

You usually only need:

- `.agent-state/INDEX.md`
- `.agent-state/root/TASK_STATE.md`
- `.agent-state/root/PACKET.md`
- `.agent-state/root/HANDOFF.md`

Stay here until you have a real child task with a different owner, scope, or risk boundary.

### Expanded Mode

Move into expanded mode when at least one of these becomes true:

- the root task is carrying too much unrelated local detail
- another agent should own a bounded slice of the work
- packet-sized continuation is better than loading the whole root summary
- archived stale detail is making active state unreadable

## Common Mistakes

### Treating Packets As Full State

Packets are not the durable canonical record.
They are the minimum next-turn injection object.
If you keep shoving full history into packets, you lose the point of compression.

### Keeping Child-Task Detail In Root State

If a child task has its own files, risks, and exit criteria, give it its own state.
Otherwise the root summary becomes the place where all context goes to rot.

### Using `skill-phase-gate` As The Continuity Center

If the main problem is stale state, use `skill-context-keeper`.
If the main problem is bounded child-task isolation, use `skill-subtask-context`.
If the main problem is context budget, use `skill-context-packet`.

### Writing Handoffs For Work That Is Not Actually Pausing

If the work is still live and the next turn just needs a small injection surface, write a packet instead of a handoff.

## What Does Not Change

- public install paths stay under `skills/<skill-name>/`
- the suite is still repo-first and documentation-first
- routing remains narrow on purpose
- static evals remain the maintainer regression surface

## Quick Decision Table

| Need | Use |
| --- | --- |
| Refresh the main task picture | `skill-context-keeper` |
| Open or refresh a child task | `skill-subtask-context` |
| Shrink the next turn into minimal context | `skill-context-packet` |
| Add a risky-change checkpoint | `skill-phase-gate` |
| Pause or transfer with a durable note | `skill-handoff-summary` |
| Bootstrap the suite or choose the next package | `skill-task-continuity` |
