import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "bootstrap_suite.py"
LIBRARY_ROOT = ROOT.parents[1]
REPO_ROOT = ROOT.parents[2]
TEMPLATE_MAP = {
    "AGENTS.md": "assets/AGENTS.repo-template.md",
    ".agent-state/TASK_STATE.md": "assets/agent-state/TASK_STATE.template.md",
    ".agent-state/HANDOFF.md": "assets/agent-state/HANDOFF.template.md",
    ".agent-state/DECISIONS.md": "assets/agent-state/DECISIONS.template.md",
    ".agent-state/RUN_LOG.md": "assets/agent-state/RUN_LOG.template.md",
}


class BootstrapSuiteTests(unittest.TestCase):
    def run_bootstrap(self, target, *extra_args):
        return subprocess.run(
            ["python3", str(SCRIPT), "--target", str(target), *extra_args],
            check=False,
            text=True,
            capture_output=True,
        )

    def test_bootstrap_allows_downstream_repo_with_installed_package_layout(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            downstream_root = Path(tmpdir) / "consumer-repo"
            installed_package = downstream_root / "skills" / "skill-task-continuity"
            shutil.copytree(ROOT, installed_package)

            installed_script = installed_package / "scripts" / "bootstrap_suite.py"
            result = subprocess.run(
                ["python3", str(installed_script), "--target", str(downstream_root)],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((downstream_root / "AGENTS.md").exists())

    def test_bootstrap_rejects_copied_public_library_style_tree_without_git_metadata(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            copied_root = Path(tmpdir) / "codex-skill-library-copy"
            installed_package = copied_root / "skills" / "skill-task-continuity"
            shutil.copytree(ROOT, installed_package)

            for relative_path in [
                "README.md",
                "skills/README.md",
                "skills/README.zh-CN.md",
                "docs/publishing.md",
                "docs/publishing.zh-CN.md",
            ]:
                source = REPO_ROOT / relative_path
                destination = copied_root / relative_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, destination)

            for package_name in [
                "skill-context-keeper",
                "skill-phase-gate",
                "skill-handoff-summary",
            ]:
                package_dir = copied_root / "skills" / package_name
                package_dir.mkdir(parents=True)
                (package_dir / "README.md").write_text(
                    f"# {package_name}\n",
                    encoding="utf-8",
                )

            installed_script = installed_package / "scripts" / "bootstrap_suite.py"
            result = subprocess.run(
                ["python3", str(installed_script), "--target", str(copied_root)],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Refusing to bootstrap inside the public skill library", result.stderr)

    def test_bootstrap_copies_expected_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "demo-repo"
            target.mkdir()

            result = self.run_bootstrap(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            for relative_path in TEMPLATE_MAP:
                self.assertTrue(
                    (target / relative_path).exists(),
                    f"expected downstream file to exist: {relative_path}",
                )

    def test_bootstrap_never_mutates_public_library_root(self):
        for relative_path in TEMPLATE_MAP:
            self.assertFalse(
                (LIBRARY_ROOT / relative_path).exists(),
                f"library root must stay untouched: {relative_path}",
            )

        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "consumer-repo"
            target.mkdir()

            result = self.run_bootstrap(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            for relative_path in TEMPLATE_MAP:
                self.assertFalse(
                    (LIBRARY_ROOT / relative_path).exists(),
                    f"bootstrap must not write into the library root: {relative_path}",
                )

    def test_bootstrap_preserves_existing_files_without_force(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "consumer-repo"
            target.mkdir()

            existing = target / ".agent-state" / "RUN_LOG.md"
            existing.parent.mkdir()
            existing.write_text("keep me\n", encoding="utf-8")

            result = self.run_bootstrap(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(existing.read_text(encoding="utf-8"), "keep me\n")

    def test_bootstrap_force_overwrites_existing_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "consumer-repo"
            target.mkdir()

            existing = target / ".agent-state" / "RUN_LOG.md"
            existing.parent.mkdir()
            existing.write_text("old value\n", encoding="utf-8")

            result = self.run_bootstrap(target, "--force")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotEqual(existing.read_text(encoding="utf-8"), "old value\n")

    def test_task_state_and_handoff_templates_match_atomic_assets(self):
        suite_task_state = ROOT / "assets" / "agent-state" / "TASK_STATE.template.md"
        atomic_task_state = (
            ROOT.parents[0]
            / "skill-context-keeper"
            / "assets"
            / "TASK_STATE.template.md"
        )
        suite_handoff = ROOT / "assets" / "agent-state" / "HANDOFF.template.md"
        atomic_handoff = (
            ROOT.parents[0]
            / "skill-handoff-summary"
            / "assets"
            / "HANDOFF.template.md"
        )

        self.assertTrue(suite_task_state.exists())
        self.assertTrue(suite_handoff.exists())
        self.assertEqual(
            suite_task_state.read_text(encoding="utf-8"),
            atomic_task_state.read_text(encoding="utf-8"),
        )
        self.assertEqual(
            suite_handoff.read_text(encoding="utf-8"),
            atomic_handoff.read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
