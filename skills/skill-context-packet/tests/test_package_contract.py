from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SkillContextPacketPackageTests(unittest.TestCase):
    def test_skill_frontmatter_name(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: skill-context-packet", text)

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
            ROOT / "assets" / "PACKET.template.md",
        ]:
            self.assertTrue(path.exists(), f"expected package file to exist: {path}")

    def test_packet_template_has_required_sections(self):
        text = (ROOT / "assets" / "PACKET.template.md").read_text(encoding="utf-8")
        for heading in [
            "# Context Packet",
            "## Objective For This Turn",
            "## Scope For This Turn",
            "## Inputs To Load",
            "## Facts To Preserve",
            "## Constraints To Preserve",
            "## Risks / Open Questions",
            "## Exit Criteria",
            "## Next Command / Prompt",
        ]:
            self.assertIn(heading, text)

    def test_bilingual_use_cases_include_trigger_sections(self):
        english = (ROOT / "references" / "use-cases.md").read_text(encoding="utf-8")
        chinese = (ROOT / "references" / "use-cases.zh-CN.md").read_text(encoding="utf-8")

        self.assertRegex(english, r"(?im)^## +Positive Trigger Prompts$")
        self.assertRegex(english, r"(?im)^## +Negative Trigger Prompts$")
        self.assertRegex(chinese, r"(?m)^## +适用触发示例$")
        self.assertRegex(chinese, r"(?m)^## +不适用触发示例$")

    def test_readme_describes_packet_boundary(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("minimum context object", text)
        self.assertIn("does not own root task state", text)
        self.assertIn("does not own workflow gates", text)

    def test_readme_includes_direct_natural_language_usage(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("if you want to tell codex exactly what to do", text)
        self.assertIn(
            "use skill-context-packet to compress the next turn",
            text,
        )

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
        self.assertIn(".agent-state/root/PACKET.md", text)
        self.assertIn("Try this first:", text)
        self.assertIn("Use skill-context-packet", text)

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
        self.assertIn(".agent-state/root/PACKET.md", text)
        self.assertIn("先这样对 Codex 说：", text)
        self.assertIn("请用 skill-context-packet", text)

    def test_reference_indexes_point_to_published_files(self):
        english = (ROOT / "references" / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "references" / "README.zh-CN.md").read_text(encoding="utf-8")

        for text in [english, chinese]:
            self.assertIn("use-cases", text)
            self.assertIn("prompt-templates", text)


if __name__ == "__main__":
    unittest.main()
