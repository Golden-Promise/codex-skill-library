# Long-Task Continuity Suite

## Problem Statement

Long threads usually do not fail all at once. They fail by degrees: the shared state gets stale, the workflow loses its shape, and handoffs become too thin for the next agent to trust.

This suite exists to make those failure modes explicit. It treats long-task degradation as three separate problems:

- state drift, where the working picture no longer matches reality
- workflow drift, where the task stops following a deliberate sequence of phases and checkpoints
- handoff friction, where another agent cannot resume without guessing

The goal is not to add more ceremony. The goal is to make continuity measurable so that long tasks stay resumable, inspectable, and transferable.

## State Drift, Workflow Drift, And Handoff Friction

These three failure modes overlap, but they are not the same thing.

State drift appears when summaries, context, or task memory lag behind the actual work. The risk is silent divergence: the thread sounds confident while carrying the wrong assumptions.

Workflow drift appears when a task that needs staged execution starts behaving like a single shot. The work may still move forward, but it loses checkpoints, decision points, and clear boundaries.

Handoff friction appears when a pause or transfer leaves too little signal for the next agent. The work is not necessarily wrong, just expensive to resume.

The suite uses these distinctions to decide which package should trigger and which one should stay out of the way.

## Package Map

| Package | Responsibility | Trigger Shape |
| --- | --- | --- |
| `skill-context-keeper` | Preserve and reconstruct working state across long threads, especially after interruptions or stale summaries. | Resume, refresh, or reconcile context. |
| `skill-phase-gate` | Decide when work needs phase boundaries, checkpoints, or a deliberate pause before execution continues. | Split, gate, or stage the work. |
| `skill-handoff-summary` | Produce a clean transfer note when work is paused or handed to another agent. | Summarize status, blockers, and next steps. |
| `skill-task-continuity` | Orchestrate the three atomic packages when the task itself is about maintaining long-thread continuity. | Bootstrap the suite, coordinate boundaries, and keep the flow coherent. |

## Repository Boundary Rules

This repository is a public installable skill library, so the suite docs must stay reader-facing and maintainable.

- Keep the suite spec in `docs/`, not in live agent state files.
- Do not create a root `AGENTS.md`, `.agent-state/`, or public-package `.agents/skills` content for this task.
- Treat `evals/cases.csv` as the source of truth for trigger coverage, but keep the prose docs understandable on their own.
- Describe package boundaries in plain language; do not require readers to open package implementation files first.
- Prefer the narrowest package that matches the prompt. The composition package should not steal work that belongs to an atomic package.
- Make ambiguity explicit in the matrix so maintainers can see when a keyword match is not a real trigger.

## Success Criteria

### Outcome

- Long-thread work can be resumed, paused, or transferred without losing intent.
- The suite catches both false positives and false negatives for the four target packages.
- A maintainer can understand the architecture and boundaries without opening package source files.

### Process

- The eval matrix includes positive trigger cases and negative trigger cases for every atomic package.
- The matrix includes at least one composition-package bootstrap case and one boundary-protection case.
- Each case records the expected artifacts and the expected workflow event or command shape when that matters.

### Style

- The docs stay concise, public-reader-friendly, and easy to scan.
- English and Chinese versions share the same major section order.
- Trigger notes read like maintainer guidance, not like internal scratchpad text.

### Efficiency

- Maintainers can validate the suite from the docs and CSV without reverse-engineering package code.
- The matrix is small enough to extend without becoming noisy.
- Ambiguous prompts are documented once, then reused as regression coverage.

## Initial Evaluation Matrix

The seed matrix lives in `evals/cases.csv`. The table below shows the initial coverage shape and the kinds of expected artifacts and workflow events to look for.

| Case | Package | Trigger | Prompt Shape | Expected Artifacts | Expected Events |
| --- | --- | --- | --- | --- | --- |
| `context_resume` | `skill-context-keeper` | Yes | Resume the last known state and carry forward unresolved work. | State snapshot, continuity note, or refreshed context summary. | Reload prior state, rebuild active facts, emit continuity summary. |
| `context_resume_not_needed` | `skill-context-keeper` | No | Answer a one-off question with no continuity risk. | None. | Direct answer only; no state reload. |
| `phase_gate_before_multi_step` | `skill-phase-gate` | Yes | Split a multi-step task into phases before coding starts. | Phase plan, checkpoint list, stop/go criteria. | Create phase boundaries and checkpoints. |
| `tiny_edit_not_gate` | `skill-phase-gate` | No | Make a tiny local edit with no staged workflow. | None. | Skip gating for the small change. |
| `handoff_before_pause` | `skill-handoff-summary` | Yes | Pause work and hand it to another agent. | Handoff summary, blockers, next actions. | Capture transfer state and mark the pause point. |
| `handoff_not_needed` | `skill-handoff-summary` | No | Give a final answer without transfer notes. | None. | No handoff workflow event. |
| `suite_bootstrap` | `skill-task-continuity` | Yes | Coordinate the long-task suite across the atomic packages. | Suite spec, package map, evaluation matrix. | Bootstrap downstream guidance and align package boundaries. |
| `suite_boundary_clean` | `skill-task-continuity` | No | A trivial edit that merely mentions all the keywords. | None. | Do not promote a keyword match into suite orchestration. |

## Phase Plan

The current task is the bootstrap phase: define the suite, seed the matrix, and make the boundaries legible.

Phase 1 should keep the documentation stable while the package implementations are still being shaped. That means adding new cases only when they improve coverage, not when they repeat the same trigger in different words.

Phase 2 should expand the matrix with more realistic long-thread scenarios, especially ones where the wrong package could plausibly trigger.

Phase 3 should use the suite as a regression harness for future package changes, so trigger behavior stays narrow and intentional.
