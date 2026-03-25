import csv
import importlib.util
import tempfile
import sys
import unittest
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
            csv_path.write_text(
                "\n".join(
                    [
                        "case_id,package,scenario_type,should_trigger,user_prompt,expected_artifacts,expected_events,notes,max_commands,max_verbosity",
                        "demo,skill-context-keeper,positive,yes,Refresh state,assets/TASK_STATE.template.md,context:reload,optional guardrails,3,low",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            cases = module.load_cases(csv_path)
            self.assertEqual(cases[0].max_commands, 3)
            self.assertEqual(cases[0].max_verbosity, "low")


if __name__ == "__main__":
    unittest.main()
