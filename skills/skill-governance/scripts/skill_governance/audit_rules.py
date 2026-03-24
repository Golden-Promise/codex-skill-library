"""Audit rules for lifecycle, ownership, and version governance."""

from __future__ import annotations

from .constants import ALLOWED_LIFECYCLE_STATUSES
from .versioning import compare_versions, version_metadata


def build_audit_findings(
    registry_payload: dict[str, object],
    persisted_registry_payload: dict[str, object] | None = None,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    issues: list[dict[str, object]] = []
    recommendations: list[dict[str, object]] = []
    skills = registry_payload.get("skills", {})
    if not isinstance(skills, dict):
        return issues, recommendations

    persisted_skills = (
        persisted_registry_payload.get("skills", {})
        if isinstance(persisted_registry_payload, dict)
        and isinstance(persisted_registry_payload.get("skills"), dict)
        else {}
    )

    for skill_name, entry in sorted(skills.items()):
        if not isinstance(entry, dict):
            continue
        lifecycle_status = str(entry.get("lifecycle_status", "") or "")
        usage_stats = entry.get("usage_stats", {})
        if not isinstance(usage_stats, dict):
            usage_stats = {}
        active_projects_total = int(usage_stats.get("active_projects_total", 0) or 0)
        owner = str(entry.get("owner", "") or "")
        reviewer = str(entry.get("reviewer", "") or "")
        team = str(entry.get("team", "") or "")
        version = str(entry.get("version", "") or "")
        deprecation_policy = str(entry.get("deprecation_policy", "") or "")
        version_info = version_metadata(version)

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

        if lifecycle_status in {"active", "review", "deprecated", "blocked"} and not owner:
            issues.append(
                {
                    "type": "missing-owner",
                    "skill_name": skill_name,
                    "priority": "high",
                    "summary": f"{skill_name} is {lifecycle_status} but has no owner in the central registry.",
                    "next_step": "Set the owner field before treating this skill as a governed shared asset.",
                }
            )

        if lifecycle_status == "review" and not reviewer:
            issues.append(
                {
                    "type": "review-missing-reviewer",
                    "skill_name": skill_name,
                    "priority": "high",
                    "summary": f"{skill_name} is in review but has no reviewer assigned.",
                    "next_step": "Set the reviewer field before keeping this skill in review status.",
                }
            )

        if lifecycle_status in {"active", "review"} and not team:
            recommendations.append(
                {
                    "type": "missing-team",
                    "skill_name": skill_name,
                    "priority": "medium",
                    "summary": f"{skill_name} has no team in the central registry.",
                    "next_step": "Set the team field to clarify ownership routing and escalation.",
                }
            )

        if lifecycle_status in {"active", "review", "deprecated", "blocked"} and not version:
            issues.append(
                {
                    "type": "missing-version",
                    "skill_name": skill_name,
                    "priority": "high",
                    "summary": f"{skill_name} is {lifecycle_status} but has no version recorded.",
                    "next_step": "Record a version so upgrades, rollback planning, and audit history are easier to track.",
                }
            )
        elif version and not bool(version_info["valid"]):
            issues.append(
                {
                    "type": "invalid-version",
                    "skill_name": skill_name,
                    "priority": "high",
                    "summary": f"{skill_name} uses an invalid version value '{version}'.",
                    "next_step": "Use a semver-like value such as 1.2.3 or 2.0.0-beta.",
                }
            )
        elif lifecycle_status == "active" and str(version_info["channel"]) == "prerelease":
            recommendations.append(
                {
                    "type": "active-uses-prerelease-version",
                    "skill_name": skill_name,
                    "priority": "medium",
                    "summary": f"{skill_name} is active but still uses prerelease version {version}.",
                    "next_step": "Promote to a stable version when the skill is ready for broad reuse.",
                }
            )

        previous_entry = persisted_skills.get(skill_name)
        if isinstance(previous_entry, dict):
            previous_version = str(previous_entry.get("version", "") or "")
            version_change = compare_versions(version, previous_version)
            if version and previous_version and version_change == -1:
                issues.append(
                    {
                        "type": "version-regression",
                        "skill_name": skill_name,
                        "priority": "high",
                        "summary": (
                            f"{skill_name} version regressed from {previous_version} to {version}."
                        ),
                        "next_step": "Confirm whether this is intentional. If not, bump the version forward before release.",
                    }
                )

    return issues, recommendations

