# Context Protocol Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the first executable slice of the context protocol redesign by introducing the new repo starter layout, bootstrapping root/subtask state artifacts, and adding the two new atomic packages that own subtask state and context packets.

**Architecture:** Extend `skill-task-continuity` from the current flat `.agent-state/` bootstrap into a layered repo workflow with `INDEX.md`, `root/`, `subtasks/`, and `archive/` semantics. Add `skill-subtask-context` and `skill-context-packet` as documentation-first atomic packages with their own assets, prompts, and contract tests. Keep existing packages compatible for now, and defer deeper refocusing of legacy package boundaries plus richer eval coverage to follow-on plans.

**Tech Stack:** Markdown package docs, Python `bootstrap_suite.py`, Python `unittest`, repo templates under `skills/`, existing continuity package structure

---

## Scope Note

The approved design spec spans three coupled implementation slices:

1. foundation layout + bootstrap + new atomic packages
2. legacy skill refocus around root vs subtask scope
3. workflow evals, migration docs, and release hardening

This plan intentionally covers **Slice 1 only** so the result is coherent, bootstrappable, and testable before the broader refactor lands.

## File Map

### Existing Files To Modify

- Modify: `skills/README.md`
  - Add `skill-subtask-context` and `skill-context-packet` to the published package index and continuity picker.
- Modify: `skills/README.zh-CN.md`
  - Mirror the new package index and routing guidance in Chinese.
- Modify: `skills/skill-task-continuity/SKILL.md`
  - Update suite routing language to account for root state, subtask state, and packets.
- Modify: `skills/skill-task-continuity/README.md`
  - Replace the flat starter-file explanation with the layered root/subtask layout and beginner mode.
- Modify: `skills/skill-task-continuity/README.zh-CN.md`
  - Mirror the English layout and beginner-mode changes in Chinese.
- Modify: `skills/skill-task-continuity/references/composition-guide.md`
  - Explain packet-first execution and when to create a subtask.
- Modify: `skills/skill-task-continuity/references/composition-guide.zh-CN.md`
  - Mirror the English composition-guide changes in Chinese.
- Modify: `skills/skill-task-continuity/references/install-playbook.md`
  - Document bootstrap output for `INDEX.md`, `root/`, `subtasks/`, and `archive/`.
- Modify: `skills/skill-task-continuity/references/install-playbook.zh-CN.md`
  - Mirror the English install-playbook changes in Chinese.
- Modify: `skills/skill-task-continuity/assets/AGENTS.repo-template.md`
  - Rework the repo template around `INDEX.md`, root packets, subtask packets, and compression flow.
- Modify: `skills/skill-task-continuity/scripts/bootstrap_suite.py`
  - Replace the flat `TEMPLATE_MAP` with the layered bootstrap layout and starter directory creation.
- Modify: `skills/skill-task-continuity/tests/test_bootstrap_suite.py`
  - Lock in the layered bootstrap output, duplicate-template mapping, and beginner-mode behavior.
- Modify: `skills/skill-task-continuity/tests/test_docs_contract.py`
  - Assert the new package names, new layout, and packet-first wording appear in suite docs.

### New Files To Create Under `skill-task-continuity`

- Create: `skills/skill-task-continuity/assets/agent-state/INDEX.template.md`
- Create: `skills/skill-task-continuity/assets/agent-state/root/TASK_STATE.template.md`
- Create: `skills/skill-task-continuity/assets/agent-state/root/PACKET.template.md`
- Create: `skills/skill-task-continuity/assets/agent-state/root/DECISIONS.template.md`
- Create: `skills/skill-task-continuity/assets/agent-state/root/RUN_LOG.template.md`
- Create: `skills/skill-task-continuity/assets/agent-state/root/HANDOFF.template.md`
- Create: `skills/skill-task-continuity/assets/agent-state/subtasks/TASK_STATE.template.md`
- Create: `skills/skill-task-continuity/assets/agent-state/subtasks/PACKET.template.md`
- Create: `skills/skill-task-continuity/assets/agent-state/subtasks/HANDOFF.template.md`
- Create: `skills/skill-task-continuity/assets/agent-state/subtasks/RUN_LOG.template.md`

