import csv
import importlib.util
import re
import tempfile
import sys
import unittest
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "evals" / "run_evals.py"
CASES_CSV = ROOT / "evals" / "cases.csv"


def load_runner_module():
    spec = importlib.util.spec_from_file_location("run_evals", RUNNER)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_cases_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "case_id",
        "package",
        "scenario_type",
        "should_trigger",
        "user_prompt",
        "expected_artifacts",
        "expected_events",
        "notes",
    ]
    extra_fields = []
    for row in rows:
        for key in row:
            if key not in fieldnames and key not in extra_fields:
                extra_fields.append(key)
    fieldnames.extend(extra_fields)

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class RunEvalsTests(unittest.TestCase):
    def test_seed_cases_csv_has_expected_columns(self):
        self.assertTrue(CASES_CSV.exists(), "seed cases file should exist")

        with CASES_CSV.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))

        self.assertEqual(len(rows), 8)
        self.assertEqual(
            list(rows[0].keys()),
            [
                "case_id",
                "package",
                "scenario_type",
                "should_trigger",
                "user_prompt",
                "expected_artifacts",
                "expected_events",
                "notes",
            ],
        )

    def test_load_cases_normalizes_seed_matrix(self):
        self.assertTrue(RUNNER.exists(), "evaluation runner should exist")
        module = load_runner_module()

        cases = module.load_cases(CASES_CSV)

        self.assertEqual(len(cases), 8)
        context_resume = next(case for case in cases if case.case_id == "context_resume")
        self.assertTrue(context_resume.should_trigger)
        self.assertEqual(
            context_resume.expected_artifacts,
            ["state/context.snapshot", "state/continuity.note"],
        )
        self.assertEqual(
            context_resume.expected_events,
            ["context:reload", "context:reconstruct", "context:summary"],
        )

        suite_boundary_clean = next(
            case for case in cases if case.case_id == "suite_boundary_clean"
        )
        self.assertFalse(suite_boundary_clean.should_trigger)

    def test_run_evaluations_produces_case_and_dimension_results(self):
        self.assertTrue(RUNNER.exists(), "evaluation runner should exist")
        module = load_runner_module()

        result = module.run_evaluations(ROOT, CASES_CSV)

        self.assertEqual(result["summary"]["cases"], 8)
        self.assertIn("passed", result["summary"])
        self.assertIn("failed", result["summary"])
        self.assertIn("routing_quality", result["dimensions"])
        self.assertIn("artifact_presence", result["dimensions"])
        self.assertIn("workflow_completeness", result["dimensions"])
        self.assertIn("docs_clarity", result["dimensions"])

        case = next(item for item in result["cases"] if item["case_id"] == "suite_bootstrap")
        self.assertIn("routing_quality", case["dimensions"])
        self.assertIn("artifact_presence", case["dimensions"])
        self.assertIn("workflow_completeness", case["dimensions"])
        self.assertIn("docs_clarity", case["dimensions"])

    def test_optional_guardrail_columns_are_supported(self):
        self.assertTrue(RUNNER.exists(), "evaluation runner should exist")
        module = load_runner_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "cases.csv"
            write_cases_csv(
                csv_path,
                [
                    {
                        "case_id": "demo",
                        "package": "skill-context-keeper",
                        "scenario_type": "positive",
                        "should_trigger": "yes",
                        "user_prompt": "Refresh state",
                        "expected_artifacts": "assets/TASK_STATE.template.md",
                        "expected_events": "context:reload",
                        "notes": "optional guardrails",
                        "max_commands": "3",
                        "max_verbosity": "low",
                    }
                ],
            )

            cases = module.load_cases(csv_path)
            self.assertEqual(cases[0].max_commands, 3)
            self.assertEqual(cases[0].max_verbosity, "low")

    def test_positive_case_requires_trigger_cues_to_pass(self):
        self.assertTrue(RUNNER.exists(), "evaluation runner should exist")
        module = load_runner_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "cases.csv"
            write_cases_csv(
                csv_path,
                [
                    {
                        "case_id": "bad_positive",
                        "package": "skill-context-keeper",
                        "scenario_type": "positive",
                        "should_trigger": "yes",
                        "user_prompt": "Please answer this one-off punctuation question in the README and do nothing else.",
                        "expected_artifacts": "state/context.snapshot",
                        "expected_events": "context:reload",
                        "notes": "should fail if routing ignores polarity",
                    }
                ],
            )

            report = module.run_evaluations(ROOT, csv_path)

        case = report["cases"][0]
        self.assertEqual(report["summary"]["failed"], 1)
        self.assertEqual(case["dimensions"]["routing_quality"]["status"], "fail")
        self.assertIn("trigger cues", case["dimensions"]["routing_quality"]["reason"])

    def test_negative_case_requires_suppress_cues_to_block_routing(self):
        self.assertTrue(RUNNER.exists(), "evaluation runner should exist")
        module = load_runner_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "cases.csv"
            write_cases_csv(
                csv_path,
                [
                    {
                        "case_id": "bad_negative",
                        "package": "skill-handoff-summary",
                        "scenario_type": "negative",
                        "should_trigger": "no",
                        "user_prompt": "Please write a handoff with blockers and next steps for the pause.",
                        "expected_artifacts": "none",
                        "expected_events": "handoff:skip|direct:answer",
                        "notes": "should fail if negative polarity is ignored",
                    }
                ],
            )

            report = module.run_evaluations(ROOT, csv_path)

        case = report["cases"][0]
        self.assertEqual(report["summary"]["failed"], 1)
        self.assertEqual(case["dimensions"]["routing_quality"]["status"], "fail")
        self.assertIn("suppress cues", case["dimensions"]["routing_quality"]["reason"])

    def test_expected_events_must_match_package_namespace(self):
        self.assertTrue(RUNNER.exists(), "evaluation runner should exist")
        module = load_runner_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "cases.csv"
            write_cases_csv(
                csv_path,
                [
                    {
                        "case_id": "bad_events",
                        "package": "skill-phase-gate",
                        "scenario_type": "positive",
                        "should_trigger": "yes",
                        "user_prompt": "We need to split this multi-step refactor into phases before coding.",
                        "expected_artifacts": "plan/phase.plan",
                        "expected_events": "context:reload",
                        "notes": "should fail if expected events are not scored",
                    }
                ],
            )

            report = module.run_evaluations(ROOT, csv_path)

        case = report["cases"][0]
        self.assertEqual(report["summary"]["failed"], 1)
        self.assertEqual(case["dimensions"]["workflow_completeness"]["status"], "fail")
        self.assertIn("event", case["dimensions"]["workflow_completeness"]["reason"])

    def test_unmapped_expected_artifacts_fail_strict_mapping(self):
        self.assertTrue(RUNNER.exists(), "evaluation runner should exist")
        module = load_runner_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "cases.csv"
            write_cases_csv(
                csv_path,
                [
                    {
                        "case_id": "bad_artifacts",
                        "package": "skill-handoff-summary",
                        "scenario_type": "positive",
                        "should_trigger": "yes",
                        "user_prompt": "I need to stop for today; please write a handoff with blockers and next steps.",
                        "expected_artifacts": "handoff/HANDOFF.md|handoff/missing.md",
                        "expected_events": "handoff:capture",
                        "notes": "should fail if unmapped artifact tokens are ignored",
                    }
                ],
            )

            report = module.run_evaluations(ROOT, csv_path)

        case = report["cases"][0]
        self.assertEqual(report["summary"]["failed"], 1)
        self.assertEqual(case["dimensions"]["artifact_presence"]["status"], "fail")
        self.assertIn("unmapped", case["dimensions"]["artifact_presence"]["reason"])

    def test_routing_quality_fails_when_trigger_docs_are_missing(self):
        self.assertTrue(RUNNER.exists(), "evaluation runner should exist")
        module = load_runner_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir) / "repo"
            package_root = repo_root / "skills" / "skill-context-keeper"
            shutil.copytree(ROOT / "skills" / "skill-context-keeper", package_root)
            for relative in ["README.md", "README.zh-CN.md", "SKILL.md"]:
                path = package_root / relative
                text = path.read_text(encoding="utf-8")
                for index, cue in enumerate(module.PACKAGE_RULES["skill-context-keeper"]["trigger_cues"]):
                    text = re.sub(
                        re.escape(cue),
                        f"REMOVED_TRIGGER_{index}",
                        text,
                        flags=re.IGNORECASE,
                    )
                path.write_text(text, encoding="utf-8")

            csv_path = Path(tmpdir) / "cases.csv"
            write_cases_csv(
                csv_path,
                [
                    {
                        "case_id": "context_resume",
                        "package": "skill-context-keeper",
                        "scenario_type": "positive",
                        "should_trigger": "yes",
                        "user_prompt": "We’ve been iterating for a while; please resume from the last known state, summarize what changed, and carry forward unresolved TODOs.",
                        "expected_artifacts": "state/context.snapshot|state/continuity.note",
                        "expected_events": "context:reload|context:reconstruct|context:summary",
                        "notes": "trigger docs should be required",
                    }
                ],
            )

            report = module.run_evaluations(repo_root, csv_path)

        case = next(item for item in report["cases"] if item["case_id"] == "context_resume")
        self.assertEqual(report["summary"]["failed"], 1)
        self.assertEqual(case["dimensions"]["routing_quality"]["status"], "fail")
        self.assertIn("routing docs", case["dimensions"]["routing_quality"]["reason"])

    def test_workflow_completeness_rejects_bogus_same_namespace_token(self):
        self.assertTrue(RUNNER.exists(), "evaluation runner should exist")
        module = load_runner_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "cases.csv"
            write_cases_csv(
                csv_path,
                [
                    {
                        "case_id": "bad_workflow",
                        "package": "skill-phase-gate",
                        "scenario_type": "positive",
                        "should_trigger": "yes",
                        "user_prompt": "We need to split this multi-step refactor into phases before coding.",
                        "expected_artifacts": "plan/phase.plan",
                        "expected_events": "phase:anything",
                        "notes": "should fail when same-namespace nonsense tokens are used",
                    }
                ],
            )

            report = module.run_evaluations(ROOT, csv_path)

        case = report["cases"][0]
        self.assertEqual(report["summary"]["failed"], 1)
        self.assertEqual(case["dimensions"]["workflow_completeness"]["status"], "fail")
        self.assertIn("allowed tokens", case["dimensions"]["workflow_completeness"]["reason"])

    def test_guardrails_fail_when_invalid_metadata_values_are_present(self):
        self.assertTrue(RUNNER.exists(), "evaluation runner should exist")
        module = load_runner_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "cases.csv"
            write_cases_csv(
                csv_path,
                [
                    {
                        "case_id": "bad_guardrails",
                        "package": "skill-task-continuity",
                        "scenario_type": "positive",
                        "should_trigger": "yes",
                        "user_prompt": "Set up the long-task continuity suite and coordinate the context keeper, phase gate, and handoff packages.",
                        "expected_artifacts": "AGENTS.md",
                        "expected_events": "bootstrap:agents_md",
                        "notes": "invalid guardrail metadata should fail",
                        "max_commands": "0",
                        "max_verbosity": "extreme",
                    }
                ],
            )

            report = module.run_evaluations(ROOT, csv_path)

        case = report["cases"][0]
        self.assertEqual(report["summary"]["failed"], 1)
        self.assertEqual(case["dimensions"]["guardrails"]["status"], "fail")
        self.assertIn("guardrail", case["dimensions"]["guardrails"]["reason"])


if __name__ == "__main__":
    unittest.main()
