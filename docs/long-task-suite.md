# Long-Task Continuity Suite

## Problem Statement

Long-running work rarely fails in one dramatic moment.
It drifts.

- root state becomes stale or bloated
- child-task details leak into the wrong place
- the next turn loads too much context
- risky edits lose checkpoints
- pauses leave the next agent guessing

The context protocol exists to make those failure modes explicit and routable.
Instead of treating “continuity” as one vague summary problem, the suite separates root state, subtask state, packet compression, checkpoints, and handoffs.

## The Context Protocol

The current suite is organized around three state layers:

- **Root state:** the durable top-level picture for the main task
- **Subtask state:** bounded child-task context that should not pollute the root summary
- **Packets:** the minimum context object for the next root or subtask turn

These layers are backed by a repo-first starter layout:

- `AGENTS.md`
- `.agent-state/INDEX.md`
- `.agent-state/root/`
- `.agent-state/subtasks/`
- `.agent-state/archive/`

Beginner mode usually stays in `INDEX.md` plus `.agent-state/root/`.
Expanded mode starts when work is split into child tasks or archived into packet-sized continuation objects.

## Package Map

| Package | Responsibility | Trigger Shape |
| --- | --- | --- |
| `skill-context-keeper` | Refresh and compress trusted root-task state. | The root task is active but stale, noisy, or bloated. |
| `skill-subtask-context` | Open, refresh, or close bounded child-task state. | A child task needs its own local scope and restart state. |
| `skill-context-packet` | Write the minimum context packet for the next turn. | The next step needs less than a full state file. |
| `skill-phase-gate` | Add an optional operational checkpoint around risky work. | A meaningful multi-file change needs explicit preflight or postflight control. |
| `skill-handoff-summary` | Capture a compact root or subtask handoff. | Work is about to pause, transfer, or cross sessions. |
| `skill-task-continuity` | Bootstrap the suite and route to the correct atomic package. | A repo needs starter files, protocol guidance, or package-selection help. |

## Compatibility And Migration

If you previously thought of this suite as four packages that handled “state, gates, handoff, and orchestration,” you should read the migration guide:

- [docs/context-protocol-migration.md](context-protocol-migration.md)
- [docs/context-protocol-migration.zh-CN.md](context-protocol-migration.zh-CN.md)

The short version:

- root-state refresh still belongs to `skill-context-keeper`
- `skill-phase-gate` is no longer the continuity center
- subtask isolation now has a first-class owner: `skill-subtask-context`
- minimal next-turn injection now has a first-class owner: `skill-context-packet`

## Repository Boundary Rules

This repository is a public installable skill library, so the suite docs must stay reader-facing and maintainable.

- Keep public architecture in `docs/`, not in live repo state files for this library itself.
- Treat `evals/cases.csv` as the normalized routing matrix, not as a private scratchpad.
- Prefer the narrowest package that matches the request.
- Do not let the suite entry package steal work that belongs to a single atomic package.
- Keep beginner-mode guidance obvious for users who do not need subtask splitting yet.
- Keep migration guidance explicit so older four-package users do not guess their way into the new model.

## Success Criteria

The suite is successful when a downstream repo can follow this path without rereading a whole thread:

1. bootstrap continuity starter files
2. refresh root state
3. split a bounded subtask
4. inject only a packet into the next execution turn
5. checkpoint a risky change when needed
6. pause with a valid handoff
7. resume from root or subtask artifacts without context bleed

## Seed Evaluation Matrix

The seed matrix lives in `evals/cases.csv`.
It now validates the protocol model rather than the older flat-layout model.

| Case | Package | Trigger | Prompt Shape | Expected Artifacts | Expected Events |
| --- | --- | --- | --- | --- | --- |
| `root_state_refresh` | `skill-context-keeper` | Yes | Refresh the root task picture from the repo. | `root/task_state` | `root:refresh`, `root:reconcile`, `root:compress` |
| `root_state_compress` | `skill-context-keeper` | Yes | Shrink bloated root state without opening a new packet-only flow. | `root/task_state` | `root:refresh`, `root:reconcile`, `root:compress` |
| `root_state_refresh_not_needed` | `skill-context-keeper` | No | A trivial one-off ask with no continuity risk. | `none` | `root:skip`, `route:other` |
| `subtask_split_from_root` | `skill-subtask-context` | Yes | Split bounded child work from the root thread. | `subtask/task_state` | `subtask:split`, `subtask:refresh`, `subtask:isolate` |
| `subtask_resume_from_packet` | `skill-subtask-context` | Yes | Refresh local state for a child task resumed from a packet. | `subtask/task_state` | `subtask:split`, `subtask:refresh`, `subtask:isolate` |
| `subtask_state_not_needed` | `skill-subtask-context` | No | Stay in root state; do not open a child task. | `none` | `subtask:skip`, `route:root_or_packet` |
| `packet_root_minimal_injection` | `skill-context-packet` | Yes | Compress the next root turn into a minimal packet. | `root/packet` | `packet:compose`, `packet:trim`, `packet:inject` |
| `packet_not_needed_for_full_refresh` | `skill-context-packet` | No | Do a full-state refresh instead of packet compression. | `none` | `packet:skip`, `route:state_or_handoff` |
| `phase_gate_risky_checkpoint` | `skill-phase-gate` | Yes | Add a checkpoint around risky multi-file work. | `phase/preflight`, `phase/postflight` | `phase:preflight`, `phase:checkpoint`, `phase:postflight` |
| `tiny_edit_not_gate` | `skill-phase-gate` | No | Make a trivial local edit. | `none` | `phase:skip`, `direct:edit` |
| `handoff_subtask_pause` | `skill-handoff-summary` | Yes | Pause a child task and leave a restart note. | `subtask/handoff` | `handoff:capture`, `handoff:pause`, `handoff:resume` |
| `handoff_not_needed` | `skill-handoff-summary` | No | Give a final answer with no continuation artifact. | `none` | `handoff:skip`, `direct:answer` |
| `suite_bootstrap_protocol` | `skill-task-continuity` | Yes | Bootstrap the protocol and route across the suite. | `suite/agents`, `suite/index`, root and subtask templates | `suite:bootstrap`, `suite:route`, `suite:explain` |
| `suite_boundary_clean` | `skill-task-continuity` | No | Mention continuity keywords inside a trivial README fix. | `none` | `suite:skip`, `direct:edit` |

## Validation Strategy

The current static harness checks:

- routing polarity
- exact event namespaces
- strict artifact mapping
- required file presence
- workflow-doc coverage
- boundary language in published docs

That gives maintainers a regression surface for the protocol without requiring live model execution.