### New `skill-subtask-context` Package

- Create: `skills/skill-subtask-context/SKILL.md`
- Create: `skills/skill-subtask-context/README.md`
- Create: `skills/skill-subtask-context/README.zh-CN.md`
- Create: `skills/skill-subtask-context/agents/openai.yaml`
- Create: `skills/skill-subtask-context/assets/TASK_STATE.template.md`
- Create: `skills/skill-subtask-context/references/README.md`
- Create: `skills/skill-subtask-context/references/README.zh-CN.md`
- Create: `skills/skill-subtask-context/references/use-cases.md`
- Create: `skills/skill-subtask-context/references/use-cases.zh-CN.md`
- Create: `skills/skill-subtask-context/references/prompt-templates.en.md`
- Create: `skills/skill-subtask-context/references/prompt-templates.zh-CN.md`
- Create: `skills/skill-subtask-context/tests/test_package_contract.py`

### New `skill-context-packet` Package

- Create: `skills/skill-context-packet/SKILL.md`
- Create: `skills/skill-context-packet/README.md`
- Create: `skills/skill-context-packet/README.zh-CN.md`
- Create: `skills/skill-context-packet/agents/openai.yaml`
- Create: `skills/skill-context-packet/assets/PACKET.template.md`
- Create: `skills/skill-context-packet/references/README.md`
- Create: `skills/skill-context-packet/references/README.zh-CN.md`
- Create: `skills/skill-context-packet/references/use-cases.md`
- Create: `skills/skill-context-packet/references/use-cases.zh-CN.md`
- Create: `skills/skill-context-packet/references/prompt-templates.en.md`
- Create: `skills/skill-context-packet/references/prompt-templates.zh-CN.md`
- Create: `skills/skill-context-packet/tests/test_package_contract.py`

## Approved Design Notes

- Keep the current four packages installable during this slice; add the two new packages without deleting anything yet.
- Make `INDEX.md` the repo entry point, not `TASK_STATE.md`.
- Make packets the default injection object.
- Use beginner mode as a subset of the expanded layout, not a separate bootstrap system.
- Reuse the current `skill-context-keeper` task-state asset and `skill-handoff-summary` handoff asset where possible, but duplicate them into the suite assets for downstream bootstrap.
- Leave deep rewrites of `skill-context-keeper`, `skill-handoff-summary`, and `skill-phase-gate` to the follow-on legacy-refocus plan.

## Out Of Scope For This Plan

- Rewriting legacy package prompts around root-vs-subtask scope
- Expanding `evals/cases.csv` for packet/subtask/compression scenarios
- Adding archive automation beyond bootstrap directory creation and documented compression flow
- Renaming or retiring legacy skills

### Task 1: Add Failing Bootstrap And Documentation Contracts

**Files:**
- Modify: `skills/skill-task-continuity/tests/test_bootstrap_suite.py`
- Modify: `skills/skill-task-continuity/tests/test_docs_contract.py`
- Test: `skills/skill-task-continuity/tests/test_bootstrap_suite.py`
- Test: `skills/skill-task-continuity/tests/test_docs_contract.py`

- [ ] **Step 1: Extend the bootstrap tests to describe the new layered output**

Add failing assertions for:
- `.agent-state/INDEX.md`
- `root/TASK_STATE.md`, `root/PACKET.md`, `root/HANDOFF.md`
- `subtasks/` starter structure or documented empty-directory behavior
- template duplication between suite assets and the relevant atomic package assets
- preservation of existing files without `--force`

- [ ] **Step 2: Extend the docs contract tests to cover the new package topology**

Add failing assertions that suite docs now mention:
- `skill-subtask-context`
- `skill-context-packet`
- `INDEX.md`
- root/subtask packet-first workflow
- beginner mode vs expanded mode

- [ ] **Step 3: Run the two test modules to verify they fail**

Run:
```bash
cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-maintenance
python3 -m unittest discover -s skills/skill-task-continuity/tests -p 'test_bootstrap_suite.py' -v
python3 -m unittest discover -s skills/skill-task-continuity/tests -p 'test_docs_contract.py' -v
```
Expected: FAIL because the current suite still describes the flat layout and lacks the new package docs.

