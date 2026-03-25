# skill-phase-gate Use Cases

`skill-phase-gate` is for meaningful checkpoints around substantial coding work.
Use it for a compact preflight before risky execution or a compact postflight after a meaningful edit, while leaving long-term task state with `skill-context-keeper`.

## Positive Trigger Prompts

- `Use skill-phase-gate to write a preflight gate before this multi-file refactor.`
- `Before I touch the migration, add a checkpoint with expected files, non-goals, and a verification plan.`
- `We just finished a meaningful edit. Run a postflight gate that records actual changes, validations, and remaining risks.`
- `Give me a pre-commit checkpoint for this risky edit so we can sanity-check scope and verification.`

## Negative Trigger Prompts

- `Fix this typo in one line and move on.`
- `Explain how this package works without generating any checkpoint artifact.`
- `Refresh the current task state and keep an ongoing summary for the next hour of work.`
- `Write the final handoff package for the next agent taking over.`

## Common Use Cases

### Preflight Before a Multi-File Change

Use the preflight gate when you want a fast statement of:

- the current goal
- the active constraints
- which files or modules you expect to touch
- which files or modules you are explicitly not changing
- how you plan to verify the work

This is especially useful before refactors, migrations, or edits where it is easy for scope to drift.

### Postflight After a Meaningful Edit

Use the postflight gate when implementation is done and you want to capture:

- which files or modules actually changed
- which validations you actually ran
- what risks remain
- whether a handoff is recommended

The postflight gate is a checkpoint, not a replacement for a final handoff package.

## State Ownership Boundary

If the thread also needs durable task-state ownership, keep that with `skill-context-keeper`.
`skill-phase-gate` may mention the current state briefly inside the checkpoint, but it does not own the running task record.
