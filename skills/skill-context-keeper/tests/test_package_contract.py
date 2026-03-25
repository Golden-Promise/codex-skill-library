from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ContextKeeperPackageTests(unittest.TestCase):
    def test_skill_frontmatter_name(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: skill-context-keeper", text)

    def test_readmes_exist(self):
        self.assertTrue((ROOT / "README.md").exists())
        self.assertTrue((ROOT / "README.zh-CN.md").exists())

    def test_task_state_template_has_required_sections(self):
        text = (ROOT / "assets" / "TASK_STATE.template.md").read_text(encoding="utf-8")
        for heading in [
            "## Current Objective",
            "## Scope / Non-Goals",
            "## Hard Constraints",
            "## Current Codebase Facts",
            "## Completed Work",
            "## Open Issues / Risks",
            "## Next Recommended Action",
            "## Verification Still Needed",
            "## Recent Decisions",
            "## Resume Checklist",
        ]:
            self.assertIn(heading, text)

    def test_reference_guides_include_trigger_sections(self):
        for relative_path in [
            ROOT / "references" / "use-cases.md",
            ROOT / "references" / "use-cases.zh-CN.md",
        ]:
            text = relative_path.read_text(encoding="utf-8")
            self.assertRegex(text, r"(?im)^## .*positive trigger")
            self.assertRegex(text, r"(?im)^## .*negative trigger")

    def test_readme_spells_out_package_boundary(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("does not own workflow gating", text)
        self.assertIn("does not own final handoffs", text)


if __name__ == "__main__":
    unittest.main()
