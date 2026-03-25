# Continuity Install UX Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the long-task continuity suite easier to adopt by documenting a one-command full-suite install path, preferring natural-language Codex invocation for bootstrap, and tightening the atomic package README guidance.

**Architecture:** Keep package boundaries unchanged and avoid implicit multi-package installation side effects. Reuse the existing `skill-installer` capability to accept multiple `--path` values, then document that clearly in `skill-task-continuity`. Add lightweight documentation-contract tests so future README edits do not regress installation or natural-language usage guidance.

**Tech Stack:** Markdown package docs, Python `unittest`, existing `skill-installer` behavior, existing continuity package structure under `skills/`

---

## File Map

- Modify: `skills/skill-task-continuity/README.md`
  - Add “install just this package” vs “install the full suite” guidance.
  - Add natural-language Codex installation and bootstrap wording.
- Modify: `skills/skill-task-continuity/README.zh-CN.md`
  - Mirror the English changes in Chinese.
- Modify: `skills/skill-task-continuity/references/install-playbook.md`
  - Rework bootstrap guidance so natural-language Codex invocation is the first path and CLI is the precise fallback.
- Modify: `skills/skill-task-continuity/references/install-playbook.zh-CN.md`
  - Mirror the English playbook changes in Chinese.
- Modify: `skills/skill-task-continuity/references/composition-guide.md`
  - Add an explicit one-command full-suite install example and suite-entry wording if needed.
- Modify: `skills/skill-task-continuity/references/composition-guide.zh-CN.md`
  - Mirror the English composition-guide changes in Chinese.
- Create: `skills/skill-task-continuity/tests/test_docs_contract.py`
  - Lock in suite install UX and natural-language bootstrap wording.
- Modify: `skills/skill-context-keeper/README.md`
  - Add direct natural-language “ask Codex to use this skill” usage guidance.
- Modify: `skills/skill-context-keeper/README.zh-CN.md`
  - Mirror the English usage guidance in Chinese.
- Modify: `skills/skill-phase-gate/README.md`
  - Add direct natural-language “ask Codex to use this skill” usage guidance.
- Modify: `skills/skill-phase-gate/README.zh-CN.md`
  - Mirror the English usage guidance in Chinese.
- Modify: `skills/skill-handoff-summary/README.md`
  - Add direct natural-language “ask Codex to use this skill” usage guidance.
- Modify: `skills/skill-handoff-summary/README.zh-CN.md`
  - Mirror the English usage guidance in Chinese.
- Modify: `skills/skill-context-keeper/tests/test_package_contract.py`
  - Assert the README contains direct natural-language usage guidance.
- Modify: `skills/skill-phase-gate/tests/test_package_contract.py`
  - Assert the README contains direct natural-language usage guidance.
- Modify: `skills/skill-handoff-summary/tests/test_package_contract.py`
  - Assert the README contains direct natural-language usage guidance.

## Approved Design Notes

- Use the existing `skill-installer --path <path1> <path2> ...` behavior for full-suite installation.
- Do **not** make `skill-task-continuity` auto-install the three atomic skills.
- Prefer natural-language Codex enable/bootstrap wording in package docs, with shell commands retained as exact execution fallbacks.
- Tighten the atomic package READMEs only where it materially improves “how do I actually use this with Codex?” clarity.

### Task 1: Add Suite Documentation Contract Tests

**Files:**
- Create: `skills/skill-task-continuity/tests/test_docs_contract.py`
- Test: `skills/skill-task-continuity/tests/test_docs_contract.py`

- [ ] **Step 1: Write the failing documentation-contract tests**

Add tests that assert:
- the suite README mentions installing the whole suite in one command
- the full-suite install path uses multiple `--path` values instead of implicit side effects
- the install playbook mentions asking Codex in natural language to bootstrap a downstream repo
- the playbook still preserves explicit CLI fallback examples

- [ ] **Step 2: Run the new tests to verify they fail**

Run: `cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-install-ux && python3 -m unittest discover -s skills/skill-task-continuity/tests -p 'test_docs_contract.py' -v`
Expected: FAIL because the current docs do not yet contain the new full-suite install and natural-language bootstrap wording.

- [ ] **Step 3: Commit the failing-test checkpoint only if you want a visible TDD breadcrumb**

```bash
git add skills/skill-task-continuity/tests/test_docs_contract.py
git commit -m "test: add continuity install ux doc contracts"
```

### Task 2: Implement Suite Install And Bootstrap Documentation Changes

**Files:**
- Modify: `skills/skill-task-continuity/README.md`
- Modify: `skills/skill-task-continuity/README.zh-CN.md`
- Modify: `skills/skill-task-continuity/references/install-playbook.md`
- Modify: `skills/skill-task-continuity/references/install-playbook.zh-CN.md`
- Modify: `skills/skill-task-continuity/references/composition-guide.md`
- Modify: `skills/skill-task-continuity/references/composition-guide.zh-CN.md`
- Test: `skills/skill-task-continuity/tests/test_docs_contract.py`

- [ ] **Step 1: Update the suite README files**

Add:
- a “just this package” install path
- a one-command “install the full suite” path using multiple `--path` arguments
- natural-language Codex install wording
- natural-language Codex bootstrap wording before the shell commands

- [ ] **Step 2: Update the install playbooks**

Rework the bootstrap walkthrough so it says, in plain language, how to ask Codex to:
- install the suite entry package
- install all four continuity packages together when desired
- preview downstream bootstrap changes
- run the real bootstrap

