#!/usr/bin/env python3

"""Create, update, validate, and link skills using a shared-library workflow."""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_LIBRARY_ENV = "CODEX_SKILL_LIBRARY_ROOT"
DEFAULT_COMPAT_ENV = "CODEX_SKILL_COMPAT_ROOT"
DEFAULT_CODEX_HOME_ENV = "CODEX_HOME"
DEFAULT_LIBRARY_DIRNAME = "_skill-library"
DEFAULT_RUNTIME_SKILLS_DIRNAME = "skills"
EXTERNAL_SOURCE_REGISTRY_DIRNAME = "skill-workflow-manager"
EXTERNAL_SOURCE_REGISTRY_FILENAME = "external-sources.json"
MAX_NAME_LENGTH = 64
ALLOWED_RESOURCES = {"scripts", "references", "assets"}
PLACEHOLDER_DESCRIPTION = (
    "TODO: replace with a precise description of what this skill does and when to use it."
)
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)


class UsageError(Exception):
    pass


@dataclass
class ExecutionContext:
    args: argparse.Namespace
    runtime_skill_dir: Path
    project_root: Path | None
    import_path: Path | None
    skill_name: str
    library_root: Path
    compat_root: Path | None
    runtime_skills_root: Path | None
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


def detect_library_root(
    explicit_root: str | None,
    project_root: Path | None = None,
    bootstrap_project_layout: bool = False,
) -> Path:
    if explicit_root:
        return Path(explicit_root).expanduser().resolve()
    env_root = os.environ.get(DEFAULT_LIBRARY_ENV)
    if env_root:
        return Path(env_root).expanduser().resolve()
    if bootstrap_project_layout and project_root is not None:
        return (project_root / DEFAULT_LIBRARY_DIRNAME).resolve()
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


def detect_runtime_skills_root(explicit_root: str | None) -> Path:
    if explicit_root:
        return Path(explicit_root).expanduser().resolve()
    codex_home = os.environ.get(DEFAULT_CODEX_HOME_ENV)
    if codex_home:
        return (Path(codex_home).expanduser().resolve() / DEFAULT_RUNTIME_SKILLS_DIRNAME)
    return (Path.home() / ".codex" / DEFAULT_RUNTIME_SKILLS_DIRNAME).resolve()


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
) -> Path | None:
    if import_path is None:
        return None
    cwd = Path.cwd().resolve()
    for source_dir in (import_path.resolve(), runtime_skill_dir.resolve()):
        if cwd == source_dir or path_is_within(cwd, source_dir):
            return None
    if looks_like_skill_dir(cwd):
        return None
    return find_nearest_project_root(cwd)


def external_source_registry_path(project_root: Path) -> Path:
    return (
        project_root
        / ".agents"
        / EXTERNAL_SOURCE_REGISTRY_DIRNAME
        / EXTERNAL_SOURCE_REGISTRY_FILENAME
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


def build_skill_md(skill_name: str, purpose: str | None) -> str:
    display_name = title_case_skill_name(skill_name)
    description = purpose.strip() if purpose else PLACEHOLDER_DESCRIPTION
    return f"""---
name: {skill_name}
description: {yaml_quote(description)}
---

# {display_name}

## Purpose

[TODO: State the skill's job in 1-2 short sentences.]

## Use This Skill When

- [TODO: Describe the requests that should trigger this skill.]
- [TODO: Add one clear boundary or secondary trigger.]

## Workflow

1. [TODO: Identify the task and the required inputs.]
2. [TODO: Use the bundled scripts, references, or files needed for the task.]
3. [TODO: Validate the result and report the outcome.]

## Resources

- `agents/openai.yaml`: keep UI metadata aligned with the skill purpose.
- `references/`: move longer examples or domain rules here when they do not belong in the main file.

## Example Requests

- `${skill_name} [TODO: add a short, concrete example request]`
"""


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
    overwrite: bool,
    dry_run: bool,
) -> str:
    if not path.exists() or overwrite:
        return write_file(path, build_skill_md(skill_name, purpose), dry_run=dry_run)

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
        f"for example: manage_skill.py {retry_name} --import-path {source_dir}"
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
        project_link = project_root / ".agents" / "skills" / desired_name
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
                f"manage_skill.py {suggestions[0]} --import-path {source_dir}"
            )

    print("[INSPECT] Recommended import mode: copy")
    print(
        "[INSPECT] Move guidance: use --import-mode move only if you want the shared-library "
        "copy to become the sole source and you no longer need the original download directory."
    )

    if project_root:
        project_link = project_root / ".agents" / "skills" / desired_name
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
    if skill_md.exists():
        content = skill_md.read_text()
        summary["name"] = extract_frontmatter_value(content, "name") or skill_dir.name
        summary["description"] = extract_frontmatter_value(content, "description") or ""
    openai_path = skill_dir / "agents" / "openai.yaml"
    if openai_path.exists():
        interface = parse_openai_interface(openai_path.read_text())
        for key in ("display_name", "short_description", "default_prompt"):
            if interface.get(key):
                summary[key] = interface[key]
    return summary


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


