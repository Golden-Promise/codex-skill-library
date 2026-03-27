# Context Protocol + Repo Workflow Design

**Date:** 2026-03-26
**Status:** Draft
**Scope:** Product model and implementation direction for the next generation of the long-task continuity suite
**Audience:** Maintainers of `codex-skill-library` and downstream users adopting the suite for long-running coding tasks

## Summary

The current long-task continuity suite already provides useful continuity primitives:
state refresh, checkpoints, handoff writing, and bootstrap guidance.
It does not yet behave like a full context-management system for small-team or multi-agent work.

This design proposes a layered hybrid model:

- a **Context Protocol** that defines how task state, subtask state, context packets, compression, and handoff should work
- a **Repo Workflow** that makes the protocol usable through repository files, default wrappers, and lightweight operational flows

The goal is to let agents resume, split, hand off, and compress work without rereading entire thread histories or flooding the active context window with stale information.

## Problem Statement

The current suite is strong on package boundaries and durable artifacts, but it still has four major product gaps:

1. **Subtask isolation is weak**
   The suite does not yet model subtasks as first-class context owners with independent state and handoff surfaces.
2. **Just-in-time context injection is implicit**
   Current guidance helps users choose the next skill, but does not define a minimal context packet for the next action.
3. **Compression is template-level, not system-level**
   Current artifacts are compact, but there is no explicit lifecycle for pruning, rolling up, and archiving stale state.
4. **Day-2 operation still expects informed users**
   Installation is friendly, but sustained use still depends on manual judgment about which artifact to update and which context to carry forward.

## Target Users

### Primary User

Small teams or multi-agent workflows that need:

- durable task continuity across sessions
- safe subtask splitting
- low-noise handoffs
- predictable repo-local artifacts that can be shared by humans and agents

### Secondary User

Individual developers running long tasks in a single repository who still benefit from the same repo-first workflow, even if they never use multiple concurrent agents.

## Product Goals

### 1. Context Isolation

Subtasks must have independent local context so execution noise from one unit of work does not contaminate another.

### 2. Just-In-Time Injection

Agents should receive the minimum sufficient context for the next action instead of broad, eager context loading.

### 3. Context Compression

The active context window should stay lean while useful history remains available through layered summaries and archive paths.

### 4. Beginner-Friendly Adoption

The default repository workflow must be simple enough that a new user can succeed without first understanding the full protocol model.

## Non-Goals

- This project is not trying to become a general project-management system.
- This project is not trying to replace issue trackers, kanban tools, or long-form project docs.
- This project is not trying to create hidden automatic orchestration that users cannot inspect.
- This project is not required to preserve the exact current four-skill topology.
- V1 does not need native integrations for every agent platform if the repo-first workflow is coherent and portable.

## Design Principles

### Protocol First, Repo First In Practice

The protocol must be defined clearly before the workflow is implemented, but the first user experience should still be repository files and natural-language invocation.

### State Is Layered

Current state, subtask state, handoff state, and execution logs must not collapse into one undifferentiated summary.

### Minimal Sufficient Context

Default injection should be constrained to the smallest useful packet for the current action.

### Compression Is Active Work

Compression is not "write a shorter paragraph." It is the deliberate movement of information between active, working, and archive layers.

### Subtasks Are First-Class Objects

A subtask is not a note under the root task. It is an independent context unit with its own state, packet, log, and handoff surface.

### Beginner Path Must Be Obvious

The suite should scale up to multi-agent workflows without forcing single-repo users to adopt the full model on day one.

## Chosen Direction

This design uses a **Layered Hybrid Model**:

- **Layer 1: Context Protocol**
  Defines the object model, state lifecycle, packet rules, injection rules, and handoff contract.
- **Layer 2: Repo Workflow**
  Applies the protocol to repository files, bootstrap helpers, wrappers, and day-to-day usage flows.

This model is preferred over a small evolution of the current four-skill suite because the missing capabilities are structural, not cosmetic.
It is preferred over a protocol-only redesign because the default user experience still needs to be approachable in ordinary repositories.

## Core Object Model

