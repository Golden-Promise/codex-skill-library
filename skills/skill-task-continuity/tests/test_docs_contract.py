from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SkillTaskContinuityDocsContractTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