- [ ] **Step 4: Commit the red-test checkpoint if you want an explicit TDD breadcrumb**

```bash
git add skills/skill-task-continuity/tests/test_bootstrap_suite.py skills/skill-task-continuity/tests/test_docs_contract.py
git commit -m "test: add context protocol foundation contracts"
```

### Task 2: Implement The Layered Bootstrap Layout In `skill-task-continuity`

**Files:**
- Modify: `skills/skill-task-continuity/SKILL.md`
- Modify: `skills/skill-task-continuity/README.md`
- Modify: `skills/skill-task-continuity/README.zh-CN.md`
- Modify: `skills/skill-task-continuity/references/composition-guide.md`
- Modify: `skills/skill-task-continuity/references/composition-guide.zh-CN.md`
- Modify: `skills/skill-task-continuity/references/install-playbook.md`
- Modify: `skills/skill-task-continuity/references/install-playbook.zh-CN.md`
- Modify: `skills/skill-task-continuity/assets/AGENTS.repo-template.md`
- Modify: `skills/skill-task-continuity/scripts/bootstrap_suite.py`
- Create: `skills/skill-task-continuity/assets/agent-state/INDEX.template.md`
- Create: `skills/skill-task-continuity/assets/agent-state/root/TASK_STATE.template.md`
- Create: `skills/skill-task-continuity/assets/agent-state/root/PACKET.template.md`
- Create: `skills/skill-task-continuity/assets/agent-state/root/DECISIONS.template.md`
- Create: `skills/skill-task-continuity/assets/agent-state/root/RUN_LOG.template.md`
- Create: `skills/skill-task-continuity/assets/agent-state/root/HANDOFF.template.md`
- Create: `skills/skill-task-continuity/assets/agent-state/subtasks/TASK_STATE.template.md`
- Create: `skills/skill-task-continuity/assets/agent-state/subtasks/PACKET.template.md`
- Create: `skills/skill-task-continuity/assets/agent-state/subtasks/HANDOFF.template.md`
- Create: `skills/skill-task-continuity/assets/agent-state/subtasks/RUN_LOG.template.md`
- Test: `skills/skill-task-continuity/tests/test_bootstrap_suite.py`
- Test: `skills/skill-task-continuity/tests/test_docs_contract.py`

- [ ] **Step 1: Create the new suite starter templates**

Author the layered templates so:
- `INDEX.template.md` routes into root or subtask packets
- root templates model durable top-level state
- subtask templates model local state and local packet execution
- handoff templates are consistent with the existing continuation contract

- [ ] **Step 2: Replace the flat bootstrap mapping with the layered layout**

Update `bootstrap_suite.py` so it:
- copies the new root and subtask starter files
- creates the missing archive directories
- preserves existing files unless `--force`
- continues refusing the public library root

- [ ] **Step 3: Rewrite suite docs around beginner mode and expanded mode**

Update package docs so they explain:
- beginner mode = `INDEX.md` + `root/` only
- expanded mode = `subtasks/` and `archive/`
- packets are the default injection surface
- root task and subtask are distinct context owners

- [ ] **Step 4: Re-run the two task-continuity test modules**

Run:
```bash
cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-maintenance
python3 -m unittest discover -s skills/skill-task-continuity/tests -p 'test_bootstrap_suite.py' -v
python3 -m unittest discover -s skills/skill-task-continuity/tests -p 'test_docs_contract.py' -v
```
Expected: PASS

- [ ] **Step 5: Commit the layered bootstrap slice**

