# skill-context-keeper Use Cases

`skill-context-keeper` is for maintaining structured long-task state while work is still in progress.
Use it when the thread needs a reliable refresh of the current task picture, not when it needs staged workflow control or a final handoff.

## Positive Trigger Prompts

- `Use skill-context-keeper to refresh the current task state before we continue coding.`
- `Rebuild the current task picture from the repo and update .agent-state/TASK_STATE.md.`
- `The summary is stale. Reconstruct facts, open risks, and the next action for this task.`
- `Refresh the current task state and carry forward unresolved work without making a handoff note.`
- `Before we continue, update the structured state file at .agent-state/TASK_STATE.md with verified codebase facts.`

## Negative Trigger Prompts

- `Split this migration into phases with checkpoints before we start implementation.`
- `Write the final handoff summary for the next agent taking over this task.`
- `Create a release checklist and decide which phase gate we need to pass next.`
- `Prepare the final user-facing completion note and wrap up the task.`
- `Coordinate the whole continuity suite for planning, state refresh, and handoff generation.`

## Refresh Wording Patterns

Use wording like this when the request is specifically about refreshing state:

- `Refresh the current task state.`
- `Update the working state snapshot for this task.`
- `Reconcile the current summary with the repository and rewrite the task state file.`
- `Bring .agent-state/TASK_STATE.md up to date before more implementation.`

## Facts vs Assumptions vs Decisions Example

Example for `.agent-state/TASK_STATE.md`:

- Fact: `tests/test_package_contract.py` exists and currently checks for trigger sections in both use-case references.
- Assumption: The next agent will continue using `.agent-state/TASK_STATE.md` as the downstream path because the package examples point there.
- Decision: Keep this package focused on state maintenance only, so phase gates and final handoffs stay in sibling packages.

## Typical Output Shape

The package usually refreshes a compact state artifact such as `.agent-state/TASK_STATE.md` with:

- verified facts from the codebase
- unresolved risks and open questions
- the next recommended action
- verification still needed before claiming completion
