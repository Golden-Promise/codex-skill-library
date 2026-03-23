# Changelog

All notable changes to `codex-skill-library` should be documented in this file.

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
