# skill-subtask-context Use Cases

`skill-subtask-context` is for maintaining isolated local child-task state during a larger task.
Use it when the work should split into a bounded subtask instead of stretching the root task summary further.

## Positive Trigger Prompts

- `Use skill-subtask-context to open a child task for the parser cleanup and write .agent-state/subtasks/parser-cleanup/TASK_STATE.md.`
- `Refresh the local state for the api-migration subtask without rewriting the full root task.`
- `This workstream needs its own owner, local risks, and exit criteria. Open a subtask state file for it.`
- `Capture the parent facts that still matter locally and keep the rest out of the child task.`
- `Close this child task by updating its merge notes and next recommended action.`

## Negative Trigger Prompts

- `Refresh the overall root task summary before we continue.`
- `Compress the next turn into a tiny packet instead of a full state file.`
- `Run a preflight gate before this risky refactor starts.`
- `Write the pause handoff for the next agent taking over this work.`
- `Bootstrap the whole continuity suite in a repository for the first time.`

## Subtask State Wording Patterns

Use wording like this when the request is specifically about local child-task state:

- `Open a child task for this bounded slice of work.`
- `Refresh the local subtask state without restating the whole parent task.`
- `Keep only the parent facts that this subtask must preserve.`
- `Record merge notes for the parent task before closing the child task.`

## Typical Output Shape

The package usually refreshes a compact state artifact such as `.agent-state/subtasks/<slug>/TASK_STATE.md` with:

- the subtask objective and local scope
- parent context worth preserving locally
- local facts, blockers, and exit criteria
- the next recommended action and merge notes
