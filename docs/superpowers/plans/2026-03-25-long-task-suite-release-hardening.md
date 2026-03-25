# Long-Task Suite Release Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prepare the long-task continuity suite for a clean draft PR, merge, and GitHub release flow without expanding product scope.

**Architecture:** Treat this as repository release hardening, not new feature work. Keep the four published packages unchanged unless a real release-facing issue appears, move maintainer guidance into `docs/`, keep user entry points in package `README.md`, and add one simple PR-facing CI workflow that validates package contracts plus the continuity eval harness.

**Tech Stack:** Markdown, YAML (GitHub Actions), Python `unittest`, existing `evals/run_evals.py`, existing `skill-installer` install flow

---

## File Map

### Create

- `.github/workflows/pull-request-checks.yml`
  Purpose: Run repository release-confidence checks on pull requests with a simple Python workflow.
- `docs/release-checklist-long-task-suite.md`
  Purpose: Maintainer-facing English checklist for pre-release, tag, and post-release validation.
- `docs/release-checklist-long-task-suite.zh-CN.md`
  Purpose: Maintainer-facing Simplified Chinese checklist aligned with the English checklist.
- `docs/superpowers/plans/2026-03-25-long-task-suite-release-hardening.md`
  Purpose: Execution plan for this release-hardening pass.

### Modify

- `README.md`
  Purpose: Keep repository entry docs release-ready, make all four long-task packages discoverable, and point readers to maintainer release docs.
- `README.zh-CN.md`
  Purpose: Keep bilingual root docs aligned with the English repository entry docs.
- `skills/README.md`
  Purpose: Keep the published package index crisp, non-overlapping, and release-ready.
- `skills/README.zh-CN.md`
  Purpose: Keep the Chinese package index aligned with the English index.
- `CHANGELOG.md`
  Purpose: Turn the current unreleased continuity notes into clean, reader-visible release notes for the next minor release.
- `docs/publishing.md`
  Purpose: Add PR CI guidance, smoke-test guidance, and release-checklist links for maintainers.
- `docs/publishing.zh-CN.md`
  Purpose: Keep the Chinese publishing guide aligned with the English guide.
- `skills/skill-context-keeper/README.md`
  Purpose: Fix only real release-facing clarity issues around installation wording, boundaries, and downstream artifact references if found.
- `skills/skill-context-keeper/README.zh-CN.md`
  Purpose: Keep bilingual package guidance aligned if English package wording changes.
- `skills/skill-phase-gate/README.md`
  Purpose: Fix only real release-facing clarity issues if found during the consistency pass.
- `skills/skill-phase-gate/README.zh-CN.md`
  Purpose: Keep bilingual package guidance aligned if English package wording changes.
- `skills/skill-handoff-summary/README.md`
  Purpose: Fix only real release-facing clarity issues if found during the consistency pass.
- `skills/skill-handoff-summary/README.zh-CN.md`
  Purpose: Keep bilingual package guidance aligned if English package wording changes.
- `skills/skill-task-continuity/README.md`
  Purpose: Fix only real release-facing clarity issues around bootstrap usage, downstream templates, and suite composition if found.
- `skills/skill-task-continuity/README.zh-CN.md`
  Purpose: Keep bilingual package guidance aligned if English package wording changes.

### Verify

- `skills/skill-context-keeper/tests/test_package_contract.py`
- `skills/skill-phase-gate/tests/test_package_contract.py`
- `skills/skill-handoff-summary/tests/test_package_contract.py`
- `skills/skill-task-continuity/tests/test_bootstrap_suite.py`
- `evals/test_run_evals.py`
- `evals/run_evals.py`

## Implementation Notes

- Keep the release target conservative: propose `v0.6.0` because `CHANGELOG.md` currently ends at `v0.5.1` and this suite adds four new published packages plus repo-level eval/CI guidance.
- Do not add new runtime assets at the repository root.
- Keep install guidance in the repository docs aligned with the existing `skill-installer` command shape:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/<skill-name>
```

- For tagged-release examples, use the next proposed version string consistently once `CHANGELOG.md` is updated:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/<skill-name> \
  --ref v0.6.0
```

- Keep CI simple: one workflow, one Ubuntu job, Python setup, package test loop, eval tests, then `python3 evals/run_evals.py`.

### Task 1: Audit Repository Docs And Indexes

**Files:**
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `skills/README.md`
- Modify: `skills/README.zh-CN.md`
- Modify: `CHANGELOG.md`
- Modify: `docs/publishing.md`
- Modify: `docs/publishing.zh-CN.md`

- [ ] **Step 1: Capture the current doc gaps**

