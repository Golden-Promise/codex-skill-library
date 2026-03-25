# Changelog

All notable changes to `codex-skill-library` should be documented in this file.

## [Unreleased]

### Added

- Publish four long-task continuity packages under `skills/`: `skill-context-keeper`, `skill-phase-gate`, `skill-handoff-summary`, and `skill-task-continuity`.
- Add bilingual package entry docs, routing-first `SKILL.md` files, OpenAI agent metadata, reader-facing references, downstream template assets, and package contract tests for the new continuity packages.
- Add the continuity-suite bootstrap helper and downstream template set for `AGENTS.md` plus `.agent-state/*.md` files without turning the repository root into a consumer repo.
- Add `docs/long-task-suite.md` and `docs/long-task-suite.zh-CN.md` so maintainers and readers can understand the suite architecture without opening package internals.
- Add a static continuity eval harness under `evals/` with seed cases, per-package artifact checks, routing checks, exact workflow-token checks, and optional guardrail metadata validation.
- Add a pull-request workflow for published package tests plus continuity eval checks.
- Add bilingual release checklist guidance for the continuity-suite publication flow.

### Changed

- Update root docs, skills indexes, and publishing guides so all four continuity packages are discoverable, install guidance stays aligned with `skill-installer`, and maintainers can find smoke-test and release-checklist steps quickly.
- Move command-heavy install examples out of the repository root README and keep package-level install guidance closer to the published package entry points.
- Polish the four continuity package READMEs so they read more like package landing pages, stay friendlier for first-time readers, and preserve strict package boundaries.
- Keep pinned install guidance aligned to the upcoming `v0.6.1` release after withdrawing the original `v0.6.0` tag.
- Treat the continuity eval contract as a release-facing surface: routing now depends on published trigger guidance, workflow tokens must match exact package and polarity contracts, and optional guardrail metadata must be valid when present.

## [0.5.1] - 2026-03-25

### Changed

- Polish the published `skill-governance` docs so the package README reads more like a GitHub landing page, the `use-cases` pages read more like command references, and runtime metadata stays aligned with the public package voice.
- Add natural-language install examples to the package README for both the latest install path and a pinned `ref`.
- Add missing `upgrade` and `retire` command examples to the reference pages and tighten prompt-template naming across the package docs.

## [0.5.0] - 2026-03-24

### Added

- Add `manage` as a higher-level project take-over task that inspects a project directory, discovers local skill packages, adopts them into managed storage, and builds the project structure.
- Add `setup` as a quick project bootstrap task for creating the project-owned library, exposure root, and platform state layout.
- Add regression coverage for the new `manage` and `setup` task flows.

### Changed

- Rewrite package quick-start guidance around natural-language, task-first project onboarding instead of command-first onboarding.
- Update the skill entry point, task guide, and prompt templates to prioritize `manage` and `setup` for new users.
- Make `setup` and `manage` default to project-local `.skill-platform` state when no explicit platform root is configured.

## [0.4.1] - 2026-03-24

### Fixed

- Replace published repository placeholders with the real GitHub location `Golden-Promise/codex-skill-library` in repository docs, package docs, and publishing guides.
- Update fixed-version install examples from `v0.4.0` to `v0.4.1` for the next patch release.
- Remove the `TODO: replace ...` style placeholder from generated skill description guidance so new packages start from a cleaner default.

## [0.4.0] - 2026-03-24

### Added

- Add a first extracted module layer under `scripts/skill_governance/` for config, constants, registry payloads, version parsing, and audit rules.
- Add stronger governance metadata checks for `owner`, `reviewer`, `team`, and `version` in `audit`.
- Add lightweight version governance with normalized `version_info`, prerelease detection, and version regression checks.
- Add CLI metadata flags such as `--owner`, `--reviewer`, `--team`, `--version`, `--lifecycle-status`, and `--deprecation-policy`.

### Changed

- Persist governance metadata overrides through task flows such as `add`, `enable`, and `upgrade` so the central registry reflects task-time decisions.
- Include version change summaries in upgrade and retire impact reporting.
- Expand regression coverage for audit rules, registry version metadata, bootstrap with extracted modules, and read-only command behavior.

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