Retain the existing shell commands as precise alternatives.

- [ ] **Step 3: Update the composition guides if needed**

Make sure the suite package now clearly says:
- one package can teach and bootstrap the suite
- one command can install all four packages
- atomic packages still own the actual task actions

- [ ] **Step 4: Re-run the suite documentation-contract tests**

Run: `cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-install-ux && python3 -m unittest discover -s skills/skill-task-continuity/tests -p 'test_docs_contract.py' -v`
Expected: PASS

- [ ] **Step 5: Commit the suite install UX changes**

```bash
git add skills/skill-task-continuity/README.md skills/skill-task-continuity/README.zh-CN.md skills/skill-task-continuity/references/install-playbook.md skills/skill-task-continuity/references/install-playbook.zh-CN.md skills/skill-task-continuity/references/composition-guide.md skills/skill-task-continuity/references/composition-guide.zh-CN.md skills/skill-task-continuity/tests/test_docs_contract.py
git commit -m "docs: streamline continuity suite install guidance"
```

### Task 3: Tighten Atomic Package “Use It With Codex” Guidance

**Files:**
- Modify: `skills/skill-context-keeper/README.md`
- Modify: `skills/skill-context-keeper/README.zh-CN.md`
- Modify: `skills/skill-phase-gate/README.md`
- Modify: `skills/skill-phase-gate/README.zh-CN.md`
- Modify: `skills/skill-handoff-summary/README.md`
- Modify: `skills/skill-handoff-summary/README.zh-CN.md`
- Modify: `skills/skill-context-keeper/tests/test_package_contract.py`
- Modify: `skills/skill-phase-gate/tests/test_package_contract.py`
- Modify: `skills/skill-handoff-summary/tests/test_package_contract.py`

- [ ] **Step 1: Add failing README contract checks for direct natural-language usage**

Extend the package-contract tests so each README must contain at least one direct “ask Codex to use this skill” phrasing, not just install wording and links to prompt templates.

- [ ] **Step 2: Run the three package-contract test files and verify they fail**

Run:
```bash
cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-install-ux
python3 -m unittest discover -s skills/skill-context-keeper/tests -p 'test_package_contract.py' -v
python3 -m unittest discover -s skills/skill-phase-gate/tests -p 'test_package_contract.py' -v
python3 -m unittest discover -s skills/skill-handoff-summary/tests -p 'test_package_contract.py' -v
```
Expected: at least one FAIL per package before the README updates land.

- [ ] **Step 3: Update the three atomic package README pairs**

For each package, add a short, direct section or paragraph that shows how to tell Codex to use the skill in natural language.

Keep the package boundaries intact:
- `skill-context-keeper` = state refresh only
- `skill-phase-gate` = checkpoint only
- `skill-handoff-summary` = handoff only

- [ ] **Step 4: Re-run the three package-contract test files**

Run the same three `python3 -m unittest discover ...` commands from Step 2.
Expected: PASS

- [ ] **Step 5: Commit the atomic README clarity pass**

```bash
git add skills/skill-context-keeper/README.md skills/skill-context-keeper/README.zh-CN.md skills/skill-phase-gate/README.md skills/skill-phase-gate/README.zh-CN.md skills/skill-handoff-summary/README.md skills/skill-handoff-summary/README.zh-CN.md skills/skill-context-keeper/tests/test_package_contract.py skills/skill-phase-gate/tests/test_package_contract.py skills/skill-handoff-summary/tests/test_package_contract.py
git commit -m "docs: clarify continuity skill invocation wording"
```

### Task 4: Full Verification And Release-Safe Wrap-Up

**Files:**
- Verify only: `skills/skill-task-continuity/tests/test_docs_contract.py`
- Verify only: `skills/skill-context-keeper/tests/test_package_contract.py`
- Verify only: `skills/skill-phase-gate/tests/test_package_contract.py`
- Verify only: `skills/skill-handoff-summary/tests/test_package_contract.py`
- Verify only: `evals/test_run_evals.py`
- Verify only: `evals/cases.csv`

- [ ] **Step 1: Run the continuity package tests**

Run:
```bash
cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-install-ux
for test_dir in skills/*/tests; do
  python3 -m unittest discover -s "$test_dir" -p 'test_*.py' -v
done
```
Expected: all package tests PASS

- [ ] **Step 2: Run the additional governance validation**

Run: `cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-install-ux/skills/skill-governance && python3 scripts/manage_skill.py --validate-only`
Expected: `[OK] Validation passed`

- [ ] **Step 3: Run eval unit tests**

Run: `cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-install-ux && python3 -m unittest discover -s evals -p 'test_*.py' -v`
Expected: PASS

- [ ] **Step 4: Run the continuity eval seed matrix**

Run: `cd /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-install-ux && python3 evals/run_evals.py`
Expected: `Cases: 8  Passed: 8  Failed: 0`

- [ ] **Step 5: Check git state and prepare summary**

Run:
```bash
git -C /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-install-ux status --short
git -C /home/jn/projects/codex/codex-skill-library/.worktrees/continuity-install-ux diff --stat
```
Expected: only the planned doc and test files are changed

- [ ] **Step 6: Commit the final verified state**

```bash
git add docs/superpowers/plans/2026-03-25-continuity-install-ux.md
git commit -m "docs: record continuity install ux plan"
```