def collect_project_skills(project_root: Path, library_root: Path) -> dict[str, object]:
    skills_dir = project_root / ".agents" / "skills"
    source_registry = load_external_source_registry(project_root)
    payload: dict[str, object] = {
        "mode": "list-project-skills",
        "project_root": str(project_root),
        "skills_directory": str(skills_dir),
        "skills_directory_exists": skills_dir.exists(),
        "count": 0,
        "entries": [],
    }
    if not skills_dir.exists():
        return payload

    entries = sorted(skills_dir.iterdir(), key=lambda path: path.name)
    payload["count"] = len(entries)
    for entry in entries:
        entry_payload: dict[str, object] = {
            "name": entry.name,
            "path": str(entry),
        }
        if entry.is_symlink():
            target = Path(os.path.realpath(entry))
            if not target.exists():
                status = "broken symlink"
            elif target.parent == library_root:
                status = "managed library link"
            else:
                status = "external symlink"
            entry_payload["status"] = status
            entry_payload["target"] = str(target)
            if target.exists() and (target / "SKILL.md").exists():
                summary = summarize_skill_metadata(target)
                if summary.get("display_name"):
                    entry_payload["display_name"] = summary["display_name"]
                if summary.get("short_description"):
                    entry_payload["short_description"] = summary["short_description"]
            registry_entry = source_registry.get(entry.name)
            if registry_entry and registry_entry.get("source_path"):
                entry_payload["source_path"] = registry_entry["source_path"]
                if registry_entry.get("import_mode"):
                    entry_payload["source_import_mode"] = registry_entry["import_mode"]
        elif entry.is_dir():
            entry_payload["status"] = "local directory (not a symlink)"
        else:
            entry_payload["status"] = "non-directory entry"
        payload["entries"].append(entry_payload)
    return payload


def list_project_skills(project_root: Path, library_root: Path, output_format: str = "text") -> int:
    payload = collect_project_skills(project_root, library_root)
    if output_format == "json":
        return emit_json(payload)

    print(f"[LIST] Project root: {project_root}")
    print(f"[LIST] Skills directory: {payload['skills_directory']}")
    if not payload["skills_directory_exists"]:
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


def ensure_existing_skill_dir(library_root: Path, skill_name: str) -> Path:
    skill_dir = library_root / skill_name
    if not skill_dir.exists():
        raise FileNotFoundError(
            f"Canonical skill not found for '{skill_name}': {skill_dir}"
        )
    return skill_dir


