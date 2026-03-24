#!/usr/bin/env python3

"""Govern Codex skills through task-first add, enable, repair, and audit flows."""

from __future__ import annotations

import argparse
import ast
import difflib
import json
import math
import os
import re
import shlex
import shutil
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

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
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
TOKEN_RE = re.compile(r"[a-z0-9]+")
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


class UsageError(Exception):
    pass


@dataclass
class WorkflowConfig:
    path: Path | None
    shared_root: Path | None
    project_library_root: Path | None
    exposure_root: Path | None
    exposure_mode: str | None
    workspace_root: Path | None
    platform_root: Path | None


@dataclass
class ExecutionContext:
    args: argparse.Namespace
    runtime_skill_dir: Path
    config: WorkflowConfig
    platform_root: Path
    workspace_root: Path | None
    project_root: Path | None
    import_path: Path | None
    skill_name: str
    library_root: Path
    compat_root: Path | None
    exposure_root: Path | None
    exposure_mode: str
    resources: list[str]
    project_skills: list[str]
    unlink_skills: list[str]
    sync_project_skills: list[str]
    effective_bootstrap_project_layout: bool
    project_root_inferred_from_cwd: bool
    kept_existing_canonical: bool
    report_compat_root: bool
    bootstrap_cleanup_source: Path | None


def normalize_skill_name(raw_name: str) -> str:
    normalized = raw_name.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    normalized = re.sub(r"-{2,}", "-", normalized)
    return normalized


def title_case_skill_name(skill_name: str) -> str:
    return " ".join(word.capitalize() for word in skill_name.split("-"))


def default_short_description(display_name: str) -> str:
    candidates = [
        f"Manage {display_name} workflows",
        f"Support {display_name} workflow tasks",
        f"{display_name} workflow support",
    ]
    for candidate in candidates:
        if 25 <= len(candidate) <= 64:
            return candidate
    fallback = candidates[-1]
    if len(fallback) < 25:
        fallback = f"{display_name} task workflow support"
    return fallback[:64].rstrip()


def default_prompt_text(skill_name: str, display_name: str) -> str:
    return f"Use ${skill_name} to help with {display_name.lower()} workflows."


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{escaped}"'


def emit_json(payload: dict) -> int:
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def parse_simple_scalar(raw: str) -> str:
    raw = raw.strip()
    if not raw:
        return ""
    if raw[0] in {'"', "'"}:
        try:
            return str(ast.literal_eval(raw))
        except Exception:
            return raw.strip("\"'")
    return raw


def parse_skill_list(raw_value: str | None) -> list[str]:
    if not raw_value:
        return []
    result = []
    seen = set()
    for item in raw_value.split(","):
        normalized = normalize_skill_name(item)
        if not normalized or normalized in seen:
            continue
        result.append(normalized)
        seen.add(normalized)
    return result


def parse_resource_list(raw_value: str | None) -> list[str]:
    if not raw_value:
        return []
    resources = []
    seen = set()
    for item in raw_value.split(","):
        resource = item.strip()
        if not resource:
            continue
        if resource not in ALLOWED_RESOURCES:
            allowed = ", ".join(sorted(ALLOWED_RESOURCES))
            raise ValueError(f"Unknown resource '{resource}'. Allowed: {allowed}")
        if resource not in seen:
            resources.append(resource)
            seen.add(resource)
    return resources


def detect_runtime_skill_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def looks_like_path_argument(raw_value: str) -> bool:
    raw = raw_value.strip()
    if not raw:
        return False
    if raw.startswith((".", "~", "/", "..")):
        return True
    return os.sep in raw or Path(raw).exists()


def normalize_cli_args(argv: list[str]) -> list[str]:
    if not argv:
        return argv

    task = argv[0]
    if task not in {"add", "enable", "doctor", "audit", "document", "upgrade", "retire", "repair"}:
        return argv

    rest = list(argv[1:])
    rewritten = ["--task-kind", task]

    if task in {"add", "upgrade", "doctor", "document"}:
        if rest and not rest[0].startswith("-"):
            target = rest.pop(0)
            if looks_like_path_argument(target):
                rewritten.extend(["--adopt", target])
            else:
                rewritten.append(target)

    if task == "add" or task == "upgrade":
        return rewritten + rest
    if task == "enable":
        if not rest or rest[0].startswith("-"):
            raise UsageError("[ERROR] enable requires a skill name, for example: manage_skill.py enable demo-skill --project-root <project-root>")
        skill_name = rest.pop(0)
        return rewritten + ["--project-skills", skill_name] + rest
    if task == "retire":
        if not rest or rest[0].startswith("-"):
            raise UsageError("[ERROR] retire requires a skill name, for example: manage_skill.py retire demo-skill --project-root <project-root>")
        skill_name = rest.pop(0)
        return rewritten + ["--unlink-skills", skill_name] + rest
    if task == "repair":
        if not rest or rest[0].startswith("-"):
            raise UsageError("[ERROR] repair requires a skill name, for example: manage_skill.py repair demo-skill --workspace-root <workspace-root>")
        skill_name = rest.pop(0)
        return rewritten + [skill_name] + rest
    if task == "document":
        return rewritten + rest
    if task == "audit":
        return rewritten + rest + ["--audit"]
    return rewritten + rest + ["--doctor"]


def resolve_configured_path(raw_value: object, config_dir: Path) -> Path | None:
    if raw_value is None:
        return None
    if not isinstance(raw_value, str) or not raw_value.strip():
        raise UsageError("[ERROR] skill_registry paths in the config file must be non-empty strings.")
    candidate = Path(raw_value).expanduser()
    if not candidate.is_absolute():
        candidate = (config_dir / candidate).resolve()
    else:
        candidate = candidate.resolve()
    return candidate


def discover_workflow_config_path(
    explicit_path: str | None,
    project_root: Path | None,
) -> Path | None:
    if explicit_path:
        return Path(explicit_path).expanduser().resolve()
    if project_root is None:
        return None
    for filename in DEFAULT_CONFIG_FILENAMES:
        candidate = project_root / filename
        if candidate.exists():
            return candidate.resolve()
    return None


def load_workflow_config(config_path: Path | None) -> WorkflowConfig:
    if config_path is None:
        return WorkflowConfig(None, None, None, None, None, None, None)
    if not config_path.exists():
        raise UsageError(f"[ERROR] Config file does not exist: {config_path}")
    try:
        data = tomllib.loads(config_path.read_text())
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise UsageError(f"[ERROR] Could not parse config file {config_path}: {error}") from error

    registry = data.get("skill_registry")
    if registry is None:
        return WorkflowConfig(config_path, None, None, None, None, None, None)
    if not isinstance(registry, dict):
        raise UsageError("[ERROR] [skill_registry] in the config file must be a table.")

    config_dir = config_path.parent
    exposure_mode = registry.get("exposure_mode")
    if exposure_mode is not None:
        if not isinstance(exposure_mode, str) or exposure_mode not in ALLOWED_EXPOSURE_MODES:
            allowed = ", ".join(sorted(ALLOWED_EXPOSURE_MODES))
            raise UsageError(
                f"[ERROR] skill_registry.exposure_mode must be one of: {allowed}."
            )

    return WorkflowConfig(
        path=config_path,
        shared_root=resolve_configured_path(registry.get("shared_root"), config_dir),
        project_library_root=resolve_configured_path(registry.get("project_root"), config_dir),
        exposure_root=resolve_configured_path(registry.get("exposure_root"), config_dir),
        exposure_mode=exposure_mode,
        workspace_root=resolve_configured_path(registry.get("workspace_root"), config_dir),
        platform_root=resolve_configured_path(registry.get("platform_root"), config_dir),
    )


def detect_library_root(
    explicit_root: str | None,
    config: WorkflowConfig,
    project_root: Path | None = None,
    bootstrap_project_layout: bool = False,
    prefer_project_library: bool = False,
) -> Path:
    if explicit_root:
        return Path(explicit_root).expanduser().resolve()
    env_root = os.environ.get(DEFAULT_LIBRARY_ENV)
    if env_root:
        return Path(env_root).expanduser().resolve()
    if (bootstrap_project_layout or prefer_project_library) and config.project_library_root:
        return config.project_library_root
    if (bootstrap_project_layout or prefer_project_library) and project_root is not None:
        return (project_root / DEFAULT_LIBRARY_DIRNAME).resolve()
    if config.shared_root:
        return config.shared_root
    return Path(__file__).resolve().parents[2]


def detect_compat_root(
    explicit_root: str | None,
    library_root: Path,
    allow_default: bool,
) -> Path | None:
    if explicit_root:
        return Path(explicit_root).expanduser().resolve()
    env_root = os.environ.get(DEFAULT_COMPAT_ENV)
    if env_root:
        return Path(env_root).expanduser().resolve()
    if not allow_default:
        return None
    candidate = library_root.parent
    if (candidate / ".agents" / "skills").exists():
        return candidate
    return None


def detect_exposure_root(
    explicit_root: str | None,
    config: WorkflowConfig,
    project_root: Path | None,
) -> Path | None:
    if explicit_root:
        return Path(explicit_root).expanduser().resolve()
    if config.exposure_root:
        return config.exposure_root
    if project_root is None:
        return None
    return (project_root / ".agents" / "skills").resolve()


def resolve_exposure_mode(
    requested_mode: str | None,
    config: WorkflowConfig,
) -> str:
    mode = requested_mode or config.exposure_mode or "auto"
    if mode not in ALLOWED_EXPOSURE_MODES:
        allowed = ", ".join(sorted(ALLOWED_EXPOSURE_MODES))
        raise UsageError(f"[ERROR] Exposure mode must be one of: {allowed}.")
    if mode != "auto":
        return mode
    if os.environ.get("CI") or os.name == "nt":
        return "manifest" if os.environ.get("CI") else "copy"
    return "symlink"


def detect_workspace_root(
    explicit_root: str | None,
    config: WorkflowConfig,
    project_root: Path | None,
) -> Path | None:
    if explicit_root:
        return Path(explicit_root).expanduser().resolve()
    if config.workspace_root:
        return config.workspace_root
    if project_root is not None:
        return project_root.parent.resolve()
    return None


def detect_platform_root(
    explicit_root: str | None,
    config: WorkflowConfig,
    workspace_root: Path | None,
    project_root: Path | None,
    library_root: Path,
) -> Path:
    if explicit_root:
        return Path(explicit_root).expanduser().resolve()
    if config.platform_root:
        return config.platform_root
    if workspace_root is not None:
        return (workspace_root / DEFAULT_PLATFORM_DIRNAME).resolve()
    if project_root is not None:
        return (project_root / DEFAULT_PLATFORM_DIRNAME).resolve()
    return (library_root.parent / DEFAULT_PLATFORM_DIRNAME).resolve()


def infer_project_root_for_bootstrap(
    import_path: Path | None,
    runtime_skill_dir: Path,
) -> Path | None:
    for candidate in (import_path, runtime_skill_dir):
        if candidate is None or not (candidate / "SKILL.md").exists():
            continue
        parent = candidate.parent
        if parent.name == DEFAULT_LIBRARY_DIRNAME:
            return parent.parent.resolve()
        return parent.resolve()
    return None


def path_is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def looks_like_skill_dir(path: Path) -> bool:
    return (path / "SKILL.md").exists() and (path / "agents" / "openai.yaml").exists()


def find_nearest_project_root(start: Path) -> Path:
    candidate = start.resolve()
    for current in (candidate, *candidate.parents):
        if (
            (current / ".git").exists()
            or (current / ".agents").exists()
            or (current / DEFAULT_LIBRARY_DIRNAME).exists()
        ):
            return current
    return candidate


def infer_project_root_from_cwd(
    import_path: Path | None,
    runtime_skill_dir: Path,
    allow_without_import: bool = False,
) -> Path | None:
    if import_path is None and not allow_without_import:
        return None
    cwd = Path.cwd().resolve()
    candidate_sources = [runtime_skill_dir.resolve()]
    if import_path is not None:
        candidate_sources.insert(0, import_path.resolve())
    for source_dir in candidate_sources:
        if cwd == source_dir or path_is_within(cwd, source_dir):
            return None
    if looks_like_skill_dir(cwd):
        return None
    return find_nearest_project_root(cwd)


def sync_imported_skill_tree(
    source_dir: Path,
    target_dir: Path,
    mode: str,
    dry_run: bool,
) -> str:
    if not source_dir.exists():
        raise FileNotFoundError(f"Import source does not exist: {source_dir}")
    if not source_dir.is_dir():
        raise NotADirectoryError(f"Import source is not a directory: {source_dir}")
    if not target_dir.exists():
        raise FileNotFoundError(
            f"Cannot upgrade missing canonical skill: {target_dir}. Use add instead."
        )

    source_resolved = source_dir.resolve()
    target_resolved = target_dir.resolve(strict=False)
    if source_resolved == target_resolved:
        return "kept"
    if path_is_within(source_resolved, target_resolved) or path_is_within(target_resolved, source_resolved):
        raise ValueError(
            "Upgrade source and canonical target cannot be nested inside one another."
        )

    if dry_run:
        return f"would refresh from {mode}"

    shutil.rmtree(target_dir)
    if mode == "copy":
        shutil.copytree(source_dir, target_dir, symlinks=True)
        return "refreshed from copy"
    if mode == "move":
        shutil.move(str(source_dir), str(target_dir))
        return "refreshed from move"
    raise ValueError(f"Unsupported import mode: {mode}")


def storage_decision_label(ctx: ExecutionContext) -> str:
    if ctx.project_root and ctx.library_root == (
        (ctx.config.project_library_root or (ctx.project_root / DEFAULT_LIBRARY_DIRNAME).resolve())
    ):
        return "project-owned"
    return "shared"


def primary_task_skill_name(ctx: ExecutionContext) -> str:
    if ctx.skill_name:
        return ctx.skill_name
    if ctx.args.task_kind == "enable" and len(ctx.project_skills) == 1:
        return ctx.project_skills[0]
    if ctx.args.task_kind == "retire" and len(ctx.unlink_skills) == 1:
        return ctx.unlink_skills[0]
    return ""


def external_source_registry_path(project_root: Path) -> Path:
    return (
        project_root
        / ".agents"
        / EXTERNAL_SOURCE_REGISTRY_DIRNAME
        / EXTERNAL_SOURCE_REGISTRY_FILENAME
    )


def managed_exposure_registry_path(exposure_root: Path) -> Path:
    return (
        exposure_root.parent
        / EXTERNAL_SOURCE_REGISTRY_DIRNAME
        / MANAGED_EXPOSURE_REGISTRY_FILENAME
    )


def exposure_manifest_path(exposure_root: Path) -> Path:
    return (
        exposure_root.parent
        / EXTERNAL_SOURCE_REGISTRY_DIRNAME
        / EXPOSURE_MANIFEST_FILENAME
    )


def load_external_source_registry(project_root: Path) -> dict[str, dict[str, str]]:
    path = external_source_registry_path(project_root)
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(data, dict):
        return {}
    normalized: dict[str, dict[str, str]] = {}
    for key, value in data.items():
        if not isinstance(key, str) or not isinstance(value, dict):
            continue
        normalized[key] = {
            inner_key: str(inner_value)
            for inner_key, inner_value in value.items()
            if isinstance(inner_key, str)
        }
    return normalized


def load_managed_exposure_registry(
    exposure_root: Path | None,
) -> dict[str, dict[str, str]]:
    if exposure_root is None:
        return {}
    path = managed_exposure_registry_path(exposure_root)
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(data, dict):
        return {}
    normalized: dict[str, dict[str, str]] = {}
    for key, value in data.items():
        if not isinstance(key, str) or not isinstance(value, dict):
            continue
        normalized[key] = {
            inner_key: str(inner_value)
            for inner_key, inner_value in value.items()
            if isinstance(inner_key, str)
        }
    return normalized


def write_managed_exposure_registry(
    exposure_root: Path | None,
    registry: dict[str, dict[str, str]],
    dry_run: bool,
) -> str:
    if exposure_root is None:
        return "kept"
    path = managed_exposure_registry_path(exposure_root)
    content = json.dumps(registry, indent=2, sort_keys=True) + "\n"
    return write_file(path, content, dry_run=dry_run)


def write_exposure_manifest(
    exposure_root: Path | None,
    registry: dict[str, dict[str, str]],
    dry_run: bool,
) -> str:
    if exposure_root is None:
        return "kept"
    manifest_entries: dict[str, dict[str, str]] = {}
    for skill_name, entry in sorted(registry.items()):
        manifest_entries[skill_name] = {
            "canonical_path": str(entry.get("canonical_path", "")),
            "exposure_path": str(entry.get("exposure_path", "")),
            "mode": str(entry.get("mode", "")),
        }
    content = json.dumps(
        {
            "schema_version": 1,
            "exposure_root": str(exposure_root),
            "skills": manifest_entries,
        },
        indent=2,
        sort_keys=True,
    ) + "\n"
    return write_file(exposure_manifest_path(exposure_root), content, dry_run=dry_run)


def record_external_source(
    project_root: Path,
    skill_name: str,
    source_dir: Path,
    canonical_dir: Path,
    import_mode: str,
    dry_run: bool,
) -> str:
    registry_path = external_source_registry_path(project_root)
    existing = load_external_source_registry(project_root)
    updated = dict(existing)
    updated[skill_name] = {
        "source_path": str(source_dir.resolve()),
        "canonical_path": str(canonical_dir.resolve()),
        "import_mode": import_mode,
    }
    content = json.dumps(updated, indent=2, sort_keys=True) + "\n"
    return write_file(registry_path, content, dry_run=dry_run)


def detect_skill_name_from_source(source_dir: Path) -> str:
    skill_md = source_dir / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text()
        frontmatter_name = extract_frontmatter_value(content, "name")
        if frontmatter_name:
            return normalize_skill_name(frontmatter_name)
    return normalize_skill_name(source_dir.name)


def suggest_available_skill_names(
    library_root: Path,
    base_name: str,
    limit: int = 4,
) -> list[str]:
    suggestions: list[str] = []
    seen = set()

    def add(candidate: str) -> None:
        normalized = normalize_skill_name(candidate)
        if not normalized or normalized in seen:
            return
        if not (library_root / normalized).exists():
            suggestions.append(normalized)
            seen.add(normalized)

    add(f"{base_name}-imported")
    add(f"{base_name}-local")
    add(f"{base_name}-copy")

    suffix = 2
    while len(suggestions) < limit:
        add(f"{base_name}-{suffix}")
        suffix += 1

    return suggestions[:limit]


def collect_skill_draft_context(
    skill_name: str,
    source_dir: Path | None,
    planned_resources: list[str] | None,
) -> dict[str, object]:
    source_resources = {
        resource
        for resource in sorted(ALLOWED_RESOURCES)
        if source_dir is not None and (source_dir / resource).exists()
    }
    resource_dirs = sorted(source_resources | set(planned_resources or []))
    script_names: list[str] = []
    reference_names: list[str] = []
    readme_hint = ""

    if source_dir is not None:
        scripts_dir = source_dir / "scripts"
        if scripts_dir.exists():
            script_names = sorted(
                child.stem
                for child in scripts_dir.iterdir()
                if child.is_file() and child.suffix in {".py", ".sh", ".js", ".ts"}
            )[:4]
        references_dir = source_dir / "references"
        if references_dir.exists():
            reference_names = sorted(
                child.stem
                for child in references_dir.iterdir()
                if child.is_file() and child.suffix in {".md", ".txt"}
            )[:4]
        readme_path = source_dir / "README.md"
        if readme_path.exists():
            for line in readme_path.read_text().splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith("#") or stripped.startswith("["):
                    continue
                readme_hint = stripped
                break

    pretty_name = skill_name.replace("-", " ")
    example_noun = script_names[0].replace("-", " ") if script_names else pretty_name
    return {
        "resource_dirs": resource_dirs,
        "script_names": script_names,
        "reference_names": reference_names,
        "readme_hint": readme_hint,
        "pretty_name": pretty_name,
        "example_noun": example_noun,
    }


