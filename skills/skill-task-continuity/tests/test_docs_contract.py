from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SkillTaskContinuityDocsContractTests(unittest.TestCase):
    def test_skills_index_includes_quick_continuity_picker(self):
        english = ROOT.parents[0] / "README.md"
        chinese = ROOT.parents[0] / "README.zh-CN.md"

        english_text = english.read_text(encoding="utf-8")
        chinese_text = chinese.read_text(encoding="utf-8")

        self.assertIn("## Pick the Right Continuity Skill", english_text)
        self.assertIn("skill-context-keeper", english_text)
        self.assertIn("skill-phase-gate", english_text)
        self.assertIn("skill-handoff-summary", english_text)
        self.assertIn("skill-task-continuity", english_text)

        self.assertIn("## 选择合适的连续性技能", chinese_text)
        self.assertIn("skill-context-keeper", chinese_text)
        self.assertIn("skill-phase-gate", chinese_text)
        self.assertIn("skill-handoff-summary", chinese_text)
        self.assertIn("skill-task-continuity", chinese_text)

    def test_english_readme_mentions_full_suite_install(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        lowered = text.lower()

        self.assertIn("install the full suite", lowered)
        self.assertIn("one command", lowered)
        for skill_path in [
            "skills/skill-context-keeper",
            "skills/skill-phase-gate",
            "skills/skill-handoff-summary",
            "skills/skill-task-continuity",
        ]:
            self.assertIn(skill_path, text)

    def test_chinese_readme_mentions_full_suite_install(self):
        text = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")

        self.assertIn("一条命令", text)
        self.assertIn("整套", text)
        for skill_path in [
            "skills/skill-context-keeper",
            "skills/skill-phase-gate",
            "skills/skill-handoff-summary",
            "skills/skill-task-continuity",
        ]:
            self.assertIn(skill_path, text)

    def test_english_install_playbook_prefers_natural_language_bootstrap(self):
        text = (ROOT / "references" / "install-playbook.md").read_text(encoding="utf-8")
        lowered = text.lower()

        self.assertIn("ask codex", lowered)
        self.assertIn("bootstrap", lowered)
        self.assertIn("--dry-run", text)
        self.assertIn("--force", text)

    def test_chinese_install_playbook_prefers_natural_language_bootstrap(self):
        text = (ROOT / "references" / "install-playbook.zh-CN.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("直接这样对 Codex 说", text)
        self.assertIn("启动", text)
        self.assertIn("--dry-run", text)
        self.assertIn("--force", text)

    def test_bilingual_readme_has_beginner_entry_sections(self):
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")

        for heading in [
            "## Start Here In 30 Seconds",
            "## What Gets Created In Your Repo",
            "## Fastest Setup",
            "## Which Skill To Use Next",
            "## Install",
            "## Related Skills",
        ]:
            self.assertIn(heading, english)

        for heading in [
            "## 30 秒快速开始",
            "## 你的仓库里会创建什么",
            "## 最快的开始方式",
            "## 下一步该用哪个技能",
            "## 安装",
            "## 相关技能",
        ]:
            self.assertIn(heading, chinese)

        self.assertIn("Try this first:", english)
        self.assertIn("Use skill-task-continuity", english)
        self.assertIn("先这样对 Codex 说：", chinese)
        self.assertIn("请用 skill-task-continuity", chinese)


if __name__ == "__main__":
    unittest.main()
