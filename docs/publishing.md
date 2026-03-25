# Publishing codex-skill-library

[简体中文](publishing.zh-CN.md)

This guide covers repository-level publishing, release, and versioning for `codex-skill-library`.

## Who This Guide Is For

Use this guide if you are maintaining the repository itself rather than using one skill package as a reader.

## Release Goals

- keep install paths stable for `skill-installer`
- keep repository docs clean and easy to read
- keep package runtime docs separate from repository release notes

## Recommended Release Flow

1. Review the package README files, repository indexes, and publishing docs for release clarity.
2. Update [CHANGELOG.md](../CHANGELOG.md) with reader-visible changes and confirm the intended tag for this release.
3. Run local package tests, eval tests, and the continuity seed matrix before opening or merging the PR.
4. Let the PR checks workflow confirm the same core package and eval contracts.
5. Run install smoke tests from a pushed release branch or from `main` before tagging.
6. Create the release tag and GitHub Release once the branch is merge-ready.
7. Re-run the smoke tests against the tagged release and record any follow-up.

## Validation Commands

Repository package tests:

```bash
for test_dir in skills/*/tests; do
  python3 -m unittest discover -s "$test_dir" -p 'test_*.py' -v
done
```

Additional packaging sanity for `skill-governance`:

```bash
(cd skills/skill-governance && python3 scripts/manage_skill.py --validate-only)
```

Long-task continuity suite validation:

```bash
python3 -m unittest discover -s evals -p 'test_*.py' -v
python3 evals/run_evals.py
```

The suite runner now scores prompt polarity, event namespaces, and strict artifact mapping in addition to repository shape checks.
Routing quality also requires trigger guidance to remain visible in published `SKILL.md` and README files, and guardrail metadata is validated statically when optional columns are present.

## Pull Request Checks

Pull requests should run [.github/workflows/pull-request-checks.yml](../.github/workflows/pull-request-checks.yml).
That workflow is intentionally small: it runs package test directories under `skills/*/tests`, then the continuity eval unit tests, then the continuity seed matrix.

## Versioning Rules

- Use repository-level tags such as `v0.1.0`, `v0.2.0`, and `v1.0.0`.
- Increase the minor version for backward-compatible additions.
- Increase the major version when package layout or workflow changes in a breaking way.
- Keep `skills/skill-governance` stable as the public install path.
- For the current long-task continuity publication pass, the expected next minor release is `v0.6.0` unless other user-visible scope lands first.

## Install Smoke Tests For The Continuity Packages

If you want to smoke-test a pushed but untagged release branch, add `--ref <branch-name>` and point the installer at an isolated temp directory:

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

If you want to smoke-test the current `main`, use the same loop without `--ref`:

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

Repeat the same smoke tests against the release tag after publishing:

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
    --ref v0.6.0 \
    --dest "$tmpdir"
done
```

If you want to inspect the public package page directly, use a GitHub tree URL such as:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --url https://github.com/Golden-Promise/codex-skill-library/tree/main/skills/skill-task-continuity
```

## Release Checklist

Use [docs/release-checklist-long-task-suite.md](release-checklist-long-task-suite.md) for the full continuity-suite release checklist, including tag creation, GitHub release steps, and post-release smoke verification.

## Maintainer Notes

- Keep repository-wide guidance in the root `README.md` and `docs/`.
- Keep runtime guidance inside the skill package itself.
- Keep static suite checks in `evals/` so maintainers can validate trigger coverage, package boundaries, event namespaces, and artifact mapping without executing a model.
- Treat `max_commands` as a positive integer contract and `max_verbosity` as a `low` / `medium` / `high` metadata check when those columns appear in `evals/cases.csv`.
- Prefer bilingual key docs when the repository is meant for public sharing.
