import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

RELEASE_FACING_DOCS = [
    "skills/skill-context-keeper/README.md",
    "skills/skill-context-keeper/README.zh-CN.md",
    "skills/skill-phase-gate/README.md",
    "skills/skill-phase-gate/README.zh-CN.md",
    "skills/skill-handoff-summary/README.md",
    "skills/skill-handoff-summary/README.zh-CN.md",
    "skills/skill-task-continuity/README.md",
    "skills/skill-task-continuity/README.zh-CN.md",
    "skills/skill-governance/README.md",
    "skills/skill-governance/README.zh-CN.md",
    "skills/skill-governance/docs/publishing-with-skill-installer.md",
    "skills/skill-governance/docs/publishing-with-skill-installer.zh-CN.md",
    "skills/skill-governance/references/use-cases.md",
    "skills/skill-governance/references/use-cases.zh-CN.md",
]


class ReleaseDocsTests(unittest.TestCase):
    def test_release_facing_docs_do_not_pin_a_stale_fixed_tag(self):
        for relative in RELEASE_FACING_DOCS:
            path = ROOT / relative
            self.assertTrue(path.exists(), f"missing release-facing doc: {relative}")
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=relative):
                self.assertNotIn("v0.6.1", text)


if __name__ == "__main__":
    unittest.main()
