# Changelog

All notable changes to `codex-skill-library` should be documented in this file.

## [0.3.0] - 2026-03-24

### Changed

- Rename `skill-workflow-manager` to `skill-governance`.
- Rewrite package READMEs and reader guides around task-first skill asset governance.
- Update install paths, package indexes, and publishing guides to the new package name.
- Support `skill-governance.toml` as the preferred repo config filename while keeping `skill-workflow.toml` compatible.

## [0.2.0] - 2026-03-24

Usability release for `skill-workflow-manager`.

### Added

- Add `--doctor` / `--check` as a read-only health check for shared skills, adoption candidates, and project links.
- Add `--adopt` as a task-first alias for importing a downloaded local skill into the shared library.
- Add regression coverage for doctor edge cases including missing targets, broken symlinks, and blocked project-link paths.

### Changed

- Reposition `skill-workflow-manager` around the default shared library at `$CODEX_HOME/skills`.
- Rewrite package guides around 3 main paths: create or refresh, adopt, and attach.
- Add quick-start and symlink/platform guidance to the package README and align repository entry docs with the new model.

## [0.1.1] - 2026-03-23

Patch release for `skill-workflow-manager`.

### Fixed

- Fix bootstrap cleanup so adopting a standalone in-project `skill-workflow-manager` no longer leaves a duplicate source directory behind.
- Add regression coverage for bootstrap cleanup scenarios, including the case where the canonical copy already exists.

## [0.1.0] - 2026-03-23

First public release of `codex-skill-library`.

### Added

- Publish `skill-workflow-manager` as the first installable package under `skills/skill-workflow-manager`.
- Add bilingual repository guides, package READMEs, and publishing documentation.
- Add repository-level release files including `LICENSE`, `.gitignore`, and version tracking through `CHANGELOG.md`.
- Include validation and automated tests for the initial published package.
