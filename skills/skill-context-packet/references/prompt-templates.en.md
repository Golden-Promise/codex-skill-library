# skill-context-packet Prompt Templates

Use these templates when you want `skill-context-packet` to compress the next turn into a minimum context object without drifting into full state refresh, gates, or handoffs.

## Positive Trigger Prompts

- `Use skill-context-packet to compress the next turn into .agent-state/root/PACKET.md.`
- `Write a compact packet for this subtask and keep only the facts that still matter.`
- `Shrink this state into a packet-first restart object with one exact next command.`

## Negative Trigger Prompts

- `Refresh the full root task state before we continue.`
- `Open a child task with its own local state.`
- `Run a risky-change gate before editing.`
- `Write the pause handoff for the next session.`

## Compress the Next Turn

```text
Use skill-context-packet to compress the next turn.
Write or refresh .agent-state/root/PACKET.md or .agent-state/subtasks/<slug>/PACKET.md,
preserve only the objective, narrow scope, smallest useful inputs,
verified facts, hard constraints, risks, exit criteria, and the next command,
and keep the boundary narrow: packet compression only.
```

## Rewrite a Bloated State File into a Packet

```text
This state file is too large for the next turn.
Compress it into a minimum context object for the next owner.
Drop stale detail, keep only what the next turn must know,
and end with the exact next command or prompt.
Do not refresh full state, run a gate, or generate a handoff.
```
