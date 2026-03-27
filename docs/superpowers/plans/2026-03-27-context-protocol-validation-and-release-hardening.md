# Context Protocol Validation And Release Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the context-protocol redesign shippable by expanding static workflow evals, publishing a repo-level migration guide, and hardening the release docs around the new six-package continuity workflow.

**Architecture:** Treat the current foundation and legacy-refocus slices as the baseline, then update the repository-facing validation layer to understand root state, subtask state, and packet-sized context. Publish a dedicated migration guide plus refreshed suite overview docs so readers can move from the legacy four-package mental model to the new protocol model, and finish by tightening publishing and release-checklist docs so maintainers validate and ship the correct surface area.

**Tech Stack:** Markdown docs, CSV seed matrix, Python `evals/run_evals.py`, Python `unittest`, repository release docs under `docs/`

---

## Scope Note

This plan covers **Slice 3 only** from the approved design:

1. workflow eval expansion
2. migration and overview docs for the context protocol
3. release and publishing hardening

This plan assumes the following baseline has already landed in the worktree:

- `cfe3581` `feat: add context protocol foundation`
- `101fde0` `feat: refocus legacy continuity skills`

## File Map

### Existing Files To Modify

- Modify: `README.md`
  - Publish the two new continuity packages from the repo root and link the migration guide.
- Modify: `README.zh-CN.md`
  - Mirror the English root-index and migration-guide changes in Chinese.
- Modify: `CHANGELOG.md`
  - Record the context-protocol rollout slices and replace stale release-target wording with release-scope-driven guidance.
- Modify: `docs/long-task-suite.md`
  - Rewrite the suite overview around the six-package protocol model and the new evaluation matrix.
- Modify: `docs/long-task-suite.zh-CN.md`
  - Mirror the English suite-overview and matrix changes in Chinese.
- Modify: `docs/publishing.md`
  - Replace the old four-package continuity publication flow with the six-package protocol flow and release-target placeholders.
- Modify: `docs/publishing.zh-CN.md`
  - Mirror the English publishing-guide changes in Chinese.
- Modify: `docs/release-checklist-long-task-suite.md`
  - Update the checklist, smoke-test loops, and release-verification language for the protocol model.
- Modify: `docs/release-checklist-long-task-suite.zh-CN.md`
  - Mirror the English checklist changes in Chinese.
- Modify: `evals/README.md`
  - Explain the protocol-aware seed matrix, new package coverage, and updated artifact tokens.
- Modify: `evals/cases.csv`
  - Replace the old eight-case matrix with the protocol-era workflow cases and normalized artifact/event tokens.
- Modify: `evals/run_evals.py`
  - Update package rules, artifact mapping, and workflow checks for `skill-subtask-context`, `skill-context-packet`, and the root/subtask layout.
- Modify: `evals/test_run_evals.py`
  - Lock in the new seed matrix, package rules, and runner behavior.

### New Files To Create

- Create: `docs/context-protocol-migration.md`
  - Explain how existing users should move from the legacy four-package continuity mental model to the root/subtask/packet protocol.
- Create: `docs/context-protocol-migration.zh-CN.md`
  - Mirror the English migration guide in Chinese.

## Approved Design Notes

- Keep the static eval harness repo-driven; do not add live model execution in this slice.
- Treat the migration guide as a compatibility document for existing users, not as a new product spec.
- Make `docs/long-task-suite.*` reflect the current six-package topology instead of the withdrawn four-package framing.
- Remove hard-coded “current release target is `v0.6.1`” wording from maintainer docs; release docs should derive the next tag from actual release scope.
- Keep package install paths stable; this slice documents migration and release posture, not package renames.

## Out Of Scope For This Plan

- Renaming or deleting legacy packages
- Adding automatic repository migration scripts
- Adding platform-specific telemetry, dashboards, or live evaluation services
- Changing GitHub Actions unless the existing release docs cannot be expressed accurately without it

### Task 1: Add Failing Protocol-Eval Contracts

**Files:**
- Modify: `evals/test_run_evals.py`
- Modify: `evals/cases.csv`
- Test: `evals/test_run_evals.py`

- [ ] **Step 1: Expand the eval tests to describe the protocol-era matrix**

Update `evals/test_run_evals.py` so it fails against the current runner and seed data unless all of the following become true:
- the seed matrix now covers all six continuity packages
- the seed matrix grows beyond the old eight-row topology and includes protocol cases such as:
  - `root_state_refresh`
  - `root_state_compress`
  - `subtask_split_from_root`
  - `subtask_resume_from_packet`
  - `packet_root_minimal_injection`
  - `suite_bootstrap_protocol`