def build_skill_md(
    skill_name: str,
    purpose: str | None,
    source_dir: Path | None = None,
    planned_resources: list[str] | None = None,
) -> str:
    display_name = title_case_skill_name(skill_name)
    description = purpose.strip() if purpose else PLACEHOLDER_DESCRIPTION
    context = collect_skill_draft_context(skill_name, source_dir, planned_resources)
    purpose_body = (
        purpose.strip()
        if purpose
        else (
            context["readme_hint"]
            or f"Use this skill when the user needs help with {context['pretty_name']} workflows."
        )
    )

    use_when_lines = [
        f"- Use it when the request clearly matches {context['pretty_name']} work.",
        "- Use it when the bundled resources, references, or scripts help the task.",
    ]
    if context["script_names"]:
        use_when_lines.append(
            "- Use it when deterministic helper scripts are available in `scripts/`."
        )

    do_not_use_lines = [
        f"- Do not use it for tasks unrelated to {context['pretty_name']}.",
        "- Do not use it when a simpler built-in workflow solves the request without this package.",
    ]

    inputs_lines = [
        "- Inputs: the user request, relevant repo files, and any task-specific inputs.",
        "- Outputs: validated file changes, generated artifacts, or a concise status summary.",
    ]
    if context["resource_dirs"]:
        inputs_lines.append(
            "- Bundled resources: "
            + ", ".join(f"`{resource}/`" for resource in context["resource_dirs"])
            + "."
        )
    if context["script_names"]:
        inputs_lines.append(
            "- Helper scripts: "
            + ", ".join(f"`scripts/{script}`" for script in context["script_names"])
            + "."
        )
    if context["reference_names"]:
        inputs_lines.append(
            "- Reference files: "
            + ", ".join(f"`references/{name}`" for name in context["reference_names"])
            + "."
        )

    workflow_lines = [
        "1. Confirm the goal, inputs, and the target files or systems.",
        "2. Use bundled scripts or references when they improve reliability or clarity.",
        "3. Validate the result and report what changed, what was checked, and any follow-up risk.",
    ]

    example_lines = [
        f"- `$${skill_name}` help me with {context['pretty_name']} in this repo.".replace("$$", "$"),
        f"- `$${skill_name}` use the packaged workflow to handle {context['example_noun']} tasks.".replace("$$", "$"),
    ]

    risk_lines = [
        "- Read the bundled references before making assumptions about local conventions or schemas.",
        "- Prefer deterministic scripts for fragile steps, and validate outputs before finishing.",
    ]

    body_lines = [
        "---",
        f"name: {skill_name}",
        f"description: {yaml_quote(description)}",
        "---",
        "",
        f"# {display_name}",
        "",
        "## Purpose",
        "",
        purpose_body,
        "",
        "## Use This Skill When",
        "",
        *use_when_lines,
        "",
        "## Do Not Use This Skill When",
        "",
        *do_not_use_lines,
        "",
        "## Inputs / Outputs",
        "",
        *inputs_lines,
        "",
        "## Workflow",
        "",
        *workflow_lines,
        "",
        "## Example Requests",
        "",
        *example_lines,
        "",
        "## Risks / Boundaries",
        "",
        *risk_lines,
        "",
    ]
    return "\n".join(body_lines)


def build_openai_yaml(
    skill_name: str,
    display_name: str | None,
    short_description: str | None,
    default_prompt: str | None,
) -> str:
    resolved_display_name = display_name or title_case_skill_name(skill_name)
    resolved_short_description = short_description or default_short_description(
        resolved_display_name
    )
    resolved_default_prompt = default_prompt or default_prompt_text(
        skill_name,
        resolved_display_name,
    )
    return "\n".join(
        [
            "interface:",
            f"  display_name: {yaml_quote(resolved_display_name)}",
            f"  short_description: {yaml_quote(resolved_short_description)}",
            f"  default_prompt: {yaml_quote(resolved_default_prompt)}",
            "",
        ]
    )


def ensure_directory(path: Path, dry_run: bool = False) -> str:
    if path.exists():
        return "kept"
    if dry_run:
        return "would create"
    path.mkdir(parents=True, exist_ok=True)
    return "created"


def write_file(path: Path, content: str, dry_run: bool = False) -> str:
    existed = path.exists()
    if existed and path.read_text() == content:
        return "kept"
    if dry_run:
        return "would update" if existed else "would create"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return "updated" if existed else "created"


def split_frontmatter(content: str) -> tuple[str | None, str]:
    match = FRONTMATTER_RE.match(content)
    if not match:
        return None, content
    return match.group(1), content[match.end() :]


def set_frontmatter_value(content: str, key: str, value: str) -> str:
    frontmatter, body = split_frontmatter(content)
    formatted = yaml_quote(value) if key == "description" else value
    if frontmatter is None:
        prefix = f"---\n{key}: {formatted}\n---\n"
        return prefix + body

    lines = frontmatter.splitlines()
    updated = []
    replaced = False
    for line in lines:
        if re.match(rf"^{re.escape(key)}:\s*", line):
            updated.append(f"{key}: {formatted}")
            replaced = True
        else:
            updated.append(line)
    if not replaced:
        updated.append(f"{key}: {formatted}")

    rebuilt = "---\n" + "\n".join(updated) + "\n---"
    if body and not body.startswith("\n"):
        rebuilt += "\n"
    return rebuilt + body


def extract_frontmatter_value(content: str, key: str) -> str | None:
    frontmatter, _body = split_frontmatter(content)
    if frontmatter is None:
        return None
    for line in frontmatter.splitlines():
        match = re.match(rf"^{re.escape(key)}:\s*(.*)$", line)
        if match:
            return parse_simple_scalar(match.group(1))
    return None


def compose_markdown_document(frontmatter: str | None, body: str) -> str:
    body = body.rstrip()
    if frontmatter is None:
        return (body + "\n") if body else ""
    pieces = ["---", frontmatter.rstrip(), "---"]
    if body:
        pieces.extend(["", body])
    return "\n".join(pieces).rstrip() + "\n"


def parse_markdown_h2_sections(
    content: str,
) -> tuple[str | None, str, dict[str, str], list[str]]:
    frontmatter, body = split_frontmatter(content)
    prefix_lines: list[str] = []
    sections: dict[str, str] = {}
    order: list[str] = []
    current_title: str | None = None
    current_lines: list[str] = []

    for line in body.splitlines():
        if line.startswith("## "):
            if current_title is None:
                prefix = "\n".join(prefix_lines).rstrip()
            else:
                sections[current_title] = "\n".join(current_lines).rstrip()
            current_title = line[3:].strip()
            order.append(current_title)
            current_lines = [line]
            continue
        if current_title is None:
            prefix_lines.append(line)
        else:
            current_lines.append(line)

    if current_title is not None:
        sections[current_title] = "\n".join(current_lines).rstrip()
    prefix = "\n".join(prefix_lines).rstrip()
    return frontmatter, prefix, sections, order


def prepare_existing_skill_md_content(
    existing_content: str,
    skill_name: str,
    purpose: str | None,
) -> str:
    if not existing_content:
        return existing_content

    updated = existing_content
    if extract_frontmatter_value(updated, "name") != skill_name:
        updated = set_frontmatter_value(updated, "name", skill_name)
    if purpose:
        updated = set_frontmatter_value(updated, "description", purpose.strip())
    elif extract_frontmatter_value(updated, "description") is None:
        updated = set_frontmatter_value(updated, "description", PLACEHOLDER_DESCRIPTION)
    return updated


def merge_missing_skill_md_sections(
    existing_content: str,
    draft_content: str,
) -> dict[str, object]:
    draft_frontmatter, draft_prefix, draft_sections, draft_order = parse_markdown_h2_sections(
        draft_content
    )
    if not existing_content.strip() or not draft_sections:
        return {
            "content": draft_content,
            "rewrite_mode": "full-rewrite",
            "missing_sections_added": list(draft_order or DOCUMENT_SECTION_TITLES),
            "preserved_sections": [],
        }

    existing_frontmatter, existing_prefix, existing_sections, existing_order = parse_markdown_h2_sections(
        existing_content
    )
    has_existing_structure = bool(existing_sections) or existing_prefix.lstrip().startswith("# ")
    if not has_existing_structure:
        return {
            "content": draft_content,
            "rewrite_mode": "full-rewrite",
            "missing_sections_added": list(draft_order or DOCUMENT_SECTION_TITLES),
            "preserved_sections": [],
        }

    preserved_sections = [title for title in draft_order if title in existing_sections]
    missing_sections_added = [title for title in draft_order if title not in existing_sections]

    body_parts: list[str] = []
    prefix_block = existing_prefix or draft_prefix
    if prefix_block:
        body_parts.append(prefix_block.rstrip())

    for title in draft_order:
        block = existing_sections.get(title, draft_sections[title])
        body_parts.append(block.rstrip())

    for title in existing_order:
        if title not in draft_sections and title in existing_sections:
            body_parts.append(existing_sections[title].rstrip())
            preserved_sections.append(title)

    merged_content = compose_markdown_document(
        existing_frontmatter or draft_frontmatter,
        "\n\n".join(part for part in body_parts if part).rstrip(),
    )
    return {
        "content": merged_content,
        "rewrite_mode": "merge-missing-sections",
        "missing_sections_added": missing_sections_added,
        "preserved_sections": preserved_sections,
    }


