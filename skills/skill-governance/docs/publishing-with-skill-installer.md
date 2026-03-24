# Publishing With Skill Installer

Chinese version: [publishing-with-skill-installer.zh-CN.md](publishing-with-skill-installer.zh-CN.md)

This document is for maintainers publishing the `skill-governance` package itself.
It is intentionally kept outside `references/` so it does not look like a runtime skill guide.

## Who This Is For

Use this guide if you are packaging or releasing `skill-governance` as a public skill package.

## Goal

Publish this package to GitHub in a way that is easy to:

- read in a public repository
- install with `skill-installer`
- maintain without mixing release notes into runtime skill documentation

## Repository Layout In This Repo

This package is published inside the multi-skill repository `codex-skill-library`.

```text
repo-root/
  README.md
  LICENSE
  .gitignore
  CHANGELOG.md
  skills/
    README.md
    skill-governance/
      README.md
      SKILL.md
      docs/
      agents/
      scripts/
      references/
      tests/
```

Install it with:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-governance
```

If you want to pin the current release, use:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-governance \
  --ref v0.5.0
```

## Repository Files In This Repo

This repository already includes the root files needed for public distribution:

- Root `README.md`: [../../../README.md](../../../README.md)
- Root `LICENSE`: [../../../LICENSE](../../../LICENSE)
- Root `.gitignore`: [../../../.gitignore](../../../.gitignore)
- Root `CHANGELOG.md`: [../../../CHANGELOG.md](../../../CHANGELOG.md)
- `skills/README.md`: [../../README.md](../../README.md)

## Versioning

This package does not require a separate runtime version field inside `SKILL.md`.
For public distribution, version the repository itself:

- use Git tags such as `v0.1.0`, `v0.2.0`, `v1.0.0`
- record user-visible changes in `CHANGELOG.md`
- keep the install path stable, for example `skills/skill-governance`
- publish GitHub Releases when you want a clear downloadable milestone

Recommended release rhythm:

- start with `v0.1.0` for the first public release
- increment minor versions for compatible feature additions
- increment major versions when the workflow or file layout changes in a breaking way

## Release Checklist

- `SKILL.md` frontmatter `name` matches the directory name and uses hyphen-case.
- `agents/openai.yaml` contains `display_name`, `short_description`, and `default_prompt`.
- `references/` only contains runtime reader guides, not repository release notes.
- Repository-level docs such as `README.md` and `docs/` explain installation and publishing.
- Repository root files such as `CHANGELOG.md`, `LICENSE`, and `.gitignore` are present if you publish as a multi-skill repository.
- Remove `__pycache__/`, `.pyc`, and editor-generated junk before release.
- Run:

```bash
python3 scripts/manage_skill.py --validate-only
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## GitHub Tree URL Example

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --url https://github.com/Golden-Promise/codex-skill-library/tree/main/skills/skill-governance
```
