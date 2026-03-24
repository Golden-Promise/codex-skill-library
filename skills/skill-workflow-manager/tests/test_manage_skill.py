import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT_DIR / "scripts" / "manage_skill.py"


def load_manage_skill_module():
    spec = spec_from_file_location("manage_skill", SCRIPT_PATH)
    module = module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_skill_dir(path: Path, skill_name: str = "demo-skill") -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / "agents").mkdir(parents=True, exist_ok=True)
    (path / "SKILL.md").write_text(
        "\n".join(
            [
                "---",
                f"name: {skill_name}",
                f'description: "Use this skill when the user wants help with {skill_name} tasks."',
                "---",
                "",
                "# Demo Skill",
                "",
                "## Purpose",
                "",
                "A valid test skill.",
                "",
            ]
        )
        + "\n"
    )
    (path / "agents" / "openai.yaml").write_text(
        "\n".join(
            [
                "interface:",
                '  display_name: "Demo Skill"',
                '  short_description: "Manage demo skill workflows"',
                f'  default_prompt: "Use ${skill_name} to help with demo skill workflows."',
                "",
            ]
        )
    )


class ManageSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_manage_skill_module()

    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(SCRIPT_PATH), *args],
            check=False,
            text=True,
            capture_output=True,
        )

    def run_script_from_path(self, script_path: Path, cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(script_path), *args],
            check=False,
            text=True,
            capture_output=True,
            cwd=str(cwd),
        )

    def test_default_prompt_generation_is_consistent(self):
        prompt = self.module.default_prompt_text(
            "demo-skill",
            "Demo Skill",
        )
        self.assertEqual(
            prompt,
            "Use $demo-skill to help with demo skill workflows.",
        )

        yaml_content = self.module.build_openai_yaml(
            "demo-skill",
            "Demo Skill",
            None,
            None,
        )
        self.assertIn(prompt, yaml_content)
        self.assertEqual(
            self.module.normalize_default_prompt_reference(
                None,
                "demo-skill",
                "Demo Skill",
            ),
            prompt,
        )

    def test_validate_only_defaults_to_runtime_skill_dir(self):
        result = self.run_script("--validate-only")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[INFO] Validation target:", result.stdout)
        self.assertIn("[OK] Validation passed:", result.stdout)

    def test_validate_only_supports_import_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / "imported-skill"
            write_skill_dir(skill_dir, skill_name="imported-skill")

            result = self.run_script("--validate-only", "--import-path", str(skill_dir))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"[INFO] Validation target: {skill_dir}", result.stdout)
        self.assertIn(f"[OK] Validation passed: {skill_dir}", result.stdout)

    def test_validate_only_supports_skill_name_and_library_root(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            skill_dir = library_root / "demo-skill"
            write_skill_dir(skill_dir, skill_name="demo-skill")

            result = self.run_script(
                "demo-skill",
                "--library-root",
                str(library_root),
                "--validate-only",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"[INFO] Validation target: {skill_dir}", result.stdout)
        self.assertIn(f"[OK] Validation passed: {skill_dir}", result.stdout)

    def test_validate_only_rejects_mutating_flags(self):
        result = self.run_script("--validate-only", "--dry-run")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--validate-only is read-only", result.stdout)

    def test_validate_only_supports_json_output(self):
        result = self.run_script("--validate-only", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["mode"], "validate-only")
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["errors"], [])

    def test_doctor_supports_json_output_for_current_package(self):
        result = self.run_script("--doctor", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["mode"], "doctor")
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["target_location"], "canonical shared-library skill")

    def test_doctor_reports_missing_project_link_without_failing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            skill_dir = library_root / "demo-skill"
            project_root = Path(tmpdir) / "demo-project"
            write_skill_dir(skill_dir, skill_name="demo-skill")
            project_root.mkdir(parents=True, exist_ok=True)

            result = self.run_script(
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_root),
                "--doctor",
                "--format",
                "json",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["project_link"]["status"], "missing")
        self.assertIn("--project-skills demo-skill", payload["recommendations"][0])

    def test_doctor_reports_duplicate_canonical_copy_for_adopt(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            import_path = Path(tmpdir) / "incoming-skill"
            write_skill_dir(library_root / "incoming-skill", skill_name="incoming-skill")
            write_skill_dir(import_path, skill_name="incoming-skill")

            result = self.run_script(
                "--library-root",
                str(library_root),
                "--doctor",
                "--adopt",
                str(import_path),
                "--format",
                "json",
            )

        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["duplicate_canonical_copy"])
        self.assertIn("Canonical copy already exists", payload["issues"][0])

    def test_doctor_rejects_mutating_flags(self):
        result = self.run_script("--doctor", "--dry-run")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--doctor is read-only", result.stdout)

    def test_doctor_reports_missing_target_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"

            result = self.run_script(
                "missing-skill",
                "--library-root",
                str(library_root),
                "--doctor",
                "--format",
                "json",
            )

        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["target_location"], "missing target")
        self.assertIn("Target does not exist", payload["issues"][0])

    def test_doctor_reports_broken_project_symlink(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            skill_dir = library_root / "demo-skill"
            project_root = Path(tmpdir) / "demo-project"
            project_skills_dir = project_root / ".agents" / "skills"
            write_skill_dir(skill_dir, skill_name="demo-skill")
            project_skills_dir.mkdir(parents=True, exist_ok=True)
            (project_skills_dir / "demo-skill").symlink_to(project_root / "missing-target")

            result = self.run_script(
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_root),
                "--doctor",
                "--format",
                "json",
            )

        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["project_link"]["status"], "broken symlink")
        self.assertIn("Project link is broken", payload["issues"][0])

    def test_doctor_reports_project_link_blocked_by_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            skill_dir = library_root / "demo-skill"
            project_root = Path(tmpdir) / "demo-project"
            project_link = project_root / ".agents" / "skills" / "demo-skill"
            write_skill_dir(skill_dir, skill_name="demo-skill")
            project_link.mkdir(parents=True, exist_ok=True)

            result = self.run_script(
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_root),
                "--doctor",
                "--format",
                "json",
            )

        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["project_link"]["status"], "local directory (not a symlink)")
        self.assertIn("blocked by an existing entry", payload["issues"][0])

    def test_list_library_skills_supports_json_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            write_skill_dir(library_root / "demo-skill", skill_name="demo-skill")

            result = self.run_script(
                "--library-root",
                str(library_root),
                "--list-library-skills",
                "--format",
                "json",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["mode"], "list-library-skills")
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["skills"][0]["name"], "demo-skill")

    def test_list_project_skills_supports_json_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            skill_dir = library_root / "demo-skill"
            project_root = Path(tmpdir) / "demo-project"
            project_skills_dir = project_root / ".agents" / "skills"
            write_skill_dir(skill_dir, skill_name="demo-skill")
            project_skills_dir.mkdir(parents=True, exist_ok=True)
            (project_skills_dir / "demo-skill").symlink_to(skill_dir)

            result = self.run_script(
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_root),
                "--list-project-skills",
                "--format",
                "json",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["mode"], "list-project-skills")
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["entries"][0]["name"], "demo-skill")
        self.assertEqual(payload["entries"][0]["status"], "managed library link")

    def test_inspect_import_supports_json_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            import_path = Path(tmpdir) / "incoming-skill"
            write_skill_dir(import_path, skill_name="incoming-skill")

            result = self.run_script(
                "--library-root",
                str(library_root),
                "--inspect-import",
                "--import-path",
                str(import_path),
                "--format",
                "json",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["mode"], "inspect-import")
        self.assertEqual(payload["import_status"], "ready to import")
        self.assertEqual(payload["detected_source_skill_name"], "incoming-skill")
        self.assertTrue(payload["validation"]["ok"])

    def test_adopt_alias_supports_inspect_import(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            adopt_path = Path(tmpdir) / "incoming-skill"
            write_skill_dir(adopt_path, skill_name="incoming-skill")

            result = self.run_script(
                "--library-root",
                str(library_root),
                "--inspect-import",
                "--adopt",
                str(adopt_path),
                "--format",
                "json",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["mode"], "inspect-import")
        self.assertEqual(payload["source_path"], str(adopt_path))

    def test_adopt_and_import_path_cannot_be_combined(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            adopt_path = Path(tmpdir) / "incoming-skill"
            write_skill_dir(adopt_path, skill_name="incoming-skill")

            result = self.run_script(
                "--inspect-import",
                "--import-path",
                str(adopt_path),
                "--adopt",
                str(adopt_path),
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Use only one of --import-path or --adopt", result.stdout)

    def test_json_format_is_rejected_for_mutation_mode(self):
        result = self.run_script("demo-skill", "--format", "json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--format json is supported only", result.stdout)

    def test_infer_project_root_from_cwd_ignores_skill_dir_context(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            runtime_skill_dir = Path(tmpdir) / "runtime-skill"
            import_path = Path(tmpdir) / "incoming-skill"
            write_skill_dir(runtime_skill_dir, skill_name="runtime-skill")
            write_skill_dir(import_path, skill_name="incoming-skill")

            previous_cwd = Path.cwd()
            try:
                os_module = self.module.os
                os_module.chdir(runtime_skill_dir)
                inferred = self.module.infer_project_root_from_cwd(
                    import_path,
                    runtime_skill_dir,
                )
            finally:
                os_module.chdir(previous_cwd)

        self.assertIsNone(inferred)

    def test_bootstrap_project_layout_removes_in_project_runtime_source(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "demo-project"
            source_dir = project_root / "skill-workflow-manager"
            scripts_dir = source_dir / "scripts"
            write_skill_dir(source_dir, skill_name="skill-workflow-manager")
            scripts_dir.mkdir(parents=True, exist_ok=True)
            script_copy = scripts_dir / "manage_skill.py"
            shutil.copy2(SCRIPT_PATH, script_copy)
            project_root.mkdir(parents=True, exist_ok=True)

            result = self.run_script_from_path(
                script_copy,
                project_root,
                "--bootstrap-project-layout",
            )

            canonical_dir = project_root / "_skill-library" / "skill-workflow-manager"
            project_link = project_root / ".agents" / "skills" / "skill-workflow-manager"

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Bootstrap source cleanup (removed)", result.stdout)
            self.assertTrue(canonical_dir.exists())
            self.assertFalse(source_dir.exists())
            self.assertTrue(project_link.is_symlink())
            self.assertEqual(project_link.resolve(), canonical_dir.resolve())

    def test_bootstrap_project_layout_removes_duplicate_source_when_canonical_exists(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "demo-project"
            source_dir = project_root / "skill-workflow-manager"
            canonical_dir = project_root / "_skill-library" / "skill-workflow-manager"
            scripts_dir = source_dir / "scripts"
            write_skill_dir(source_dir, skill_name="skill-workflow-manager")
            write_skill_dir(canonical_dir, skill_name="skill-workflow-manager")
            scripts_dir.mkdir(parents=True, exist_ok=True)
            script_copy = scripts_dir / "manage_skill.py"
            shutil.copy2(SCRIPT_PATH, script_copy)
            project_root.mkdir(parents=True, exist_ok=True)

            result = self.run_script_from_path(
                script_copy,
                project_root,
                "--bootstrap-project-layout",
            )

            project_link = project_root / ".agents" / "skills" / "skill-workflow-manager"

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Keeping", result.stdout)
            self.assertIn("Bootstrap source cleanup (removed)", result.stdout)
            self.assertTrue(canonical_dir.exists())
            self.assertFalse(source_dir.exists())
            self.assertTrue(project_link.is_symlink())
            self.assertEqual(project_link.resolve(), canonical_dir.resolve())


if __name__ == "__main__":
    unittest.main()
