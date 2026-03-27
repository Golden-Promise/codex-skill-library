# skill-subtask-context Prompt Templates

Use these templates when you want `skill-subtask-context` to open or refresh isolated child-task state without drifting into root-state refresh, packet compression, gates, or handoffs.

## Positive Trigger Prompts

- `Use skill-subtask-context to open a child task for this bounded workstream.`
- `Refresh the local state at .agent-state/subtasks/<slug>/TASK_STATE.md and keep only the parent facts that still matter.`
- `Update the subtask objective, local blockers, exit criteria, and merge notes before we continue.`

## Negative Trigger Prompts

- `Refresh the root task summary before the next turn.`
- `Compress the next turn into a packet.`
- `Gate this risky change before implementation.`
- `Write the pause handoff for the next owner.`

## Open a New Child Task

```text
Use skill-subtask-context to open a child task.
Write or refresh .agent-state/subtasks/<slug>/TASK_STATE.md,
copy in only the parent facts that the child task must preserve,
define local scope, local risks, exit criteria, and the next recommended action,
and keep the boundary narrow: local child-task state only.
```

## Refresh an Existing Child Task

```text
Refresh the local state for this child task without rewriting the full root task.
Assume the downstream artifact lives at .agent-state/subtasks/<slug>/TASK_STATE.md.
Capture parent context that still matters locally, new verified facts, blockers,
verification still needed, and merge / closure notes for the parent task.
Do not compress a packet or generate a handoff.
```
