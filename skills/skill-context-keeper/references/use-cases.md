# skill-context-keeper Use Cases

`skill-context-keeper` is for maintaining trusted root-task state while work is still in progress.
Use it when the thread needs a reliable refresh of the root task picture or a root-state compression pass, not when it needs subtask-local state, packet compression, staged workflow control, or a final handoff.

## Positive Trigger Prompts

- `Use skill-context-keeper to refresh the root task state before we continue coding.`
- `Rebuild the current root task picture from the repo and update .agent-state/root/TASK_STATE.md.`
- `The root summary is stale. Reconstruct facts, open risks, and the next action for this task.`
- `Refresh the root task state and carry forward unresolved work without making a handoff note.`
- `Before we continue, update .agent-state/root/TASK_STATE.md with verified codebase facts and compression notes.`

## Negative Trigger Prompts

- `Split this migration into phases with checkpoints before we start implementation.`
- `Open a child task with its own local state for the parser cleanup.`
- `Compress the next turn into a small packet instead of rewriting full state.`
- `Write the final handoff summary for the next agent taking over this task.`
- `Create a release checklist and decide which phase gate we need to pass next.`
- `Prepare the final user-facing completion note and wrap up the task.`
- `Coordinate the whole continuity suite for planning, state refresh, and handoff generation.`

## Refresh Wording Patterns

Use wording like this when the request is specifically about refreshing state:

- `Refresh the root task state.`
- `Update the working root-state snapshot for this task.`
- `Reconcile the current root summary with the repository and rewrite the task-state file.`
- `Bring .agent-state/root/TASK_STATE.md up to date before more implementation.`
- `Compress stale root-state detail into archive notes while preserving active facts.`

## Facts vs Assumptions vs Decisions Example

Example for `.agent-state/root/TASK_STATE.md`:

- Fact: `tests/test_package_contract.py` exists and currently checks for trigger sections in both use-case references.
- Assumption: The next agent will continue using `.agent-state/root/TASK_STATE.md` as the downstream path because the package examples point there.
- Decision: Keep this package focused on root-state refresh and compression only, so subtask state, packets, phase gates, and handoffs stay in sibling packages.

## Typical Output Shape

The package usually refreshes a compact state artifact such as `.agent-state/root/TASK_STATE.md` with:

- verified facts from the codebase
- unresolved risks and open questions
- compression or archive notes for stale detail
- the next recommended action
- verification still needed before claiming completion
