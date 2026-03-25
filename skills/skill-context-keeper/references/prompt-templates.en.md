# skill-context-keeper Prompt Templates

Use these templates when you want `skill-context-keeper` to refresh structured long-task state without drifting into workflow gating or final handoffs.

## Positive Trigger Prompts

- `Use skill-context-keeper to refresh the current task state from the repository before we continue.`
- `Reconcile the existing summary with the codebase and rewrite .agent-state/TASK_STATE.md.`
- `Refresh the current task state, keep facts separate from assumptions, and list the next recommended action.`

## Negative Trigger Prompts

- `Decide the project phases and gate the work before implementation starts.`
- `Generate the final handoff note for the next agent and close out the thread.`
- `Handle planning, state refresh, and the final transfer as one combined workflow.`

## Refresh the Current Task State

Use this phrasing when you want a straightforward state refresh:

```text
Use skill-context-keeper to refresh the current task state.
Check the repository, keep verified facts separate from assumptions and decisions,
update .agent-state/TASK_STATE.md, and end with the next recommended action plus verification still needed.
Do not add workflow gates or a final handoff.
```

## Compact Resume Prompt

```text
Refresh the current task state for this long-running coding task.
Assume the downstream artifact lives at .agent-state/TASK_STATE.md.
Capture current objective, scope, hard constraints, verified codebase facts,
completed work, open risks, recent decisions, and the next recommended action.
Keep the package boundary narrow: state maintenance only.
```

## Facts, Assumptions, and Decisions Prompt

```text
Rebuild the task state and explicitly label each item as Fact, Assumption, or Decision.
Use repository evidence for facts, keep assumptions short, and record only decisions that are already made.
Write the refreshed state to .agent-state/TASK_STATE.md without generating a phase gate or final handoff.
```