Run:

```bash
sed -n '1,260p' README.md
sed -n '1,260p' README.zh-CN.md
sed -n '1,220p' skills/README.md
sed -n '1,220p' skills/README.zh-CN.md
sed -n '1,260p' CHANGELOG.md
sed -n '1,260p' docs/publishing.md
sed -n '1,260p' docs/publishing.zh-CN.md
```

Expected:
- Root docs still center install examples on `skill-governance`
- Publishing docs do not yet show four-package smoke tests or PR CI
- `CHANGELOG.md` has continuity notes, but the `Unreleased` wording still needs release-ready polish

- [ ] **Step 2: Write the failing release-doc contract mentally before editing**

Treat the following as the doc contract to satisfy:

```text
1. All four continuity packages are visible from root and skills indexes.
2. Package blur is minimized with short, non-overlapping descriptions.
3. Maintainers can find CI, smoke-test, and release-checklist guidance from docs/publishing*.
4. Release examples consistently use the same next-version placeholder/value.
5. English and Chinese docs stay structurally aligned.
```

Expected:
- Current docs do not yet satisfy all five points

- [ ] **Step 3: Apply minimal doc edits**

Edit the files so they:
- keep the four continuity packages visible from the two indexes
- replace single-package release examples with concise multi-package release guidance
- point maintainers to the release checklist docs
- align the next release reference to `v0.6.0`
- keep the Chinese docs structurally parallel to the English docs

- [ ] **Step 4: Re-read the edited docs**

Run:

```bash
sed -n '1,260p' README.md
sed -n '1,260p' README.zh-CN.md
sed -n '1,220p' skills/README.md
sed -n '1,220p' skills/README.zh-CN.md
sed -n '1,260p' CHANGELOG.md
sed -n '1,260p' docs/publishing.md
sed -n '1,260p' docs/publishing.zh-CN.md
```

Expected:
- Descriptions read cleanly and do not overlap badly
- Release/install references are consistent
- Root docs do not imply the repo itself is a downstream consumer repo

- [ ] **Step 5: Commit the doc/index audit pass**

```bash
git add README.md README.zh-CN.md skills/README.md skills/README.zh-CN.md CHANGELOG.md docs/publishing.md docs/publishing.zh-CN.md docs/superpowers/plans/2026-03-25-long-task-suite-release-hardening.md
git commit -m "docs: harden release-facing continuity docs"
```

### Task 2: Add Pull-Request CI Coverage

**Files:**
- Create: `.github/workflows/pull-request-checks.yml`
- Test: `skills/skill-context-keeper/tests/test_package_contract.py`
- Test: `skills/skill-phase-gate/tests/test_package_contract.py`
- Test: `skills/skill-handoff-summary/tests/test_package_contract.py`
- Test: `skills/skill-task-continuity/tests/test_bootstrap_suite.py`
- Test: `evals/test_run_evals.py`

- [ ] **Step 1: Write the intended CI contract before adding the workflow**

The workflow should effectively enforce:

```text
1. Pull requests run on Ubuntu with Python 3.
2. Every published package test directory under skills/*/tests is executed.
3. eval unit tests run.
4. eval seed cases run.
5. The workflow is understandable from a single YAML file.
```

Expected:
- No current workflow exists, so this contract is failing by absence

- [ ] **Step 2: Add a simple GitHub Actions workflow**

Implement a single workflow file with:

```yaml
name: pull-request-checks

on:
  pull_request:
  workflow_dispatch:

jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Run package tests
        run: |
          set -eu
          for test_dir in skills/*/tests; do
            python3 -m unittest discover -s "$test_dir" -p 'test_*.py' -v
          done
      - name: Run eval unit tests
        run: python3 -m unittest discover -s evals -p 'test_*.py' -v
      - name: Run eval seed cases
        run: python3 evals/run_evals.py
```

- [ ] **Step 3: Sanity-check the workflow content locally**

Run:

```bash
sed -n '1,220p' .github/workflows/pull-request-checks.yml
```

Expected:
- Triggers and commands are easy to read
- No package-specific path is hard-coded beyond the simple `skills/*/tests` loop

- [ ] **Step 4: Commit the CI workflow**

```bash
git add .github/workflows/pull-request-checks.yml
git commit -m "ci: add pull request checks for published packages"
```

### Task 3: Add Release Checklist Docs

**Files:**
- Create: `docs/release-checklist-long-task-suite.md`
- Create: `docs/release-checklist-long-task-suite.zh-CN.md`
- Modify: `docs/publishing.md`
- Modify: `docs/publishing.zh-CN.md`

