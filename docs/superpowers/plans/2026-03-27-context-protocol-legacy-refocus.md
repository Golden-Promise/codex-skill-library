# Context Protocol Legacy Refocus Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refocus the legacy continuity packages so `skill-context-keeper`, `skill-handoff-summary`, and `skill-phase-gate` align with the new context-protocol model without deleting stable install paths.

**Architecture:** Use contract-first updates to the three legacy packages, then rewrite their docs, prompts, and shared templates around root-state refresh, standardized root/subtask handoffs, and optional operational checkpoints. Keep `skill-task-continuity` as the suite router and synchronize its duplicated assets anywhere the atomic packages remain the source of truth.

**Tech Stack:** Markdown skill docs, template assets under `skills/`, Python `unittest`, existing continuity package layout

---

## Scope Note

This plan covers **Slice 2 only** from the approved design:

1. refocus legacy packages around root vs subtask scope
2. keep the newly added protocol packages installable
3. leave eval expansion, migration docs, and release hardening to the follow-on slice

This plan assumes the current foundation slice in this worktree is the baseline.
If you want clean commit boundaries, commit the foundation slice before executing this plan.

## File Map

### Existing Files To Modify

- Modify: `skills/README.md`
  - Update the published package blurbs so legacy roles match the new protocol model.
- Modify: `skills/README.zh-CN.md`
  - Mirror the revised package blurbs in Chinese.
- Modify: `skills/skill-context-keeper/SKILL.md`
  - Narrow the package to root-state refresh and compression guidance.
- Modify: `skills/skill-context-keeper/README.md`
  - Change the default artifact path to `.agent-state/root/TASK_STATE.md` and explain the compression boundary.
- Modify: `skills/skill-context-keeper/README.zh-CN.md`
  - Mirror the English root-state and compression guidance.
- Modify: `skills/skill-context-keeper/agents/openai.yaml`
  - Align the default prompt with root-state refresh only.
- Modify: `skills/skill-context-keeper/assets/TASK_STATE.template.md`
  - Add an explicit compression / archive section for root-state maintenance.
- Modify: `skills/skill-context-keeper/references/use-cases.md`
  - Shift examples to root-state refresh and compression.
- Modify: `skills/skill-context-keeper/references/use-cases.zh-CN.md`
  - Mirror the English use-case changes in Chinese.
- Modify: `skills/skill-context-keeper/references/prompt-templates.en.md`
  - Update prompt wording for `.agent-state/root/TASK_STATE.md` and archive-minded refreshes.
- Modify: `skills/skill-context-keeper/references/prompt-templates.zh-CN.md`
  - Mirror the English prompt changes in Chinese.
- Modify: `skills/skill-context-keeper/tests/test_package_contract.py`
  - Assert root-state paths and compression-specific package boundaries.
- Modify: `skills/skill-handoff-summary/SKILL.md`
  - Refocus the package on a standard handoff contract usable for root or subtask scope.
- Modify: `skills/skill-handoff-summary/README.md`
  - Replace the single flat handoff path with root/subtask handoff guidance.
- Modify: `skills/skill-handoff-summary/README.zh-CN.md`
  - Mirror the English root/subtask handoff guidance in Chinese.
- Modify: `skills/skill-handoff-summary/agents/openai.yaml`
  - Align the default prompt with root/subtask handoff generation.
- Modify: `skills/skill-handoff-summary/assets/HANDOFF.template.md`
  - Make the template path-neutral enough to serve both root and subtask handoffs.
- Modify: `skills/skill-handoff-summary/references/use-cases.md`
  - Update trigger examples so the package works for root and subtask pauses.
- Modify: `skills/skill-handoff-summary/references/use-cases.zh-CN.md`
  - Mirror the English use-case changes in Chinese.
- Modify: `skills/skill-handoff-summary/references/prompt-templates.en.md`
  - Replace flat-path prompts with root/subtask handoff prompts.
- Modify: `skills/skill-handoff-summary/references/prompt-templates.zh-CN.md`
  - Mirror the English prompt changes in Chinese.
- Modify: `skills/skill-handoff-summary/tests/test_package_contract.py`
  - Assert the generalized handoff contract and root/subtask wording.
- Modify: `skills/skill-phase-gate/SKILL.md`
  - Reframe the package as an optional operational checkpoint, not a continuity centerpiece.
- Modify: `skills/skill-phase-gate/README.md`
  - Clarify that the package is for risky edits, not root-state refresh or packet management.
- Modify: `skills/skill-phase-gate/README.zh-CN.md`
  - Mirror the English boundary changes in Chinese.
- Modify: `skills/skill-phase-gate/agents/openai.yaml`
  - Align the default prompt with optional checkpoint usage.
