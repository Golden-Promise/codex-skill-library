# Continuity README Entry Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the long-task continuity docs feel friendlier and faster for first-time users while preserving package boundaries and bilingual alignment.

**Architecture:** Rework the `skills/` index into a true decision entry page, then reshape the four continuity package READMEs into landing pages that lead with use cases, outputs, and natural-language Codex prompts. Keep shell commands available, but push them below the first-screen newcomer path.

**Tech Stack:** Markdown docs, Python `unittest` contract tests

---

### Task 1: Lock the New Entry-Page Contract

**Files:**
- Modify: `skills/skill-context-keeper/tests/test_package_contract.py`
- Modify: `skills/skill-phase-gate/tests/test_package_contract.py`
- Modify: `skills/skill-handoff-summary/tests/test_package_contract.py`
- Modify: `skills/skill-task-continuity/tests/test_docs_contract.py`

- [ ] **Step 1: Add failing assertions for the new README entry structure**

Add tests that require:
- a quick-pick continuity block in `skills/README.md` and `skills/README.zh-CN.md`
- newcomer-first headings in the four README files
- natural-language install wording near the top
- explicit “what file gets created or updated” wording

- [ ] **Step 2: Run the targeted docs-contract tests and verify they fail**

Run: `python3 -m unittest skills/skill-context-keeper/tests/test_package_contract.py skills/skill-phase-gate/tests/test_package_contract.py skills/skill-handoff-summary/tests/test_package_contract.py skills/skill-task-continuity/tests/test_docs_contract.py -v`
Expected: FAIL because the current README files still use the older structure.

### Task 2: Rewrite the Skills Index as a True Entry Page

**Files:**
- Modify: `skills/README.md`
- Modify: `skills/README.zh-CN.md`

- [ ] **Step 1: Add a quick continuity decision block near the top**

Write a short “pick the right continuity skill” guide that maps:
- stale task state -> `skill-context-keeper`
- risky or multi-file change -> `skill-phase-gate`
- pause or handoff -> `skill-handoff-summary`
- first-time suite setup -> `skill-task-continuity`

- [ ] **Step 2: Keep the package table, but demote it to second-level detail**

Retain the published package table and package conventions, but make the fast decision guide the first thing new users read.

### Task 3: Reshape the Three Atomic README Pages

**Files:**
- Modify: `skills/skill-context-keeper/README.md`
- Modify: `skills/skill-context-keeper/README.zh-CN.md`
- Modify: `skills/skill-phase-gate/README.md`
- Modify: `skills/skill-phase-gate/README.zh-CN.md`
- Modify: `skills/skill-handoff-summary/README.md`
- Modify: `skills/skill-handoff-summary/README.zh-CN.md`

- [ ] **Step 1: Move each README to a faster landing-page flow**

Use a newcomer-friendly order that leads with:
- when to use the package
- what the user will get
- what file or artifact usually changes
- what to say to Codex first
- related skills

Keep “don’t use this when” and boundary wording, but move it below the first-screen orientation.

- [ ] **Step 2: Keep install guidance natural-language first**

Show the natural-language install prompt in the main install section.
Keep the exact shell install command available, but lower on the page so first-time users can start without hunting for script paths.

### Task 4: Reposition `skill-task-continuity` as the Beginner Entry Package

**Files:**
- Modify: `skills/skill-task-continuity/README.md`
- Modify: `skills/skill-task-continuity/README.zh-CN.md`

- [ ] **Step 1: Rewrite the opening as a first-time setup page**

Lead with language like:
- start here for first-time setup
- what gets created in the repo
- fastest setup
- which skill to use next

Move terms such as atomic package boundaries or maintainer-style design notes lower on the page.

- [ ] **Step 2: Keep full-suite install easy without implying hidden auto-install**

Preserve the explicit one-command full-suite install path and the statement that `skill-task-continuity` does not auto-install the atomic packages.
Lead with natural-language prompts first, and keep the exact CLI command available later.

### Task 5: Verify the New Entry Experience

**Files:**
- Verify: `skills/README.md`
- Verify: `skills/README.zh-CN.md`
- Verify: the four package README files

- [ ] **Step 1: Re-run the targeted docs-contract tests**

Run: `python3 -m unittest skills/skill-context-keeper/tests/test_package_contract.py skills/skill-phase-gate/tests/test_package_contract.py skills/skill-handoff-summary/tests/test_package_contract.py skills/skill-task-continuity/tests/test_docs_contract.py -v`
Expected: PASS

- [ ] **Step 2: Re-read the edited README files for tone and symmetry**

Check that:
- English and Chinese pages stay aligned
- first-screen wording is user-friendly
- commands are no longer the first thing a newcomer sees
- package boundaries still remain clear
