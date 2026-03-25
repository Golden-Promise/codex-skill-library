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
        "trigger_cues": [
            "use this skill when",
            "resuming a task",
            "resume from the last known state",
            "refresh state",
            "rebuilding the last known task state",
            "carry forward unresolved todo",
            "carry forward unresolved todos",
            "update .agent-state/task_state.md",
        ],
        "suppress_cues": [
            "one-off",
            "do nothing else",
            "just answer",
            "punctuation question",
            "does not own workflow gating",
            "does not own final handoffs",
        ],
        "artifact_map": {
            "state/context.snapshot": "assets/TASK_STATE.template.md",
            "state/continuity.note": "assets/TASK_STATE.template.md",
        },
        "positive_event_prefixes": ["context:"],
        "negative_event_prefixes": ["context:skip", "direct:answer"],
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
        "trigger_cues": [
            "meaningful coding checkpoint",
            "preflight",
            "postflight",
            "split",
            "phases",
            "multi-step",
            "refactor",
            "before coding",
            "use this skill when",
        ],
        "suppress_cues": [
            "not for trivial one-line edits",
            "tiny edit",
            "rename this heading",
            "one-line change",
            "not for pure explanation tasks",
            "does not replace planning packages",
            "does not become a handoff generator",
        ],
        "artifact_map": {
            "plan/phase.plan": "assets/PREFLIGHT.template.md",
            "plan/checkpoints.md": "assets/PREFLIGHT.template.md",
            "plan/exit-criteria.md": "assets/POSTFLIGHT.template.md",
        },
        "positive_event_prefixes": ["phase:"],
        "negative_event_prefixes": ["phase:skip", "direct:edit"],
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
        "trigger_cues": [
            "continuation-oriented",
            "handoff",
            "write a handoff",
            "pause",
            "transfer",
            "use this skill when",
            "writing or refreshing a compact artifact such as `.agent-state/handoff.md`",
        ],
        "suppress_cues": [
            "final answer",
            "no handoff",
            "just give me",
            "do nothing else",
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
        "positive_event_prefixes": ["handoff:"],
        "negative_event_prefixes": ["handoff:skip", "direct:answer"],
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
        "trigger_cues": [
            "bootstrapping the long-task continuity suite",
            "continuity suite",
            "set up the long-task continuity suite",
            "coordinate",
            "deciding which atomic package should trigger first",
            "composition boundary",
            "use this skill when",
        ],
        "suppress_cues": [
            "one-line readme fix",
            "trivial edit",
            "do not use this package to mutate the public library root into a consumer repo",
            "does not replace the three atomic skills",
            "route suite-shaped requests to the atomic package",
        ],
        "artifact_map": {
            "AGENTS.md": "assets/AGENTS.repo-template.md",
            ".agent-state/TASK_STATE.md": "assets/agent-state/TASK_STATE.template.md",
            ".agent-state/HANDOFF.md": "assets/agent-state/HANDOFF.template.md",
        },
        "positive_event_prefixes": ["bootstrap:"],
        "negative_event_prefixes": ["bootstrap:skip", "direct:edit"],
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


def _matched_phrases(text: str, phrases: list[str]) -> list[str]:
    normalized = _normalize_text(text)
    return [phrase for phrase in phrases if phrase in normalized]


def _artifact_targets(case: EvalCase, package_rules: dict[str, Any]) -> tuple[list[Path], list[str]]:
    artifact_map: dict[str, str] = package_rules["artifact_map"]
    targets = []
    unmapped = []
    for artifact in case.expected_artifacts:
        mapped = artifact_map.get(artifact)
        if mapped is not None:
            targets.append(mapped)
        else:
            unmapped.append(artifact)
    return [Path(target) for target in targets], unmapped


def _score_routing(case: EvalCase, package_rules: dict[str, Any]) -> dict[str, Any]:
    trigger_hits = _matched_phrases(case.user_prompt, package_rules["trigger_cues"])
    suppress_hits = _matched_phrases(case.user_prompt, package_rules["suppress_cues"])

    if case.should_trigger:
        status = "pass" if trigger_hits and not suppress_hits else "fail"
        if status == "pass":
            reason = f"trigger cues matched: {', '.join(trigger_hits)}"
        else:
            reason = (
                "missing trigger cues or conflicting suppress cues: "
                f"trigger={trigger_hits or ['none']}, suppress={suppress_hits or ['none']}"
            )
    else:
        status = "pass" if suppress_hits else "fail"
        if status == "pass":
            reason = f"suppress cues matched: {', '.join(suppress_hits)}"
        else:
            reason = "missing suppress cues for a should-not-trigger case"

    return {
        "status": status,
        "reason": reason,
        "trigger_hits": trigger_hits,
        "suppress_hits": suppress_hits,
    }


def _score_events(case: EvalCase, package_rules: dict[str, Any]) -> dict[str, Any]:
    allowed_prefixes = (
        package_rules["positive_event_prefixes"]
        if case.should_trigger
        else package_rules["negative_event_prefixes"]
    )
    matching = []
    mismatched = []
    for event in case.expected_events:
        if any(event.startswith(prefix) for prefix in allowed_prefixes):
            matching.append(event)
        else:
            mismatched.append(event)

    if not case.expected_events:
        status = "fail"
        reason = "expected events were not provided"
    elif mismatched:
        status = "fail"
        reason = (
            "event tokens do not match the expected namespace: "
            f"allowed={allowed_prefixes}, mismatched={mismatched}"
        )
    else:
        status = "pass"
        reason = f"event namespace matched: {', '.join(matching)}"

    return {
        "status": status,
        "reason": reason,
        "matching": matching,
        "mismatched": mismatched,
    }


def _score_docs(package_root: Path, package_rules: dict[str, Any]) -> dict[str, Any]:
    missing_files = _check_required_files(package_root, package_rules["required_files"])
    missing_workflow_docs = _check_required_files(package_root, package_rules["workflow_files"])
    boundary_sources = (
        _read_text(package_root / "README.md")
        + "\n"
        + _read_text(package_root / "README.zh-CN.md")
        + "\n"
        + _read_text(package_root / "SKILL.md")
    )
    boundary_hits = _matched_phrases(boundary_sources, package_rules["suppress_cues"])

    if missing_files:
        status = "fail"
        reason = f"missing required files: {', '.join(missing_files)}"
    elif missing_workflow_docs:
        status = "fail"
        reason = f"missing workflow docs: {', '.join(missing_workflow_docs)}"
    elif not boundary_hits:
        status = "fail"
        reason = "missing boundary language in README and SKILL docs"
    else:
        status = "pass"
        reason = "required docs, workflow docs, and boundary language are present"

    return {
        "status": status,
        "reason": reason,
        "missing_files": missing_files,
        "missing_workflow_docs": missing_workflow_docs,
        "boundary_hits": boundary_hits,
    }


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

    routing = _score_routing(case, package_rules)
    events = _score_events(case, package_rules)
    docs = _score_docs(package_root, package_rules)

    artifact_targets, unmapped_artifacts = _artifact_targets(case, package_rules)
    artifact_missing = [str((package_root / path).relative_to(package_root)) for path in artifact_targets if not (package_root / path).exists()]
    if unmapped_artifacts:
        artifact_status = "fail"
        artifact_reason = f"unmapped expected artifacts: {', '.join(unmapped_artifacts)}"
    elif artifact_missing:
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
        "routing_quality": {
            "status": routing["status"],
            "reason": routing["reason"],
        },
        "artifact_presence": {"status": artifact_status, "reason": artifact_reason},
        "workflow_completeness": {
            "status": events["status"],
            "reason": events["reason"],
        },
        "docs_clarity": {"status": docs["status"], "reason": docs["reason"]},
        "guardrails": {"status": guardrail_status, "reason": guardrail_reason},
    }

    result["details"] = {
        "required_files": package_rules["required_files"],
        "workflow_files": package_rules["workflow_files"],
        "expected_events": list(case.expected_events),
        "expected_artifacts": list(case.expected_artifacts),
        "trigger_hits": routing["trigger_hits"],
        "suppress_hits": routing["suppress_hits"],
        "matching_events": events["matching"],
        "mismatched_events": events["mismatched"],
        "unmapped_artifacts": unmapped_artifacts,
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
