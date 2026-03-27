# skill-context-packet Use Cases

`skill-context-packet` is for compressing the next root or subtask turn into a minimum context object.
Use it when the next agent should load only the smallest useful packet instead of a full state file.

## Positive Trigger Prompts

- `Use skill-context-packet to compress the next turn into .agent-state/root/PACKET.md.`
- `Write a compact packet for the parser-cleanup subtask and keep only the facts that still matter.`
- `The state file is too large for the next turn. Compress it into a packet-first restart object.`
- `Prepare the minimum context object for a handoff between active owners without rewriting the whole task.`
- `Update the packet so the next agent can start with the exact next command.`

## Negative Trigger Prompts

- `Refresh the full root task state before we continue.`
- `Open a new child task with local state and merge notes.`
- `Run a preflight gate before this risky multi-file change.`
- `Write the pause handoff for the next session.`
- `Bootstrap the continuity suite in this repository.`

## Packet Wording Patterns

Use wording like this when the request is specifically about packet compression:

- `Compress the next turn into a packet.`
- `Write the minimum context object for the next agent.`
- `Keep only the facts, constraints, and next command that still matter.`
- `Shrink this state into a packet-first restart note.`

## Typical Output Shape

The package usually refreshes `.agent-state/root/PACKET.md` or `.agent-state/subtasks/<slug>/PACKET.md` with:

- the objective for the next turn
- the smallest useful scope and input list
- the facts and constraints worth preserving
- risks, exit criteria, and the next command
