from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ContextKeeperPackageTests(unittest.TestCase):
    def test_skill_frontmatter_name(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: skill-context-keeper", text)

    def test_core_package_files_exist(self):
        self.assertTrue((ROOT / "README.md").exists())
        self.assertTrue((ROOT / "README.zh-CN.md").exists())
        self.assertTrue((ROOT / "agents" / "openai.yaml").exists())
        self.assertTrue((ROOT / "references" / "prompt-templates.en.md").exists())
        self.assertTrue((ROOT / "references" / "prompt-templates.zh-CN.md").exists())

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

    def test_english_use_cases_include_trigger_sections(self):
        text = (ROOT / "references" / "use-cases.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"(?im)^## +Positive Trigger Prompts$")
        self.assertRegex(text, r"(?im)^## +Negative Trigger Prompts$")

    def test_chinese_use_cases_include_trigger_sections(self):
        text = (ROOT / "references" / "use-cases.zh-CN.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^## +适用触发示例$")
        self.assertRegex(text, r"(?m)^## +不适用触发示例$")

    def test_readme_spells_out_package_boundary(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("does not own workflow gating", text)
        self.assertIn("does not own final handoffs", text)

    def test_readme_includes_direct_natural_language_usage(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("if you want to tell codex exactly what to do", text)
        self.assertIn("use skill-context-keeper to refresh the current task state", text)

    def test_readme_has_fast_entry_sections(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for heading in [
            "## Start Here In 30 Seconds",
            "## Install",
            "## What File Will This Create Or Update?",
            "## Don't Use This When",
            "## Related Skills",
        ]:
            self.assertIn(heading, text)
        self.assertIn("Typical output:", text)
        self.assertIn(".agent-state/TASK_STATE.md", text)
        self.assertIn("Try this first:", text)
        self.assertIn("Use skill-context-keeper", text)

    def test_chinese_readme_has_fast_entry_sections(self):
        text = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        for heading in [
            "## 30 秒快速开始",
            "## 安装",
            "## 会创建或更新什么文件？",
            "## 不适合什么时候用",
            "## 相关技能",
        ]:
            self.assertIn(heading, text)
        self.assertIn("典型产物：", text)
        self.assertIn(".agent-state/TASK_STATE.md", text)
        self.assertIn("先这样对 Codex 说：", text)
        self.assertIn("请用 skill-context-keeper", text)

    def test_reference_indexes_point_to_published_files(self):
        english = (ROOT / "references" / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "references" / "README.zh-CN.md").read_text(encoding="utf-8")

        for text in [english, chinese]:
            self.assertIn("use-cases", text)
            self.assertIn("prompt-templates", text)


if __name__ == "__main__":
    unittest.main()