### Root Task

The top-level context owner for a long-running effort.

It holds:

- global objective
- global constraints
- shared verified facts
- cross-cutting risks
- current top-level status
- open subtasks

The root task should remain trustworthy and durable, but not overloaded with every local detail.

### Subtask

A child execution unit derived from the root task.

It holds:

- local objective
- local scope and non-goals
- inherited constraints that still apply
- local verified facts
- local decisions
- local risks
- local next action

Subtasks must be resumable and handoff-ready on their own.

### Context Layers

Every task object is organized into three layers:

- **Active Layer**
  What the next action must know now.
- **Working Layer**
  Useful near-term state that does not belong in the default injected packet.
- **Archive Layer**
  Retained history that should not occupy active context unless explicitly requested.

### Context Packet

The minimum injection unit used to start or continue an action.

A packet should include only:

- current objective
- directly relevant constraints
- verified facts required for the action
- active risks or blockers
- exact next action
- minimal file or module references when needed

Packets are narrower than full task state and are the default artifact for agent injection.

### Handoff Contract

The standard continuation object for pauses or transfers.

A handoff must capture:

- current status
- preserved constraints
- open problems
- exact next action
- files or artifacts to inspect first
- resume wording for the next session

## Context Lifecycle

### Creation

- A root task is initialized when continuity starts for a repo or meaningful workstream.
- A subtask is created when a branch of work can proceed with partially independent local state.

### Refresh

- Root and subtask state are refreshed when the trusted picture changes materially.
- Refresh must preserve facts, separate assumptions, and record decisions already made.

### Injection

- Default injection should use the target object's packet first.
- Broader task state is loaded only if the packet is insufficient.

### Compression

- Fresh findings begin in the working layer.
- Active, currently necessary items are promoted into the packet or active task summary.
- Stale but still relevant details are archived.
- Repeated or superseded items should be folded or deleted rather than endlessly appended.

### Closure

- A closed subtask should be marked resolved, merged back into root state where needed, and archived.
- A root task can produce a final handoff or closure summary, but only after its active subtasks are resolved or explicitly deferred.

## Injection Rules

### Default Rule

Inject only the current subtask's active packet.

### Escalation Rule

If the action depends on global constraints or shared decisions, inject the minimal root-task packet supplement.

### Recovery Rule

If the packet cannot support progress, read the corresponding task state file before scanning logs or archives.

### Anti-Rule

Do not inject:

- the whole thread
- every task artifact
- every open subtask
- the full run log

unless the current action explicitly requires reconstruction at that scope.

## Recommended Repo Workflow

### Default Layout

```text
AGENTS.md
.agent-state/
  INDEX.md
  root/
    TASK_STATE.md
    PACKET.md
    DECISIONS.md
    RUN_LOG.md
    HANDOFF.md
  subtasks/
    <subtask-id>/
      TASK_STATE.md
      PACKET.md
      HANDOFF.md
      RUN_LOG.md
  archive/
    root/
    subtasks/
    packets/
```

### Layout Semantics

- `INDEX.md` is the operator entry point.
  It answers which root task is active, which subtasks are open, and which packets are current.
- `root/TASK_STATE.md` holds durable top-level state.
- `root/PACKET.md` is the default injected summary for root-level work.
- `subtasks/<id>/TASK_STATE.md` is the durable local state for a subtask.
- `subtasks/<id>/PACKET.md` is the default injected context for that subtask.
- `archive/` stores retired or compressed artifacts that should stay discoverable without polluting active state.

### Beginner Mode

V1 should allow a lightweight mode:

```text
AGENTS.md
.agent-state/
  INDEX.md
  root/
    TASK_STATE.md
    PACKET.md
    HANDOFF.md
```

Users only expand into `subtasks/` and `archive/` when the task complexity justifies it.

## Recommended Workflow Loop

1. Read `INDEX.md`.
2. Open the current target packet.
3. If the work is large enough to split, create a subtask.
4. Execute using the subtask packet, not the full root state.
5. Refresh subtask state after meaningful changes.
6. Merge durable outcomes back into root state where necessary.
7. Compress stale detail into archive rather than growing active state indefinitely.
8. Write a handoff before a meaningful pause or transfer.