def list_managed_project_links(project_root: Path, library_root: Path) -> dict[str, Path]:
    skills_dir = project_root / ".agents" / "skills"
    if not skills_dir.exists():
        return {}
    result = {}
    for child in skills_dir.iterdir():
        if not child.is_symlink():
            continue
        target = Path(os.path.realpath(child))
        if target.parent == library_root:
            result[child.name] = child
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create, update, validate, and link skills using the shared-library workflow."
    )
    parser.add_argument(
        "skill_name",
        nargs="?",
        help="Skill name to create, update, or import (normalized to hyphen-case)",
    )
    parser.add_argument(
        "--library-root",
        help=(
            f"Canonical shared-library root. Defaults to ${DEFAULT_LIBRARY_ENV} or "
            "the parent library directory inferred from this script."
        ),
    )
    parser.add_argument(
        "--project-root",
        help="Project root where .agents/skills/<skill-name> should be linked",
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
        "--inspect-import",
        action="store_true",
        help="Inspect a local skill import candidate without writing any files",
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
        "--runtime-skills-root",
        help=(
            "Optional runtime skills root for direct Codex discovery. "
            f"Defaults to ${DEFAULT_CODEX_HOME_ENV}/{DEFAULT_RUNTIME_SKILLS_DIRNAME}."
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
        help="Attach only skill-workflow-manager when onboarding a project without an explicit skill list",
    )
    parser.add_argument(
        "--bootstrap-project-layout",
        action="store_true",
        help=(
            "Initialize a project root for shared-library management by ensuring "
            "_skill-library and .agents/skills exist and by linking the current "
            "skill package into that managed layout."
        ),
    )
    parser.add_argument(
        "--register-runtime-skill",
        action="store_true",
        help=(
            "Register a skill package into the runtime skills root so Codex can "
            "discover it directly."
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
        help="Rewrite SKILL.md from the template instead of updating only the frontmatter",
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
            "Defaults to --import-path, the canonical skill, or this package."
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
    return parser.parse_args()


def resolve_execution_context(args: argparse.Namespace) -> ExecutionContext:
    root_override_provided = bool(args.library_root or os.environ.get(DEFAULT_LIBRARY_ENV))
    runtime_skill_dir = detect_runtime_skill_dir()
    project_root = Path(args.project_root).expanduser().resolve() if args.project_root else None
    import_path = Path(args.import_path).expanduser().resolve() if args.import_path else None
    auto_bootstrap_import = False
    kept_existing_canonical = False
    project_root_inferred_from_cwd = False
    effective_bootstrap_project_layout = args.bootstrap_project_layout
    bootstrap_cleanup_source: Path | None = None
    bootstrap_source_candidate: Path | None = None
    runtime_skills_root = (
        detect_runtime_skills_root(args.runtime_skills_root)
        if args.register_runtime_skill
        else None
    )

    if project_root is None:
        inferred_cwd_project_root = infer_project_root_from_cwd(import_path, runtime_skill_dir)
        if inferred_cwd_project_root is not None:
            project_root = inferred_cwd_project_root
            project_root_inferred_from_cwd = True
            if import_path is not None:
                effective_bootstrap_project_layout = True

    if effective_bootstrap_project_layout and project_root is None:
        project_root = infer_project_root_for_bootstrap(import_path, runtime_skill_dir)
        if project_root is None:
            print(
                "[ERROR] Could not infer a project root for --bootstrap-project-layout. "
                "Provide --project-root explicitly."
            )
            return 1

    if effective_bootstrap_project_layout and import_path is None:
        if not (runtime_skill_dir / "SKILL.md").exists():
            print(
                "[ERROR] Could not infer an import source for --bootstrap-project-layout. "
                "Provide --import-path explicitly."
            )
            return 1
        import_path = runtime_skill_dir
        auto_bootstrap_import = True
    if effective_bootstrap_project_layout and import_path is not None:
        bootstrap_source_candidate = import_path

    inferred_import_name = detect_skill_name_from_source(import_path) if import_path else ""
    skill_name = normalize_skill_name(args.skill_name) if args.skill_name else inferred_import_name
    library_root = detect_library_root(
        args.library_root,
        project_root=project_root,
        bootstrap_project_layout=effective_bootstrap_project_layout,
    )
    compat_root = detect_compat_root(
        args.compat_root,
        library_root,
        allow_default=bool(skill_name and not args.no_compat_link),
    )
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
        (project_root / DEFAULT_LIBRARY_DIRNAME).resolve() if project_root else None
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
        bool(args.register_runtime_skill),
    ]
    if sum(project_modes) > 1:
        raise UsageError(
            "[ERROR] Use only one of --project-skills, --unlink-skills, "
            "--sync-project-skills, --bootstrap-project, --bootstrap-project-layout, "
            "or --register-runtime-skill at a time."
        )

    if args.bootstrap_project and not project_skills:
        project_skills = ["skill-workflow-manager"]

    report_compat_root = bool(compat_root and (project_root is None or compat_root != project_root))

    return ExecutionContext(
        args=args,
        runtime_skill_dir=runtime_skill_dir,
        project_root=project_root,
        import_path=import_path,
        skill_name=skill_name,
        library_root=library_root,
        compat_root=compat_root,
        runtime_skills_root=runtime_skills_root,
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
        and not args.register_runtime_skill
        and not args.validate_only
    ):
        raise UsageError(
            "[ERROR] Provide a skill name to create/update, or use a project skill operation."
        )

    if ctx.import_path and (ctx.project_skills or ctx.unlink_skills or ctx.sync_project_skills):
        raise UsageError(
            "[ERROR] --import-path cannot be combined with project skill add/remove/sync modes."
        )

    if args.inspect_import and not ctx.import_path:
        raise UsageError("[ERROR] --inspect-import requires --import-path.")

    if args.validate_only:
        if (
            args.list_library_skills
            or args.list_project_skills
            or ctx.project_skills
            or ctx.unlink_skills
            or ctx.sync_project_skills
            or args.bootstrap_project
            or args.bootstrap_project_layout
            or args.register_runtime_skill
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
            or args.runtime_skills_root
            or args.no_compat_link
        ):
            raise UsageError(
                "[ERROR] --validate-only is read-only and cannot be combined with "
                "listing, mutation, inspect, dry-run, compat-link, or metadata flags."
            )

    if args.format == "json" and not (
        args.validate_only or args.list_library_skills or args.list_project_skills or args.inspect_import
    ):
        raise UsageError(
            "[ERROR] --format json is supported only with --validate-only, "
            "--list-library-skills, --list-project-skills, or --inspect-import."
        )

    if args.list_library_skills or args.list_project_skills:
        if (
            ctx.skill_name
            or ctx.import_path
            or ctx.project_skills
            or ctx.unlink_skills
            or ctx.sync_project_skills
            or args.bootstrap_project
            or args.bootstrap_project_layout
            or args.register_runtime_skill
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
            or args.runtime_skills_root
        ):
            raise UsageError(
                "[ERROR] Listing modes are read-only and cannot be combined with create, import, "
                "inspect, update, or project mutation flags."
            )
            return

    if args.inspect_import and not ctx.skill_name:
        raise UsageError("[ERROR] Could not determine a canonical skill name for inspection.")

    if args.register_runtime_skill:
        if (
            args.list_library_skills
            or args.list_project_skills
            or ctx.project_skills
            or ctx.unlink_skills
            or ctx.sync_project_skills
            or args.bootstrap_project
            or args.bootstrap_project_layout
            or args.inspect_import
            or args.resources
            or args.purpose
            or args.display_name
            or args.short_description
            or args.default_prompt
            or args.overwrite_skill_md
            or args.overwrite_openai
            or args.compat_root
            or args.no_compat_link
        ):
            raise UsageError(
                "[ERROR] --register-runtime-skill can be combined only with an optional "
                "<skill-name>, --import-path, --library-root, --runtime-skills-root, "
                "--dry-run, and --skip-validate."
            )
        if args.import_mode != "copy":
            raise UsageError(
                "[ERROR] --register-runtime-skill does not use --import-mode. "
                "Remove that flag or keep the default copy mode."
            )


def print_execution_context(ctx: ExecutionContext) -> None:
    args = ctx.args

    print(f"[INFO] Library root: {ctx.library_root}")
    if ctx.project_root:
        print(f"[INFO] Project root: {ctx.project_root}")
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
    if args.register_runtime_skill and ctx.runtime_skills_root:
        print(f"[INFO] Runtime skills root: {ctx.runtime_skills_root}")
    if args.dry_run:
        print("[INFO] Dry-run mode enabled. No files will be modified.")


def resolve_runtime_registration_source(
    ctx: ExecutionContext,
) -> tuple[Path, str]:
    if ctx.import_path is not None:
        source_dir = ctx.import_path
        detected_name = detect_skill_name_from_source(source_dir)
        if ctx.skill_name and detected_name and ctx.skill_name != detected_name:
            raise ValueError(
                f"Explicit skill name '{ctx.skill_name}' does not match import source "
                f"name '{detected_name}'."
            )
        skill_name = ctx.skill_name or detected_name
    elif ctx.skill_name:
        source_dir = ensure_existing_skill_dir(ctx.library_root, ctx.skill_name)
        skill_name = ctx.skill_name
    else:
        source_dir = ctx.runtime_skill_dir
        skill_name = detect_skill_name_from_source(source_dir)

    if not source_dir.exists():
        raise FileNotFoundError(f"Runtime registration source does not exist: {source_dir}")
    if not source_dir.is_dir():
        raise NotADirectoryError(
            f"Runtime registration source is not a directory: {source_dir}"
        )
    if not skill_name:
        raise ValueError(
            "Could not determine a skill name for runtime registration. "
            "Provide <skill-name> or --import-path explicitly."
        )

    return source_dir, skill_name


def ensure_runtime_skill_registration(
    runtime_skills_root: Path,
    skill_name: str,
    source_dir: Path,
    dry_run: bool = False,
) -> tuple[Path, str]:
    registration_path = runtime_skills_root / skill_name
    if (
        registration_path.exists()
        and not registration_path.is_symlink()
        and registration_path.resolve() == source_dir.resolve()
    ):
        return registration_path, "already present"
    status = ensure_symlink(registration_path, source_dir, dry_run=dry_run)
    return registration_path, status


def handle_runtime_registration_mode(ctx: ExecutionContext) -> int:
    print_execution_context(ctx)

    try:
        source_dir, runtime_skill_name = resolve_runtime_registration_source(ctx)
        if not ctx.args.skip_validate:
            if ctx.args.dry_run:
                print(
                    f"[NEXT] Dry-run complete. Validation would run for {source_dir} "
                    "before registering the runtime skill."
                )
            else:
                validation_status = report_validation(source_dir)
                if validation_status != 0:
                    return validation_status
        else:
            print("[NEXT] Validation skipped by request.")

        registration_path, registration_status = ensure_runtime_skill_registration(
            ctx.runtime_skills_root,
            runtime_skill_name,
            source_dir,
            dry_run=ctx.args.dry_run,
        )
    except (FileExistsError, FileNotFoundError, NotADirectoryError, ValueError) as error:
        print(f"[ERROR] {error}")
        return 1

    print(f"[INFO] Runtime registration source: {source_dir}")
    print(
        f"[OK] Runtime skill registration ({registration_status}): "
        f"{registration_path}"
    )
    return 0


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


def handle_listing_mode(ctx: ExecutionContext) -> int:
    if ctx.args.list_library_skills:
        list_library_skills(ctx.library_root, output_format=ctx.args.format)
    if ctx.args.list_project_skills:
        list_project_skills(ctx.project_root, ctx.library_root, output_format=ctx.args.format)
    return 0


def handle_inspect_mode(ctx: ExecutionContext) -> int:
    return inspect_import_source(
        ctx.import_path,
        ctx.library_root,
        ctx.skill_name,
        ctx.project_root,
        output_format=ctx.args.format,
    )


def manage_canonical_skill(ctx: ExecutionContext) -> Path | None:
    if not ctx.skill_name:
        return None

    args = ctx.args
    canonical_skill_dir = ctx.library_root / ctx.skill_name
    library_status = ensure_directory(ctx.library_root, dry_run=args.dry_run)
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
    if ctx.import_path:
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
        project_link = ctx.project_root / ".agents" / "skills" / ctx.skill_name
        link_status = ensure_symlink(
            project_link,
            canonical_skill_dir,
            dry_run=args.dry_run,
        )
        print(f"[OK] Project link ({link_status}): {project_link}")

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
    for requested_skill in ctx.project_skills:
        requested_dir = ensure_existing_skill_dir(ctx.library_root, requested_skill)
        project_link = ctx.project_root / ".agents" / "skills" / requested_skill
        link_status = ensure_symlink(
            project_link,
            requested_dir,
            dry_run=ctx.args.dry_run,
        )
        print(f"[OK] Project skill link ({link_status}): {project_link}")

    for requested_skill in ctx.unlink_skills:
        project_link = ctx.project_root / ".agents" / "skills" / requested_skill
        unlink_status = unlink_symlink(project_link, dry_run=ctx.args.dry_run)
        print(f"[OK] Project skill unlink ({unlink_status}): {project_link}")

    if ctx.sync_project_skills:
        desired_skills = set(ctx.sync_project_skills)
        for requested_skill in ctx.sync_project_skills:
            requested_dir = ensure_existing_skill_dir(ctx.library_root, requested_skill)
            project_link = ctx.project_root / ".agents" / "skills" / requested_skill
            link_status = ensure_symlink(
                project_link,
                requested_dir,
                dry_run=ctx.args.dry_run,
            )
            print(f"[OK] Project sync link ({link_status}): {project_link}")

        existing_links = list_managed_project_links(ctx.project_root, ctx.library_root)
        for existing_name, existing_link in sorted(existing_links.items()):
            if existing_name in desired_skills:
                continue
            unlink_status = unlink_symlink(existing_link, dry_run=ctx.args.dry_run)
            print(f"[OK] Project sync unlink ({unlink_status}): {existing_link}")


def finalize_mutation_mode(ctx: ExecutionContext, canonical_skill_dir: Path | None) -> int:
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
    if ctx.bootstrap_cleanup_source is not None and canonical_skill_dir is not None:
        cleanup_status = remove_path(ctx.bootstrap_cleanup_source, dry_run=ctx.args.dry_run)
        print(
            f"[OK] Bootstrap source cleanup ({cleanup_status}): "
            f"{ctx.bootstrap_cleanup_source}"
        )
    return 0


def handle_mutation_mode(ctx: ExecutionContext) -> int:
    print_execution_context(ctx)

    canonical_skill_dir: Path | None = None
    try:
        canonical_skill_dir = manage_canonical_skill(ctx)
        run_project_skill_operations(ctx)
    except (FileExistsError, FileNotFoundError, NotADirectoryError, ValueError) as error:
        print(f"[ERROR] {error}")
        return 1

    return finalize_mutation_mode(ctx, canonical_skill_dir)


def main() -> int:
    args = parse_args()
    try:
        ctx = resolve_execution_context(args)
        validate_execution_context(ctx)
    except UsageError as error:
        print(error)
        return 1

    if args.validate_only:
        return handle_validate_only_mode(ctx)
    if args.list_library_skills or args.list_project_skills:
        return handle_listing_mode(ctx)
    if args.inspect_import:
        if args.format == "text":
            print_execution_context(ctx)
        return handle_inspect_mode(ctx)
    if args.register_runtime_skill:
        return handle_runtime_registration_mode(ctx)
    return handle_mutation_mode(ctx)


if __name__ == "__main__":
    sys.exit(main())
