# Context Index

Use this file as the repo entry point for the context protocol.
Read it first, then open only the root or subtask packet you actually need.

## Beginner Mode

- Start with `.agent-state/root/PACKET.md`.
- Read `.agent-state/root/TASK_STATE.md` only when the packet is not enough.
- Stay in beginner mode when one agent owns one active task and there are no parallel subtasks yet.

## Expanded Mode

- Create a subtask folder under `.agent-state/subtasks/` when work splits into a bounded child task with its own owner, scope, or risk profile.
- Archive closed material under `.agent-state/archive/root/`, `.agent-state/archive/subtasks/`, or `.agent-state/archive/packets/`.
- Keep packets short and treat them as the default injection surface for the next turn.

## Root Artifacts

- `root/TASK_STATE.md`: durable top-level task state
- `root/PACKET.md`: minimum context to inject for the next root-level action
- `root/HANDOFF.md`: pause or transfer note for the top-level task
- `root/DECISIONS.md`: durable decisions to preserve
- `root/RUN_LOG.md`: session evidence worth keeping

## Active Subtasks

- Add one bullet per active subtask with its folder name, owner, and exact status.
- Point each bullet to the subtask packet first, then to deeper state only if needed.

## Compression Rules

- Keep packets smaller than task-state files.
- Move stale detail out of root state before it crowds out current facts.
- Prefer linking to evidence over copying long command transcripts into packets.
