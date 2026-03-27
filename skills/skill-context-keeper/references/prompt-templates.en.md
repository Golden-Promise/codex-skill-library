# skill-context-keeper Prompt Templates

Use these templates when you want `skill-context-keeper` to refresh or compress trusted root-task state without drifting into subtask-local state, packet compression, workflow gating, or final handoffs.

## Positive Trigger Prompts

- `Use skill-context-keeper to refresh the root task state from the repository before we continue.`
- `Reconcile the existing root summary with the codebase and rewrite .agent-state/root/TASK_STATE.md.`
- `Refresh the root task state, keep facts separate from assumptions, and list the next recommended action.`
- `Compress stale root-state detail into archive notes while preserving active facts.`

## Negative Trigger Prompts

- `Decide the project phases and gate the work before implementation starts.`
- `Open a child task with its own local state.`
- `Compress the next turn into a packet instead of refreshing full root state.`
- `Generate the final handoff note for the next agent and close out the thread.`
- `Handle planning, state refresh, and the final transfer as one combined workflow.`

## Refresh the Current Task State

Use this phrasing when you want a straightforward state refresh:

```text
Use skill-context-keeper to refresh the root task state.
Check the repository, keep verified facts separate from assumptions and decisions,
update .agent-state/root/TASK_STATE.md, add compression or archive notes if stale detail should move out of active state,
and end with the next recommended action plus verification still needed.
Do not add subtask-local state, packet compression, workflow gates, or a final handoff.
```

## Compact Resume Prompt

```text
Refresh the root task state for this long-running coding task.
Assume the downstream artifact lives at .agent-state/root/TASK_STATE.md.
Capture current objective, scope, hard constraints, verified codebase facts,
completed work, open risks, recent decisions, compression / archive notes, and the next recommended action.
Keep the package boundary narrow: root-state refresh and compression only.
```

## Facts, Assumptions, and Decisions Prompt

```text
Rebuild the task state and explicitly label each item as Fact, Assumption, or Decision.
Use repository evidence for facts, keep assumptions short, and record only decisions that are already made.
Write the refreshed state to .agent-state/root/TASK_STATE.md without creating subtask-local state, a packet, a phase gate, or a final handoff.
```