- Modify: `skills/skill-phase-gate/references/use-cases.md`
  - Tighten positive/negative triggers around risky edits only.
- Modify: `skills/skill-phase-gate/references/use-cases.zh-CN.md`
  - Mirror the English use-case changes in Chinese.
- Modify: `skills/skill-phase-gate/references/prompt-templates.en.md`
  - Remove stale continuity-center wording and keep packet/root-state out of scope.
- Modify: `skills/skill-phase-gate/references/prompt-templates.zh-CN.md`
  - Mirror the English prompt changes in Chinese.
- Modify: `skills/skill-phase-gate/tests/test_package_contract.py`
  - Assert the new “optional checkpoint only” boundary.
- Modify: `skills/skill-task-continuity/assets/agent-state/root/TASK_STATE.template.md`
  - Keep the suite duplicate in sync with the atomic root-state template.
- Modify: `skills/skill-task-continuity/assets/agent-state/root/HANDOFF.template.md`
  - Keep the suite duplicate in sync with the atomic handoff template.
- Modify: `skills/skill-task-continuity/assets/agent-state/subtasks/HANDOFF.template.md`
  - Reuse the standardized handoff contract for subtask scope.
- Modify: `skills/skill-task-continuity/tests/test_bootstrap_suite.py`
  - Extend duplicate-template checks to cover the standardized handoff contract.

## Out Of Scope For This Plan

- Expanding `evals/cases.csv` or adding workflow eval runners
- Writing downstream migration guides or release notes
- Renaming or retiring the older package names
- Adding archive automation beyond doc and template guidance

### Task 1: Add Failing Legacy-Refocus Contracts

**Files:**
- Modify: `skills/skill-context-keeper/tests/test_package_contract.py`
- Modify: `skills/skill-handoff-summary/tests/test_package_contract.py`
- Modify: `skills/skill-phase-gate/tests/test_package_contract.py`
- Modify: `skills/skill-task-continuity/tests/test_bootstrap_suite.py`
- Test: `skills/skill-context-keeper/tests/test_package_contract.py`
- Test: `skills/skill-handoff-summary/tests/test_package_contract.py`
- Test: `skills/skill-phase-gate/tests/test_package_contract.py`
- Test: `skills/skill-task-continuity/tests/test_bootstrap_suite.py`

- [ ] **Step 1: Extend the context-keeper contract around root-state ownership**

Add failing assertions for:
- `.agent-state/root/TASK_STATE.md` instead of the old flat path
- explicit wording that the package owns root-state refresh and compression
- a new template heading such as `## Compression / Archive Notes`

- [ ] **Step 2: Extend the handoff-summary contract around root/subtask reuse**

Add failing assertions for:
- root and subtask handoff wording in the README and prompt templates
- a path-neutral resume prompt in the atomic handoff template
- package boundary wording that rules out whole-project docs and state refresh

- [ ] **Step 3: Extend the phase-gate contract around optional checkpoint-only usage**

Add failing assertions for:
- “optional operational checkpoint” wording
- explicit rejection of root-state refresh, packet compression, and suite bootstrap usage
- related-skill routing to the newer packet and subtask packages

- [ ] **Step 4: Extend the suite duplication test for the standardized handoff template**

Require both:
- `assets/agent-state/root/HANDOFF.template.md`
- `assets/agent-state/subtasks/HANDOFF.template.md`

to match the atomic `skill-handoff-summary` handoff asset exactly.

- [ ] **Step 5: Run the legacy contract modules to verify they fail**

Run:
```bash
cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-maintenance
python3 -m unittest discover -s skills/skill-context-keeper/tests -p 'test_package_contract.py' -v
python3 -m unittest discover -s skills/skill-handoff-summary/tests -p 'test_package_contract.py' -v
python3 -m unittest discover -s skills/skill-phase-gate/tests -p 'test_package_contract.py' -v
python3 -m unittest discover -s skills/skill-task-continuity/tests -p 'test_bootstrap_suite.py' -v
```
Expected: FAIL because the legacy packages still describe the old flat paths and narrower handoff contract.

### Task 2: Refocus `skill-context-keeper` On Root-State Refresh And Compression