def parse_openai_interface(content: str) -> dict[str, str]:
    result: dict[str, str] = {}
    in_interface = False
    for line in content.splitlines():
        if line.strip() == "interface:":
            in_interface = True
            continue
        if not in_interface:
            continue
        if not line.startswith("  "):
            break
        match = re.match(r"^\s{2}([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            result[match.group(1)] = parse_simple_scalar(match.group(2))
    return result


def normalize_default_prompt_reference(
    default_prompt: str | None,
    skill_name: str,
    display_name: str,
) -> str:
    if not default_prompt:
        return default_prompt_text(skill_name, display_name)
    if f"${skill_name}" in default_prompt:
        return default_prompt
    if re.search(r"\$[a-z0-9-]+", default_prompt):
        return re.sub(r"\$[a-z0-9-]+", f"${skill_name}", default_prompt, count=1)
    return default_prompt


def upsert_skill_md(
    path: Path,
    skill_name: str,
    purpose: str | None,
    source_dir: Path | None,
    planned_resources: list[str],
    overwrite: bool,
    dry_run: bool,
) -> str:
    if not path.exists() or overwrite:
        return write_file(
            path,
            build_skill_md(
                skill_name,
                purpose,
                source_dir=source_dir,
                planned_resources=planned_resources,
            ),
            dry_run=dry_run,
        )

    content = path.read_text()
    updated = content
    if extract_frontmatter_value(content, "name") != skill_name:
        updated = set_frontmatter_value(updated, "name", skill_name)
    if purpose:
        updated = set_frontmatter_value(updated, "description", purpose.strip())
    elif extract_frontmatter_value(updated, "description") is None:
        updated = set_frontmatter_value(updated, "description", PLACEHOLDER_DESCRIPTION)
    return write_file(path, updated, dry_run=dry_run)


def upsert_openai_yaml(
    path: Path,
    skill_name: str,
    display_name: str | None,
    short_description: str | None,
    default_prompt: str | None,
    overwrite: bool,
    dry_run: bool,
) -> str:
    existing = parse_openai_interface(path.read_text()) if path.exists() and not overwrite else {}
    merged_display_name = display_name or existing.get("display_name")
    merged_short_description = short_description or existing.get("short_description")
    resolved_display_name = merged_display_name or title_case_skill_name(skill_name)
    merged_default_prompt = normalize_default_prompt_reference(
        default_prompt or existing.get("default_prompt"),
        skill_name,
        resolved_display_name,
    )
    content = build_openai_yaml(
        skill_name,
        resolved_display_name,
        merged_short_description,
        merged_default_prompt,
    )
    return write_file(path, content, dry_run=dry_run)


def ensure_optional_dirs(skill_dir: Path, resources: list[str], dry_run: bool) -> list[tuple[str, str]]:
    created = []
    for resource in resources:
        status = ensure_directory(skill_dir / resource, dry_run=dry_run)
        created.append((resource, status))
    return created


def import_skill_tree(
    source_dir: Path,
    target_dir: Path,
    mode: str,
    dry_run: bool,
) -> str:
    if not source_dir.exists():
        raise FileNotFoundError(f"Import source does not exist: {source_dir}")
    if not source_dir.is_dir():
        raise NotADirectoryError(f"Import source is not a directory: {source_dir}")

    source_resolved = source_dir.resolve()
    target_resolved = target_dir.resolve(strict=False)
    if source_resolved == target_resolved:
        return "kept"

    if target_dir.exists():
        raise FileExistsError(
            f"Cannot import into {target_dir}: destination already exists."
        )

    if dry_run:
        return f"would {mode}"

    target_dir.parent.mkdir(parents=True, exist_ok=True)
    if mode == "copy":
        shutil.copytree(source_dir, target_dir, symlinks=True)
        return "copied"
    if mode == "move":
        shutil.move(str(source_dir), str(target_dir))
        return "moved"
    raise ValueError(f"Unsupported import mode: {mode}")


def ensure_import_target_available(
    source_dir: Path,
    target_dir: Path,
    library_root: Path,
    desired_name: str,
) -> None:
    if not source_dir.exists():
        raise FileNotFoundError(f"Import source does not exist: {source_dir}")
    if not source_dir.is_dir():
        raise NotADirectoryError(f"Import source is not a directory: {source_dir}")

    if source_dir.resolve() == target_dir.resolve(strict=False):
        return
    if not target_dir.exists():
        return

    suggestions = suggest_available_skill_names(library_root, desired_name)
    suggestion_text = ", ".join(suggestions) if suggestions else "no alternative names available"
    retry_name = suggestions[0] if suggestions else f"{desired_name}-renamed"
    raise FileExistsError(
        "Import target already exists: "
        f"{target_dir}\n"
        f"Try importing with a different canonical name, for example: {suggestion_text}\n"
        "You can override the imported name by passing it as the positional skill name, "
        f"for example: manage_skill.py {retry_name} --adopt {source_dir}"
    )


def preview_symlink_action(link_path: Path, target_path: Path) -> str:
    if link_path.is_symlink():
        current_target = Path(os.path.realpath(link_path))
        if current_target == target_path.resolve(strict=False):
            return "kept"
        return "would relink"
    if link_path.exists():
        return "blocked by existing non-symlink"
    return "would link"


def inspect_import_source(
    source_dir: Path,
    library_root: Path,
    desired_name: str,
    project_root: Path | None,
    exposure_root: Path | None,
    output_format: str = "text",
) -> int:
    if not source_dir.exists():
        if output_format == "json":
            return emit_json(
                {
                    "mode": "inspect-import",
                    "ok": False,
                    "error": f"Import source does not exist: {source_dir}",
                    "source_path": str(source_dir),
                    "library_root": str(library_root),
                }
            )
        print(f"[ERROR] Import source does not exist: {source_dir}")
        return 1
    if not source_dir.is_dir():
        if output_format == "json":
            return emit_json(
                {
                    "mode": "inspect-import",
                    "ok": False,
                    "error": f"Import source is not a directory: {source_dir}",
                    "source_path": str(source_dir),
                    "library_root": str(library_root),
                }
            )
        print(f"[ERROR] Import source is not a directory: {source_dir}")
        return 1

    skill_md = source_dir / "SKILL.md"
    openai_path = source_dir / "agents" / "openai.yaml"
    detected_name = detect_skill_name_from_source(source_dir)
    detected_description = ""
    interface: dict[str, str] = {}
    if skill_md.exists():
        detected_description = extract_frontmatter_value(skill_md.read_text(), "description") or ""
    if openai_path.exists():
        interface = parse_openai_interface(openai_path.read_text())

    target_dir = library_root / desired_name
    source_resolved = source_dir.resolve()
    target_resolved = target_dir.resolve(strict=False)
    if source_resolved == target_resolved:
        import_status = "already managed at canonical path"
    elif target_dir.exists():
        import_status = "name conflict"
    else:
        import_status = "ready to import"

    resource_dirs = [
        resource for resource in sorted(ALLOWED_RESOURCES) if (source_dir / resource).exists()
    ]
    errors, warnings = validate_skill_dir(source_dir)
    payload: dict[str, object] = {
        "mode": "inspect-import",
        "ok": True,
        "source_path": str(source_dir),
        "library_root": str(library_root),
        "detected_source_skill_name": detected_name,
        "desired_canonical_name": desired_name,
        "proposed_canonical_path": str(target_dir),
        "import_status": import_status,
        "skill_md_present": skill_md.exists(),
        "openai_yaml_present": openai_path.exists(),
        "description": detected_description or None,
        "interface": {
            key: value
            for key, value in interface.items()
            if key in {"display_name", "short_description", "default_prompt"} and value
        },
        "resource_directories": resource_dirs,
        "validation": {
            "ok": not errors,
            "errors": errors,
            "warnings": warnings,
        },
        "recommended_import_mode": "copy",
        "move_guidance": (
            "Use --import-mode move only if you want the shared-library copy to become "
            "the sole source and you no longer need the original download directory."
        ),
    }
    suggestions: list[str] = []
    if import_status == "name conflict":
        suggestions = suggest_available_skill_names(library_root, desired_name)
        payload["suggested_canonical_names"] = suggestions

    if project_root:
        project_link = (exposure_root or (project_root / ".agents" / "skills")) / desired_name
        project_action = preview_symlink_action(project_link, target_dir)
        project_payload: dict[str, object] = {
            "project_root": str(project_root),
            "project_link_path": str(project_link),
            "project_link_action": project_action,
        }
        if not path_is_within(source_dir, project_root):
            registry_path = external_source_registry_path(project_root)
            project_payload["external_source_registry"] = str(registry_path)
            project_payload["external_source_registry_action"] = "would record source path"
        payload["project"] = project_payload

    if output_format == "json":
        return emit_json(payload)

    print(f"[INSPECT] Source path: {source_dir}")
    print(f"[INSPECT] Library root: {library_root}")
    print(f"[INSPECT] Detected source skill name: {detected_name or '(missing)'}")
    print(f"[INSPECT] Desired canonical name: {desired_name}")
    print(f"[INSPECT] Proposed canonical path: {target_dir}")
    print(f"[INSPECT] Import status: {import_status}")
    print(f"[INSPECT] SKILL.md present: {'yes' if skill_md.exists() else 'no'}")
    print(f"[INSPECT] agents/openai.yaml present: {'yes' if openai_path.exists() else 'no'}")
    if detected_description:
        print(f"[INSPECT] Description: {detected_description}")
    if interface.get("display_name"):
        print(f"[INSPECT] Display name: {interface['display_name']}")
    if interface.get("short_description"):
        print(f"[INSPECT] Short description: {interface['short_description']}")
    if interface.get("default_prompt"):
        print(f"[INSPECT] Default prompt: {interface['default_prompt']}")
    print(
        "[INSPECT] Resource directories: "
        + (", ".join(resource_dirs) if resource_dirs else "none detected")
    )

    if errors:
        print("[INSPECT] Source validation: has errors")
        for error in errors:
            print(f"  - {error}")
    else:
        print("[INSPECT] Source validation: passes structural checks")
    for warning in warnings:
        print(f"  - Warning: {warning}")

    if import_status == "name conflict":
        suggestion_text = ", ".join(suggestions) if suggestions else "no suggestions available"
        print(f"[INSPECT] Suggested canonical names: {suggestion_text}")
        if suggestions:
            print(
                "[INSPECT] Retry example: "
                f"manage_skill.py {suggestions[0]} --adopt {source_dir}"
            )

    print("[INSPECT] Recommended import mode: copy")
    print(
        "[INSPECT] Move guidance: use --import-mode move only if you want the shared-library "
        "copy to become the sole source and you no longer need the original download directory."
    )

    if project_root:
        project_link = (exposure_root or (project_root / ".agents" / "skills")) / desired_name
        project_action = preview_symlink_action(project_link, target_dir)
        print(f"[INSPECT] Project root: {project_root}")
        print(f"[INSPECT] Project link path: {project_link}")
        print(f"[INSPECT] Project link action: {project_action}")
        if not path_is_within(source_dir, project_root):
            registry_path = external_source_registry_path(project_root)
            print(f"[INSPECT] External source registry: {registry_path}")
            print("[INSPECT] External source registry action: would record source path")

    print("[NEXT] Inspect complete. No files were modified.")
    return 0


def summarize_skill_metadata(skill_dir: Path) -> dict[str, str]:
    summary: dict[str, str] = {
        "path": str(skill_dir),
        "name": skill_dir.name,
    }
    skill_md = skill_dir / "SKILL.md"
    skill_body = ""
    if skill_md.exists():
        content = skill_md.read_text()
        summary["name"] = extract_frontmatter_value(content, "name") or skill_dir.name
        summary["description"] = extract_frontmatter_value(content, "description") or ""
        _frontmatter, skill_body = split_frontmatter(content)
    openai_path = skill_dir / "agents" / "openai.yaml"
    if openai_path.exists():
        interface = parse_openai_interface(openai_path.read_text())
        for key in ("display_name", "short_description", "default_prompt"):
            if interface.get(key):
                summary[key] = interface[key]
    if skill_body:
        summary["body"] = skill_body
    return summary


def extract_markdown_headings(body: str) -> set[str]:
    headings = set()
    for line in body.splitlines():
        if not line.startswith("#"):
            continue
        heading = line.lstrip("#").strip().lower()
        if heading:
            headings.add(heading)
    return headings


def tokenize_skill_text(*parts: str) -> set[str]:
    tokens = set()
    for part in parts:
        for token in TOKEN_RE.findall(part.lower()):
            if token in SKILL_TEXT_STOPWORDS or len(token) <= 2:
                continue
            tokens.add(SEMANTIC_TOKEN_ALIASES.get(token, token))
    return tokens


def weighted_skill_terms(target_summary: dict[str, str]) -> dict[str, float]:
    weighted_parts = [
        (target_summary.get("name", ""), 3.0),
        (target_summary.get("description", ""), 4.0),
        (target_summary.get("display_name", ""), 2.0),
        (target_summary.get("short_description", ""), 2.0),
        (target_summary.get("default_prompt", ""), 1.5),
        (target_summary.get("body", ""), 1.0),
    ]
    weights: dict[str, float] = {}
    for part, weight in weighted_parts:
        for token in tokenize_skill_text(part):
            weights[token] = weights.get(token, 0.0) + weight
    return weights


def cosine_similarity(left: dict[str, float], right: dict[str, float]) -> float:
    if not left or not right:
        return 0.0
    dot = sum(left.get(token, 0.0) * right.get(token, 0.0) for token in set(left) & set(right))
    if dot <= 0:
        return 0.0
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


def normalized_sequence_similarity(*parts: str) -> float:
    non_empty = [part.strip().lower() for part in parts if part and part.strip()]
    if len(non_empty) < 2:
        return 0.0
    return difflib.SequenceMatcher(a=non_empty[0], b=non_empty[1]).ratio()


def score_band(score: int) -> str:
    if score >= 85:
        return "excellent"
    if score >= 70:
        return "good"
    if score >= 50:
        return "fair"
    return "poor"


def clamp_score(value: int) -> int:
    return max(0, min(100, value))


def is_active_project_consumer(status: str) -> bool:
    return status in ACTIVE_PROJECT_LINK_STATUSES


def find_similar_library_skills(
    library_root: Path,
    target_dir: Path,
    target_summary: dict[str, str],
    limit: int = 5,
) -> list[dict[str, object]]:
    if not library_root.exists():
        return []

    target_tokens = tokenize_skill_text(
        target_summary.get("name", ""),
        target_summary.get("description", ""),
        target_summary.get("display_name", ""),
        target_summary.get("short_description", ""),
        target_summary.get("body", ""),
    )
    target_weighted_terms = weighted_skill_terms(target_summary)
    target_headings = extract_markdown_headings(target_summary.get("body", ""))
    target_description = target_summary.get("description", "").strip().lower()
    candidates: list[dict[str, object]] = []

    for child in sorted(library_root.iterdir()):
        if not child.is_dir() or not (child / "SKILL.md").exists():
            continue
        if child.resolve() == target_dir.resolve():
            continue
        candidate_summary = summarize_skill_metadata(child)
        candidate_tokens = tokenize_skill_text(
            candidate_summary.get("name", ""),
            candidate_summary.get("description", ""),
            candidate_summary.get("display_name", ""),
            candidate_summary.get("short_description", ""),
            candidate_summary.get("body", ""),
        )
        candidate_weighted_terms = weighted_skill_terms(candidate_summary)
        candidate_headings = extract_markdown_headings(candidate_summary.get("body", ""))
        if not target_tokens or not candidate_tokens:
            continue
        union = target_tokens | candidate_tokens
        intersection = target_tokens & candidate_tokens
        if not union:
            continue
        lexical_similarity = len(intersection) / len(union)
        cosine = cosine_similarity(target_weighted_terms, candidate_weighted_terms)
        description_similarity = normalized_sequence_similarity(
            target_summary.get("description", ""),
            candidate_summary.get("description", ""),
        )
        heading_similarity = 0.0
        if target_headings and candidate_headings:
            heading_union = target_headings | candidate_headings
            heading_intersection = target_headings & candidate_headings
            if heading_union:
                heading_similarity = len(heading_intersection) / len(heading_union)
        similarity = max(
            lexical_similarity,
            round(
                (cosine * 0.5)
                + (lexical_similarity * 0.25)
                + (description_similarity * 0.15)
                + (heading_similarity * 0.10),
                4,
            ),
        )
        candidate_description = candidate_summary.get("description", "").strip().lower()
        if target_description and candidate_description and target_description == candidate_description:
            similarity = max(similarity, 0.95)
        if similarity < 0.35:
            continue
        candidates.append(
            {
                "name": candidate_summary.get("name", child.name),
                "path": str(child),
                "similarity": round(similarity, 2),
                "signals": {
                    "cosine": round(cosine, 2),
                    "lexical": round(lexical_similarity, 2),
                    "description": round(description_similarity, 2),
                    "headings": round(heading_similarity, 2),
                },
                "shared_terms": sorted(intersection)[:8],
            }
        )

    candidates.sort(
        key=lambda item: (-float(item["similarity"]), str(item["name"]))
    )
    return candidates[:limit]


def build_governance_profile(
    target_dir: Path,
    target_summary: dict[str, str],
    validation: dict[str, object] | None,
    target_location: str,
    project_link: dict[str, object] | None,
    library_root: Path,
) -> dict[str, object]:
    body = target_summary.get("body", "")
    headings = extract_markdown_headings(body)
    resource_dirs = [
        resource for resource in sorted(ALLOWED_RESOURCES) if (target_dir / resource).exists()
    ]
    unmentioned_resources = [
        resource
        for resource in resource_dirs
        if resource not in body and f"{resource}/" not in body
    ]
    description = target_summary.get("description", "")
    default_prompt = target_summary.get("default_prompt", "")
    short_description = target_summary.get("short_description", "")

    sections = {
        "purpose": "purpose" in headings,
        "use_this_skill_when": "use this skill when" in headings,
        "inputs_outputs": "inputs / outputs" in headings or "inputs/outputs" in headings,
        "workflow": "workflow" in headings,
        "example_requests": "example requests" in headings or "examples" in headings,
        "boundaries": (
            "do not use this skill when" in headings
            or "risks / boundaries" in headings
            or "risks/boundaries" in headings
        ),
    }
    missing_sections = [name for name, present in sections.items() if not present]

    validation_errors = len(validation["errors"]) if validation else 0
    validation_warnings = len(validation["warnings"]) if validation else 0
    structure_health = clamp_score(100 - (validation_errors * 25) - (validation_warnings * 5))

    content_completeness = 20
    if description and description != PLACEHOLDER_DESCRIPTION:
        content_completeness += 20
    if sections["purpose"]:
        content_completeness += 15
    if sections["use_this_skill_when"]:
        content_completeness += 20
    if sections["inputs_outputs"]:
        content_completeness += 10
    if sections["workflow"]:
        content_completeness += 20
    if sections["example_requests"]:
        content_completeness += 15
    if sections["boundaries"]:
        content_completeness += 10
    content_completeness = clamp_score(content_completeness)

    discoverability = 20
    if 40 <= len(description) <= 240:
        discoverability += 25
    if short_description:
        discoverability += 20
    if default_prompt and f"${target_summary.get('name', '')}" in default_prompt:
        discoverability += 20
    if sections["example_requests"]:
        discoverability += 15
    if target_summary.get("display_name"):
        discoverability += 10
    if target_summary.get("name") and target_summary.get("name") in target_summary.get("path", ""):
        discoverability += 10
    discoverability = clamp_score(discoverability)

    duplicate_candidates = find_similar_library_skills(
        library_root,
        target_dir,
        target_summary,
    )
    top_similarity = float(duplicate_candidates[0]["similarity"]) if duplicate_candidates else 0.0
    reuse_value = 35
    if target_location in {"canonical shared-library skill", "shared-library entry"}:
        reuse_value += 20
    elif target_location == "project-local skill directory":
        reuse_value += 5
    if project_link and project_link.get("status") in {"managed symlink", "managed copy"}:
        reuse_value += 15
    if sections["example_requests"]:
        reuse_value += 10
    if resource_dirs:
        reuse_value += 10
    if top_similarity >= 0.8:
        reuse_value -= 25
    elif top_similarity >= 0.55:
        reuse_value -= 10
    reuse_value = clamp_score(reuse_value)

    maintenance_risk = 5
    maintenance_risk += validation_errors * 20
    maintenance_risk += validation_warnings * 5
    maintenance_risk += len(missing_sections) * 6
    maintenance_risk += len(unmentioned_resources) * 10
    if top_similarity >= 0.8:
        maintenance_risk += 25
    elif top_similarity >= 0.55:
        maintenance_risk += 12
    if project_link and project_link.get("status") in {
        "broken symlink",
        "external symlink",
        "local directory (not a managed exposure)",
        "non-directory entry",
    }:
        maintenance_risk += 20
    maintenance_risk = clamp_score(maintenance_risk)

    health_score = clamp_score(
        round(
            (structure_health * 0.30)
            + (content_completeness * 0.25)
            + (discoverability * 0.20)
            + (reuse_value * 0.15)
            + ((100 - maintenance_risk) * 0.10)
        )
    )

    suggestions: list[str] = []
    if missing_sections:
        human_sections = ", ".join(missing_sections)
        suggestions.append(
            f"Add or strengthen these SKILL.md sections: {human_sections}."
        )
    if unmentioned_resources:
        human_resources = ", ".join(f"{resource}/" for resource in unmentioned_resources)
        suggestions.append(
            f"Document these resource directories in SKILL.md or remove them if they are no longer needed: {human_resources}."
        )
    if top_similarity >= 0.8:
        suggestions.append(
            f"Review overlap with {duplicate_candidates[0]['name']}; this may deserve merge, rename, or deprecation planning."
        )
    elif top_similarity >= 0.55:
        suggestions.append(
            f"Check whether {duplicate_candidates[0]['name']} overlaps too much with this skill."
        )
    if not default_prompt:
        suggestions.append("Add a concrete default_prompt so the skill is easier to discover.")
    if not sections["example_requests"]:
        suggestions.append("Add at least one example request so the main trigger is easier to understand.")

    return {
        "health_score": health_score,
        "health_band": score_band(health_score),
        "dimensions": {
            "structure_health": structure_health,
            "content_completeness": content_completeness,
            "discoverability": discoverability,
            "reuse_value": reuse_value,
            "maintenance_risk": maintenance_risk,
        },
        "signals": {
            "sections_present": [name for name, present in sections.items() if present],
            "sections_missing": missing_sections,
            "resource_directories": resource_dirs,
            "unmentioned_resource_directories": unmentioned_resources,
            "default_prompt_present": bool(default_prompt),
            "default_prompt_references_skill": bool(
                default_prompt and f"${target_summary.get('name', '')}" in default_prompt
            ),
            "attached_to_current_project": bool(
                project_link and project_link.get("status") in {"managed symlink", "managed copy"}
            ),
        },
        "duplicate_candidates": duplicate_candidates,
        "suggestions": suggestions,
    }


def find_project_config_path(project_root: Path) -> Path | None:
    for filename in DEFAULT_CONFIG_FILENAMES:
        candidate = project_root / filename
        if candidate.exists():
            return candidate
    return None


def safe_load_project_config(project_root: Path) -> tuple[WorkflowConfig, str | None]:
    config_path = find_project_config_path(project_root)
    try:
        return load_workflow_config(config_path), None
    except UsageError as error:
        return WorkflowConfig(config_path, None, None, None, None, None, None), str(error)


def discover_project_roots(workspace_root: Path, limit: int = 200) -> list[Path]:
    if not workspace_root.exists() or not workspace_root.is_dir():
        return []

    markers = {".git", ".agents", DEFAULT_LIBRARY_DIRNAME, *DEFAULT_CONFIG_FILENAMES}
    pruned = {
        ".git",
        ".hg",
        ".svn",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "dist",
        "build",
    }
    discovered: list[Path] = []
    seen: set[Path] = set()

    for current_root, dirnames, filenames in os.walk(workspace_root):
        current = Path(current_root)
        dirnames[:] = [
            name for name in dirnames if name not in pruned and not name.startswith(".tox")
        ]
        current_markers = set(dirnames) | set(filenames)
        if current_markers & markers:
            resolved = current.resolve()
            if resolved not in seen:
                discovered.append(resolved)
                seen.add(resolved)
                if len(discovered) >= limit:
                    break
    return sorted(discovered)


def collect_impact_analysis(
    skill_name: str,
    library_root: Path,
    workspace_root: Path | None,
    current_project_root: Path | None,
) -> dict[str, object] | None:
    if workspace_root is None:
        return None

    project_entries: list[dict[str, object]] = []
    counts = {
        "projects_total": 0,
        "managed_symlink": 0,
        "managed_copy": 0,
        "managed_manifest": 0,
        "broken": 0,
        "blocked": 0,
        "external": 0,
        "config_errors": 0,
    }

    for project_root in discover_project_roots(workspace_root):
        config, config_error = safe_load_project_config(project_root)
        exposure_root = detect_exposure_root(None, config, project_root)
        if config_error:
            counts["config_errors"] += 1
            if project_root == current_project_root:
                project_entries.append(
                    {
                        "project_root": str(project_root),
                        "status": "config-error",
                        "error": config_error,
                    }
                )
            continue
        if exposure_root is None:
            continue
        project_link = collect_project_link_status(
            project_root,
            exposure_root,
            library_root,
            skill_name,
        )
        status = str(project_link["status"])
        if status == "missing":
            continue
        entry = {
            "project_root": str(project_root),
            "status": status,
            "path": project_link["path"],
            "managed_mode": project_link.get("managed_mode"),
            "target": project_link.get("target"),
            "is_current_project": bool(
                current_project_root and project_root.resolve() == current_project_root.resolve()
            ),
        }
        project_entries.append(entry)
        counts["projects_total"] += 1
        if status == "managed symlink":
            counts["managed_symlink"] += 1
        elif status == "managed copy":
            counts["managed_copy"] += 1
        elif status == "managed manifest":
            counts["managed_manifest"] += 1
        elif status == "broken symlink":
            counts["broken"] += 1
        elif status in {"local directory (not a managed exposure)", "non-directory entry"}:
            counts["blocked"] += 1
        elif status in {"external symlink", "shared-library link to another skill"}:
            counts["external"] += 1

    recommendations: list[str] = []
    if counts["managed_copy"] > 0:
        recommendations.append(
            f"{counts['managed_copy']} project(s) use copy exposure; plan refresh or re-enable after upgrades because copy mode does not hot-switch."
        )
    if counts["managed_manifest"] > 0:
        recommendations.append(
            f"{counts['managed_manifest']} project(s) use manifest exposure; this records managed intent without creating a direct runtime link."
        )
    if counts["broken"] > 0:
        recommendations.append(
            f"{counts['broken']} project exposure(s) are broken and should be repaired before major refactors or retire actions."
        )
    if counts["blocked"] > 0:
        recommendations.append(
            f"{counts['blocked']} project exposure path(s) are blocked by unmanaged entries and may require manual cleanup."
        )

    active_projects = [
        entry for entry in project_entries if is_active_project_consumer(str(entry["status"]))
    ]
    current_project_entry = next(
        (entry for entry in project_entries if entry.get("is_current_project")),
        None,
    )
    current_project_status = (
        str(current_project_entry["status"]) if current_project_entry is not None else "missing"
    )
    current_project_is_active = is_active_project_consumer(current_project_status)

    return {
        "workspace_root": str(workspace_root),
        "counts": counts,
        "projects": sorted(project_entries, key=lambda item: str(item["project_root"])),
        "reference_graph": {
            "active_projects_total": len(active_projects),
            "other_active_projects_total": (
                len(active_projects) - (1 if current_project_is_active else 0)
            ),
            "current_project_status": current_project_status,
            "copy_projects": [
                str(entry["project_root"])
                for entry in project_entries
                if str(entry["status"]) == "managed copy"
            ],
            "manifest_projects": [
                str(entry["project_root"])
                for entry in project_entries
                if str(entry["status"]) == "managed manifest"
            ],
            "broken_projects": [
                str(entry["project_root"])
                for entry in project_entries
                if str(entry["status"]) == "broken symlink"
            ],
            "blocked_projects": [
                str(entry["project_root"])
                for entry in project_entries
                if str(entry["status"]) in {"local directory (not a managed exposure)", "non-directory entry"}
            ],
        },
        "recommendations": recommendations,
    }


def platform_registry_path(platform_root: Path) -> Path:
    return platform_root / PLATFORM_REGISTRY_FILENAME


def platform_dependency_graph_path(platform_root: Path) -> Path:
    return platform_root / PLATFORM_DEPENDENCY_GRAPH_FILENAME


def load_json_state(path: Path) -> tuple[dict[str, object] | None, str | None]:
    if not path.exists():
        return None, None
    try:
        payload = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        return None, f"Could not parse {path}: {error}"
    if not isinstance(payload, dict):
        return None, f"State file must contain a top-level JSON object: {path}"
    return payload, None


def discover_dependency_project_roots(
    workspace_root: Path | None,
    current_project_root: Path | None,
) -> list[Path]:
    if workspace_root is not None:
        project_roots = discover_project_roots(workspace_root)
        if current_project_root is not None and current_project_root.resolve() not in {
            project_root.resolve() for project_root in project_roots
        }:
            project_roots.append(current_project_root.resolve())
        return sorted({project_root.resolve() for project_root in project_roots})
    if current_project_root is not None:
        return [current_project_root.resolve()]
    return []


def collect_dependency_graph(
    library_root: Path,
    workspace_root: Path | None,
    current_project_root: Path | None,
) -> dict[str, object]:
    library_skills = collect_library_skills(library_root)["skills"]
    skill_names = sorted(str(summary["name"]) for summary in library_skills)
    skill_nodes: dict[str, dict[str, object]] = {}
    for summary in library_skills:
        skill_name = str(summary["name"])
        skill_nodes[skill_name] = {
            "skill_name": skill_name,
            "canonical_location": str(summary["path"]),
            "projects_total": 0,
            "active_projects_total": 0,
            "counts": {
                "managed_symlink": 0,
                "managed_copy": 0,
                "managed_manifest": 0,
                "broken": 0,
                "blocked": 0,
                "external": 0,
            },
            "projects": [],
            "active_projects": [],
        }

    project_nodes: dict[str, dict[str, object]] = {}
    for project_root in discover_dependency_project_roots(workspace_root, current_project_root):
        config, config_error = safe_load_project_config(project_root)
        exposure_root = (
            None if config_error else detect_exposure_root(None, config, project_root)
        )
        project_entry: dict[str, object] = {
            "project_root": str(project_root),
            "config_error": config_error,
            "exposure_root": str(exposure_root) if exposure_root else None,
            "skills": [],
            "active_skills_total": 0,
        }
        if config_error or exposure_root is None:
            project_nodes[str(project_root)] = project_entry
            continue

        project_skills: list[dict[str, object]] = []
        active_skills_total = 0
        for skill_name in skill_names:
            link_status = collect_project_link_status(
                project_root,
                exposure_root,
                library_root,
                skill_name,
            )
            status = str(link_status["status"])
            if status == "missing":
                continue
            skill_project_entry = {
                "skill_name": skill_name,
                "status": status,
                "path": str(link_status["path"]),
                "target": str(link_status["target"]) if link_status.get("target") else None,
                "managed_mode": (
                    str(link_status["managed_mode"])
                    if link_status.get("managed_mode")
                    else None
                ),
            }
            project_skills.append(skill_project_entry)

            skill_node = skill_nodes.get(skill_name)
            if skill_node is None:
                continue
            skill_node["projects"].append(
                {
                    "project_root": str(project_root),
                    "status": status,
                    "path": str(link_status["path"]),
                    "target": str(link_status["target"]) if link_status.get("target") else None,
                    "managed_mode": (
                        str(link_status["managed_mode"])
                        if link_status.get("managed_mode")
                        else None
                    ),
                }
            )
            skill_node["projects_total"] = int(skill_node["projects_total"]) + 1
            if status == "managed symlink":
                skill_node["counts"]["managed_symlink"] += 1
            elif status == "managed copy":
                skill_node["counts"]["managed_copy"] += 1
            elif status == "managed manifest":
                skill_node["counts"]["managed_manifest"] += 1
            elif status == "broken symlink":
                skill_node["counts"]["broken"] += 1
            elif status in {"local directory (not a managed exposure)", "non-directory entry"}:
                skill_node["counts"]["blocked"] += 1
            elif status in {"external symlink", "shared-library link to another skill"}:
                skill_node["counts"]["external"] += 1
            if is_active_project_consumer(status):
                active_skills_total += 1
                skill_node["active_projects_total"] = int(skill_node["active_projects_total"]) + 1
                skill_node["active_projects"].append(str(project_root))

        project_entry["skills"] = sorted(project_skills, key=lambda item: str(item["skill_name"]))
        project_entry["active_skills_total"] = active_skills_total
        project_nodes[str(project_root)] = project_entry

    for skill_name, skill_node in skill_nodes.items():
        skill_node["projects"] = sorted(
            skill_node["projects"],
            key=lambda item: str(item["project_root"]),
        )
        skill_node["active_projects"] = sorted(set(skill_node["active_projects"]))
        skill_node["projects_total"] = len(skill_node["projects"])
        skill_node["active_projects_total"] = len(skill_node["active_projects"])

    return {
        "schema_version": 1,
        "library_root": str(library_root),
        "workspace_root": str(workspace_root) if workspace_root else None,
        "projects_total": len(project_nodes),
        "skills_total": len(skill_nodes),
        "skills": {key: skill_nodes[key] for key in sorted(skill_nodes)},
        "projects": {key: project_nodes[key] for key in sorted(project_nodes)},
    }


def normalize_string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    result = []
    seen: set[str] = set()
    for item in value:
        if not isinstance(item, str):
            continue
        normalized = item.strip()
        if not normalized or normalized in seen:
            continue
        result.append(normalized)
        seen.add(normalized)
    return result


def derive_registry_exposure_mode(skill_graph: dict[str, object]) -> str:
    counts = skill_graph["counts"]
    has_symlink = int(counts["managed_symlink"]) > 0
    has_copy = int(counts["managed_copy"]) > 0
    has_manifest = int(counts["managed_manifest"]) > 0
    active_modes = sum(1 for present in (has_symlink, has_copy, has_manifest) if present)
    if active_modes > 1:
        return "mixed"
    if has_symlink:
        return "symlink"
    if has_copy:
        return "copy"
    if has_manifest:
        return "manifest"
    if int(skill_graph["projects_total"]) > 0:
        return "indirect"
    return "unexposed"


def build_registry_entry(
    skill_name: str,
    skill_dir: Path,
    library_root: Path,
    dependency_graph: dict[str, object],
    existing_entry: dict[str, object] | None,
) -> dict[str, object]:
    target_summary = summarize_skill_metadata(skill_dir)
    validation = collect_validation_result(skill_dir)
    governance = build_governance_profile(
        skill_dir,
        target_summary,
        validation,
        "canonical shared-library skill",
        None,
        library_root,
    )
    skill_graph = dependency_graph["skills"].get(
        skill_name,
        {
            "projects_total": 0,
            "active_projects_total": 0,
            "counts": {
                "managed_symlink": 0,
                "managed_copy": 0,
                "managed_manifest": 0,
                "broken": 0,
                "blocked": 0,
                "external": 0,
            },
            "projects": [],
            "active_projects": [],
        },
    )
    existing = existing_entry or {}
    lifecycle_status = str(existing.get("lifecycle_status", "active") or "active")
    version = str(existing.get("version", "") or "")
    owner = str(existing.get("owner", "") or "")
    reviewer = str(existing.get("reviewer", "") or "")
    team = str(existing.get("team", "") or "")
    deprecation_policy = str(existing.get("deprecation_policy", "") or "")
    last_reviewed_at = str(existing.get("last_reviewed_at", "") or "")

    usage_stats = {
        "projects_total": int(skill_graph["projects_total"]),
        "active_projects_total": int(skill_graph["active_projects_total"]),
        "managed_symlink": int(skill_graph["counts"]["managed_symlink"]),
        "managed_copy": int(skill_graph["counts"]["managed_copy"]),
        "managed_manifest": int(skill_graph["counts"]["managed_manifest"]),
        "broken": int(skill_graph["counts"]["broken"]),
        "blocked": int(skill_graph["counts"]["blocked"]),
        "external": int(skill_graph["counts"]["external"]),
    }

    return {
        "skill_id": skill_name,
        "display_name": str(target_summary.get("display_name", title_case_skill_name(skill_name))),
        "owner": owner,
        "reviewer": reviewer,
        "team": team,
        "version": version,
        "lifecycle_status": lifecycle_status,
        "canonical_location": str(skill_dir.resolve()),
        "description": str(target_summary.get("description", "") or ""),
        "short_description": str(target_summary.get("short_description", "") or ""),
        "default_prompt": str(target_summary.get("default_prompt", "") or ""),
        "exposure_mode": derive_registry_exposure_mode(skill_graph),
        "dependencies": normalize_string_list(existing.get("dependencies")),
        "dependents": list(skill_graph["active_projects"]),
        "quality_score": int(governance["health_score"]),
        "quality_band": str(governance["health_band"]),
        "usage_stats": usage_stats,
        "deprecation_policy": deprecation_policy,
        "last_reviewed_at": last_reviewed_at,
    }


def collect_platform_state(ctx: ExecutionContext) -> tuple[dict[str, object], dict[str, object]]:
    dependency_graph = collect_dependency_graph(
        ctx.library_root,
        ctx.workspace_root,
        ctx.project_root,
    )
    existing_registry_payload, _registry_error = load_json_state(
        platform_registry_path(ctx.platform_root)
    )
    existing_skills = (
        existing_registry_payload.get("skills", {})
        if isinstance(existing_registry_payload, dict)
        and isinstance(existing_registry_payload.get("skills"), dict)
        else {}
    )
    registry_skills: dict[str, dict[str, object]] = {}
    for skill_name, node in dependency_graph["skills"].items():
        skill_dir = Path(str(node["canonical_location"]))
        if not skill_dir.exists():
            continue
        registry_skills[skill_name] = build_registry_entry(
            skill_name,
            skill_dir,
            ctx.library_root,
            dependency_graph,
            existing_skills.get(skill_name) if isinstance(existing_skills, dict) else None,
        )

    registry_payload = {
        "schema_version": 1,
        "library_root": str(ctx.library_root),
        "platform_root": str(ctx.platform_root),
        "workspace_root": str(ctx.workspace_root) if ctx.workspace_root else None,
        "skills_total": len(registry_skills),
        "skills": {key: registry_skills[key] for key in sorted(registry_skills)},
    }
    return registry_payload, dependency_graph


def write_platform_state(
    platform_root: Path,
    registry_payload: dict[str, object],
    dependency_graph: dict[str, object],
    dry_run: bool,
) -> dict[str, str]:
    platform_status = ensure_directory(platform_root, dry_run=dry_run)
    registry_status = write_file(
        platform_registry_path(platform_root),
        json.dumps(registry_payload, indent=2, sort_keys=True) + "\n",
        dry_run=dry_run,
    )
    graph_status = write_file(
        platform_dependency_graph_path(platform_root),
        json.dumps(dependency_graph, indent=2, sort_keys=True) + "\n",
        dry_run=dry_run,
    )
    return {
        "platform_root": platform_status,
        "registry": registry_status,
        "dependency_graph": graph_status,
    }


def collect_task_impact_summary(
    ctx: ExecutionContext,
    action: str,
    skill_name: str,
    canonical_skill_dir: Path | None = None,
) -> dict[str, object] | None:
    impact_analysis = collect_impact_analysis(
        skill_name,
        ctx.library_root,
        ctx.workspace_root,
        ctx.project_root,
    )
    if impact_analysis is None:
        return None

    counts = impact_analysis["counts"]
    reference_graph = impact_analysis["reference_graph"]
    active_projects_total = int(reference_graph["active_projects_total"])
    other_active_projects_total = int(reference_graph["other_active_projects_total"])
    current_project_status = str(reference_graph["current_project_status"])

    canonical_path = canonical_skill_dir or (ctx.library_root / skill_name)
    follow_up: list[str] = []
    if action == "upgrade":
        if counts["managed_copy"] > 0:
            follow_up.append(
                f"Refresh or re-enable {counts['managed_copy']} copy-based project exposure(s) after this upgrade."
            )
        if counts["broken"] > 0:
            follow_up.append(
                f"Repair {counts['broken']} broken project exposure(s) before the next retire or migration."
            )
        if counts["blocked"] > 0:
            follow_up.append(
                f"Clean up {counts['blocked']} blocked project exposure path(s) before the next relink."
            )
    elif action == "retire":
        if ctx.args.dry_run:
            if is_active_project_consumer(current_project_status):
                follow_up.append(
                    f"If you apply this retire, {other_active_projects_total} other active project(s) would still use {skill_name}."
                )
            else:
                follow_up.append(
                    f"The current project is not using an active managed exposure for {skill_name}; this retire would mainly clean up the managed path or registry."
                )
            follow_up.append(f"The canonical skill would remain at {canonical_path}.")
        else:
            follow_up.append(f"Current project exposure removed for {skill_name}.")
            if active_projects_total > 0:
                follow_up.append(
                    f"{active_projects_total} active project(s) still use {skill_name}."
                )
            else:
                follow_up.append(f"No active project exposures remain for {skill_name}.")
            follow_up.append(f"The canonical skill remains at {canonical_path}.")

    return {
        "action": action,
        "skill_name": skill_name,
        "canonical_path": str(canonical_path),
        "impact_analysis": impact_analysis,
        "follow_up": follow_up,
    }


def sort_action_suggestions(actions: list[dict[str, object]]) -> list[dict[str, object]]:
    priority_order = {"high": 0, "medium": 1, "low": 2}
    return sorted(
        actions,
        key=lambda item: (
            priority_order.get(str(item.get("priority", "medium")), 9),
            str(item.get("type", "")),
        ),
    )


def render_cli_command(parts: list[str]) -> str:
    return shlex.join(parts)


def build_enable_command(
    script_path: Path,
    skill_name: str,
    project_root: str,
    library_root: Path,
    exposure_mode: str | None = None,
) -> str:
    command = [
        "python3",
        str(script_path),
        "enable",
        skill_name,
        "--project",
        project_root,
        "--library-root",
        str(library_root),
    ]
    if exposure_mode in {"symlink", "copy"}:
        command.extend(["--exposure-mode", exposure_mode])
    return render_cli_command(command)


def build_repair_plan(
    ctx: ExecutionContext,
    skill_name: str | None,
    project_link: dict[str, object] | None,
    impact_analysis: dict[str, object] | None,
) -> dict[str, object]:
    steps: list[dict[str, object]] = []
    if not skill_name:
        return {"autofix_ready_steps": 0, "manual_steps": 0, "steps": steps}

    script_path = ctx.runtime_skill_dir / "scripts" / "manage_skill.py"
    seen: set[tuple[str, str]] = set()

    def add_enable_step(
        *,
        step_type: str,
        priority: str,
        summary: str,
        project_root: str,
        reason: str,
        exposure_mode: str | None = None,
    ) -> None:
        dedupe_key = (step_type, project_root)
        if dedupe_key in seen:
            return
        seen.add(dedupe_key)
        steps.append(
            {
                "type": step_type,
                "priority": priority,
                "automatic": True,
                "project_root": project_root,
                "reason": reason,
                "exposure_mode": exposure_mode,
                "command": build_enable_command(
                    script_path,
                    skill_name,
                    project_root,
                    ctx.library_root,
                    exposure_mode=exposure_mode,
                ),
                "summary": summary,
            }
        )

    def add_manual_blocker_step(
        *,
        project_root: str,
        reason: str,
        path: str,
        exposure_mode: str | None = None,
    ) -> None:
        dedupe_key = ("clear-project-exposure-blocker", project_root)
        if dedupe_key in seen:
            return
        seen.add(dedupe_key)
        steps.append(
            {
                "type": "clear-project-exposure-blocker",
                "priority": "high",
                "automatic": False,
                "project_root": project_root,
                "reason": reason,
                "exposure_mode": exposure_mode,
                "path": path,
                "summary": f"Remove the blocker at {path} before recreating the managed exposure.",
                "next_command": build_enable_command(
                    script_path,
                    skill_name,
                    project_root,
                    ctx.library_root,
                    exposure_mode=exposure_mode,
                ),
            }
        )

    def add_steps_for_project_status(
        *,
        project_root: str,
        status: str,
        path: str | None = None,
        managed_mode: str | None = None,
    ) -> None:
        if status == "missing":
            add_enable_step(
                step_type="enable-missing-project-exposure",
                priority="medium",
                summary=f"Enable {skill_name} for the current project.",
                project_root=project_root,
                reason="missing exposure",
                exposure_mode=managed_mode,
            )
        elif status == "broken symlink":
            add_enable_step(
                step_type="repair-broken-project-exposure",
                priority="high",
                summary=f"Rebuild the broken managed exposure for {skill_name} in {project_root}.",
                project_root=project_root,
                reason=status,
                exposure_mode=managed_mode,
            )
        elif status == "managed copy":
            add_enable_step(
                step_type="refresh-copy-project-exposure",
                priority="medium",
                summary=f"Refresh the copy-based managed exposure for {skill_name} in {project_root}.",
                project_root=project_root,
                reason=status,
                exposure_mode="copy",
            )
        elif status in {"external symlink", "shared-library link to another skill"}:
            add_enable_step(
                step_type="normalize-project-exposure",
                priority="high",
                summary=f"Repoint the project exposure for {skill_name} in {project_root} back to the managed canonical skill.",
                project_root=project_root,
                reason=status,
                exposure_mode=managed_mode,
            )
        elif status in {"local directory (not a managed exposure)", "non-directory entry"} and path is not None:
            add_manual_blocker_step(
                project_root=project_root,
                reason=status,
                path=path,
                exposure_mode=managed_mode,
            )

    if project_link is not None and ctx.project_root is not None:
        add_steps_for_project_status(
            project_root=str(ctx.project_root),
            status=str(project_link["status"]),
            path=str(project_link["path"]),
            managed_mode=(
                str(project_link["managed_mode"])
                if isinstance(project_link.get("managed_mode"), str)
                else None
            ),
        )

    if impact_analysis is not None:
        for entry in impact_analysis["projects"]:
            add_steps_for_project_status(
                project_root=str(entry["project_root"]),
                status=str(entry["status"]),
                path=str(entry["path"]) if entry.get("path") else None,
                managed_mode=(
                    str(entry["managed_mode"])
                    if isinstance(entry.get("managed_mode"), str)
                    else None
                ),
            )

    steps = sort_action_suggestions(steps)
    return {
        "autofix_ready_steps": sum(1 for step in steps if bool(step.get("automatic"))),
        "manual_steps": sum(1 for step in steps if not bool(step.get("automatic"))),
        "steps": steps,
    }


def build_work_queue(
    actions: list[dict[str, object]],
    repair_plan: dict[str, object] | None,
) -> dict[str, object]:
    safe_auto_fix: list[dict[str, object]] = []
    manual_cleanup_first: list[dict[str, object]] = []
    governance_review: list[dict[str, object]] = []

    if repair_plan is not None:
        for step in repair_plan["steps"]:
            if bool(step.get("automatic")):
                safe_auto_fix.append(step)
            else:
                manual_cleanup_first.append(step)

    for action in actions:
        if str(action.get("type")) in GOVERNANCE_REVIEW_ACTION_TYPES:
            governance_review.append(action)

    safe_auto_fix = sort_action_suggestions(safe_auto_fix)
    manual_cleanup_first = sort_action_suggestions(manual_cleanup_first)
    governance_review = sort_action_suggestions(governance_review)

    return {
        "counts": {
            "safe_auto_fix": len(safe_auto_fix),
            "manual_cleanup_first": len(manual_cleanup_first),
            "governance_review": len(governance_review),
        },
        "safe_auto_fix": safe_auto_fix,
        "manual_cleanup_first": manual_cleanup_first,
        "governance_review": governance_review,
    }


def build_batch_repair_preview(
    skill_name: str | None,
    work_queue: dict[str, object] | None,
) -> dict[str, object]:
    if not skill_name or work_queue is None:
        return {
            "eligible_steps": 0,
            "projects_total": 0,
            "projects": [],
            "commands": [],
            "summary": "No batch repair preview is available.",
        }

    commands: list[dict[str, object]] = []
    projects: set[str] = set()
    for step in work_queue["safe_auto_fix"]:
        command = step.get("command")
        if not command:
            continue
        project_root = str(step.get("project_root", ""))
        if project_root:
            projects.add(project_root)
        commands.append(
            {
                "type": str(step["type"]),
                "priority": str(step["priority"]),
                "project_root": project_root or None,
                "reason": str(step.get("reason", "")) or None,
                "exposure_mode": str(step.get("exposure_mode")) if step.get("exposure_mode") else None,
                "summary": str(step["summary"]),
                "command": str(command),
            }
        )

    eligible_steps = len(commands)
    projects_list = sorted(projects)
    if eligible_steps == 0:
        summary = f"No safe auto-fix batch actions are currently queued for {skill_name}."
    else:
        summary = (
            f"{eligible_steps} safe auto-fix step(s) across {len(projects_list)} project(s) "
            f"could be executed in a future batch repair run for {skill_name}."
        )

    return {
        "eligible_steps": eligible_steps,
        "projects_total": len(projects_list),
        "projects": projects_list,
        "commands": commands,
        "summary": summary,
    }


def execute_safe_auto_fix_queue(
    ctx: ExecutionContext,
    skill_name: str,
    payload: dict[str, object],
) -> int:
    work_queue = payload.get("work_queue")
    batch_preview = payload.get("batch_repair_preview")
    if work_queue is None or batch_preview is None:
        print("[ERROR] Repair queue is unavailable for this skill.")
        return 1

    safe_steps = list(work_queue["safe_auto_fix"])
    manual_count = int(work_queue["counts"]["manual_cleanup_first"])
    governance_count = int(work_queue["counts"]["governance_review"])

    print(
        "[REPAIR] Safe auto-fix queue: "
        f"{len(safe_steps)} step(s), "
        f"manual_cleanup_first={manual_count}, "
        f"governance_review={governance_count}"
    )
    print(f"[REPAIR] {batch_preview['summary']}")

    if not safe_steps:
        print("[NEXT] No safe auto-fix steps were queued.")
        return 0

    canonical_dir = ensure_existing_skill_dir(ctx.library_root, skill_name)
    failures = 0
    for step in safe_steps:
        project_root = Path(str(step["project_root"])).resolve()
        config, config_error = safe_load_project_config(project_root)
        if config_error:
            print(f"[ERROR] Could not load project config for {project_root}: {config_error}")
            failures += 1
            continue
        exposure_root = detect_exposure_root(None, config, project_root)
        if exposure_root is None:
            print(f"[ERROR] Could not determine an exposure root for {project_root}.")
            failures += 1
            continue

        requested_mode = (
            str(step["exposure_mode"])
            if isinstance(step.get("exposure_mode"), str) and step.get("exposure_mode")
            else None
        )
        effective_mode = resolve_exposure_mode(requested_mode, config)

        try:
            link_status, project_link, registry_status = ensure_project_exposure(
                exposure_root,
                skill_name,
                canonical_dir,
                effective_mode,
                dry_run=ctx.args.dry_run,
            )
        except (FileExistsError, FileNotFoundError, NotADirectoryError, ValueError) as error:
            print(f"[ERROR] Repair step failed for {project_root}: {error}")
            failures += 1
            continue

        print(
            f"[OK] Repair step ({step['type']}, {link_status}): "
            f"{project_link}"
        )
        print(
            f"[OK] Exposure registry ({registry_status}): "
            f"{managed_exposure_registry_path(exposure_root)}"
        )

    if manual_count > 0:
        print(
            f"[NEXT] {manual_count} manual cleanup item(s) remain before the queue is fully clean."
        )
    if governance_count > 0:
        print(
            f"[NEXT] {governance_count} governance review item(s) remain after safe auto-fix."
        )

    return 0 if failures == 0 else 1


def build_action_suggestions(
    skill_name: str | None,
    canonical_path: Path | None,
    duplicate_canonical_copy: bool,
    governance: dict[str, object] | None,
    impact_analysis: dict[str, object] | None,
) -> list[dict[str, object]]:
    actions: list[dict[str, object]] = []
    if not skill_name:
        return actions

    if duplicate_canonical_copy and canonical_path is not None:
        actions.append(
            {
                "type": "resolve-duplicate-canonical",
                "priority": "high",
                "summary": f"Resolve the duplicate canonical copy and keep one source of truth for {skill_name}.",
                "next_step": f"Keep or refresh the canonical skill at {canonical_path}, then remove or rename the duplicate copy.",
            }
        )

    if governance is not None:
        signals = governance["signals"]
        missing_sections = list(signals["sections_missing"])
        if missing_sections:
            actions.append(
                {
                    "type": "improve-skill-docs",
                    "priority": "medium",
                    "summary": f"Strengthen SKILL.md so {skill_name} is easier to maintain and discover.",
                    "missing_sections": missing_sections,
                    "next_step": "Add or improve the missing sections in SKILL.md, especially workflow and example requests.",
                }
            )

        duplicate_candidates = list(governance["duplicate_candidates"])
        if duplicate_candidates:
            top_candidate = duplicate_candidates[0]
            top_similarity = float(top_candidate["similarity"])
            if top_similarity >= 0.8:
                actions.append(
                    {
                        "type": "review-overlap",
                        "priority": "high",
                        "summary": f"{skill_name} strongly overlaps with {top_candidate['name']}.",
                        "related_skills": [top_candidate["name"]],
                        "next_step": (
                            f"Review whether {skill_name} should merge into {top_candidate['name']}, "
                            "be deprecated, or be renamed to reduce overlap."
                        ),
                    }
                )
            elif top_similarity >= 0.55:
                actions.append(
                    {
                        "type": "review-overlap",
                        "priority": "medium",
                        "summary": f"{skill_name} may overlap with {top_candidate['name']}.",
                        "related_skills": [top_candidate["name"]],
                        "next_step": f"Compare triggers and examples for {skill_name} and {top_candidate['name']} before adding more variants.",
                    }
                )

    if impact_analysis is not None:
        counts = impact_analysis["counts"]
        reference_graph = impact_analysis["reference_graph"]
        copy_projects = list(reference_graph["copy_projects"])
        manifest_projects = list(reference_graph["manifest_projects"])
        broken_projects = list(reference_graph["broken_projects"])
        blocked_projects = list(reference_graph["blocked_projects"])

        if copy_projects:
            actions.append(
                {
                    "type": "refresh-copy-exposures",
                    "priority": "medium",
                    "summary": f"{len(copy_projects)} project(s) use copy exposure for {skill_name}.",
                    "projects": copy_projects,
                    "next_step": "After upgrades, re-run enable or refresh the copy-based project exposures.",
                }
            )

        if manifest_projects:
            actions.append(
                {
                    "type": "review-manifest-exposures",
                    "priority": "low",
                    "summary": f"{len(manifest_projects)} project(s) use manifest exposure for {skill_name}.",
                    "projects": manifest_projects,
                    "next_step": "Keep manifest mode for CI/governance-only usage, or switch to symlink/copy when the project needs a direct runtime exposure.",
                }
            )

        if broken_projects:
            actions.append(
                {
                    "type": "repair-broken-exposures",
                    "priority": "high",
                    "summary": f"{len(broken_projects)} project exposure(s) for {skill_name} are broken.",
                    "projects": broken_projects,
                    "next_step": "Repair each broken project exposure before retire, migration, or large refactors.",
                }
            )

        if blocked_projects:
            actions.append(
                {
                    "type": "cleanup-blocked-exposures",
                    "priority": "high",
                    "summary": f"{len(blocked_projects)} project exposure path(s) are blocked for {skill_name}.",
                    "projects": blocked_projects,
                    "next_step": "Remove unmanaged blockers in the project exposure path, then recreate the managed exposure.",
                }
            )

        if (
            governance is not None
            and int(governance["health_score"]) < 70
            and int(reference_graph["active_projects_total"]) == 0
        ):
            actions.append(
                {
                    "type": "consider-retire-candidate",
                    "priority": "low",
                    "summary": f"{skill_name} currently has no active project dependents and a low health score.",
                    "next_step": "Consider deprecating, archiving, or consolidating this skill after reviewing whether it is still needed.",
                }
            )

        if counts["external"] > 0:
            actions.append(
                {
                    "type": "normalize-external-exposures",
                    "priority": "medium",
                    "summary": f"{counts['external']} project exposure(s) point outside the managed canonical path.",
                    "next_step": "Normalize external links so projects point back to the managed canonical skill.",
                }
            )

    return sort_action_suggestions(actions)


def report_task_impact_summary(summary: dict[str, object]) -> None:
    action = str(summary["action"])
    skill_name = str(summary["skill_name"])
    impact_analysis = summary["impact_analysis"]
    counts = impact_analysis["counts"]
    reference_graph = impact_analysis["reference_graph"]
    preview = bool(summary.get("preview"))

    if action == "upgrade":
        print(
            f"[IMPACT] Active projects using {skill_name}: "
            f"{reference_graph['active_projects_total']}"
        )
    elif action == "retire":
        label = "Other active projects after retire" if preview else "Remaining active projects"
        value = (
            reference_graph["other_active_projects_total"]
            if preview
            else reference_graph["active_projects_total"]
        )
        print(f"[IMPACT] {label} for {skill_name}: {value}")

    print(
        "[IMPACT] Exposure modes: "
        f"symlink={counts['managed_symlink']}, "
        f"copy={counts['managed_copy']}, "
        f"manifest={counts['managed_manifest']}, "
        f"broken={counts['broken']}, "
        f"blocked={counts['blocked']}"
    )

    for message in summary["follow_up"]:
        print(f"[IMPACT] {message}")


def collect_library_skills(library_root: Path) -> dict[str, object]:
    skill_dirs = []
    if library_root.exists():
        skill_dirs = sorted(
            child for child in library_root.iterdir() if child.is_dir() and (child / "SKILL.md").exists()
        )
    skills = [summarize_skill_metadata(skill_dir) for skill_dir in skill_dirs]
    return {
        "mode": "list-library-skills",
        "library_root": str(library_root),
        "library_root_exists": library_root.exists(),
        "count": len(skills),
        "skills": skills,
    }


def list_library_skills(library_root: Path, output_format: str = "text") -> int:
    payload = collect_library_skills(library_root)
    if output_format == "json":
        return emit_json(payload)

    print(f"[LIST] Library root: {library_root}")
    if not payload["library_root_exists"]:
        print("[LIST] Library root does not exist.")
        return 0

    skills = payload["skills"]
    if not skills:
        print("[LIST] No canonical skills found.")
        return 0

    for summary in skills:
        print(f"[SKILL] {summary['name']}")
        print(f"  path: {summary['path']}")
        if summary.get("display_name"):
            print(f"  display_name: {summary['display_name']}")
        if summary.get("short_description"):
            print(f"  short_description: {summary['short_description']}")
        if summary.get("description"):
            print(f"  description: {summary['description']}")
    print(f"[NEXT] Listed {payload['count']} canonical skill(s).")
    return 0


def summarize_exposure_entry(
    entry: Path,
    library_root: Path,
    exposure_registry: dict[str, dict[str, str]],
    source_registry: dict[str, dict[str, str]],
) -> dict[str, object]:
    entry_payload: dict[str, object] = {
        "name": entry.name,
        "path": str(entry),
    }
    registry_entry = exposure_registry.get(entry.name)

    if entry.is_symlink():
        target = Path(os.path.realpath(entry))
        if not target.exists():
            status = "broken symlink"
        elif target.parent == library_root:
            status = "managed symlink"
        else:
            status = "external symlink"
        entry_payload["status"] = status
        entry_payload["target"] = str(target)
        if registry_entry and registry_entry.get("mode"):
            entry_payload["managed_mode"] = registry_entry["mode"]
        if target.exists() and (target / "SKILL.md").exists():
            summary = summarize_skill_metadata(target)
            if summary.get("display_name"):
                entry_payload["display_name"] = summary["display_name"]
            if summary.get("short_description"):
                entry_payload["short_description"] = summary["short_description"]
    elif entry.is_dir():
        if registry_entry and registry_entry.get("mode") == "copy":
            status = "managed copy"
            entry_payload["managed_mode"] = "copy"
            canonical_path = registry_entry.get("canonical_path")
            if canonical_path:
                entry_payload["target"] = canonical_path
            if (entry / "SKILL.md").exists():
                summary = summarize_skill_metadata(entry)
                if summary.get("display_name"):
                    entry_payload["display_name"] = summary["display_name"]
                if summary.get("short_description"):
                    entry_payload["short_description"] = summary["short_description"]
        else:
            status = "local directory (not a managed exposure)"
        entry_payload["status"] = status
    else:
        entry_payload["status"] = "non-directory entry"

    source_entry = source_registry.get(entry.name)
    if source_entry and source_entry.get("source_path"):
        entry_payload["source_path"] = source_entry["source_path"]
        if source_entry.get("import_mode"):
            entry_payload["source_import_mode"] = source_entry["import_mode"]
    return entry_payload


def summarize_registry_only_exposure(
    skill_name: str,
    project_root: Path,
    exposure_root: Path,
    library_root: Path,
    exposure_registry: dict[str, dict[str, str]],
    source_registry: dict[str, dict[str, str]],
) -> dict[str, object]:
    project_link = collect_project_link_status(
        project_root,
        exposure_root,
        library_root,
        skill_name,
    )
    entry_payload: dict[str, object] = {
        "name": skill_name,
        "path": str(project_link["path"]),
        "status": str(project_link["status"]),
    }
    if project_link.get("target"):
        entry_payload["target"] = str(project_link["target"])
    if project_link.get("managed_mode"):
        entry_payload["managed_mode"] = str(project_link["managed_mode"])
    source_entry = source_registry.get(skill_name)
    if source_entry and source_entry.get("source_path"):
        entry_payload["source_path"] = source_entry["source_path"]
        if source_entry.get("import_mode"):
            entry_payload["source_import_mode"] = source_entry["import_mode"]
    return entry_payload


def collect_project_skills(
    project_root: Path,
    library_root: Path,
    exposure_root: Path | None,
) -> dict[str, object]:
    skills_dir = exposure_root or (project_root / ".agents" / "skills")
    source_registry = load_external_source_registry(project_root)
    exposure_registry = load_managed_exposure_registry(exposure_root)
    payload: dict[str, object] = {
        "mode": "list-project-skills",
        "project_root": str(project_root),
        "skills_directory": str(skills_dir),
        "skills_directory_exists": skills_dir.exists(),
        "count": 0,
        "entries": [],
    }
    seen_names: set[str] = set()
    if skills_dir.exists():
        entries = sorted(skills_dir.iterdir(), key=lambda path: path.name)
        for entry in entries:
            payload["entries"].append(
                summarize_exposure_entry(
                    entry,
                    library_root,
                    exposure_registry,
                    source_registry,
                )
            )
            seen_names.add(entry.name)

    for skill_name, entry in sorted(exposure_registry.items()):
        if skill_name in seen_names:
            continue
        if entry.get("mode") != "manifest":
            continue
        payload["entries"].append(
            summarize_registry_only_exposure(
                skill_name,
                project_root,
                skills_dir,
                library_root,
                exposure_registry,
                source_registry,
            )
        )

    payload["count"] = len(payload["entries"])
    return payload


def list_project_skills(
    project_root: Path,
    library_root: Path,
    exposure_root: Path | None,
    output_format: str = "text",
) -> int:
    payload = collect_project_skills(project_root, library_root, exposure_root)
    if output_format == "json":
        return emit_json(payload)

    print(f"[LIST] Project root: {project_root}")
    print(f"[LIST] Skills directory: {payload['skills_directory']}")
    if not payload["skills_directory_exists"] and not payload["entries"]:
        print("[LIST] Project skills directory does not exist.")
        return 0

    entries = payload["entries"]
    if not entries:
        print("[LIST] Project skills directory is empty.")
        return 0

    for entry in entries:
        print(f"[PROJECT-SKILL] {entry['name']}")
        print(f"  path: {entry['path']}")
        print(f"  status: {entry['status']}")
        if entry.get("target"):
            print(f"  target: {entry['target']}")
        if entry.get("managed_mode"):
            print(f"  managed_mode: {entry['managed_mode']}")
        if entry.get("display_name"):
            print(f"  display_name: {entry['display_name']}")
        if entry.get("short_description"):
            print(f"  short_description: {entry['short_description']}")
        if entry.get("source_path"):
            print(f"  source_path: {entry['source_path']}")
        if entry.get("source_import_mode"):
            print(f"  source_import_mode: {entry['source_import_mode']}")
    print(f"[NEXT] Listed {payload['count']} project skill entries.")
    return 0


def ensure_symlink(link_path: Path, target_path: Path, dry_run: bool = False) -> str:
    link_path.parent.mkdir(parents=True, exist_ok=True)
    if link_path.is_symlink():
        current_target = Path(os.path.realpath(link_path))
        if current_target == target_path.resolve():
            return "kept"
        if dry_run:
            return "would relink"
        link_path.unlink()
    elif link_path.exists():
        raise FileExistsError(
            f"Cannot create symlink at {link_path}: a non-symlink path already exists."
        )

    if dry_run:
        return "would link"
    relative_target = os.path.relpath(target_path, start=link_path.parent)
    link_path.symlink_to(relative_target)
    return "linked"


def unlink_symlink(link_path: Path, dry_run: bool = False) -> str:
    if link_path.is_symlink():
        if dry_run:
            return "would unlink"
        link_path.unlink()
        return "unlinked"
    if not link_path.exists():
        return "absent"
    raise FileExistsError(
        f"Cannot unlink {link_path}: the path exists but is not a symlink."
    )


def remove_path(path: Path, dry_run: bool = False) -> str:
    if path.is_symlink():
        if dry_run:
            return "would remove symlink"
        path.unlink()
        return "removed symlink"
    if not path.exists():
        return "absent"
    if path.is_dir():
        if dry_run:
            return "would remove"
        shutil.rmtree(path)
        return "removed"
    if dry_run:
        return "would remove file"
    path.unlink()
    return "removed file"


def ensure_copy_exposure(
    exposure_path: Path,
    target_path: Path,
    registry_entry: dict[str, str] | None,
    dry_run: bool = False,
) -> str:
    managed_copy = (
        registry_entry is not None
        and registry_entry.get("mode") == "copy"
        and registry_entry.get("canonical_path") == str(target_path.resolve())
    )

    if exposure_path.is_symlink():
        if dry_run:
            return "would replace symlink with copy"
        exposure_path.unlink()
    elif exposure_path.exists():
        if not managed_copy or not exposure_path.is_dir():
            raise FileExistsError(
                f"Cannot create managed copy at {exposure_path}: a non-managed entry already exists."
            )
        if dry_run:
            return "would refresh copy"
        shutil.rmtree(exposure_path)

    if dry_run:
        return "would refresh copy" if managed_copy else "would copy"

    exposure_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(target_path, exposure_path, symlinks=True)
    return "refreshed copy" if managed_copy else "copied"


def ensure_manifest_exposure(
    exposure_path: Path,
    target_path: Path,
    registry_entry: dict[str, str] | None,
    dry_run: bool = False,
) -> str:
    managed_entry = (
        registry_entry is not None
        and registry_entry.get("canonical_path") == str(target_path.resolve())
        and registry_entry.get("mode") in {"symlink", "copy", "manifest"}
    )
    if exposure_path.is_symlink():
        if not managed_entry:
            raise FileExistsError(
                f"Cannot switch {exposure_path} to manifest mode: the existing symlink is not managed."
            )
        if dry_run:
            return "would replace symlink with manifest"
        exposure_path.unlink()
        return "replaced symlink with manifest"
    if exposure_path.exists():
        if not managed_entry or not exposure_path.is_dir():
            raise FileExistsError(
                f"Cannot switch {exposure_path} to manifest mode: a non-managed entry already exists."
            )
        if dry_run:
            return "would replace copy with manifest"
        shutil.rmtree(exposure_path)
        return "replaced copy with manifest"
    return "would record manifest" if dry_run else "recorded manifest"


def ensure_project_exposure(
    exposure_root: Path,
    skill_name: str,
    target_path: Path,
    exposure_mode: str,
    dry_run: bool = False,
) -> tuple[str, Path, str]:
    exposure_path = exposure_root / skill_name
    registry = load_managed_exposure_registry(exposure_root)
    registry_entry = registry.get(skill_name)

    if exposure_mode == "symlink":
        status = ensure_symlink(exposure_path, target_path, dry_run=dry_run)
    elif exposure_mode == "copy":
        status = ensure_copy_exposure(
            exposure_path,
            target_path,
            registry_entry,
            dry_run=dry_run,
        )
    elif exposure_mode == "manifest":
        status = ensure_manifest_exposure(
            exposure_path,
            target_path,
            registry_entry,
            dry_run=dry_run,
        )
    else:
        raise ValueError(f"Unsupported exposure mode: {exposure_mode}")

    updated_registry = dict(registry)
    updated_registry[skill_name] = {
        "canonical_path": str(target_path.resolve()),
        "exposure_path": str(exposure_path.resolve(strict=False)),
        "mode": exposure_mode,
    }
    registry_status = write_managed_exposure_registry(
        exposure_root,
        updated_registry,
        dry_run=dry_run,
    )
    manifest_status = write_exposure_manifest(
        exposure_root,
        updated_registry,
        dry_run=dry_run,
    )
    return f"{status}; manifest {manifest_status}", exposure_path, registry_status


def unlink_project_exposure(
    exposure_root: Path,
    skill_name: str,
    dry_run: bool = False,
) -> tuple[str, Path, str]:
    exposure_path = exposure_root / skill_name
    registry = load_managed_exposure_registry(exposure_root)
    registry_entry = registry.get(skill_name)

    if exposure_path.is_symlink():
        status = unlink_symlink(exposure_path, dry_run=dry_run)
    elif exposure_path.exists():
        if registry_entry and registry_entry.get("mode") == "copy":
            status = remove_path(exposure_path, dry_run=dry_run)
        else:
            raise FileExistsError(
                f"Cannot remove {exposure_path}: the path exists but is not a managed exposure."
            )
    else:
        status = "absent"

    updated_registry = dict(registry)
    if skill_name in updated_registry:
        updated_registry.pop(skill_name)
    registry_status = write_managed_exposure_registry(
        exposure_root,
        updated_registry,
        dry_run=dry_run,
    )
    write_exposure_manifest(
        exposure_root,
        updated_registry,
        dry_run=dry_run,
    )
    return status, exposure_path, registry_status


def ensure_existing_skill_dir(library_root: Path, skill_name: str) -> Path:
    skill_dir = library_root / skill_name
    if not skill_dir.exists():
        raise FileNotFoundError(
            f"Canonical skill not found for '{skill_name}': {skill_dir}"
        )
    return skill_dir


def list_managed_project_links(
    exposure_root: Path,
    library_root: Path,
) -> dict[str, Path]:
    skills_dir = exposure_root
    registry = load_managed_exposure_registry(exposure_root)
    result = {}
    if skills_dir.exists():
        for child in skills_dir.iterdir():
            if child.is_symlink():
                target = Path(os.path.realpath(child))
                if target.parent == library_root:
                    result[child.name] = child
                continue
            registry_entry = registry.get(child.name)
            if child.is_dir() and registry_entry and registry_entry.get("mode") == "copy":
                result[child.name] = child
    for skill_name, entry in registry.items():
        if entry.get("mode") == "manifest" and skill_name not in result:
            result[skill_name] = skills_dir / skill_name
    return result


def validate_skill_dir(skill_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append("SKILL.md not found.")
        return errors, warnings

    content = skill_md.read_text()
    frontmatter, _body = split_frontmatter(content)
    if frontmatter is None:
        errors.append("SKILL.md is missing YAML frontmatter.")
        return errors, warnings

    name = extract_frontmatter_value(content, "name")
    description = extract_frontmatter_value(content, "description")
    if not name:
        errors.append("Frontmatter is missing 'name'.")
    elif not re.match(r"^[a-z0-9-]+$", name):
        errors.append(f"Frontmatter name '{name}' must be hyphen-case.")
    elif len(name) > MAX_NAME_LENGTH:
        errors.append(
            f"Frontmatter name '{name}' is too long ({len(name)} characters)."
        )
    elif name != skill_dir.name:
        warnings.append(
            f"Frontmatter name '{name}' does not match directory name '{skill_dir.name}'."
        )

    if description is None:
        errors.append("Frontmatter is missing 'description'.")
    else:
        if "<" in description or ">" in description:
            errors.append("Description cannot contain angle brackets.")
        if len(description) > 1024:
            errors.append(
                f"Description is too long ({len(description)} characters)."
            )

    openai_path = skill_dir / "agents" / "openai.yaml"
    if not openai_path.exists():
        errors.append("agents/openai.yaml not found.")
        return errors, warnings

    interface = parse_openai_interface(openai_path.read_text())
    if not interface.get("display_name"):
        errors.append("agents/openai.yaml is missing interface.display_name.")
    short_description = interface.get("short_description", "")
    if not short_description:
        errors.append("agents/openai.yaml is missing interface.short_description.")
    elif not (25 <= len(short_description) <= 64):
        errors.append(
            "interface.short_description must be between 25 and 64 characters."
        )
    default_prompt = interface.get("default_prompt", "")
    if not default_prompt:
        warnings.append("agents/openai.yaml is missing interface.default_prompt.")
    elif name and f"${name}" not in default_prompt:
        warnings.append(
            f"interface.default_prompt does not reference ${name}."
        )

    return errors, warnings


def collect_validation_result(skill_dir: Path) -> dict[str, object]:
    errors, warnings = validate_skill_dir(skill_dir)
    return {
        "mode": "validate-only",
        "target": str(skill_dir),
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
    }


def report_validation(skill_dir: Path, output_format: str = "text") -> int:
    payload = collect_validation_result(skill_dir)
    if output_format == "json":
        return emit_json(payload)

    errors = payload["errors"]
    warnings = payload["warnings"]
    if errors:
        print(f"[ERROR] Validation failed for {skill_dir}")
        for error in errors:
            print(f"  - {error}")
        for warning in warnings:
            print(f"  - Warning: {warning}")
        return 1

    print(f"[OK] Validation passed: {skill_dir}")
    for warning in warnings:
        print(f"  - Warning: {warning}")
    return 0


def resolve_validate_target(
    skill_name: str,
    import_path: Path | None,
    library_root: Path,
    runtime_skill_dir: Path,
) -> Path:
    if import_path is not None:
        return import_path
    if skill_name:
        return library_root / skill_name
    return runtime_skill_dir


def resolve_effective_skill_name(
    target_dir: Path,
    fallback_name: str,
) -> str:
    if target_dir.exists() and target_dir.is_dir() and (target_dir / "SKILL.md").exists():
        detected_name = detect_skill_name_from_source(target_dir)
        if detected_name:
            return detected_name
    if fallback_name:
        return fallback_name
    return normalize_skill_name(target_dir.name)


def collect_project_link_status(
    project_root: Path,
    exposure_root: Path | None,
    library_root: Path,
    skill_name: str,
) -> dict[str, object]:
    canonical_path = library_root / skill_name
    resolved_exposure_root = exposure_root or (project_root / ".agents" / "skills")
    project_link = resolved_exposure_root / skill_name
    exposure_registry = load_managed_exposure_registry(exposure_root)
    registry_entry = exposure_registry.get(skill_name)
    payload: dict[str, object] = {
        "project_root": str(project_root),
        "path": str(project_link),
        "exists": project_link.exists() or project_link.is_symlink(),
    }

    if registry_entry and registry_entry.get("mode") == "manifest" and not payload["exists"]:
        payload["status"] = "managed manifest"
        payload["target"] = registry_entry.get("canonical_path")
        payload["managed_mode"] = "manifest"
        return payload

    if project_link.is_symlink():
        target = Path(os.path.realpath(project_link))
        payload["target"] = str(target)
        if not target.exists():
            payload["status"] = "broken symlink"
        elif target == canonical_path.resolve(strict=False):
            payload["status"] = "managed symlink"
        elif target.parent == library_root:
            payload["status"] = "shared-library link to another skill"
        else:
            payload["status"] = "external symlink"
        if registry_entry and registry_entry.get("mode"):
            payload["managed_mode"] = registry_entry["mode"]
        return payload

    if project_link.exists():
        if project_link.is_dir():
            if registry_entry and registry_entry.get("mode") == "copy":
                payload["status"] = "managed copy"
                if registry_entry.get("canonical_path"):
                    payload["target"] = registry_entry["canonical_path"]
                payload["managed_mode"] = "copy"
            elif registry_entry and registry_entry.get("mode") == "manifest":
                payload["status"] = "managed manifest"
                if registry_entry.get("canonical_path"):
                    payload["target"] = registry_entry["canonical_path"]
                payload["managed_mode"] = "manifest"
            else:
                payload["status"] = "local directory (not a managed exposure)"
        else:
            payload["status"] = "non-directory entry"
        return payload

    payload["status"] = "missing"
    return payload


def collect_doctor_result(ctx: ExecutionContext) -> dict[str, object]:
    target_dir = resolve_validate_target(
        ctx.skill_name,
        ctx.import_path,
        ctx.library_root,
        ctx.runtime_skill_dir,
    )
    target_exists = target_dir.exists()
    target_is_dir = target_dir.is_dir() if target_exists else False
    effective_skill_name = resolve_effective_skill_name(target_dir, ctx.skill_name)
    canonical_path = ctx.library_root / effective_skill_name if effective_skill_name else None
    canonical_exists = bool(canonical_path and canonical_path.exists())

    if not target_exists:
        target_location = "missing target"
    elif not target_is_dir:
        target_location = "non-directory target"
    elif canonical_path and target_dir.resolve() == canonical_path.resolve(strict=False):
        target_location = "canonical shared-library skill"
    elif target_dir.resolve() == ctx.runtime_skill_dir.resolve():
        target_location = "runtime package outside shared library"
    elif path_is_within(target_dir, ctx.library_root):
        target_location = "shared-library entry"
    elif ctx.project_root and path_is_within(target_dir, ctx.project_root):
        target_location = "project-local skill directory"
    elif ctx.import_path is not None:
        target_location = "external import candidate"
    else:
        target_location = "external skill directory"

    validation: dict[str, object] | None = None
    issues: list[str] = []
    recommendations: list[str] = []
    duplicate_canonical_copy = False
    governance: dict[str, object] | None = None
    impact_analysis: dict[str, object] | None = None
    action_suggestions: list[dict[str, object]] = []
    repair_plan: dict[str, object] | None = None
    work_queue: dict[str, object] | None = None
    batch_repair_preview: dict[str, object] | None = None

    if not target_exists:
        issues.append(f"Target does not exist: {target_dir}")
        recommendations.append(
            "Create or import the skill before using it as a managed shared-library package."
        )
    elif not target_is_dir:
        issues.append(f"Target is not a directory: {target_dir}")
        recommendations.append(
            "Point doctor at a skill directory instead of a file or other filesystem entry."
        )
    else:
        validation = collect_validation_result(target_dir)
        validation_errors = validation["errors"]
        if validation_errors:
            issues.extend(str(error) for error in validation_errors)
            recommendations.append(
                "Fix the structural errors in SKILL.md and agents/openai.yaml before relying on this skill."
            )
        if (
            canonical_path
            and target_dir.resolve() != canonical_path.resolve(strict=False)
            and canonical_exists
        ):
            duplicate_canonical_copy = True
            issues.append(f"Canonical copy already exists at {canonical_path}")
            if ctx.import_path is not None:
                recommendations.append(
                    "Import under a different canonical name, or update the existing shared-library copy instead of keeping two copies."
                )
            else:
                recommendations.append(
                    "Choose which copy should remain canonical, then remove or merge the duplicate."
                )

    if target_location == "runtime package outside shared library":
        recommendations.append(
            "Install or copy this package into $CODEX_HOME/skills when you want Codex to discover it directly as a shared skill."
        )

    project_link: dict[str, object] | None = None
    if ctx.project_root and effective_skill_name:
        project_link = collect_project_link_status(
            ctx.project_root,
            ctx.exposure_root,
            ctx.library_root,
            effective_skill_name,
        )
        project_status = str(project_link["status"])
        if project_status == "missing":
            recommendations.append(
                f"Enable {effective_skill_name} for the project so it appears under the managed exposure root."
            )
        elif project_status == "broken symlink":
            issues.append(f"Project link is broken: {project_link['path']}")
            recommendations.append(
                f"Rebuild the managed project exposure for {effective_skill_name} so it points to the canonical skill."
            )
        elif project_status == "shared-library link to another skill":
            issues.append(
                f"Project link points to a different shared-library skill: {project_link.get('target')}"
            )
            recommendations.append(
                f"Relink the project entry so {effective_skill_name} points to its own canonical directory."
            )
        elif project_status == "external symlink":
            issues.append(
                f"Project link points outside the shared library: {project_link.get('target')}"
            )
            recommendations.append(
                f"Replace the external project symlink with a managed link to {ctx.library_root / effective_skill_name}."
            )
        elif project_status in {"local directory (not a managed exposure)", "non-directory entry"}:
            issues.append(f"Project link path is blocked by an existing entry: {project_link['path']}")
            recommendations.append(
                f"Remove the blocker at {project_link['path']} and recreate the managed project link."
            )

    if target_exists and target_is_dir:
        target_summary = summarize_skill_metadata(target_dir)
        governance = build_governance_profile(
            target_dir,
            target_summary,
            validation,
            target_location,
            project_link,
            ctx.library_root,
        )
        recommendations.extend(
            suggestion
            for suggestion in governance["suggestions"]
            if suggestion not in recommendations
        )
        if effective_skill_name:
            impact_analysis = collect_impact_analysis(
                effective_skill_name,
                ctx.library_root,
                ctx.workspace_root,
                ctx.project_root,
            )
            if impact_analysis is not None:
                recommendations.extend(
                    suggestion
                    for suggestion in impact_analysis["recommendations"]
                    if suggestion not in recommendations
                )
        action_suggestions = build_action_suggestions(
            effective_skill_name or None,
            canonical_path,
            duplicate_canonical_copy,
            governance,
            impact_analysis,
        )
        repair_plan = build_repair_plan(
            ctx,
            effective_skill_name or None,
            project_link,
            impact_analysis,
        )
        work_queue = build_work_queue(action_suggestions, repair_plan)
        batch_repair_preview = build_batch_repair_preview(
            effective_skill_name or None,
            work_queue,
        )

    return {
        "mode": "doctor",
        "ok": not issues,
        "target": str(target_dir),
        "skill_name": effective_skill_name or None,
        "library_root": str(ctx.library_root),
        "runtime_skill_dir": str(ctx.runtime_skill_dir),
        "target_exists": target_exists,
        "target_is_directory": target_is_dir,
        "target_location": target_location,
        "canonical_path": str(canonical_path) if canonical_path else None,
        "canonical_exists": canonical_exists,
        "duplicate_canonical_copy": duplicate_canonical_copy,
        "validation": validation,
        "project_link": project_link,
        "governance": governance,
        "impact_analysis": impact_analysis,
        "actions": action_suggestions,
        "repair_plan": repair_plan,
        "work_queue": work_queue,
        "batch_repair_preview": batch_repair_preview,
        "issues": issues,
        "recommendations": recommendations,
    }


def report_doctor(ctx: ExecutionContext) -> int:
    payload = collect_doctor_result(ctx)
    if ctx.args.format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if payload["ok"] else 1

    print(f"[DOCTOR] Target: {payload['target']}")
    print(f"[DOCTOR] Library root: {payload['library_root']}")
    print(f"[DOCTOR] Runtime skill dir: {payload['runtime_skill_dir']}")
    if payload["skill_name"]:
        print(f"[DOCTOR] Skill name: {payload['skill_name']}")
    print(f"[DOCTOR] Target location: {payload['target_location']}")
    if payload["canonical_path"]:
        print(f"[DOCTOR] Canonical path: {payload['canonical_path']}")
        print(
            "[DOCTOR] Canonical status: "
            + ("present" if payload["canonical_exists"] else "missing")
        )

    validation = payload["validation"]
    if validation is None:
        print("[DOCTOR] Validation: skipped because the target is missing or not a directory.")
    elif validation["ok"]:
        print("[DOCTOR] Validation: passes structural checks.")
    else:
        print("[DOCTOR] Validation: has structural errors.")
        for error in validation["errors"]:
            print(f"  - {error}")
    if validation is not None:
        for warning in validation["warnings"]:
            print(f"  - Warning: {warning}")

    project_link = payload["project_link"]
    if project_link is not None:
        print(f"[DOCTOR] Project link: {project_link['status']}")
        print(f"[DOCTOR] Project link path: {project_link['path']}")
        if project_link.get("target"):
            print(f"[DOCTOR] Project link target: {project_link['target']}")
        if project_link.get("managed_mode"):
            print(f"[DOCTOR] Project link mode: {project_link['managed_mode']}")

    governance = payload.get("governance")
    if governance is not None:
        print(
            f"[DOCTOR] Health score: {governance['health_score']} "
            f"({governance['health_band']})"
        )
        dimensions = governance["dimensions"]
        print(
            "[DOCTOR] Quality dimensions: "
            f"struct={dimensions['structure_health']}, "
            f"content={dimensions['content_completeness']}, "
            f"discoverability={dimensions['discoverability']}, "
            f"reuse={dimensions['reuse_value']}, "
            f"risk={dimensions['maintenance_risk']}"
        )
        duplicate_candidates = governance["duplicate_candidates"]
        if duplicate_candidates:
            print("[DOCTOR] Similar skills:")
            for candidate in duplicate_candidates[:3]:
                print(
                    f"  - {candidate['name']} "
                    f"(similarity {candidate['similarity']}, shared terms: {', '.join(candidate['shared_terms']) or 'n/a'})"
                )

    impact_analysis = payload.get("impact_analysis")
    if impact_analysis is not None:
        counts = impact_analysis["counts"]
        reference_graph = impact_analysis["reference_graph"]
        print(
            "[DOCTOR] Impact summary: "
            f"projects={counts['projects_total']}, "
            f"active={reference_graph['active_projects_total']}, "
            f"managed_symlink={counts['managed_symlink']}, "
            f"managed_copy={counts['managed_copy']}, "
            f"managed_manifest={counts['managed_manifest']}, "
            f"broken={counts['broken']}, "
            f"blocked={counts['blocked']}"
        )
        print(
            "[DOCTOR] Reference graph: "
            f"current_project={reference_graph['current_project_status']}, "
            f"other_active={reference_graph['other_active_projects_total']}"
        )
        projects = impact_analysis["projects"]
        if projects:
            print("[DOCTOR] Impacted projects:")
            for project in projects[:5]:
                suffix = " (current project)" if project.get("is_current_project") else ""
                print(
                    f"  - {project['project_root']}: {project['status']}{suffix}"
                )

    actions = payload.get("actions") or []
    if actions:
        print("[DOCTOR] Suggested actions:")
        for action in actions[:6]:
            print(
                f"  - [{action['priority']}] {action['summary']}"
            )
            if action.get("next_step"):
                print(f"    Next: {action['next_step']}")

    repair_plan = payload.get("repair_plan")
    if repair_plan and repair_plan.get("steps"):
        print(
            "[DOCTOR] Repair plan: "
            f"autofix-ready={repair_plan['autofix_ready_steps']}, "
            f"manual={repair_plan['manual_steps']}"
        )
        for step in repair_plan["steps"][:6]:
            mode = "auto" if step.get("automatic") else "manual"
            print(f"  - [{step['priority']}/{mode}] {step['summary']}")
            if step.get("command"):
                print(f"    Command: {step['command']}")
            if step.get("next_command"):
                print(f"    Next command: {step['next_command']}")

    work_queue = payload.get("work_queue")
    if work_queue is not None:
        counts = work_queue["counts"]
        print(
            "[DOCTOR] Work queue: "
            f"safe_auto_fix={counts['safe_auto_fix']}, "
            f"manual_cleanup_first={counts['manual_cleanup_first']}, "
            f"governance_review={counts['governance_review']}"
        )
        for item in work_queue["safe_auto_fix"][:3]:
            print(f"  - [safe_auto_fix] {item['summary']}")
        for item in work_queue["manual_cleanup_first"][:3]:
            print(f"  - [manual_cleanup_first] {item['summary']}")
        for item in work_queue["governance_review"][:3]:
            print(f"  - [governance_review] {item['summary']}")

    batch_repair_preview = payload.get("batch_repair_preview")
    if batch_repair_preview is not None:
        print(
            "[DOCTOR] Batch repair preview: "
            f"eligible_steps={batch_repair_preview['eligible_steps']}, "
            f"projects={batch_repair_preview['projects_total']}"
        )
        if batch_repair_preview.get("summary"):
            print(f"  - {batch_repair_preview['summary']}")
        for command in batch_repair_preview["commands"][:5]:
            project_root = command.get("project_root") or "(unknown project)"
            print(
                f"  - [{command['type']}] {project_root}: {command['command']}"
            )

    if payload["issues"]:
        print("[DOCTOR] Issues:")
        for issue in payload["issues"]:
            print(f"  - {issue}")
    else:
        print("[DOCTOR] No blocking issues found.")

    if payload["recommendations"]:
        print("[DOCTOR] Recommendations:")
        for recommendation in payload["recommendations"]:
            print(f"  - {recommendation}")

    return 0 if payload["ok"] else 1


def collect_document_result(
    ctx: ExecutionContext,
    draft_content: str | None = None,
    final_content: str | None = None,
    write_status: str | None = None,
    rewrite_mode: str | None = None,
    missing_sections_added: list[str] | None = None,
    preserved_sections: list[str] | None = None,
) -> dict[str, object]:
    target_dir = resolve_validate_target(
        ctx.skill_name,
        ctx.import_path,
        ctx.library_root,
        ctx.runtime_skill_dir,
    )
    if not target_dir.exists():
        return {
            "mode": "document",
            "ok": False,
            "target": str(target_dir),
            "error": f"Documentation target does not exist: {target_dir}",
        }
    if not target_dir.is_dir():
        return {
            "mode": "document",
            "ok": False,
            "target": str(target_dir),
            "error": f"Documentation target is not a directory: {target_dir}",
        }

    skill_name = resolve_effective_skill_name(target_dir, ctx.skill_name)
    summary = summarize_skill_metadata(target_dir)
    purpose = ctx.args.purpose or summary.get("description") or None
    planned_resources = [
        resource for resource in sorted(ALLOWED_RESOURCES) if (target_dir / resource).exists()
    ]
    draft = draft_content or build_skill_md(
        skill_name,
        purpose,
        source_dir=target_dir,
        planned_resources=planned_resources,
    )
    existing_skill_md = (target_dir / "SKILL.md").read_text() if (target_dir / "SKILL.md").exists() else ""
    final_document = final_content or draft
    validation = collect_validation_result(target_dir)
    return {
        "mode": "document",
        "ok": True,
        "target": str(target_dir),
        "skill_name": skill_name,
        "applied": write_status is not None and not ctx.args.dry_run,
        "write_status": write_status,
        "changed": existing_skill_md != final_document,
        "purpose": purpose,
        "resource_directories": planned_resources,
        "sections": list(DOCUMENT_SECTION_TITLES),
        "rewrite_mode": rewrite_mode or "full-rewrite",
        "missing_sections_added": missing_sections_added or [],
        "preserved_sections": preserved_sections or [],
        "draft_content": final_document,
        "generated_draft": draft,
        "validation": validation,
    }


def report_document(ctx: ExecutionContext) -> int:
    target_dir = resolve_validate_target(
        ctx.skill_name,
        ctx.import_path,
        ctx.library_root,
        ctx.runtime_skill_dir,
    )
    if not target_dir.exists():
        print(f"[ERROR] Documentation target does not exist: {target_dir}")
        return 1
    if not target_dir.is_dir():
        print(f"[ERROR] Documentation target is not a directory: {target_dir}")
        return 1

    skill_name = resolve_effective_skill_name(target_dir, ctx.skill_name)
    summary = summarize_skill_metadata(target_dir)
    purpose = ctx.args.purpose or summary.get("description") or None
    planned_resources = [
        resource for resource in sorted(ALLOWED_RESOURCES) if (target_dir / resource).exists()
    ]
    draft_content = build_skill_md(
        skill_name,
        purpose,
        source_dir=target_dir,
        planned_resources=planned_resources,
    )
    existing_skill_md = (target_dir / "SKILL.md").read_text() if (target_dir / "SKILL.md").exists() else ""
    prepared_existing_skill_md = prepare_existing_skill_md_content(
        existing_skill_md,
        skill_name,
        purpose,
    )
    if ctx.args.overwrite_skill_md:
        document_plan = {
            "content": draft_content,
            "rewrite_mode": "full-rewrite",
            "missing_sections_added": list(DOCUMENT_SECTION_TITLES),
            "preserved_sections": [],
        }
    else:
        document_plan = merge_missing_skill_md_sections(
            prepared_existing_skill_md,
            draft_content,
        )
    final_content = str(document_plan["content"])
    rewrite_mode = str(document_plan["rewrite_mode"])
    missing_sections_added = list(document_plan["missing_sections_added"])
    preserved_sections = list(document_plan["preserved_sections"])
    write_status: str | None = None
    if not ctx.args.dry_run:
        write_status = write_file(target_dir / "SKILL.md", final_content, dry_run=False)
        if path_is_within(target_dir, ctx.library_root) or target_dir.resolve() == ctx.runtime_skill_dir.resolve():
            sync_platform_state_for_changes(ctx)

    payload = collect_document_result(
        ctx,
        draft_content=draft_content,
        final_content=final_content,
        write_status=write_status,
        rewrite_mode=rewrite_mode,
        missing_sections_added=missing_sections_added,
        preserved_sections=preserved_sections,
    )
    if ctx.args.format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if payload["ok"] else 1

    print(f"[DOCUMENT] Target: {payload['target']}")
    print(f"[DOCUMENT] Skill name: {payload['skill_name']}")
    print(
        "[DOCUMENT] Mode: "
        + ("preview" if ctx.args.dry_run else "apply")
    )
    print(f"[DOCUMENT] Update style: {payload['rewrite_mode']}")
    if write_status is not None:
        print(f"[DOCUMENT] SKILL.md: {write_status}")
    print(
        "[DOCUMENT] Generated sections: "
        + ", ".join(str(section) for section in payload["sections"])
    )
    if payload["missing_sections_added"]:
        print(
            "[DOCUMENT] Added sections: "
            + ", ".join(str(section) for section in payload["missing_sections_added"])
        )
    if payload["preserved_sections"] and payload["rewrite_mode"] == "merge-missing-sections":
        print(
            "[DOCUMENT] Preserved sections: "
            + ", ".join(str(section) for section in payload["preserved_sections"])
        )
    if payload["resource_directories"]:
        print(
            "[DOCUMENT] Resource hints: "
            + ", ".join(f"{resource}/" for resource in payload["resource_directories"])
        )
    if payload["validation"]["ok"]:
        print("[DOCUMENT] Validation: passes structural checks.")
    else:
        print("[DOCUMENT] Validation: has structural errors.")
        for error in payload["validation"]["errors"]:
            print(f"  - {error}")
    for warning in payload["validation"]["warnings"]:
        print(f"  - Warning: {warning}")
    print("[NEXT] Document task complete.")
    return 0


def diff_named_object_map(
    expected: dict[str, object],
    actual: dict[str, object],
) -> dict[str, list[str]]:
    expected_keys = set(expected)
    actual_keys = set(actual)
    return {
        "missing": sorted(expected_keys - actual_keys),
        "unexpected": sorted(actual_keys - expected_keys),
        "changed": sorted(
            key for key in expected_keys & actual_keys if actual.get(key) != expected.get(key)
        ),
    }


def build_audit_findings(
    registry_payload: dict[str, object],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    issues: list[dict[str, object]] = []
    recommendations: list[dict[str, object]] = []
    skills = registry_payload.get("skills", {})
    if not isinstance(skills, dict):
        return issues, recommendations

    for skill_name, entry in sorted(skills.items()):
        if not isinstance(entry, dict):
            continue
        lifecycle_status = str(entry.get("lifecycle_status", "") or "")
        usage_stats = entry.get("usage_stats", {})
        if not isinstance(usage_stats, dict):
            usage_stats = {}
        active_projects_total = int(usage_stats.get("active_projects_total", 0) or 0)
        owner = str(entry.get("owner", "") or "")
        team = str(entry.get("team", "") or "")
        version = str(entry.get("version", "") or "")
        deprecation_policy = str(entry.get("deprecation_policy", "") or "")

        if lifecycle_status not in ALLOWED_LIFECYCLE_STATUSES:
            issues.append(
                {
                    "type": "invalid-lifecycle-status",
                    "skill_name": skill_name,
                    "priority": "high",
                    "summary": (
                        f"{skill_name} uses an invalid lifecycle_status '{lifecycle_status}'."
                    ),
                    "next_step": (
                        "Use one of: "
                        + ", ".join(sorted(ALLOWED_LIFECYCLE_STATUSES))
                        + "."
                    ),
                }
            )
            continue

        if lifecycle_status == "draft" and active_projects_total > 0:
            issues.append(
                {
                    "type": "draft-skill-has-dependents",
                    "skill_name": skill_name,
                    "priority": "high",
                    "summary": (
                        f"{skill_name} is marked draft but still has {active_projects_total} active project dependent(s)."
                    ),
                    "next_step": "Promote the skill lifecycle or remove the active project exposures.",
                }
            )

        if lifecycle_status == "deprecated" and active_projects_total > 0 and not deprecation_policy:
            issues.append(
                {
                    "type": "deprecated-skill-missing-policy",
                    "skill_name": skill_name,
                    "priority": "high",
                    "summary": (
                        f"{skill_name} is deprecated, still has active dependents, and has no deprecation_policy."
                    ),
                    "next_step": "Add a deprecation policy or migrate the remaining dependents first.",
                }
            )

        if lifecycle_status in {"archived", "blocked"} and active_projects_total > 0:
            issues.append(
                {
                    "type": "inactive-lifecycle-has-dependents",
                    "skill_name": skill_name,
                    "priority": "high",
                    "summary": (
                        f"{skill_name} is {lifecycle_status} but still has {active_projects_total} active project dependent(s)."
                    ),
                    "next_step": "Remove or migrate the remaining dependents before keeping this lifecycle status.",
                }
            )

        if not owner:
            recommendations.append(
                {
                    "type": "missing-owner",
                    "skill_name": skill_name,
                    "priority": "medium",
                    "summary": f"{skill_name} has no owner in the central registry.",
                    "next_step": "Set the owner field so the skill has a clear maintainer.",
                }
            )
        if not team:
            recommendations.append(
                {
                    "type": "missing-team",
                    "skill_name": skill_name,
                    "priority": "medium",
                    "summary": f"{skill_name} has no team in the central registry.",
                    "next_step": "Set the team field to clarify responsibility.",
                }
            )
        if lifecycle_status in {"active", "review", "deprecated", "blocked"} and not version:
            recommendations.append(
                {
                    "type": "missing-version",
                    "skill_name": skill_name,
                    "priority": "low",
                    "summary": f"{skill_name} has no version recorded in the central registry.",
                    "next_step": "Add a version value so upgrades and lifecycle changes are easier to track.",
                }
            )

    return issues, recommendations


def collect_audit_result(ctx: ExecutionContext) -> dict[str, object]:
    registry_payload, dependency_graph = collect_platform_state(ctx)
    write_statuses: dict[str, str] | None = None
    if ctx.args.sync_platform_state:
        write_statuses = write_platform_state(
            ctx.platform_root,
            registry_payload,
            dependency_graph,
            dry_run=ctx.args.dry_run,
        )

    registry_path = platform_registry_path(ctx.platform_root)
    dependency_graph_path = platform_dependency_graph_path(ctx.platform_root)
    persisted_registry, registry_error = load_json_state(registry_path)
    persisted_dependency_graph, dependency_graph_error = load_json_state(dependency_graph_path)

    issues: list[str] = []
    if registry_error:
        issues.append(registry_error)
    if dependency_graph_error:
        issues.append(dependency_graph_error)
    if persisted_registry is None:
        issues.append(f"Central registry file is missing or unreadable: {registry_path}")
    if persisted_dependency_graph is None:
        issues.append(
            f"Dependency graph file is missing or unreadable: {dependency_graph_path}"
        )

    registry_matches = persisted_registry == registry_payload if persisted_registry is not None else False
    dependency_graph_matches = (
        persisted_dependency_graph == dependency_graph
        if persisted_dependency_graph is not None
        else False
    )

    persisted_registry_skills = (
        persisted_registry.get("skills", {})
        if isinstance(persisted_registry, dict)
        and isinstance(persisted_registry.get("skills"), dict)
        else {}
    )
    persisted_graph_skills = (
        persisted_dependency_graph.get("skills", {})
        if isinstance(persisted_dependency_graph, dict)
        and isinstance(persisted_dependency_graph.get("skills"), dict)
        else {}
    )
    persisted_graph_projects = (
        persisted_dependency_graph.get("projects", {})
        if isinstance(persisted_dependency_graph, dict)
        and isinstance(persisted_dependency_graph.get("projects"), dict)
        else {}
    )

    if not registry_matches and persisted_registry is not None:
        issues.append(
            "Central registry is out of date. Run audit with --sync-platform-state before pushing."
        )
    if not dependency_graph_matches and persisted_dependency_graph is not None:
        issues.append(
            "Dependency graph is out of date. Run audit with --sync-platform-state before pushing."
        )

    audit_findings, audit_recommendations = build_audit_findings(registry_payload)
    for finding in audit_findings:
        issues.append(str(finding["summary"]))

    return {
        "mode": "audit",
        "ok": not issues,
        "focus_skill": ctx.skill_name or None,
        "platform_root": str(ctx.platform_root),
        "registry_path": str(registry_path),
        "dependency_graph_path": str(dependency_graph_path),
        "sync_requested": bool(ctx.args.sync_platform_state),
        "write_statuses": write_statuses,
        "registry": registry_payload,
        "dependency_graph": dependency_graph,
        "drift": {
            "registry_matches": registry_matches,
            "dependency_graph_matches": dependency_graph_matches,
            "registry": diff_named_object_map(
                registry_payload.get("skills", {}),
                persisted_registry_skills if isinstance(persisted_registry_skills, dict) else {},
            ),
            "dependency_graph_skills": diff_named_object_map(
                dependency_graph.get("skills", {}),
                persisted_graph_skills if isinstance(persisted_graph_skills, dict) else {},
            ),
            "dependency_graph_projects": diff_named_object_map(
                dependency_graph.get("projects", {}),
                persisted_graph_projects if isinstance(persisted_graph_projects, dict) else {},
            ),
        },
        "audit_findings": audit_findings,
        "audit_recommendations": audit_recommendations,
        "issues": issues,
    }


def report_audit(ctx: ExecutionContext) -> int:
    payload = collect_audit_result(ctx)
    if ctx.args.format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0 if payload["ok"] else 1

    print(f"[AUDIT] Platform root: {payload['platform_root']}")
    print(f"[AUDIT] Registry path: {payload['registry_path']}")
    print(f"[AUDIT] Dependency graph path: {payload['dependency_graph_path']}")
    if payload.get("focus_skill"):
        print(f"[AUDIT] Focus skill: {payload['focus_skill']}")
    if payload.get("write_statuses"):
        write_statuses = payload["write_statuses"]
        print(
            "[AUDIT] Platform state sync: "
            f"platform_root={write_statuses['platform_root']}, "
            f"registry={write_statuses['registry']}, "
            f"dependency_graph={write_statuses['dependency_graph']}"
        )

    registry = payload["registry"]
    dependency_graph = payload["dependency_graph"]
    print(
        "[AUDIT] State summary: "
        f"skills={registry['skills_total']}, "
        f"projects={dependency_graph['projects_total']}"
    )

    drift = payload["drift"]
    print(
        "[AUDIT] Drift: "
        f"registry_matches={drift['registry_matches']}, "
        f"dependency_graph_matches={drift['dependency_graph_matches']}"
    )
    for section_name in ("registry", "dependency_graph_skills", "dependency_graph_projects"):
        section = drift[section_name]
        if section["missing"] or section["unexpected"] or section["changed"]:
            print(
                f"[AUDIT] {section_name}: "
                f"missing={len(section['missing'])}, "
                f"unexpected={len(section['unexpected'])}, "
                f"changed={len(section['changed'])}"
            )

    findings = payload["audit_findings"]
    if findings:
        print("[AUDIT] Blocking findings:")
        for finding in findings:
            print(f"  - [{finding['priority']}] {finding['summary']}")
            if finding.get("next_step"):
                print(f"    Next: {finding['next_step']}")
    else:
        print("[AUDIT] No blocking lifecycle findings.")

    recommendations = payload["audit_recommendations"]
    if recommendations:
        print("[AUDIT] Recommendations:")
        for recommendation in recommendations[:8]:
            print(f"  - [{recommendation['priority']}] {recommendation['summary']}")
            if recommendation.get("next_step"):
                print(f"    Next: {recommendation['next_step']}")

    if payload["issues"]:
        print("[AUDIT] Issues:")
        for issue in payload["issues"]:
            print(f"  - {issue}")
    else:
        print("[AUDIT] Audit passed.")

    return 0 if payload["ok"] else 1


def sync_platform_state_for_changes(ctx: ExecutionContext) -> None:
    if ctx.args.dry_run:
        return
    registry_payload, dependency_graph = collect_platform_state(ctx)
    write_statuses = write_platform_state(
        ctx.platform_root,
        registry_payload,
        dependency_graph,
        dry_run=False,
    )
    print(
        "[OK] Platform state sync: "
        f"platform_root={write_statuses['platform_root']}, "
        f"registry={write_statuses['registry']}, "
        f"dependency_graph={write_statuses['dependency_graph']}"
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    normalized_argv = normalize_cli_args(list(argv) if argv is not None else sys.argv[1:])
    parser = argparse.ArgumentParser(
        description=(
            "Manage Codex skills through task-oriented actions such as add, enable, "
            "doctor, document, audit, repair, upgrade, and retire. Legacy flags remain supported."
        )
    )
    parser.add_argument("--task-kind", default="legacy", help=argparse.SUPPRESS)
    parser.add_argument(
        "skill_name",
        nargs="?",
        help="Skill name to create, update, or import (normalized to hyphen-case)",
    )
    parser.add_argument(
        "--config",
        help=(
            "Optional repo-level skill governance config file "
            "(for example: skill-governance.toml)."
        ),
    )
    parser.add_argument(
        "--workspace-root",
        help="Optional workspace root for impact analysis across multiple projects.",
    )
    parser.add_argument(
        "--platform-root",
        help=(
            "Optional platform state root for the central registry and dependency graph. "
            "Defaults to config skill_registry.platform_root, <workspace-root>/.skill-platform, "
            "<project-root>/.skill-platform, or the parent of the library root."
        ),
    )
    parser.add_argument(
        "--library-root",
        help=(
            f"Canonical shared-library root. Defaults to ${DEFAULT_LIBRARY_ENV} or "
            "the parent skills directory inferred from this script. Task aliases can also "
            "derive this from the repo config."
        ),
    )
    parser.add_argument(
        "--project-root",
        "--project",
        dest="project_root",
        help="Project root where the skill should be enabled or managed",
    )
    parser.add_argument(
        "--exposure-root",
        help="Project exposure root. Defaults to config skill_registry.exposure_root or <project-root>/.agents/skills.",
    )
    parser.add_argument(
        "--exposure-mode",
        choices=sorted(ALLOWED_EXPOSURE_MODES),
        help="How a project should expose a skill: auto, symlink, copy, or manifest.",
    )
    parser.add_argument(
        "--list-library-skills",
        action="store_true",
        help="List canonical skills found in the shared library root",
    )
    parser.add_argument(
        "--list-project-skills",
        action="store_true",
        help="List skill entries attached to the given project root",
    )
    parser.add_argument(
        "--import-path",
        help="Path to an already-downloaded local skill directory to import into the shared library",
    )
    parser.add_argument(
        "--adopt",
        help="Path to a downloaded local skill directory to adopt into the shared library. Alias for --import-path.",
    )
    parser.add_argument(
        "--inspect-import",
        action="store_true",
        help="Inspect a local skill import candidate without writing any files",
    )
    parser.add_argument(
        "--doctor",
        "--check",
        dest="doctor",
        action="store_true",
        help=(
            "Run a read-only health check for the current package, a canonical shared-library "
            "skill, or a local import candidate."
        ),
    )
    parser.add_argument(
        "--document",
        action="store_true",
        help=(
            "Preview or fill missing SKILL.md sections for the current package, a canonical "
            "skill, or a local import candidate."
        ),
    )
    parser.add_argument(
        "--audit",
        action="store_true",
        help=(
            "Run a CI-friendly platform audit for the central registry, lifecycle policy, "
            "and persisted dependency graph."
        ),
    )
    parser.add_argument(
        "--sync-platform-state",
        action="store_true",
        help=(
            "Write the expected registry and dependency graph under the platform root before "
            "reporting audit results."
        ),
    )
    parser.add_argument(
        "--import-mode",
        choices=("copy", "move"),
        default="copy",
        help="How to import a local skill directory. Defaults to copy for safety.",
    )
    parser.add_argument(
        "--project-skills",
        help="Comma-separated existing skills to add or ensure for a project",
    )
    parser.add_argument(
        "--unlink-skills",
        help="Comma-separated project skill links to remove",
    )
    parser.add_argument(
        "--sync-project-skills",
        help="Comma-separated exact project skill set to keep linked",
    )
    parser.add_argument(
        "--compat-root",
        help=(
            f"Optional top-level root for compatibility links. Defaults to "
            f"${DEFAULT_COMPAT_ENV} or the parent of the library root when available."
        ),
    )
    parser.add_argument(
        "--no-compat-link",
        action="store_true",
        help="Skip creating the compatibility link for create/update operations",
    )
    parser.add_argument(
        "--bootstrap-project",
        action="store_true",
        help="Attach only skill-governance when onboarding a project without an explicit skill list",
    )
    parser.add_argument(
        "--bootstrap-project-layout",
        action="store_true",
        help=(
            "Initialize a project root for project-local managed skills by ensuring "
            "_skill-library and .agents/skills exist and by linking the current "
            "skill package into that managed layout."
        ),
    )
    parser.add_argument(
        "--purpose",
        help="Initial or updated SKILL.md description value",
    )
    parser.add_argument(
        "--display-name",
        help="Display name for agents/openai.yaml",
    )
    parser.add_argument(
        "--short-description",
        help="Short description for agents/openai.yaml",
    )
    parser.add_argument(
        "--default-prompt",
        help="Default prompt for agents/openai.yaml",
    )
    parser.add_argument(
        "--resources",
        help="Optional comma-separated resource dirs to create, e.g. scripts,references",
    )
    parser.add_argument(
        "--overwrite-skill-md",
        action="store_true",
        help="Rewrite SKILL.md from the generated draft instead of preserving existing sections",
    )
    parser.add_argument(
        "--overwrite-openai",
        action="store_true",
        help="Rewrite agents/openai.yaml from the generated template",
    )
    parser.add_argument(
        "--skip-validate",
        action="store_true",
        help="Skip automatic validation after create/update operations",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help=(
            "Validate an existing skill directory without writing files. "
            "Defaults to --adopt/--import-path, the canonical skill, or this package."
        ),
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format for read-only modes. Defaults to text.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview filesystem changes without writing files or links",
    )
    return parser.parse_args(normalized_argv)


def resolve_execution_context(args: argparse.Namespace) -> ExecutionContext:
    root_override_provided = bool(args.library_root or os.environ.get(DEFAULT_LIBRARY_ENV))
    runtime_skill_dir = detect_runtime_skill_dir()
    project_root = Path(args.project_root).expanduser().resolve() if args.project_root else None
    raw_import_path = args.import_path or args.adopt
    import_path = Path(raw_import_path).expanduser().resolve() if raw_import_path else None
    auto_bootstrap_import = False
    kept_existing_canonical = False
    project_root_inferred_from_cwd = False
    effective_bootstrap_project_layout = args.bootstrap_project_layout
    bootstrap_cleanup_source: Path | None = None
    bootstrap_source_candidate: Path | None = None

    if project_root is None:
        infer_without_import = bool(
            args.task_kind in {"enable", "doctor", "repair", "retire", "upgrade"}
            or args.list_project_skills
            or args.project_skills
            or args.unlink_skills
            or args.sync_project_skills
        )
        inferred_cwd_project_root = infer_project_root_from_cwd(
            import_path,
            runtime_skill_dir,
            allow_without_import=infer_without_import,
        )
        if inferred_cwd_project_root is not None:
            project_root = inferred_cwd_project_root
            project_root_inferred_from_cwd = True
            if import_path is not None:
                effective_bootstrap_project_layout = True

    if effective_bootstrap_project_layout and project_root is None:
        project_root = infer_project_root_for_bootstrap(import_path, runtime_skill_dir)
        if project_root is None:
            raise UsageError(
                "[ERROR] Could not infer a project root for --bootstrap-project-layout. "
                "Provide --project-root explicitly."
            )

    config_path = discover_workflow_config_path(args.config, project_root)
    config = load_workflow_config(config_path)
    workspace_root = detect_workspace_root(args.workspace_root, config, project_root)

    if effective_bootstrap_project_layout and import_path is None:
        if not (runtime_skill_dir / "SKILL.md").exists():
            raise UsageError(
                "[ERROR] Could not infer an import source for --bootstrap-project-layout. "
                "Provide --adopt or --import-path explicitly."
            )
        import_path = runtime_skill_dir
        auto_bootstrap_import = True
    if effective_bootstrap_project_layout and import_path is not None:
        bootstrap_source_candidate = import_path

    inferred_import_name = detect_skill_name_from_source(import_path) if import_path else ""
    skill_name = normalize_skill_name(args.skill_name) if args.skill_name else inferred_import_name
    prefer_project_library = bool(
        project_root
        and args.task_kind in {"add", "upgrade"}
        and not args.inspect_import
        and not args.list_library_skills
        and not args.list_project_skills
        and not args.validate_only
        and not args.doctor
        and not args.bootstrap_project
        and not args.bootstrap_project_layout
    )
    library_root = detect_library_root(
        args.library_root,
        config,
        project_root=project_root,
        bootstrap_project_layout=effective_bootstrap_project_layout,
        prefer_project_library=prefer_project_library,
    )
    platform_root = detect_platform_root(
        args.platform_root,
        config,
        workspace_root,
        project_root,
        library_root,
    )
    compat_root = detect_compat_root(
        args.compat_root,
        library_root,
        allow_default=bool(skill_name and not args.no_compat_link),
    )
    exposure_root = detect_exposure_root(
        args.exposure_root,
        config,
        project_root,
    )
    exposure_mode = resolve_exposure_mode(args.exposure_mode, config)
    if (
        effective_bootstrap_project_layout
        and auto_bootstrap_import
        and import_path is not None
        and skill_name
    ):
        canonical_candidate = library_root / skill_name
        if (
            import_path.resolve() != canonical_candidate.resolve(strict=False)
            and canonical_candidate.exists()
        ):
            import_path = None
            auto_bootstrap_import = False
            kept_existing_canonical = True
    if (
        effective_bootstrap_project_layout
        and bootstrap_source_candidate is not None
        and project_root is not None
        and skill_name
    ):
        canonical_candidate = library_root / skill_name
        if (
            path_is_within(bootstrap_source_candidate, project_root)
            and bootstrap_source_candidate.resolve()
            != canonical_candidate.resolve(strict=False)
        ):
            bootstrap_cleanup_source = bootstrap_source_candidate
    if args.skill_name and not skill_name:
        raise UsageError("[ERROR] Skill name must include at least one letter or digit.")
    if skill_name and len(skill_name) > MAX_NAME_LENGTH:
        raise UsageError(
            f"[ERROR] Skill name '{skill_name}' is too long ({len(skill_name)} chars). "
            f"Maximum is {MAX_NAME_LENGTH}."
        )

    try:
        resources = parse_resource_list(args.resources)
    except ValueError as error:
        raise UsageError(f"[ERROR] {error}") from error

    project_skills = parse_skill_list(args.project_skills)
    unlink_skills = parse_skill_list(args.unlink_skills)
    sync_project_skills = parse_skill_list(args.sync_project_skills)
    project_local_library_root = (
        config.project_library_root
        or ((project_root / DEFAULT_LIBRARY_DIRNAME).resolve() if project_root else None)
    )
    if (
        not root_override_provided
        and project_local_library_root is not None
        and project_local_library_root.exists()
        and (
            args.list_project_skills
            or project_skills
            or unlink_skills
            or sync_project_skills
            or args.validate_only
            or args.doctor
            or args.task_kind == "repair"
        )
    ):
        library_root = project_local_library_root
        compat_root = detect_compat_root(
            args.compat_root,
            library_root,
            allow_default=bool(skill_name and not args.no_compat_link),
        )
    project_modes = [
        bool(project_skills),
        bool(unlink_skills),
        bool(sync_project_skills),
        bool(args.bootstrap_project),
        bool(args.bootstrap_project_layout),
    ]
    if sum(project_modes) > 1:
        raise UsageError(
            "[ERROR] Use only one of --project-skills, --unlink-skills, "
            "--sync-project-skills, --bootstrap-project, or "
            "--bootstrap-project-layout at a time."
        )

    if args.bootstrap_project and not project_skills:
        project_skills = ["skill-governance"]

    report_compat_root = bool(compat_root and (project_root is None or compat_root != project_root))

    return ExecutionContext(
        args=args,
        runtime_skill_dir=runtime_skill_dir,
        config=config,
        platform_root=platform_root,
        workspace_root=workspace_root,
        project_root=project_root,
        import_path=import_path,
        skill_name=skill_name,
        library_root=library_root,
        compat_root=compat_root,
        exposure_root=exposure_root,
        exposure_mode=exposure_mode,
        resources=resources,
        project_skills=project_skills,
        unlink_skills=unlink_skills,
        sync_project_skills=sync_project_skills,
        effective_bootstrap_project_layout=effective_bootstrap_project_layout,
        project_root_inferred_from_cwd=project_root_inferred_from_cwd,
        kept_existing_canonical=kept_existing_canonical,
        report_compat_root=report_compat_root,
        bootstrap_cleanup_source=bootstrap_cleanup_source,
    )


def validate_execution_context(ctx: ExecutionContext) -> None:
    args = ctx.args
    document_requested = bool(args.document or args.task_kind == "document")

    if args.import_path and args.adopt:
        raise UsageError("[ERROR] Use only one of --import-path or --adopt.")

    if (ctx.project_skills or ctx.unlink_skills or ctx.sync_project_skills) and ctx.project_root is None:
        raise UsageError(
            "[ERROR] Project skill add/remove/sync operations require --project-root."
        )

    if args.list_project_skills and ctx.project_root is None:
        raise UsageError("[ERROR] --list-project-skills requires --project-root.")

    if (
        not ctx.skill_name
        and not ctx.project_skills
        and not ctx.unlink_skills
        and not ctx.sync_project_skills
        and not args.list_library_skills
        and not args.list_project_skills
        and not args.bootstrap_project_layout
        and not args.validate_only
        and not args.doctor
        and not document_requested
        and not args.audit
    ):
        raise UsageError(
            "[ERROR] Provide a skill name to create/update, or use a project skill operation."
        )

    if ctx.import_path and (ctx.project_skills or ctx.unlink_skills or ctx.sync_project_skills):
        raise UsageError(
            "[ERROR] --import-path/--adopt cannot be combined with project skill add/remove/sync modes."
        )

    if args.inspect_import and not ctx.import_path:
        raise UsageError("[ERROR] --inspect-import requires --import-path or --adopt.")

    if args.validate_only:
        if (
            args.doctor
            or args.list_library_skills
            or args.list_project_skills
            or ctx.project_skills
            or ctx.unlink_skills
            or ctx.sync_project_skills
            or args.bootstrap_project
            or args.bootstrap_project_layout
            or args.dry_run
            or args.resources
            or args.purpose
            or args.display_name
            or args.short_description
            or args.default_prompt
            or args.overwrite_skill_md
            or args.overwrite_openai
            or args.skip_validate
            or args.inspect_import
            or args.compat_root
            or args.no_compat_link
            or args.sync_platform_state
        ):
            raise UsageError(
                "[ERROR] --validate-only is read-only and cannot be combined with "
                "listing, mutation, inspect, dry-run, compat-link, or metadata flags."
            )

    if args.doctor:
        if (
            args.validate_only
            or args.document
            or args.list_library_skills
            or args.list_project_skills
            or ctx.project_skills
            or ctx.unlink_skills
            or ctx.sync_project_skills
            or args.bootstrap_project
            or args.bootstrap_project_layout
            or args.dry_run
            or args.resources
            or args.purpose
            or args.display_name
            or args.short_description
            or args.default_prompt
            or args.overwrite_skill_md
            or args.overwrite_openai
            or args.skip_validate
            or args.inspect_import
            or args.compat_root
            or args.no_compat_link
            or args.sync_platform_state
        ):
            raise UsageError(
                "[ERROR] --doctor is read-only and cannot be combined with "
                "listing, mutation, inspect, dry-run, compat-link, or metadata flags."
            )

    if document_requested:
        if (
            args.validate_only
            or args.doctor
            or args.audit
            or args.list_library_skills
            or args.list_project_skills
            or ctx.project_skills
            or ctx.unlink_skills
            or ctx.sync_project_skills
            or args.bootstrap_project
            or args.bootstrap_project_layout
            or args.resources
            or args.display_name
            or args.short_description
            or args.default_prompt
            or args.overwrite_openai
            or args.inspect_import
            or args.compat_root
            or args.no_compat_link
            or args.sync_platform_state
        ):
            raise UsageError(
                "[ERROR] --document only works with skill scope flags such as "
                "--library-root, --project-root, --workspace-root, --adopt/--import-path, "
                "--purpose, --overwrite-skill-md, --dry-run, and --format."
            )

    if args.audit:
        if (
            args.validate_only
            or args.doctor
            or args.document
            or args.list_library_skills
            or args.list_project_skills
            or ctx.project_skills
            or ctx.unlink_skills
            or ctx.sync_project_skills
            or args.bootstrap_project
            or args.bootstrap_project_layout
            or args.resources
            or args.purpose
            or args.display_name
            or args.short_description
            or args.default_prompt
            or args.overwrite_skill_md
            or args.overwrite_openai
            or args.skip_validate
            or args.inspect_import
            or args.compat_root
            or args.no_compat_link
        ):
            raise UsageError(
                "[ERROR] --audit only works with state, scope, and output flags such as "
                "--platform-root, --workspace-root, --project-root, --library-root, "
                "--sync-platform-state, --format, and --dry-run."
            )

    if args.format == "json" and not (
        args.validate_only
        or args.list_library_skills
        or args.list_project_skills
        or args.inspect_import
        or args.doctor
        or document_requested
        or args.audit
    ):
        raise UsageError(
            "[ERROR] --format json is supported only with --validate-only, "
            "--list-library-skills, --list-project-skills, --inspect-import, --doctor, --document, or --audit."
        )

    if args.sync_platform_state and not args.audit:
        raise UsageError("[ERROR] --sync-platform-state can only be used with --audit.")

    if args.list_library_skills or args.list_project_skills:
        if (
            ctx.skill_name
            or ctx.import_path
            or args.doctor
            or ctx.project_skills
            or ctx.unlink_skills
            or ctx.sync_project_skills
            or args.bootstrap_project
            or args.bootstrap_project_layout
            or args.dry_run
            or args.resources
            or args.purpose
            or args.display_name
            or args.short_description
            or args.default_prompt
            or args.overwrite_skill_md
            or args.overwrite_openai
            or args.skip_validate
            or args.inspect_import
        ):
            raise UsageError(
                "[ERROR] Listing modes are read-only and cannot be combined with create, import, "
                "inspect, update, or project mutation flags."
            )
            return

    if args.inspect_import and not ctx.skill_name:
        raise UsageError("[ERROR] Could not determine a canonical skill name for inspection.")

    if args.task_kind == "upgrade" and not ctx.skill_name:
        raise UsageError("[ERROR] upgrade requires a skill name or a local skill path.")

    if args.task_kind == "retire" and ctx.project_root is None:
        raise UsageError(
            "[ERROR] retire needs a project context. Pass --project-root/--project or run it inside the target project."
        )

    if args.task_kind == "enable" and ctx.project_root is None:
        raise UsageError(
            "[ERROR] enable needs a project context. Pass --project-root/--project or run it inside the target project."
        )

    if args.task_kind == "repair":
        if ctx.import_path:
            raise UsageError("[ERROR] repair works with a managed skill name, not --import-path/--adopt.")
        if not ctx.skill_name:
            raise UsageError("[ERROR] repair requires a managed skill name.")
        if ctx.project_root is None and ctx.workspace_root is None:
            raise UsageError(
                "[ERROR] repair needs --project-root/--project or --workspace-root so it knows which exposures to repair."
            )
        if (
            args.validate_only
            or args.doctor
            or args.list_library_skills
            or args.list_project_skills
            or ctx.project_skills
            or ctx.unlink_skills
            or ctx.sync_project_skills
            or args.bootstrap_project
            or args.bootstrap_project_layout
            or args.resources
            or args.purpose
            or args.display_name
            or args.short_description
            or args.default_prompt
            or args.overwrite_skill_md
            or args.overwrite_openai
            or args.skip_validate
            or args.inspect_import
            or args.compat_root
            or args.no_compat_link
        ):
            raise UsageError(
                "[ERROR] repair only works with managed skill scope flags such as "
                "--project-root/--project, --workspace-root, --library-root, and --dry-run."
            )


def print_execution_context(ctx: ExecutionContext) -> None:
    args = ctx.args
    display_skill_name = primary_task_skill_name(ctx)

    if args.task_kind != "legacy":
        print(f"[INFO] Task: {args.task_kind}")
    print(f"[INFO] Library root: {ctx.library_root}")
    if display_skill_name:
        print(f"[INFO] Skill name: {display_skill_name}")
    print(f"[INFO] Storage decision: {storage_decision_label(ctx)}")
    if ctx.config.path:
        print(f"[INFO] Workflow config: {ctx.config.path}")
    print(f"[INFO] Platform root: {ctx.platform_root}")
    if ctx.workspace_root:
        print(f"[INFO] Workspace root: {ctx.workspace_root}")
    if ctx.project_root:
        print(f"[INFO] Project root: {ctx.project_root}")
    if ctx.exposure_root:
        print(f"[INFO] Exposure root: {ctx.exposure_root}")
        print(f"[INFO] Exposure mode: {ctx.exposure_mode}")
    if ctx.project_root_inferred_from_cwd and ctx.project_root:
        print("[INFO] Project root was inferred from the current working directory.")
    if ctx.import_path:
        print(f"[INFO] Import source: {ctx.import_path}")
    if args.bootstrap_project_layout:
        print("[INFO] Bootstrap project layout mode enabled.")
    elif ctx.effective_bootstrap_project_layout and ctx.import_path is not None:
        print(
            "[INFO] External import will use a project-local managed layout inferred from the current working directory."
        )
    if ctx.kept_existing_canonical and ctx.skill_name:
        print(
            "[INFO] Existing canonical skill already found. "
            f"Keeping {ctx.library_root / ctx.skill_name} and refreshing project structure."
        )
    if ctx.report_compat_root and ctx.skill_name:
        print(f"[INFO] Compatibility root: {ctx.compat_root}")
    if args.dry_run:
        print("[INFO] Dry-run mode enabled. No files will be modified.")


def handle_validate_only_mode(ctx: ExecutionContext) -> int:
    validate_target = resolve_validate_target(
        ctx.skill_name,
        ctx.import_path,
        ctx.library_root,
        ctx.runtime_skill_dir,
    )
    if not validate_target.exists():
        print(f"[ERROR] Validation target does not exist: {validate_target}")
        return 1
    if not validate_target.is_dir():
        print(f"[ERROR] Validation target is not a directory: {validate_target}")
        return 1

    if ctx.args.format == "text":
        print(f"[INFO] Validation target: {validate_target}")
    return report_validation(validate_target, output_format=ctx.args.format)


def handle_doctor_mode(ctx: ExecutionContext) -> int:
    return report_doctor(ctx)


def handle_audit_mode(ctx: ExecutionContext) -> int:
    if ctx.args.format == "text":
        print_execution_context(ctx)
    return report_audit(ctx)


def handle_document_mode(ctx: ExecutionContext) -> int:
    if ctx.args.format == "text":
        print_execution_context(ctx)
    return report_document(ctx)


def handle_listing_mode(ctx: ExecutionContext) -> int:
    if ctx.args.list_library_skills:
        list_library_skills(ctx.library_root, output_format=ctx.args.format)
    if ctx.args.list_project_skills:
        list_project_skills(
            ctx.project_root,
            ctx.library_root,
            ctx.exposure_root,
            output_format=ctx.args.format,
        )
    return 0


def handle_inspect_mode(ctx: ExecutionContext) -> int:
    return inspect_import_source(
        ctx.import_path,
        ctx.library_root,
        ctx.skill_name,
        ctx.project_root,
        ctx.exposure_root,
        output_format=ctx.args.format,
    )


def handle_repair_mode(ctx: ExecutionContext) -> int:
    print_execution_context(ctx)
    payload = collect_doctor_result(ctx)
    skill_name = str(payload.get("skill_name") or primary_task_skill_name(ctx))
    if not skill_name:
        print("[ERROR] Could not determine which skill to repair.")
        return 1
    return_code = execute_safe_auto_fix_queue(ctx, skill_name, payload)
    if not ctx.args.dry_run:
        sync_platform_state_for_changes(ctx)
    if ctx.args.task_kind == "repair":
        if return_code == 0:
            print("[NEXT] Task complete: repair")
        else:
            print("[NEXT] Task incomplete: repair")
    return return_code


def manage_canonical_skill(ctx: ExecutionContext) -> Path | None:
    if not ctx.skill_name:
        return None

    args = ctx.args
    canonical_skill_dir = ctx.library_root / ctx.skill_name
    library_status = ensure_directory(ctx.library_root, dry_run=args.dry_run)
    if args.task_kind == "upgrade":
        if not canonical_skill_dir.exists():
            raise FileNotFoundError(
                f"Cannot upgrade missing canonical skill: {canonical_skill_dir}. Use add instead."
            )
        if ctx.import_path:
            skill_dir_status = sync_imported_skill_tree(
                ctx.import_path,
                canonical_skill_dir,
                mode=args.import_mode,
                dry_run=args.dry_run,
            )
        else:
            skill_dir_status = "kept"
    else:
        if ctx.import_path:
            ensure_import_target_available(
                ctx.import_path,
                canonical_skill_dir,
                ctx.library_root,
                ctx.skill_name,
            )
            skill_dir_status = import_skill_tree(
                ctx.import_path,
                canonical_skill_dir,
                mode=args.import_mode,
                dry_run=args.dry_run,
            )
        else:
            skill_dir_status = ensure_directory(canonical_skill_dir, dry_run=args.dry_run)

    skill_md_status = upsert_skill_md(
        canonical_skill_dir / "SKILL.md",
        ctx.skill_name,
        args.purpose,
        source_dir=canonical_skill_dir if canonical_skill_dir.exists() else ctx.import_path,
        planned_resources=ctx.resources,
        overwrite=args.overwrite_skill_md,
        dry_run=args.dry_run,
    )
    openai_status = upsert_openai_yaml(
        canonical_skill_dir / "agents" / "openai.yaml",
        ctx.skill_name,
        args.display_name,
        args.short_description,
        args.default_prompt,
        overwrite=args.overwrite_openai,
        dry_run=args.dry_run,
    )
    resource_statuses = ensure_optional_dirs(
        canonical_skill_dir,
        ctx.resources,
        dry_run=args.dry_run,
    )

    print(f"[OK] Library root ({library_status}): {ctx.library_root}")
    if args.task_kind == "upgrade" and ctx.import_path:
        print(
            f"[OK] Upgraded canonical skill directory ({skill_dir_status}): "
            f"{canonical_skill_dir}"
        )
    elif ctx.import_path:
        print(
            f"[OK] Imported canonical skill directory ({skill_dir_status}): "
            f"{canonical_skill_dir}"
        )
    else:
        print(
            f"[OK] Canonical skill directory ({skill_dir_status}): "
            f"{canonical_skill_dir}"
        )
    print(f"[OK] SKILL.md: {skill_md_status}")
    print(f"[OK] agents/openai.yaml: {openai_status}")
    for resource, status in resource_statuses:
        print(f"[OK] {resource}/ ({status})")

    if (
        ctx.import_path
        and ctx.project_root
        and ctx.import_path.resolve() != canonical_skill_dir.resolve(strict=False)
        and not path_is_within(ctx.import_path, ctx.project_root)
    ):
        source_record_status = record_external_source(
            ctx.project_root,
            ctx.skill_name,
            ctx.import_path,
            canonical_skill_dir,
            args.import_mode,
            dry_run=args.dry_run,
        )
        print(
            f"[OK] External source registry ({source_record_status}): "
            f"{external_source_registry_path(ctx.project_root)}"
        )

    if ctx.project_root:
        if ctx.exposure_root is None:
            raise FileNotFoundError("Could not determine a managed project exposure root.")
        link_status, project_link, registry_status = ensure_project_exposure(
            ctx.exposure_root,
            ctx.skill_name,
            canonical_skill_dir,
            ctx.exposure_mode,
            dry_run=args.dry_run,
        )
        print(f"[OK] Project exposure ({link_status}): {project_link}")
        print(f"[OK] Exposure registry ({registry_status}): {managed_exposure_registry_path(ctx.exposure_root)}")

    if ctx.report_compat_root:
        compat_link = ctx.compat_root / ".agents" / "skills" / ctx.skill_name
        link_status = ensure_symlink(
            compat_link,
            canonical_skill_dir,
            dry_run=args.dry_run,
        )
        print(f"[OK] Compatibility link ({link_status}): {compat_link}")

    return canonical_skill_dir


def run_project_skill_operations(ctx: ExecutionContext) -> None:
    if (ctx.project_skills or ctx.unlink_skills or ctx.sync_project_skills) and ctx.exposure_root is None:
        raise FileNotFoundError("Could not determine a managed project exposure root.")

    for requested_skill in ctx.project_skills:
        requested_dir = ensure_existing_skill_dir(ctx.library_root, requested_skill)
        link_status, project_link, registry_status = ensure_project_exposure(
            ctx.exposure_root,
            requested_skill,
            requested_dir,
            ctx.exposure_mode,
            dry_run=ctx.args.dry_run,
        )
        print(f"[OK] Project skill exposure ({link_status}): {project_link}")
        print(f"[OK] Exposure registry ({registry_status}): {managed_exposure_registry_path(ctx.exposure_root)}")

    for requested_skill in ctx.unlink_skills:
        unlink_status, project_link, registry_status = unlink_project_exposure(
            ctx.exposure_root,
            requested_skill,
            dry_run=ctx.args.dry_run,
        )
        print(f"[OK] Project skill retire ({unlink_status}): {project_link}")
        print(f"[OK] Exposure registry ({registry_status}): {managed_exposure_registry_path(ctx.exposure_root)}")

    if ctx.sync_project_skills:
        desired_skills = set(ctx.sync_project_skills)
        for requested_skill in ctx.sync_project_skills:
            requested_dir = ensure_existing_skill_dir(ctx.library_root, requested_skill)
            link_status, project_link, registry_status = ensure_project_exposure(
                ctx.exposure_root,
                requested_skill,
                requested_dir,
                ctx.exposure_mode,
                dry_run=ctx.args.dry_run,
            )
            print(f"[OK] Project sync exposure ({link_status}): {project_link}")
            print(f"[OK] Exposure registry ({registry_status}): {managed_exposure_registry_path(ctx.exposure_root)}")

        existing_links = list_managed_project_links(ctx.exposure_root, ctx.library_root)
        for existing_name, existing_link in sorted(existing_links.items()):
            if existing_name in desired_skills:
                continue
            unlink_status, removed_path, registry_status = unlink_project_exposure(
                ctx.exposure_root,
                existing_name,
                dry_run=ctx.args.dry_run,
            )
            print(f"[OK] Project sync retire ({unlink_status}): {removed_path}")
            print(f"[OK] Exposure registry ({registry_status}): {managed_exposure_registry_path(ctx.exposure_root)}")


def finalize_mutation_mode(ctx: ExecutionContext, canonical_skill_dir: Path | None) -> int:
    task_skill_name = primary_task_skill_name(ctx)
    sync_platform_state_for_changes(ctx)
    if canonical_skill_dir and not ctx.args.skip_validate:
        if ctx.args.dry_run:
            print(f"[NEXT] Dry-run complete. Validation would run for {canonical_skill_dir} after writing.")
        else:
            validation_status = report_validation(canonical_skill_dir)
            if validation_status != 0:
                return validation_status
    elif canonical_skill_dir and ctx.args.skip_validate:
        print("[NEXT] Validation skipped by request.")
    elif ctx.project_skills or ctx.unlink_skills or ctx.sync_project_skills:
        print("[NEXT] Project skill operation complete.")

    impact_summary: dict[str, object] | None = None
    if task_skill_name and ctx.args.task_kind == "upgrade":
        impact_summary = collect_task_impact_summary(
            ctx,
            "upgrade",
            task_skill_name,
            canonical_skill_dir=canonical_skill_dir,
        )
    elif task_skill_name and ctx.args.task_kind == "retire":
        impact_summary = collect_task_impact_summary(
            ctx,
            "retire",
            task_skill_name,
            canonical_skill_dir=(ctx.library_root / task_skill_name),
        )
        if impact_summary is not None:
            impact_summary["preview"] = bool(ctx.args.dry_run)
    if impact_summary is not None:
        report_task_impact_summary(impact_summary)

    if ctx.bootstrap_cleanup_source is not None and canonical_skill_dir is not None:
        cleanup_status = remove_path(ctx.bootstrap_cleanup_source, dry_run=ctx.args.dry_run)
        print(
            f"[OK] Bootstrap source cleanup ({cleanup_status}): "
            f"{ctx.bootstrap_cleanup_source}"
        )
    if ctx.args.task_kind != "legacy":
        if ctx.args.task_kind == "add":
            print("[NEXT] Task complete: add")
        elif ctx.args.task_kind == "enable":
            print("[NEXT] Task complete: enable")
        elif ctx.args.task_kind == "upgrade":
            print("[NEXT] Task complete: upgrade")
        elif ctx.args.task_kind == "retire":
            print("[NEXT] Task complete: retire")
    return 0


def print_mutation_error_help(ctx: ExecutionContext, error: Exception) -> None:
    task = ctx.args.task_kind
    if task == "upgrade" and isinstance(error, FileNotFoundError):
        print("[HINT] The upgrade target does not exist yet. Use `add` first, then rerun `upgrade`.")
        return
    if task == "enable" and isinstance(error, FileNotFoundError):
        print("[HINT] The canonical skill does not exist yet. Add it first, then enable it for the project.")
        return
    if task == "repair" and isinstance(error, FileNotFoundError):
        print("[HINT] The canonical skill does not exist yet. Add it first, then rerun `repair`.")
        return
    if task in {"enable", "retire", "doctor", "repair"} and ctx.project_root is None:
        print("[HINT] Pass --project-root/--project or run the command inside the target project.")
        return
    if isinstance(error, FileExistsError) and ctx.skill_name and ctx.project_root:
        print(
            "[HINT] A blocker already exists in the project exposure path. "
            f"Run `doctor {ctx.skill_name} --project-root {ctx.project_root}` first."
        )


def handle_mutation_mode(ctx: ExecutionContext) -> int:
    print_execution_context(ctx)

    canonical_skill_dir: Path | None = None
    try:
        canonical_skill_dir = manage_canonical_skill(ctx)
        run_project_skill_operations(ctx)
    except (FileExistsError, FileNotFoundError, NotADirectoryError, ValueError) as error:
        print(f"[ERROR] {error}")
        print_mutation_error_help(ctx, error)
        return 1

    return finalize_mutation_mode(ctx, canonical_skill_dir)


def main() -> int:
    try:
        args = parse_args()
        ctx = resolve_execution_context(args)
        validate_execution_context(ctx)
    except UsageError as error:
        print(error)
        return 1

    if args.validate_only:
        return handle_validate_only_mode(ctx)
    if args.audit:
        return handle_audit_mode(ctx)
    if args.document or args.task_kind == "document":
        return handle_document_mode(ctx)
    if args.doctor:
        return handle_doctor_mode(ctx)
    if args.list_library_skills or args.list_project_skills:
        return handle_listing_mode(ctx)
    if args.inspect_import:
        if args.format == "text":
            print_execution_context(ctx)
        return handle_inspect_mode(ctx)
    if args.task_kind == "repair":
        return handle_repair_mode(ctx)
    return handle_mutation_mode(ctx)


if __name__ == "__main__":
    sys.exit(main())