```bash
git add skills/skill-task-continuity/SKILL.md skills/skill-task-continuity/README.md skills/skill-task-continuity/README.zh-CN.md skills/skill-task-continuity/references/composition-guide.md skills/skill-task-continuity/references/composition-guide.zh-CN.md skills/skill-task-continuity/references/install-playbook.md skills/skill-task-continuity/references/install-playbook.zh-CN.md skills/skill-task-continuity/assets/AGENTS.repo-template.md skills/skill-task-continuity/assets/agent-state/INDEX.template.md skills/skill-task-continuity/assets/agent-state/root/TASK_STATE.template.md skills/skill-task-continuity/assets/agent-state/root/PACKET.template.md skills/skill-task-continuity/assets/agent-state/root/DECISIONS.template.md skills/skill-task-continuity/assets/agent-state/root/RUN_LOG.template.md skills/skill-task-continuity/assets/agent-state/root/HANDOFF.template.md skills/skill-task-continuity/assets/agent-state/subtasks/TASK_STATE.template.md skills/skill-task-continuity/assets/agent-state/subtasks/PACKET.template.md skills/skill-task-continuity/assets/agent-state/subtasks/HANDOFF.template.md skills/skill-task-continuity/assets/agent-state/subtasks/RUN_LOG.template.md skills/skill-task-continuity/scripts/bootstrap_suite.py skills/skill-task-continuity/tests/test_bootstrap_suite.py skills/skill-task-continuity/tests/test_docs_contract.py
git commit -m "feat: bootstrap the context protocol layout"
```

### Task 3: Add The `skill-subtask-context` Package

**Files:**
- Create: `skills/skill-subtask-context/SKILL.md`
- Create: `skills/skill-subtask-context/README.md`
- Create: `skills/skill-subtask-context/README.zh-CN.md`
- Create: `skills/skill-subtask-context/agents/openai.yaml`
- Create: `skills/skill-subtask-context/assets/TASK_STATE.template.md`
- Create: `skills/skill-subtask-context/references/README.md`
- Create: `skills/skill-subtask-context/references/README.zh-CN.md`
- Create: `skills/skill-subtask-context/references/use-cases.md`
- Create: `skills/skill-subtask-context/references/use-cases.zh-CN.md`
- Create: `skills/skill-subtask-context/references/prompt-templates.en.md`
- Create: `skills/skill-subtask-context/references/prompt-templates.zh-CN.md`
- Create: `skills/skill-subtask-context/tests/test_package_contract.py`
- Test: `skills/skill-subtask-context/tests/test_package_contract.py`

- [ ] **Step 1: Write the failing package contract**

Add tests that require:
- the new package files to exist
- README fast-entry sections in both languages
- use-case and prompt-template references in both languages
- a subtask-state asset with the required headings
- direct natural-language invocation wording

- [ ] **Step 2: Run the new test module to verify it fails**

Run:
```bash
cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-maintenance
python3 -m unittest discover -s skills/skill-subtask-context/tests -p 'test_package_contract.py' -v
```
Expected: FAIL because the package does not exist yet.

- [ ] **Step 3: Author the package**

Implement:
- the narrow package boundary around subtask creation, refresh, closure, and local state ownership
- a subtask state template aligned to the approved spec
- bilingual README and reference docs consistent with existing package style

- [ ] **Step 4: Re-run the package test**

Run the same `python3 -m unittest discover ...` command from Step 2.
Expected: PASS

- [ ] **Step 5: Commit the new package**

```bash
git add skills/skill-subtask-context
git commit -m "feat: add subtask context skill"
```

### Task 4: Add The `skill-context-packet` Package

**Files:**
- Create: `skills/skill-context-packet/SKILL.md`
- Create: `skills/skill-context-packet/README.md`
- Create: `skills/skill-context-packet/README.zh-CN.md`
- Create: `skills/skill-context-packet/agents/openai.yaml`
- Create: `skills/skill-context-packet/assets/PACKET.template.md`
- Create: `skills/skill-context-packet/references/README.md`
- Create: `skills/skill-context-packet/references/README.zh-CN.md`
- Create: `skills/skill-context-packet/references/use-cases.md`
- Create: `skills/skill-context-packet/references/use-cases.zh-CN.md`
- Create: `skills/skill-context-packet/references/prompt-templates.en.md`
- Create: `skills/skill-context-packet/references/prompt-templates.zh-CN.md`
- Create: `skills/skill-context-packet/tests/test_package_contract.py`
- Test: `skills/skill-context-packet/tests/test_package_contract.py`

- [ ] **Step 1: Write the failing package contract**