- [ ] **Step 1: Write the checklist structure**

Include sections for:

```text
- preflight repo status
- package tests
- `skill-governance` validate-only packaging sanity
- eval tests and seed cases
- root/index doc verification
- install smoke tests from a pushed branch or `main`
- changelog and version confirmation
- tag and GitHub release steps
- post-release tagged smoke verification
```

- [ ] **Step 2: Add the English checklist**

Use concise checklist items with copyable commands such as:

```bash
git status --short
(cd skills/skill-governance && python3 scripts/manage_skill.py --validate-only)
for test_dir in skills/*/tests; do
  python3 -m unittest discover -s "$test_dir" -p 'test_*.py' -v
done
python3 -m unittest discover -s evals -p 'test_*.py' -v
python3 evals/run_evals.py
```

- [ ] **Step 3: Add the Chinese checklist**

Mirror the English checklist structure closely so maintainers can compare the two versions line-by-line.

- [ ] **Step 4: Link the new checklist docs from the publishing guides**

Re-read:

```bash
sed -n '1,260p' docs/release-checklist-long-task-suite.md
sed -n '1,260p' docs/release-checklist-long-task-suite.zh-CN.md
sed -n '1,260p' docs/publishing.md
sed -n '1,260p' docs/publishing.zh-CN.md
```

Expected:
- Maintainers can discover the checklist from `docs/publishing*`
- The checklist is release-focused and does not expand into unrelated process docs

- [ ] **Step 5: Commit the checklist docs**

```bash
git add docs/release-checklist-long-task-suite.md docs/release-checklist-long-task-suite.zh-CN.md docs/publishing.md docs/publishing.zh-CN.md
git commit -m "docs: add long-task suite release checklist"
```

### Task 4: Add Install Smoke-Test Guidance

**Files:**
- Modify: `docs/publishing.md`
- Modify: `docs/publishing.zh-CN.md`
- Modify: `README.md`
- Modify: `README.zh-CN.md`

- [ ] **Step 1: Define the smoke-test command set**

