from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SkillPhaseGatePackageTests(unittest.TestCase):
    def test_core_package_files_exist(self):
        for path in [
            ROOT / "README.md",
            ROOT / "README.zh-CN.md",
            ROOT / "SKILL.md",
            ROOT / "agents" / "openai.yaml",
            ROOT / "references" / "use-cases.md",
            ROOT / "references" / "use-cases.zh-CN.md",
            ROOT / "references" / "prompt-templates.en.md",
            ROOT / "references" / "prompt-templates.zh-CN.md",
        ]:
            self.assertTrue(path.exists(), f"expected package file to exist: {path}")

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
        self.assertIn("not for root-state refresh", text)
        self.assertIn("not for packet compression", text)
        self.assertIn("not for suite bootstrap", text)

    def test_readme_describes_optional_checkpoint_boundary(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("optional operational checkpoint", text)
        self.assertIn("risky edits", text)

    def test_readme_includes_direct_natural_language_usage(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("if you want to tell codex exactly what to do", text)
        self.assertIn("use skill-phase-gate to create a preflight gate", text)

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
        self.assertIn("Typical outputs:", text)
        self.assertIn("PREFLIGHT.template.md", text)
        self.assertIn("POSTFLIGHT.template.md", text)
        self.assertIn("Try this first:", text)
        self.assertIn("Use skill-phase-gate", text)
        self.assertIn("skill-context-packet", text)
        self.assertIn("skill-subtask-context", text)

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
        self.assertIn("PREFLIGHT.template.md", text)
        self.assertIn("POSTFLIGHT.template.md", text)
        self.assertIn("先这样对 Codex 说：", text)
        self.assertIn("请用 skill-phase-gate", text)
        self.assertIn("skill-context-packet", text)
        self.assertIn("skill-subtask-context", text)


if __name__ == "__main__":
    unittest.main()
