# skill-handoff-summary Prompt Templates

Use these templates when you want `skill-handoff-summary` to create a compact continuation handoff without drifting into whole-project documentation, root-state refresh, long-term state management, or workflow gating.

## Positive Trigger Prompts

- `Use skill-handoff-summary to capture a continuation handoff before we pause this task.`
- `Write .agent-state/root/HANDOFF.md with current status, preserved constraints, open problems, and the exact next action.`
- `Write .agent-state/subtasks/<slug>/HANDOFF.md with current status, preserved constraints, open problems, and the exact next action.`
- `Prepare a concise transfer note for the next agent and end with a reusable resume prompt.`

## Negative Trigger Prompts

- `Give me a short status update in chat and do not write any durable artifact.`
- `Document the whole repository for future maintainers.`
- `Rebuild the current task state and decide the next workflow gate.`
- `Refresh the root task state instead of writing a pause artifact.`

## Write A Compact Handoff

```text
Use skill-handoff-summary to write a compact continuation-oriented handoff for the root task or a subtask.
Target .agent-state/root/HANDOFF.md or .agent-state/subtasks/<slug>/HANDOFF.md.
Summarize the task, current status, changes from this session, hard constraints to preserve,
files or modules of interest, open problems, and the exact next action.
End with a resume prompt the next session can reuse immediately.
Do not turn it into whole-project documentation, root-state refresh, long-term state, or workflow gating.
```

## Resume Prompt

```text
Resume this task from the recorded handoff.
Continue from the recorded status, preserve the listed constraints, inspect the files of interest,
resolve the open problems in priority order, perform the exact next action first,
and update the handoff if anything material changes.
```