- normalized artifact tokens reference the new layout, for example:
  - `suite/index`
  - `root/task_state`
  - `root/packet`
  - `root/handoff`
  - `subtask/task_state`
  - `subtask/packet`
  - `subtask/handoff`
- the runner result now contains cases for `skill-subtask-context` and `skill-context-packet`

- [ ] **Step 2: Add a red seed matrix that reflects the intended protocol coverage**

Replace the old rows in `evals/cases.csv` with the target protocol case IDs and tokens even though the current runner cannot score them yet.

- [ ] **Step 3: Run the eval unit tests to verify the contract fails**

Run:
```bash
cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-maintenance
python3 -m unittest discover -s evals -p 'test_*.py' -v
```
Expected: FAIL because the existing runner still hard-codes the old four-package matrix, flat artifact paths, and outdated event namespaces.

- [ ] **Step 4: Commit the red-test checkpoint if you want the TDD breadcrumb**

```bash
git add evals/test_run_evals.py evals/cases.csv
git commit -m "test: add protocol eval contracts"
```

### Task 2: Implement The Protocol-Aware Eval Harness

**Files:**
- Modify: `evals/README.md`
- Modify: `evals/cases.csv`
- Modify: `evals/run_evals.py`
- Modify: `evals/test_run_evals.py`
- Test: `evals/test_run_evals.py`

- [ ] **Step 1: Rewrite `PACKAGE_RULES` for the six-package continuity toolchain**

Update `evals/run_evals.py` so the runner understands:
- `skill-context-keeper` as root-state refresh and compression
- `skill-subtask-context` as bounded child-task state ownership
- `skill-context-packet` as minimum next-turn context compression
- `skill-phase-gate` as optional checkpointing only
- `skill-handoff-summary` as root/subtask handoff generation
- `skill-task-continuity` as protocol bootstrap and composition

Make the required file lists, trigger cues, suppress cues, artifact mappings, and event namespaces match the current package boundaries and asset layout.

- [ ] **Step 2: Normalize the protocol matrix and workflow tokens**

Refresh `evals/cases.csv` so the matrix covers:
- positive and negative routing for each package
- at least one protocol bootstrap case
- one root-state compression case
- one subtask-isolation case
- one packet-only continuation case

Keep the matrix compact, but make it realistic enough to cover the five workflow-eval scenarios named in the spec.

- [ ] **Step 3: Refresh the eval README around the new matrix**

Update `evals/README.md` so maintainers can understand:
- why the matrix now uses root/subtask/packet tokens
- how the runner checks routing and boundary language for six packages
- how to extend the matrix without reintroducing flat-path assumptions

- [ ] **Step 4: Re-run the eval unit tests and the static seed matrix**

Run:
```bash
cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-maintenance
python3 -m unittest discover -s evals -p 'test_*.py' -v
python3 evals/run_evals.py
```
Expected: PASS, with the report scoring the protocol-era cases rather than the legacy flat-layout cases.

- [ ] **Step 5: Commit the eval-harness slice**

```bash
git add evals/README.md evals/cases.csv evals/run_evals.py evals/test_run_evals.py
git commit -m "feat: expand continuity evals for the context protocol"
```

### Task 3: Publish The Migration Guide And Refresh Public Suite Docs

**Files:**
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `docs/long-task-suite.md`
- Modify: `docs/long-task-suite.zh-CN.md`
- Create: `docs/context-protocol-migration.md`
- Create: `docs/context-protocol-migration.zh-CN.md`

- [ ] **Step 1: Write the migration guide in English**

Create `docs/context-protocol-migration.md` with sections for:
- who needs to migrate and who can ignore the guide
- old four-package mental model vs new six-package protocol model
- how root state, subtask state, and packets map onto the older skills
- a recommended “start in beginner mode, expand later” adoption path
- common mistakes such as treating packets as full state or using phase-gate as the continuity center

- [ ] **Step 2: Mirror the migration guide in Chinese**

Create `docs/context-protocol-migration.zh-CN.md` with the same section order and examples adapted for Chinese readers.

- [ ] **Step 3: Rewrite the suite overview docs around the current protocol**