**Files:**
- Modify: `skills/skill-context-keeper/SKILL.md`
- Modify: `skills/skill-context-keeper/README.md`
- Modify: `skills/skill-context-keeper/README.zh-CN.md`
- Modify: `skills/skill-context-keeper/agents/openai.yaml`
- Modify: `skills/skill-context-keeper/assets/TASK_STATE.template.md`
- Modify: `skills/skill-context-keeper/references/use-cases.md`
- Modify: `skills/skill-context-keeper/references/use-cases.zh-CN.md`
- Modify: `skills/skill-context-keeper/references/prompt-templates.en.md`
- Modify: `skills/skill-context-keeper/references/prompt-templates.zh-CN.md`
- Modify: `skills/skill-context-keeper/tests/test_package_contract.py`
- Modify: `skills/skill-task-continuity/assets/agent-state/root/TASK_STATE.template.md`
- Test: `skills/skill-context-keeper/tests/test_package_contract.py`
- Test: `skills/skill-task-continuity/tests/test_bootstrap_suite.py`

- [ ] **Step 1: Update the root task-state asset and its suite duplicate**

Add the compression-specific section to both task-state templates and keep their contents byte-for-byte identical.

- [ ] **Step 2: Rewrite the package boundary and examples**

Update SKILL, README, prompt templates, and use cases so they:
- point to `.agent-state/root/TASK_STATE.md`
- describe root-state refresh and compression only
- route subtask work to `skill-subtask-context`
- route minimal injection work to `skill-context-packet`

- [ ] **Step 3: Re-run the keeper and suite tests**

Run:
```bash
cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-maintenance
python3 -m unittest discover -s skills/skill-context-keeper/tests -p 'test_package_contract.py' -v
python3 -m unittest discover -s skills/skill-task-continuity/tests -p 'test_bootstrap_suite.py' -v
```
Expected: PASS

- [ ] **Step 4: Commit the root-state refocus slice**

```bash
git add skills/skill-context-keeper/SKILL.md skills/skill-context-keeper/README.md skills/skill-context-keeper/README.zh-CN.md skills/skill-context-keeper/agents/openai.yaml skills/skill-context-keeper/assets/TASK_STATE.template.md skills/skill-context-keeper/references/use-cases.md skills/skill-context-keeper/references/use-cases.zh-CN.md skills/skill-context-keeper/references/prompt-templates.en.md skills/skill-context-keeper/references/prompt-templates.zh-CN.md skills/skill-context-keeper/tests/test_package_contract.py skills/skill-task-continuity/assets/agent-state/root/TASK_STATE.template.md
git commit -m "feat: refocus context keeper on root state"
```

### Task 3: Refocus `skill-handoff-summary` On A Standard Root/Subtask Contract

**Files:**
- Modify: `skills/skill-handoff-summary/SKILL.md`
- Modify: `skills/skill-handoff-summary/README.md`
- Modify: `skills/skill-handoff-summary/README.zh-CN.md`
- Modify: `skills/skill-handoff-summary/agents/openai.yaml`
- Modify: `skills/skill-handoff-summary/assets/HANDOFF.template.md`
- Modify: `skills/skill-handoff-summary/references/use-cases.md`
- Modify: `skills/skill-handoff-summary/references/use-cases.zh-CN.md`
- Modify: `skills/skill-handoff-summary/references/prompt-templates.en.md`
- Modify: `skills/skill-handoff-summary/references/prompt-templates.zh-CN.md`
- Modify: `skills/skill-handoff-summary/tests/test_package_contract.py`
- Modify: `skills/skill-task-continuity/assets/agent-state/root/HANDOFF.template.md`
- Modify: `skills/skill-task-continuity/assets/agent-state/subtasks/HANDOFF.template.md`
- Modify: `skills/skill-task-continuity/tests/test_bootstrap_suite.py`
- Test: `skills/skill-handoff-summary/tests/test_package_contract.py`
- Test: `skills/skill-task-continuity/tests/test_bootstrap_suite.py`

- [ ] **Step 1: Rewrite the atomic handoff template to be reusable**

Change the handoff template and its resume prompt so it can serve both root and subtask scopes without hard-coding only one flat downstream path.

- [ ] **Step 2: Copy the new handoff template into the suite duplicates**

Make both suite handoff templates match the atomic asset exactly so the bootstrap helper continues to have one source of truth.

- [ ] **Step 3: Rewrite docs and prompts around root/subtask handoffs**

Update SKILL, README, prompt templates, and use cases so they:
- mention `.agent-state/root/HANDOFF.md` and `.agent-state/subtasks/<slug>/HANDOFF.md`
- keep the package continuation-oriented
- avoid state-refresh or workflow-gate ownership

- [ ] **Step 4: Re-run the handoff and suite tests**

Run:
```bash
cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-maintenance
python3 -m unittest discover -s skills/skill-handoff-summary/tests -p 'test_package_contract.py' -v
python3 -m unittest discover -s skills/skill-task-continuity/tests -p 'test_bootstrap_suite.py' -v
```
Expected: PASS

- [ ] **Step 5: Commit the handoff refocus slice**