Add tests that require:
- package metadata and docs to exist
- README fast-entry sections and direct invocation wording
- a packet template with explicit objective, constraints, verified facts, active risks, exact next action, and file-reference sections
- bilingual reference index and prompt-template coverage

- [ ] **Step 2: Run the new test module to verify it fails**

Run:
```bash
cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-maintenance
python3 -m unittest discover -s skills/skill-context-packet/tests -p 'test_package_contract.py' -v
```
Expected: FAIL because the package does not exist yet.

- [ ] **Step 3: Author the package**

Implement:
- the boundary around building or refreshing the minimum context packet for the next action
- a generic packet template usable for root and subtask packet duplication
- bilingual docs aligned with the current package conventions

- [ ] **Step 4: Re-run the package test**

Run the same `python3 -m unittest discover ...` command from Step 2.
Expected: PASS

- [ ] **Step 5: Commit the new package**

```bash
git add skills/skill-context-packet
git commit -m "feat: add context packet skill"
```

### Task 5: Update The Published Skill Index And Suite Routing

**Files:**
- Modify: `skills/README.md`
- Modify: `skills/README.zh-CN.md`
- Modify: `skills/skill-task-continuity/tests/test_docs_contract.py`
- Test: `skills/skill-task-continuity/tests/test_docs_contract.py`

- [ ] **Step 1: Update the top-level skill index**

Add:
- the two new packages in the published package table
- quick-picker wording that differentiates root-state refresh, subtask work, and packet generation

- [ ] **Step 2: Re-run the docs contract**

Run:
```bash
cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-maintenance
python3 -m unittest discover -s skills/skill-task-continuity/tests -p 'test_docs_contract.py' -v
```
Expected: PASS

- [ ] **Step 3: Commit the routing update**

```bash
git add skills/README.md skills/README.zh-CN.md skills/skill-task-continuity/tests/test_docs_contract.py
git commit -m "docs: route continuity users to the new context packages"
```

### Task 6: Run Foundation Verification And Record The Plan

**Files:**
- Verify only: `skills/skill-task-continuity/tests/test_bootstrap_suite.py`
- Verify only: `skills/skill-task-continuity/tests/test_docs_contract.py`
- Verify only: `skills/skill-subtask-context/tests/test_package_contract.py`
- Verify only: `skills/skill-context-packet/tests/test_package_contract.py`
- Verify only: `skills/skill-context-keeper/tests/test_package_contract.py`
- Verify only: `skills/skill-handoff-summary/tests/test_package_contract.py`
- Verify only: `evals/test_run_evals.py`
- Modify: `docs/superpowers/plans/2026-03-26-context-protocol-foundation.md`

- [ ] **Step 1: Run the foundation package tests**

Run:
```bash
cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-maintenance
python3 -m unittest discover -s skills/skill-task-continuity/tests -p 'test_*.py' -v
python3 -m unittest discover -s skills/skill-subtask-context/tests -p 'test_*.py' -v
python3 -m unittest discover -s skills/skill-context-packet/tests -p 'test_*.py' -v
python3 -m unittest discover -s skills/skill-context-keeper/tests -p 'test_*.py' -v
python3 -m unittest discover -s skills/skill-handoff-summary/tests -p 'test_*.py' -v
```
Expected: PASS

- [ ] **Step 2: Run eval unit tests to catch continuity-routing regressions**

Run:
```bash
cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-maintenance
python3 -m unittest discover -s evals -p 'test_*.py' -v
```
Expected: PASS

- [ ] **Step 3: Inspect git state**

Run:
```bash
git -C /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-maintenance status --short
git -C /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-maintenance diff --stat
```
Expected: only the planned foundation files are changed

- [ ] **Step 4: Commit the plan document after execution notes are current**

```bash
git add docs/superpowers/plans/2026-03-26-context-protocol-foundation.md
git commit -m "docs: record context protocol foundation plan"
```

## Follow-On Plans

After this foundation slice lands, write separate implementation plans for:

1. **Legacy Skill Refocus**
   Rework `skill-context-keeper`, `skill-handoff-summary`, and `skill-phase-gate` around the root/subtask protocol.
2. **Workflow Evals And Migration**
   Add scenario evals for packets, subtasks, compression, and downstream migration guidance.