## Recommended Skill Topology

This design does **not** require preserving the current four-skill topology unchanged.

### Keep And Refocus

- **`skill-task-continuity`**
  Suite entry point, bootstrap helper, router, and mode selector.
- **`skill-context-keeper`**
  Root-task refresh and compression-focused state maintenance.
- **`skill-handoff-summary`**
  Standard handoff contract for root tasks and subtasks.
- **`skill-phase-gate`**
  Optional operational checkpoint for risky edits, no longer the center of the system.

### Add

- **`skill-subtask-context`**
  Create, refresh, hand off, and close subtask context units.
- **`skill-context-packet`**
  Build or refresh minimal context packets for the next action.

### Why This Split

- `skill-context-keeper` maps to trusted durable state.
- `skill-subtask-context` maps to isolation.
- `skill-context-packet` maps to just-in-time injection.
- `skill-handoff-summary` maps to continuation transfers.
- `skill-task-continuity` maps to adoption and orchestration.
- `skill-phase-gate` remains valuable for risk management, but should not be overloaded as a context-management primitive.

## Bootstrap And Wrapper Strategy

Bootstrap should create:

- `AGENTS.md`
- `.agent-state/INDEX.md`
- root-state starter files
- optional beginner wrappers under `.agents/skills/`

Suggested default wrappers:

- `refresh-root-state`
- `create-subtask`
- `refresh-subtask-packet`
- `write-handoff`
- `compress-context`

These wrappers should remain thin and point back to the canonical public skills instead of copying their behavior.

## Migration Strategy

### Near-Term

- Preserve the current four packages so downstream users do not break immediately.
- Add compatibility documentation that explains the emerging protocol model.

### Mid-Term

- Introduce `skill-subtask-context` and `skill-context-packet`.
- Update `skill-task-continuity` to bootstrap the new repo layout.
- Refocus `skill-context-keeper` on root-state refresh and compression.

### Long-Term

- Re-evaluate whether the older package names still reflect the product model.
- Retire or merge packages only after wrappers, docs, and tests cover the new workflow clearly.

## V1 Scope

V1 should ship:

- a written context protocol
- beginner and expanded repo layouts
- root task state and packet artifacts
- subtask state and packet artifacts
- standardized handoff contract
- compression guidance with archive movement
- suite entry guidance that helps users choose the next action

V1 does **not** need:

- automatic graph scheduling of all subtasks
- deep platform-specific integrations
- fully automatic compression without user-visible rules

## Validation Strategy

### Contract Tests

Add tests that verify:

- subtask artifacts exist and are structurally distinct from root artifacts
- packets are narrower than task state and preserve required sections
- handoff artifacts work for both root and subtask scopes
- beginner bootstrap and expanded bootstrap both produce expected files
- archive and compression flows preserve active-state clarity

### Workflow Evals

Add task-based evals for:

- split one root task into two subtasks without context bleed
- resume a subtask from packet plus handoff only
- recover after multiple sessions without rereading the whole thread
- compress bloated state back into a lean active packet
- onboard a new downstream repo from bootstrap to first successful handoff

## Success Criteria

The design is successful when a new repo can support this path:

1. bootstrap continuity files
2. create a root task
3. split a subtask
4. inject only the subtask packet into execution
5. pause with a valid handoff
6. resume without rereading the full history
7. keep active state lean across multiple cycles

## Risks

### Over-Modeling

If the protocol is too abstract, normal users will not adopt it.

### Under-Modeling

If subtask state and packets remain vague, the suite will keep behaving like a set of generic summaries instead of a context system.

### Wrapper Drift

If repo-local wrappers become thick forks, the public package model will fragment.

## Recommendation

Proceed with the layered hybrid redesign.
Keep the repo-first experience simple, but do not hide the underlying protocol.
The future suite should be judged less by how many markdown templates it ships and more by whether it can reliably isolate, inject, compress, and transfer context in real multi-agent work.