```bash
git add skills/skill-handoff-summary/SKILL.md skills/skill-handoff-summary/README.md skills/skill-handoff-summary/README.zh-CN.md skills/skill-handoff-summary/agents/openai.yaml skills/skill-handoff-summary/assets/HANDOFF.template.md skills/skill-handoff-summary/references/use-cases.md skills/skill-handoff-summary/references/use-cases.zh-CN.md skills/skill-handoff-summary/references/prompt-templates.en.md skills/skill-handoff-summary/references/prompt-templates.zh-CN.md skills/skill-handoff-summary/tests/test_package_contract.py skills/skill-task-continuity/assets/agent-state/root/HANDOFF.template.md skills/skill-task-continuity/assets/agent-state/subtasks/HANDOFF.template.md skills/skill-task-continuity/tests/test_bootstrap_suite.py
git commit -m "feat: standardize handoff scope"
```

### Task 4: Refocus `skill-phase-gate` As An Optional Operational Checkpoint

**Files:**
- Modify: `skills/skill-phase-gate/SKILL.md`
- Modify: `skills/skill-phase-gate/README.md`
- Modify: `skills/skill-phase-gate/README.zh-CN.md`
- Modify: `skills/skill-phase-gate/agents/openai.yaml`
- Modify: `skills/skill-phase-gate/references/use-cases.md`
- Modify: `skills/skill-phase-gate/references/use-cases.zh-CN.md`
- Modify: `skills/skill-phase-gate/references/prompt-templates.en.md`
- Modify: `skills/skill-phase-gate/references/prompt-templates.zh-CN.md`
- Modify: `skills/skill-phase-gate/tests/test_package_contract.py`
- Test: `skills/skill-phase-gate/tests/test_package_contract.py`

- [ ] **Step 1: Rewrite the package boundary in tests and docs**

Make the package explicitly about risky edits and meaningful checkpoints, not context refresh, packet compression, or suite coordination.

- [ ] **Step 2: Update related-skill routing**

Point stale-state requests to `skill-context-keeper`, packet requests to `skill-context-packet`, and subtask-local state requests to `skill-subtask-context`.

- [ ] **Step 3: Re-run the phase-gate tests**

Run:
```bash
cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-maintenance
python3 -m unittest discover -s skills/skill-phase-gate/tests -p 'test_package_contract.py' -v
```
Expected: PASS

- [ ] **Step 4: Commit the checkpoint-only refocus slice**

```bash
git add skills/skill-phase-gate/SKILL.md skills/skill-phase-gate/README.md skills/skill-phase-gate/README.zh-CN.md skills/skill-phase-gate/agents/openai.yaml skills/skill-phase-gate/references/use-cases.md skills/skill-phase-gate/references/use-cases.zh-CN.md skills/skill-phase-gate/references/prompt-templates.en.md skills/skill-phase-gate/references/prompt-templates.zh-CN.md skills/skill-phase-gate/tests/test_package_contract.py
git commit -m "feat: refocus phase gate boundaries"
```

### Task 5: Sync Top-Level Package Index And Verify The Slice

**Files:**
- Modify: `skills/README.md`
- Modify: `skills/README.zh-CN.md`
- Test: `skills/skill-context-keeper/tests/test_package_contract.py`
- Test: `skills/skill-handoff-summary/tests/test_package_contract.py`
- Test: `skills/skill-phase-gate/tests/test_package_contract.py`
- Test: `skills/skill-task-continuity/tests/test_bootstrap_suite.py`

- [ ] **Step 1: Update the published package blurbs**

Change the top-level skill index so it describes:
- `skill-context-keeper` as root-state refresh and compression
- `skill-handoff-summary` as a root/subtask continuation contract
- `skill-phase-gate` as an optional risky-change checkpoint

- [ ] **Step 2: Run the verification set**

Run:
```bash
cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-maintenance
git diff --check
python3 -m unittest discover -s skills/skill-context-keeper/tests -p 'test_package_contract.py' -v
python3 -m unittest discover -s skills/skill-handoff-summary/tests -p 'test_package_contract.py' -v
python3 -m unittest discover -s skills/skill-phase-gate/tests -p 'test_package_contract.py' -v
python3 -m unittest discover -s skills/skill-task-continuity/tests -p 'test_bootstrap_suite.py' -v
python3 -m unittest discover -s skills/skill-subtask-context/tests -p 'test_package_contract.py' -v
python3 -m unittest discover -s skills/skill-context-packet/tests -p 'test_package_contract.py' -v
```
Expected: PASS with a clean diff check.

- [ ] **Step 3: Commit the legacy-refocus slice**

```bash
git add skills/README.md skills/README.zh-CN.md
git commit -m "feat: refocus legacy continuity skills"
```
