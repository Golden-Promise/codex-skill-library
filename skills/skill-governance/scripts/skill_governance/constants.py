"""Shared constants for the skill-governance CLI."""

from __future__ import annotations

DEFAULT_LIBRARY_ENV = "CODEX_SKILL_LIBRARY_ROOT"
DEFAULT_COMPAT_ENV = "CODEX_SKILL_COMPAT_ROOT"
DEFAULT_LIBRARY_DIRNAME = "_skill-library"
DEFAULT_PLATFORM_DIRNAME = ".skill-platform"
EXTERNAL_SOURCE_REGISTRY_DIRNAME = "skill-governance"
EXTERNAL_SOURCE_REGISTRY_FILENAME = "external-sources.json"
MANAGED_EXPOSURE_REGISTRY_FILENAME = "managed-exposures.json"
EXPOSURE_MANIFEST_FILENAME = "skills-manifest.json"
PLATFORM_REGISTRY_FILENAME = "registry.json"
PLATFORM_DEPENDENCY_GRAPH_FILENAME = "dependency-graph.json"
DEFAULT_CONFIG_FILENAMES = (
    "skill-governance.toml",
    ".skill-governance.toml",
    "skill-workflow.toml",
    ".skill-workflow.toml",
)
ALLOWED_EXPOSURE_MODES = {"auto", "symlink", "copy", "manifest"}
ALLOWED_LIFECYCLE_STATUSES = {
    "draft",
    "review",
    "active",
    "deprecated",
    "archived",
    "blocked",
}
MAX_NAME_LENGTH = 64
ALLOWED_RESOURCES = {"scripts", "references", "assets"}
DOCUMENT_SECTION_TITLES = (
    "Purpose",
    "Use This Skill When",
    "Do Not Use This Skill When",
    "Inputs / Outputs",
    "Workflow",
    "Example Requests",
    "Risks / Boundaries",
)
PLACEHOLDER_DESCRIPTION = (
    "TODO: replace with a precise description of what this skill does and when to use it."
)
SKILL_TEXT_STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "before",
    "by",
    "codex",
    "do",
    "for",
    "from",
    "help",
    "in",
    "into",
    "is",
    "it",
    "its",
    "manage",
    "of",
    "on",
    "or",
    "project",
    "skill",
    "tasks",
    "task",
    "that",
    "the",
    "this",
    "to",
    "use",
    "user",
    "wants",
    "when",
    "with",
    "workflow",
    "workflows",
}
SEMANTIC_TOKEN_ALIASES = {
    "analysis": "analyze",
    "analyze": "analyze",
    "assistant": "assistant",
    "assist": "assistant",
    "bug": "issue",
    "bugs": "issue",
    "check": "diagnose",
    "checker": "diagnose",
    "checking": "diagnose",
    "docs": "documentation",
    "documentation": "documentation",
    "document": "documentation",
    "documents": "documentation",
    "error": "issue",
    "errors": "issue",
    "excel": "spreadsheet",
    "helper": "assistant",
    "inspect": "diagnose",
    "inspection": "diagnose",
    "issue": "issue",
    "issues": "issue",
    "readme": "documentation",
    "sheet": "spreadsheet",
    "sheets": "spreadsheet",
    "spreadsheet": "spreadsheet",
    "spreadsheets": "spreadsheet",
    "troubleshoot": "diagnose",
    "troubleshooting": "diagnose",
    "workbook": "spreadsheet",
    "workbooks": "spreadsheet",
}
ACTIVE_PROJECT_LINK_STATUSES = {"managed symlink", "managed copy", "managed manifest"}
GOVERNANCE_REVIEW_ACTION_TYPES = {
    "resolve-duplicate-canonical",
    "improve-skill-docs",
    "review-overlap",
    "consider-retire-candidate",
}

