#!/usr/bin/env python3
"""Static evaluation harness for the long-task continuity suite."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DIMENSIONS = (
    "routing_quality",
    "artifact_presence",
    "workflow_completeness",
    "docs_clarity",
    "guardrails",
)


@dataclass(frozen=True)
class EvalCase:
    case_id: str
    package: str
    scenario_type: str
    should_trigger: bool
    user_prompt: str
    expected_artifacts: list[str]
    expected_events: list[str]
    notes: str
    max_commands: int | None = None
    max_verbosity: str | None = None


PACKAGE_RULES: dict[str, dict[str, Any]] = {
    "skill-context-keeper": {
        "required_files": [
            "README.md",
            "README.zh-CN.md",
            "SKILL.md",
            "references/use-cases.md",
            "references/use-cases.zh-CN.md",
            "references/prompt-templates.en.md",
            "references/prompt-templates.zh-CN.md",
            "assets/TASK_STATE.template.md",
        ],
        "routing_phrases": [
            "use this skill when",
            "resuming a task",
            "rebuilding the last known task state",
            "updating a downstream state file such as `.agent-state/task_state.md`",
        ],
        "boundary_phrases": [
            "do not run phase gates",
            "do not generate final handoffs",
            "does not own workflow gating",
            "does not own final handoffs",
        ],
        "artifact_map": {
            "state/context.snapshot": "assets/TASK_STATE.template.md",
            "state/continuity.note": "assets/TASK_STATE.template.md",
        },
        "workflow_files": [
            "references/use-cases.md",
            "references/use-cases.zh-CN.md",
            "references/prompt-templates.en.md",
            "references/prompt-templates.zh-CN.md",
        ],
    },
    "skill-phase-gate": {
        "required_files": [
            "README.md",
            "README.zh-CN.md",
            "SKILL.md",
            "references/README.md",
            "references/README.zh-CN.md",
            "references/use-cases.md",
            "references/use-cases.zh-CN.md",
            "references/prompt-templates.en.md",
            "references/prompt-templates.zh-CN.md",
            "assets/PREFLIGHT.template.md",
            "assets/POSTFLIGHT.template.md",
        ],
        "routing_phrases": [
            "meaningful coding checkpoint",
            "preflight or postflight",
            "meaningful checkpoint bar",
            "use this skill when",
        ],
        "boundary_phrases": [
            "not for trivial one-line edits",
            "not for pure explanation tasks",
            "does not replace planning packages",
            "does not become a handoff generator",
        ],
        "artifact_map": {
            "plan/phase.plan": "assets/PREFLIGHT.template.md",
            "plan/checkpoints.md": "assets/PREFLIGHT.template.md",
            "plan/exit-criteria.md": "assets/POSTFLIGHT.template.md",
        },
        "workflow_files": [
            "references/README.md",
            "references/README.zh-CN.md",
            "references/use-cases.md",
            "references/use-cases.zh-CN.md",
            "assets/PREFLIGHT.template.md",
            "assets/POSTFLIGHT.template.md",
        ],
    },
    "skill-handoff-summary": {
        "required_files": [
            "README.md",
            "README.zh-CN.md",
            "SKILL.md",
            "references/README.md",
            "references/README.zh-CN.md",
            "references/use-cases.md",
            "references/use-cases.zh-CN.md",
            "references/prompt-templates.en.md",
            "references/prompt-templates.zh-CN.md",
            "assets/HANDOFF.template.md",
        ],
        "routing_phrases": [
            "continuation-oriented",
            "handoff",
            "use this skill when",
            "writing or refreshing a compact artifact such as `.agent-state/handoff.md`",
        ],
        "boundary_phrases": [
            "does not own long-term state",
            "does not own workflow gating",
            "not a full-project documentation",
            "replacing the final user-facing answer when no handoff is needed",
        ],
        "artifact_map": {
            "handoff/HANDOFF.md": "assets/HANDOFF.template.md",
            "handoff/blockers.md": "assets/HANDOFF.template.md",
            "handoff/next-steps.md": "assets/HANDOFF.template.md",
        },
        "workflow_files": [
            "references/README.md",
            "references/README.zh-CN.md",
            "references/use-cases.md",
            "references/use-cases.zh-CN.md",
            "assets/HANDOFF.template.md",
        ],
    },
    "skill-task-continuity": {
        "required_files": [
            "README.md",
            "README.zh-CN.md",
            "SKILL.md",
            "references/composition-guide.md",
            "references/install-playbook.md",
            "assets/AGENTS.repo-template.md",
            "assets/agent-state/TASK_STATE.template.md",
            "assets/agent-state/HANDOFF.template.md",
            "assets/agent-state/DECISIONS.template.md",
            "assets/agent-state/RUN_LOG.template.md",
        ],
        "routing_phrases": [
            "bootstrapping the long-task continuity suite",
            "deciding which atomic package should trigger first",
            "composition boundary",
            "use this skill when",
        ],
        "boundary_phrases": [
            "does not replace the three atomic skills",
            "do not use this package to mutate the public library root into a consumer repo",
            "downstream templates",
            "route suite-shaped requests to the atomic package",
        ],
        "artifact_map": {
            "AGENTS.md": "assets/AGENTS.repo-template.md",
            ".agent-state/TASK_STATE.md": "assets/agent-state/TASK_STATE.template.md",
            ".agent-state/HANDOFF.md": "assets/agent-state/HANDOFF.template.md",
        },
        "workflow_files": [
            "references/composition-guide.md",
            "references/install-playbook.md",
            "assets/AGENTS.repo-template.md",
            "assets/agent-state/TASK_STATE.template.md",
            "assets/agent-state/HANDOFF.template.md",
        ],
    },
}


def _normalize_text(text: str) -> str:
    return " ".join(text.lower().split())


def _split_tokens(raw: str) -> list[str]:
    value = raw.strip()
    if not value or value.lower() == "none":
        return []
    return [part.strip() for part in value.split("|") if part.strip()]


def _parse_bool(raw: str) -> bool:
    value = raw.strip().lower()
    if value in {"yes", "true", "1"}:
        return True
    if value in {"no", "false", "0"}:
        return False
    raise ValueError(f"invalid boolean value: {raw!r}")


def _optional_int(raw: str | None) -> int | None:
    if raw is None:
        return None
    value = raw.strip()
    if not value:
        return None
    return int(value)


def load_cases(csv_path: Path) -> list[EvalCase]:
    with csv_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    cases: list[EvalCase] = []
    for row in rows:
        cases.append(
            EvalCase(
                case_id=row["case_id"].strip(),
                package=row["package"].strip(),
                scenario_type=row["scenario_type"].strip(),
                should_trigger=_parse_bool(row["should_trigger"]),
                user_prompt=row["user_prompt"].strip(),
                expected_artifacts=_split_tokens(row["expected_artifacts"]),
                expected_events=_split_tokens(row["expected_events"]),
                notes=row["notes"].strip(),
                max_commands=_optional_int(row.get("max_commands")),
                max_verbosity=(row.get("max_verbosity") or "").strip() or None,
            )
        )
    return cases


def _package_dir(repo_root: Path, package: str) -> Path:
    return repo_root / "skills" / package


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _check_required_files(package_root: Path, required_files: list[str]) -> list[str]:
    missing = []
    for relative in required_files:
        if not (package_root / relative).exists():
            missing.append(relative)
    return missing


def _contains_any(text: str, phrases: list[str]) -> bool:
    normalized = _normalize_text(text)
    return any(phrase in normalized for phrase in phrases)


def _artifact_targets(case: EvalCase, package_rules: dict[str, Any]) -> list[Path]:
    artifact_map: dict[str, str] = package_rules["artifact_map"]
    targets = []
    for artifact in case.expected_artifacts:
        mapped = artifact_map.get(artifact)
        if mapped is not None:
            targets.append(mapped)
    return [Path(target) for target in targets]


def evaluate_case(repo_root: Path, case: EvalCase) -> dict[str, Any]:
    package_rules = PACKAGE_RULES.get(case.package)
    package_root = _package_dir(repo_root, case.package)
    result: dict[str, Any] = {
        "case_id": case.case_id,
        "package": case.package,
        "scenario_type": case.scenario_type,
        "should_trigger": case.should_trigger,
        "dimensions": {},
        "details": {},
    }

    if package_rules is None:
        result["dimensions"] = {
            dimension: {"status": "fail", "reason": f"unknown package: {case.package}"}
            for dimension in DIMENSIONS
        }
        result["details"]["unknown_package"] = case.package
        return result

    missing_files = _check_required_files(package_root, package_rules["required_files"])
    if missing_files:
        docs_status = "fail"
        docs_reason = f"missing required files: {', '.join(missing_files)}"
    else:
        docs_status = "pass"
        docs_reason = "required docs and assets are present"

    sk_text = _read_text(package_root / "SKILL.md")
    readme_text = _read_text(package_root / "README.md")
    readme_zh_text = _read_text(package_root / "README.zh-CN.md")
    routing_status = "pass" if _contains_any(sk_text + "\n" + readme_text, package_rules["routing_phrases"]) else "fail"
    routing_reason = "routing hints present" if routing_status == "pass" else "missing routing hints"

    boundary_sources = readme_text + "\n" + readme_zh_text + "\n" + sk_text
    workflow_status = "pass" if _contains_any(boundary_sources, package_rules["boundary_phrases"]) else "fail"
    workflow_reason = "workflow and boundary language present" if workflow_status == "pass" else "missing workflow boundary language"

    artifact_targets = [package_root / target for target in _artifact_targets(case, package_rules)]
    artifact_missing = [str(path.relative_to(package_root)) for path in artifact_targets if not path.exists()]
    if artifact_missing:
        artifact_status = "fail"
        artifact_reason = f"missing mapped artifacts: {', '.join(artifact_missing)}"
    else:
        artifact_status = "pass"
        artifact_reason = "expected artifact templates are present"

    if case.max_commands is None and case.max_verbosity is None:
        guardrail_status = "skipped"
        guardrail_reason = "no optional guardrails configured"
    else:
        guardrail_status = "pass"
        guardrail_reason = "optional guardrails parsed"

    result["dimensions"] = {
        "routing_quality": {"status": routing_status, "reason": routing_reason},
        "artifact_presence": {"status": artifact_status, "reason": artifact_reason},
        "workflow_completeness": {"status": workflow_status, "reason": workflow_reason},
        "docs_clarity": {"status": docs_status, "reason": docs_reason},
        "guardrails": {"status": guardrail_status, "reason": guardrail_reason},
    }

    result["details"] = {
        "required_files": package_rules["required_files"],
        "expected_events": list(case.expected_events),
        "expected_artifacts": list(case.expected_artifacts),
    }
    return result


def _summarize_cases(case_results: list[dict[str, Any]]) -> dict[str, Any]:
    summary = {
        "cases": len(case_results),
        "passed": 0,
        "failed": 0,
        "dimensions": {name: {"pass": 0, "fail": 0, "skipped": 0} for name in DIMENSIONS},
    }

    for case in case_results:
        dimension_statuses = [item["status"] for item in case["dimensions"].values()]
        if any(status == "fail" for status in dimension_statuses):
            summary["failed"] += 1
        else:
            summary["passed"] += 1
        for name, dimension in case["dimensions"].items():
            summary["dimensions"][name][dimension["status"]] += 1
    return summary


def run_evaluations(repo_root: Path, cases_csv: Path) -> dict[str, Any]:
    cases = load_cases(cases_csv)
    case_results = [evaluate_case(repo_root, case) for case in cases]
    return {
        "repo_root": str(repo_root),
        "cases_csv": str(cases_csv),
        "cases": case_results,
        "summary": _summarize_cases(case_results),
        "dimensions": list(DIMENSIONS),
    }


def render_text_report(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"Repo: {report['repo_root']}")
    lines.append(f"Cases: {report['summary']['cases']}  Passed: {report['summary']['passed']}  Failed: {report['summary']['failed']}")
    lines.append("")
    lines.append("By case:")
    for case in report["cases"]:
        statuses = ", ".join(
            f"{name}={dimension['status']}"
            for name, dimension in case["dimensions"].items()
        )
        lines.append(
            f"- {case['case_id']} [{case['package']}] should_trigger={str(case['should_trigger']).lower()} -> {statuses}"
        )
        for name, dimension in case["dimensions"].items():
            lines.append(f"  - {name}: {dimension['status']} ({dimension['reason']})")
    lines.append("")
    lines.append("By dimension:")
    for name, counts in report["summary"]["dimensions"].items():
        lines.append(
            f"- {name}: pass={counts['pass']} fail={counts['fail']} skipped={counts['skipped']}"
        )
    return "\n".join(lines)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root to evaluate.",
    )
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path(__file__).resolve().with_name("cases.csv"),
        help="Path to the seed cases CSV.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format for the report.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    report = run_evaluations(args.repo_root, args.cases)
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_text_report(report))
    return 0 if report["summary"]["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
