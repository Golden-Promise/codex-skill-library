# skill-handoff-summary Use Cases

`skill-handoff-summary` is for compact continuation-oriented handoffs when coding work is about to pause or move to another owner.
Use it when the next session needs a trusted restart note, not when the conversation only needs a casual status update or a whole-project writeup.

## Positive Trigger Prompts

- `Use skill-handoff-summary to write a compact handoff before we pause for today.`
- `Write .agent-state/HANDOFF.md so the next session can resume this task without rereading the whole thread.`
- `Capture the current status, hard constraints, open problems, and exact next action for the next agent taking over.`
- `We are handing this thread to another coder. Prepare a concise continuation handoff with a resume prompt.`
- `Before stopping, turn this session into a short transfer summary instead of a full project recap.`

## Negative Trigger Prompts

- `Give me a quick status update in chat about what changed today.`
- `Write full project documentation for the repository so a new team can onboard.`
- `Refresh the current task state from the repo before we continue coding right now.`
- `Decide the next phase gate and tell me whether implementation can start.`
- `Create one big summary that covers planning, long-term state, and final handoff together.`

## When To Write A Handoff

Write the handoff before pausing work for a meaningful break or before handing the task to another thread or agent.
The package is especially useful when the next session would otherwise need to reconstruct blockers, preserved constraints, or the exact next move from scattered history.

## When Not To Use This Skill

Do not use this package for a simple in-chat status update where no durable artifact is needed.
Do not use it to produce full-project documentation, rebuild long-term task state, or decide workflow gates.

## Reusable Resume Prompt Wording

Use wording like this when you want the next session to restart immediately:

`Resume this task from .agent-state/HANDOFF.md. Continue from the recorded status, preserve the listed constraints, inspect the files of interest, resolve the open problems in priority order, perform the exact next action first, and update the handoff if anything material changes.`
