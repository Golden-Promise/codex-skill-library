from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SkillPhaseGatePackageTests(unittest.TestCase):
    def test_checklist_assets_exist(self):
        self.assertTrue((ROOT / "assets" / "PREFLIGHT.template.md").exists())
        self.assertTrue((ROOT / "assets" / "POSTFLIGHT.template.md").exists())

    def test_preflight_template_has_required_sections(self):
        text = (ROOT / "assets" / "PREFLIGHT.template.md").read_text(encoding="utf-8")
        for heading in [
            "## Current Goal",
            "## Current Constraints",
            "## Expected Files / Modules To Change",
            "## Files / Modules Explicitly Not Changing",
            "## Verification Plan",
        ]:
            self.assertIn(heading, text)

    def test_postflight_template_has_required_sections(self):
        text = (ROOT / "assets" / "POSTFLIGHT.template.md").read_text(encoding="utf-8")
        for heading in [
            "## Actual Files / Modules Changed",
            "## Actual Validations Run",
            "## Remaining Risks",
            "## Handoff Recommended?",
        ]:
            self.assertIn(heading, text)

    def test_readme_rules_out_trivial_or_explanation_only_usage(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("not for trivial one-line edits", text)
        self.assertIn("not for pure explanation tasks", text)


if __name__ == "__main__":
    unittest.main()
