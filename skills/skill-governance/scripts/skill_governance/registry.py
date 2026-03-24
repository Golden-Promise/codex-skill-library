"""Registry payload helpers for skill-governance."""

from __future__ import annotations

from .versioning import version_metadata


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


def build_registry_entry_payload(
    skill_name: str,
    canonical_location: str,
    target_summary: dict[str, str],
    governance: dict[str, object],
    skill_graph: dict[str, object],
    existing_entry: dict[str, object] | None,
    title_case_skill_name: callable,
) -> dict[str, object]:
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
        "version_info": version_metadata(version),
        "lifecycle_status": lifecycle_status,
        "canonical_location": canonical_location,
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