Use a pushed branch ref when you want to smoke-test an unreleased PR branch, use `main` when you want the default public branch, and keep one pinned tagged-release pattern:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py --repo Golden-Promise/codex-skill-library --path skills/skill-context-keeper --ref <branch-name>
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py --repo Golden-Promise/codex-skill-library --path skills/skill-phase-gate
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py --repo Golden-Promise/codex-skill-library --path skills/skill-handoff-summary
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py --repo Golden-Promise/codex-skill-library --path skills/skill-task-continuity --ref v0.6.0
```

- [ ] **Step 2: Add a concise maintainer-facing smoke-test section**

Place the full command examples in `docs/publishing*`, and only add short pointers from root `README*` if needed for discoverability. Make the unreleased-branch example use `--ref <branch-name>` explicitly so it does not read like the same command as `main`.

- [ ] **Step 3: Re-read the smoke-test guidance**

Run:

```bash
rg -n "skill-context-keeper|skill-phase-gate|skill-handoff-summary|skill-task-continuity|v0.6.0|smoke" README.md README.zh-CN.md docs/publishing.md docs/publishing.zh-CN.md
```

Expected:
- All four packages appear
- Both pushed-branch / `main` and tagged examples are present where appropriate
- Commands stay concise and copyable

- [ ] **Step 4: Commit the smoke-test guidance**

```bash
git add README.md README.zh-CN.md docs/publishing.md docs/publishing.zh-CN.md
git commit -m "docs: add install smoke tests for continuity packages"
```

### Task 5: Audit Package Contract Clarity

**Files:**
- Modify if needed: `skills/skill-context-keeper/README.md`
- Modify if needed: `skills/skill-context-keeper/README.zh-CN.md`
- Modify if needed: `skills/skill-phase-gate/README.md`
- Modify if needed: `skills/skill-phase-gate/README.zh-CN.md`
- Modify if needed: `skills/skill-handoff-summary/README.md`
- Modify if needed: `skills/skill-handoff-summary/README.zh-CN.md`
- Modify if needed: `skills/skill-task-continuity/README.md`
- Modify if needed: `skills/skill-task-continuity/README.zh-CN.md`

- [ ] **Step 1: Audit the four package READMEs for release-facing clarity only**

Run:

```bash
sed -n '1,260p' skills/skill-context-keeper/README.md
sed -n '1,260p' skills/skill-phase-gate/README.md
sed -n '1,260p' skills/skill-handoff-summary/README.md
sed -n '1,320p' skills/skill-task-continuity/README.md
```

Look only for:
- contradictory ownership language
- duplicated responsibilities
- inconsistent install wording
- missing references to downstream templates or assets where users would need them
- broken or missing cross-links

- [ ] **Step 2: Write the failing contract mentally**

Package docs should satisfy:

```text
1. Context keeper = state only.
2. Phase gate = checkpoints only.
3. Handoff summary = handoff only.
4. Task continuity = suite bootstrap/composition only.
5. Install wording is parallel across packages.
6. Downstream template references are clear where relevant.
```

Expected:
- If any package violates one of the six points, it needs a minimal fix

- [ ] **Step 3: Apply only the real fixes**

Do not rewrite for style.
Touch only the package README files that have a concrete release-facing issue.

- [ ] **Step 4: Re-run package contract tests**

Run:

```bash
python3 -m unittest discover -s skills/skill-context-keeper/tests -p 'test_*.py' -v
python3 -m unittest discover -s skills/skill-phase-gate/tests -p 'test_*.py' -v
python3 -m unittest discover -s skills/skill-handoff-summary/tests -p 'test_*.py' -v
python3 -m unittest discover -s skills/skill-task-continuity/tests -p 'test_*.py' -v
```

Expected:
- All package contract tests pass

- [ ] **Step 5: Commit any package clarity fixes**

```bash
git add skills/skill-context-keeper/README.md skills/skill-context-keeper/README.zh-CN.md skills/skill-phase-gate/README.md skills/skill-phase-gate/README.zh-CN.md skills/skill-handoff-summary/README.md skills/skill-handoff-summary/README.zh-CN.md skills/skill-task-continuity/README.md skills/skill-task-continuity/README.zh-CN.md
git commit -m "docs: tighten continuity package release guidance"
```

### Task 6: Final Verification And Release Notes Synthesis

**Files:**
- Verify: `.github/workflows/pull-request-checks.yml`
- Verify: `docs/release-checklist-long-task-suite.md`
- Verify: `docs/release-checklist-long-task-suite.zh-CN.md`
- Verify: `docs/publishing.md`
- Verify: `docs/publishing.zh-CN.md`
- Verify: `CHANGELOG.md`

- [ ] **Step 1: Run the full verification set**

```bash
(cd skills/skill-governance && python3 scripts/manage_skill.py --validate-only)
for test_dir in skills/*/tests; do
  python3 -m unittest discover -s "$test_dir" -p 'test_*.py' -v
done
python3 -m unittest discover -s evals -p 'test_*.py' -v
python3 evals/run_evals.py
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py --repo Golden-Promise/codex-skill-library --path skills/skill-task-continuity --ref <branch-name> --dest "$(mktemp -d)"
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py --repo Golden-Promise/codex-skill-library --path skills/skill-task-continuity --ref v0.6.0 --dest "$(mktemp -d)"
git status --short
```

Expected:
- All tests pass
- `evals/run_evals.py` reports the full seed matrix passing
- Smoke-test commands are either executed against reachable GitHub refs or called out explicitly as pending if the branch/tag is not yet published
- The worktree is clean after final commits

- [ ] **Step 2: Gather release-note inputs**

Use the edited docs plus `CHANGELOG.md` to prepare:

```text
Proposed version: v0.6.0
Draft PR title: release: publish long-task continuity suite
Draft release title: v0.6.0 - long-task continuity suite
```

PR / release bullets should mention:
- the long-task reliability problem they solve: state drift, workflow drift, and handoff friction
- four new published packages
- downstream install paths under `skills/`
- maintainer release-checklist and smoke-test flow
- CI coverage for package contracts and eval contracts
- eval harness strictness around routing docs, event tokens, and guardrail metadata

- [ ] **Step 2.5: Draft the full PR and release text**

Prepare:

```text
- Draft PR description with summary, validation, and maintainer notes
- Draft GitHub release notes body with install guidance and eval-contract notes
```

- [ ] **Step 3: Commit any final doc or workflow touch-ups**

```bash
git add .github/workflows/pull-request-checks.yml docs/release-checklist-long-task-suite.md docs/release-checklist-long-task-suite.zh-CN.md docs/publishing.md docs/publishing.zh-CN.md README.md README.zh-CN.md skills/README.md skills/README.zh-CN.md CHANGELOG.md
git commit -m "docs: finalize long-task suite release readiness"
```

- [ ] **Step 4: Prepare the final release-readiness report**

The final handoff back to the human should include:
- changed files
- CI workflow added
- checklist docs added
- proposed next version `v0.6.0`
- draft PR title and description
- draft GitHub release title and notes
- blockers, if any
- non-blocking follow-up suggestions, if any
