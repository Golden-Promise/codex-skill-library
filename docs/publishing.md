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

1. Review the package README and repository docs for clarity.
2. Update [CHANGELOG.md](../CHANGELOG.md) with reader-visible changes.
3. Run validation and tests inside each published skill package.
4. Commit the release state and create a Git tag such as `v0.1.0`.
5. Push the tag and optionally create a GitHub Release.
6. Verify installation from GitHub with a real `skill-installer` command.

## Validation Commands

Current package validation:

```bash
cd skills/skill-workflow-manager
python3 scripts/manage_skill.py --validate-only
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## Versioning Rules

- Use repository-level tags such as `v0.1.0`, `v0.2.0`, and `v1.0.0`.
- Increase the minor version for backward-compatible additions.
- Increase the major version when package layout or workflow changes in a breaking way.
- Keep `skills/skill-workflow-manager` stable as the public install path.

## Install Verification

Verify installation from the repository path:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo <owner>/codex-skill-library \
  --path skills/skill-workflow-manager
```

Verify installation from a GitHub tree URL:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --url https://github.com/<owner>/codex-skill-library/tree/main/skills/skill-workflow-manager
```

## Maintainer Notes

- Keep repository-wide guidance in the root `README.md` and `docs/`.
- Keep runtime guidance inside the skill package itself.
- Prefer bilingual key docs when the repository is meant for public sharing.
