# skill-phase-gate Prompt Templates

Use these prompts when you want a crisp optional operational checkpoint around meaningful coding work.
If you need durable root-state ownership, subtask-local state, or packet compression too, keep those with sibling packages.

## Positive Trigger Prompts

- `Use skill-phase-gate to create a preflight gate before this multi-file change.`
- `Use skill-phase-gate to create a postflight gate for this meaningful edit before I commit.`

## Negative Trigger Prompts

- `Skip the checkpoint and just fix this one-line typo.`
- `Explain the code only; do not create a checkpoint artifact.`
- `Refresh the root task state instead of adding a gate.`
- `Compress the next turn into a packet instead of adding a gate.`

## Preflight Template Prompt

```text
Use skill-phase-gate to create a preflight gate for this meaningful coding task.
Capture the current goal, current constraints, expected files or modules to change,
files or modules explicitly not changing, and the verification plan.
Keep it brief, checklist-oriented, and task-first.
Do not turn this into generic planning or long-term state tracking.
If durable root-state ownership is needed, leave that to skill-context-keeper.
If subtask-local state is needed, leave that to skill-subtask-context.
If packet compression is needed, leave that to skill-context-packet.
```

## Postflight Template Prompt

```text
Use skill-phase-gate to create a postflight gate for this meaningful coding task.
Capture the actual files or modules changed, the actual validations run,
remaining risks, and whether handoff is recommended.
Keep it operational and brief.
Do not turn this into a final handoff package, and do not take over root-state ownership from skill-context-keeper, subtask state from skill-subtask-context, or packet compression from skill-context-packet.
```

## Trivial Change Anti-Example

```text
This is only a one-line typo fix. Do not use skill-phase-gate.
Make the edit directly without adding a preflight or postflight checkpoint.
```
