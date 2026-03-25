# Long-Task Continuity Suite Release Checklist

[简体中文](release-checklist-long-task-suite.zh-CN.md)

Use this checklist when preparing the long-task continuity suite for merge, tag creation, and GitHub release publication.

## 1. Pre-Release Sanity

- Confirm the worktree is clean: `git status --short`
- Confirm the release target is still `v0.6.1`; if more user-visible scope landed, recalculate before tagging.
- Re-read the repository entry docs and indexes:
  - [README.md](../README.md)
  - [README.zh-CN.md](../README.zh-CN.md)
  - [skills/README.md](../skills/README.md)
  - [skills/README.zh-CN.md](../skills/README.zh-CN.md)
- Confirm [CHANGELOG.md](../CHANGELOG.md) matches the release scope and does not describe unfinished work.

## 2. Local Validation

Run all published package tests:

```bash
for test_dir in skills/*/tests; do
  python3 -m unittest discover -s "$test_dir" -p 'test_*.py' -v
done
```

Run the additional `skill-governance` packaging sanity check:

```bash
(cd skills/skill-governance && python3 scripts/manage_skill.py --validate-only)
```

Run the continuity eval checks:

```bash
python3 -m unittest discover -s evals -p 'test_*.py' -v
python3 evals/run_evals.py
```

## 3. Docs And Index Verification

- Confirm all four continuity packages are still discoverable from the root and `skills/` indexes.
- Confirm package descriptions remain non-overlapping:
  - `skill-context-keeper` = state refresh only
  - `skill-phase-gate` = checkpoint only
  - `skill-handoff-summary` = handoff only
  - `skill-task-continuity` = suite bootstrap and composition only
- Confirm package `README.md` install sections still point to the published `skills/<skill-name>/` paths.
- Confirm the publishing guides still link to this checklist and to the continuity smoke-test commands.

## 4. Install Smoke Tests From A Pushed Branch Or `main`

If the release branch is already pushed to GitHub, smoke-test that exact ref before the tag exists:

```bash
tmpdir="$(mktemp -d)"

for path in \
  skills/skill-context-keeper \
  skills/skill-phase-gate \
  skills/skill-handoff-summary \
  skills/skill-task-continuity
do
  python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
    --repo Golden-Promise/codex-skill-library \
    --path "$path" \
    --ref <branch-name> \
    --dest "$tmpdir"
done
```

If you want to verify the current `main`, repeat the same loop without `--ref`:

```bash
tmpdir="$(mktemp -d)"

for path in \
  skills/skill-context-keeper \
  skills/skill-phase-gate \
  skills/skill-handoff-summary \
  skills/skill-task-continuity
do
  python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
    --repo Golden-Promise/codex-skill-library \
    --path "$path" \
    --dest "$tmpdir"
done
```

## 5. PR Readiness

- Open or update the draft PR.
- Confirm `.github/workflows/pull-request-checks.yml` runs successfully on the PR.
- Confirm the proposed PR title and summary still match the actual release contents.

## 6. Changelog And Version Confirmation

- Confirm the next release is still `v0.6.1`.
- Confirm pinned install examples that reference a tag use `v0.6.1`.
- Confirm `CHANGELOG.md` is ready to ship with minimal or no editing.

## 7. Tag And GitHub Release

- Merge the release PR.
- Create the tag:

```bash
git tag v0.6.1
git push origin v0.6.1
```

- Create the GitHub Release using the prepared release notes draft.

## 8. Post-Release Tagged Smoke Verification

Repeat the continuity install smoke tests against the published tag:

```bash
tmpdir="$(mktemp -d)"

for path in \
  skills/skill-context-keeper \
  skills/skill-phase-gate \
  skills/skill-handoff-summary \
  skills/skill-task-continuity
do
  python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
    --repo Golden-Promise/codex-skill-library \
    --path "$path" \
    --ref v0.6.1 \
    --dest "$tmpdir"
done
```

- Confirm the tagged installs resolve to the expected package paths.
- Confirm the public GitHub release page points readers to the four published package directories under `skills/`.