Update `docs/long-task-suite.md` and `docs/long-task-suite.zh-CN.md` so they:
- describe six packages instead of four
- explain the root/subtask/packet model as the continuity core
- replace the old flat-layout matrix table with the new protocol cases
- point readers to the migration guide for compatibility questions

- [ ] **Step 4: Update the root README indexes**

Refresh `README.md` and `README.zh-CN.md` so the repository root:
- lists `skill-subtask-context` and `skill-context-packet`
- links to `docs/context-protocol-migration.md`
- keeps the continuity suite discoverable from the repo landing page

- [ ] **Step 5: Commit the migration-doc slice**

```bash
git add README.md README.zh-CN.md docs/long-task-suite.md docs/long-task-suite.zh-CN.md docs/context-protocol-migration.md docs/context-protocol-migration.zh-CN.md
git commit -m "docs: publish context protocol migration guide"
```

### Task 4: Harden Publishing And Release Documentation

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `docs/publishing.md`
- Modify: `docs/publishing.zh-CN.md`
- Modify: `docs/release-checklist-long-task-suite.md`
- Modify: `docs/release-checklist-long-task-suite.zh-CN.md`
- Test: `evals/test_run_evals.py`

- [ ] **Step 1: Remove stale fixed-target release wording**

Update the publishing guide and release checklist so they no longer say the current continuity release target is `v0.6.1`.
Use release-scope-driven wording such as `<release-tag>` or explicit guidance to derive the next tag from `CHANGELOG.md` and the actual reader-visible scope.

- [ ] **Step 2: Expand the continuity smoke-test loops to six packages**

Rewrite the install-smoke examples in both publishing docs and both release-checklist docs so they include:
- `skills/skill-context-keeper`
- `skills/skill-subtask-context`
- `skills/skill-context-packet`
- `skills/skill-phase-gate`
- `skills/skill-handoff-summary`
- `skills/skill-task-continuity`

- [ ] **Step 3: Update release guidance around protocol validation**

Make the publishing docs explicitly require:
- package tests under `skills/*/tests`
- `skill-governance` validate-only packaging sanity
- the refreshed continuity eval unit tests
- the refreshed continuity seed matrix
- migration-doc and suite-overview spot checks before tagging

- [ ] **Step 4: Refresh the changelog for the protocol rollout**

Update `CHANGELOG.md` so the `Unreleased` section captures:
- the new protocol packages
- the layered bootstrap and refocused legacy boundaries
- the expanded eval harness
- the new migration and release docs

- [ ] **Step 5: Commit the release-hardening slice**

```bash
git add CHANGELOG.md docs/publishing.md docs/publishing.zh-CN.md docs/release-checklist-long-task-suite.md docs/release-checklist-long-task-suite.zh-CN.md
git commit -m "docs: harden context protocol release guidance"
```

### Task 5: Run Full Release-Facing Verification

**Files:**
- Verify only

- [ ] **Step 1: Run formatting and diff sanity**

Run:
```bash
cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-maintenance
git diff --check
```
Expected: no whitespace or conflict-marker errors

- [ ] **Step 2: Run all published package tests**

Run:
```bash
cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-maintenance
for test_dir in skills/*/tests; do
  python3 -m unittest discover -s "$test_dir" -p 'test_*.py' -v
done
```
Expected: PASS for every published package test directory

- [ ] **Step 3: Run repository-level continuity validation**

Run:
```bash
cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-maintenance
python3 -m unittest discover -s evals -p 'test_*.py' -v
python3 evals/run_evals.py
(cd skills/skill-governance && python3 scripts/manage_skill.py --validate-only)
```
Expected: PASS

- [ ] **Step 4: Verify that stale release-target wording is gone from maintainer docs**

Run:
```bash
cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-maintenance
rg -n "current .*v0\\.6\\.1|target is `v0\\.6\\.1`|ref v0\\.6\\.1" docs README.md README.zh-CN.md evals
```
Expected: either no matches in maintainer docs, or only intentional historical references outside the release-facing continuity guidance

- [ ] **Step 5: Commit the verification checkpoint or final batch**

```bash
git status --short
```
Expected: clean worktree if all slice-3 commits were created along the way

## Final Review Checklist

- The eval harness understands six continuity packages and root/subtask/packet artifact tokens.
- The seed matrix covers the spec’s workflow-eval scenarios without exploding into noisy duplicates.
- The migration guide gives existing users a concrete adoption path instead of just re-explaining the spec.
- The suite overview and repo root no longer describe a four-package continuity system.
- Publishing and release docs no longer hard-code a stale release target.
