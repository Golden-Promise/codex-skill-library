from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SkillHandoffSummaryPackageTests(unittest.TestCase):
    def test_core_package_files_exist(self):
        for path in [
            ROOT / "README.md",
            ROOT / "README.zh-CN.md",
            ROOT / "SKILL.md",
            ROOT / "agents" / "openai.yaml",
            ROOT / "references" / "README.md",
            ROOT / "references" / "README.zh-CN.md",
            ROOT / "references" / "use-cases.md",
            ROOT / "references" / "use-cases.zh-CN.md",
            ROOT / "references" / "prompt-templates.en.md",
            ROOT / "references" / "prompt-templates.zh-CN.md",
            ROOT / "assets" / "HANDOFF.template.md",
        ]:
            self.assertTrue(path.exists(), f"expected package file to exist: {path}")

    def test_handoff_template_has_required_sections(self):
        text = (ROOT / "assets" / "HANDOFF.template.md").read_text(encoding="utf-8")
        for heading in [
            "# Handoff Summary",
            "## Task Summary",
            "## Current Status",
            "## What Changed In This Session",
            "## Hard Constraints To Preserve",
            "## Files / Modules Of Interest",
            "## Open Problems",
            "## Exact Next Action",
            "## Resume Prompt",
        ]:
            self.assertIn(heading, text)

    def test_readme_describes_continuation_boundary(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("continuation-oriented", text)
        self.assertIn("not whole-project documentation", text)
        self.assertIn(".agent-state/handoff.md", text)

    def test_bilingual_references_include_positive_and_negative_examples(self):
        english = (ROOT / "references" / "use-cases.md").read_text(encoding="utf-8")
        chinese = (ROOT / "references" / "use-cases.zh-CN.md").read_text(encoding="utf-8")

        self.assertRegex(english, r"(?im)^## +Positive Trigger Prompts$")
        self.assertRegex(english, r"(?im)^## +Negative Trigger Prompts$")
        self.assertRegex(chinese, r"(?m)^## +适用触发示例$")
        self.assertRegex(chinese, r"(?m)^## +不适用触发示例$")

    def test_resume_prompt_is_explicitly_present_in_template(self):
        text = (ROOT / "assets" / "HANDOFF.template.md").read_text(encoding="utf-8")
        self.assertIn("Resume Prompt", text)
        self.assertIn("Resume this task from .agent-state/HANDOFF.md.", text)

    def test_chinese_references_use_natural_resume_prompt_wording(self):
        for path in [
            ROOT / "references" / "use-cases.zh-CN.md",
            ROOT / "references" / "prompt-templates.zh-CN.md",
        ]:
            text = path.read_text(encoding="utf-8")
            self.assertIn("请从 .agent-state/HANDOFF.md 继续这个任务。", text)


if __name__ == "__main__":
    unittest.main()
