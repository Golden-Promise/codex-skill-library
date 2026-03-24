import json
import os
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


def update_skill_description(path: Path, description: str) -> None:
    skill_md = path / "SKILL.md"
    lines = skill_md.read_text().splitlines()
    rewritten = []
    for line in lines:
        if line.startswith("description: "):
            rewritten.append(f'description: "{description}"')
        else:
            rewritten.append(line)
    skill_md.write_text("\n".join(rewritten) + "\n")


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

    def run_script_with_env(
        self,
        env: dict[str, str],
        *args: str,
    ) -> subprocess.CompletedProcess[str]:
        merged_env = dict(os.environ)
        merged_env.update(env)
        return subprocess.run(
            ["python3", str(SCRIPT_PATH), *args],
            check=False,
            text=True,
            capture_output=True,
            env=merged_env,
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
        self.assertIn("governance", payload)
        self.assertIn("health_score", payload["governance"])
        self.assertIn("dimensions", payload["governance"])

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
        self.assertIn("Enable demo-skill", payload["recommendations"][0])
        repair_steps = payload["repair_plan"]["steps"]
        self.assertTrue(
            any(step["type"] == "enable-missing-project-exposure" for step in repair_steps)
        )
        self.assertGreaterEqual(payload["work_queue"]["counts"]["safe_auto_fix"], 1)
        preview = payload["batch_repair_preview"]
        self.assertGreaterEqual(preview["eligible_steps"], 1)
        self.assertTrue(
            any(" enable demo-skill " in f" {item['command']} " for item in preview["commands"])
        )

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
        repair_steps = payload["repair_plan"]["steps"]
        self.assertTrue(
            any(
                step["type"] == "repair-broken-project-exposure"
                and " enable demo-skill " in f" {step['command']} "
                for step in repair_steps
            )
        )

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
        self.assertEqual(payload["project_link"]["status"], "local directory (not a managed exposure)")
        self.assertIn("blocked by an existing entry", payload["issues"][0])
        repair_steps = payload["repair_plan"]["steps"]
        self.assertTrue(
            any(
                step["type"] == "clear-project-exposure-blocker"
                and step["automatic"] is False
                and "next_command" in step
                for step in repair_steps
            )
        )
        self.assertGreaterEqual(payload["work_queue"]["counts"]["manual_cleanup_first"], 1)

    def test_doctor_detects_similar_skill_candidates(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            skill_a = library_root / "excel-helper"
            skill_b = library_root / "spreadsheet-assistant"
            write_skill_dir(skill_a, skill_name="excel-helper")
            write_skill_dir(skill_b, skill_name="spreadsheet-assistant")
            update_skill_description(
                skill_a,
                "Use this skill when the user wants help with spreadsheet cleanup and workbook review.",
            )
            update_skill_description(
                skill_b,
                "Use this skill when the user wants help with spreadsheet cleanup and workbook review.",
            )

            result = self.run_script(
                "excel-helper",
                "--library-root",
                str(library_root),
                "--doctor",
                "--format",
                "json",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        candidates = payload["governance"]["duplicate_candidates"]
        self.assertTrue(any(candidate["name"] == "spreadsheet-assistant" for candidate in candidates))
        self.assertTrue(
            any("spreadsheet-assistant" in recommendation for recommendation in payload["recommendations"])
        )
        self.assertTrue(
            any(action["type"] == "review-overlap" for action in payload["actions"])
        )
        self.assertTrue(
            any(item["type"] == "review-overlap" for item in payload["work_queue"]["governance_review"])
        )

    def test_doctor_detects_semantic_overlap_candidates_from_alias_terms(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            skill_a = library_root / "excel-helper"
            skill_b = library_root / "spreadsheet-assistant"
            write_skill_dir(skill_a, skill_name="excel-helper")
            write_skill_dir(skill_b, skill_name="spreadsheet-assistant")
            update_skill_description(
                skill_a,
                "Use this skill when the user wants help with Excel workbook automation.",
            )
            update_skill_description(
                skill_b,
                "Use this skill when the user wants help with spreadsheet assistant workflows.",
            )

            result = self.run_script(
                "excel-helper",
                "--library-root",
                str(library_root),
                "--doctor",
                "--format",
                "json",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        candidates = payload["governance"]["duplicate_candidates"]
        self.assertTrue(candidates)
        self.assertEqual(candidates[0]["name"], "spreadsheet-assistant")
        self.assertGreaterEqual(candidates[0]["signals"]["cosine"], 0.3)

    def test_doctor_recommends_documenting_unmentioned_resources(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            skill_dir = library_root / "demo-skill"
            write_skill_dir(skill_dir, skill_name="demo-skill")
            (skill_dir / "scripts").mkdir(parents=True, exist_ok=True)

            result = self.run_script(
                "demo-skill",
                "--library-root",
                str(library_root),
                "--doctor",
                "--format",
                "json",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("scripts", payload["governance"]["signals"]["unmentioned_resource_directories"])
        self.assertTrue(
            any("Document these resource directories" in recommendation for recommendation in payload["recommendations"])
        )

    def test_doctor_reports_workspace_impact_across_projects(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)
            library_root = workspace_root / "_skill-library"
            canonical_dir = library_root / "demo-skill"
            project_a = workspace_root / "project-a"
            project_b = workspace_root / "project-b"
            write_skill_dir(canonical_dir, skill_name="demo-skill")
            project_a.mkdir(parents=True, exist_ok=True)
            project_b.mkdir(parents=True, exist_ok=True)

            enable_a = self.run_script(
                "enable",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_a),
            )
            enable_b = self.run_script(
                "enable",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_b),
                "--exposure-mode",
                "copy",
            )
            self.assertEqual(enable_a.returncode, 0, enable_a.stderr)
            self.assertEqual(enable_b.returncode, 0, enable_b.stderr)

            result = self.run_script(
                "demo-skill",
                "--library-root",
                str(library_root),
                "--workspace-root",
                str(workspace_root),
                "--doctor",
                "--format",
                "json",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        impact = payload["impact_analysis"]
        self.assertEqual(impact["counts"]["projects_total"], 2)
        self.assertEqual(impact["counts"]["managed_copy"], 1)
        self.assertEqual(impact["counts"]["managed_symlink"], 1)
        self.assertEqual(impact["reference_graph"]["active_projects_total"], 2)
        self.assertEqual(impact["reference_graph"]["other_active_projects_total"], 2)
        self.assertEqual(impact["reference_graph"]["current_project_status"], "missing")
        self.assertTrue(
            any("copy exposure" in recommendation for recommendation in impact["recommendations"])
        )
        self.assertTrue(
            any(action["type"] == "refresh-copy-exposures" for action in payload["actions"])
        )
        self.assertTrue(
            any(
                item["type"] == "refresh-copy-project-exposure"
                for item in payload["work_queue"]["safe_auto_fix"]
            )
        )
        preview = payload["batch_repair_preview"]
        self.assertGreaterEqual(preview["eligible_steps"], 1)
        self.assertTrue(
            any(item["type"] == "refresh-copy-project-exposure" for item in preview["commands"])
        )

    def test_doctor_reports_broken_workspace_exposure_in_impact_analysis(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)
            library_root = workspace_root / "_skill-library"
            canonical_dir = library_root / "demo-skill"
            project_root = workspace_root / "project-a"
            project_skills_dir = project_root / ".agents" / "skills"
            write_skill_dir(canonical_dir, skill_name="demo-skill")
            project_skills_dir.mkdir(parents=True, exist_ok=True)
            (project_root / ".git").mkdir(parents=True, exist_ok=True)
            (project_skills_dir / "demo-skill").symlink_to(project_root / "missing-target")

            result = self.run_script(
                "demo-skill",
                "--library-root",
                str(library_root),
                "--workspace-root",
                str(workspace_root),
                "--doctor",
                "--format",
                "json",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        impact = payload["impact_analysis"]
        self.assertEqual(impact["counts"]["broken"], 1)
        self.assertEqual(impact["projects"][0]["status"], "broken symlink")
        self.assertTrue(
            any("should be repaired" in recommendation for recommendation in impact["recommendations"])
        )
        repair_steps = payload["repair_plan"]["steps"]
        self.assertTrue(
            any(
                step["type"] == "repair-broken-project-exposure"
                and step["project_root"] == str(project_root)
                for step in repair_steps
            )
        )

    def test_doctor_marks_low_value_unused_skill_as_retire_candidate(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)
            library_root = workspace_root / "_skill-library"
            skill_a = library_root / "excel-helper"
            skill_b = library_root / "spreadsheet-assistant"
            write_skill_dir(skill_a, skill_name="excel-helper")
            write_skill_dir(skill_b, skill_name="spreadsheet-assistant")
            update_skill_description(
                skill_a,
                "Use this skill when the user wants help with spreadsheet cleanup and workbook review.",
            )
            update_skill_description(
                skill_b,
                "Use this skill when the user wants help with spreadsheet cleanup and workbook review.",
            )
            (skill_a / "scripts").mkdir(parents=True, exist_ok=True)
            openai_path = skill_a / "agents" / "openai.yaml"
            openai_text = openai_path.read_text()
            openai_path.write_text(
                openai_text.replace(
                    "Use $excel-helper to help with demo skill workflows.",
                    "Use this workflow to help with demo skill workflows.",
                )
            )

            result = self.run_script(
                "excel-helper",
                "--library-root",
                str(library_root),
                "--workspace-root",
                str(workspace_root),
                "--doctor",
                "--format",
                "json",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(
            any(action["type"] == "consider-retire-candidate" for action in payload["actions"])
        )
        self.assertTrue(
            any(
                item["type"] == "consider-retire-candidate"
                for item in payload["work_queue"]["governance_review"]
            )
        )
        preview = payload["batch_repair_preview"]
        self.assertEqual(preview["eligible_steps"], 0)
        self.assertEqual(preview["commands"], [])

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
        self.assertEqual(payload["entries"][0]["status"], "managed symlink")

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
            source_dir = project_root / "skill-governance"
            scripts_dir = source_dir / "scripts"
            write_skill_dir(source_dir, skill_name="skill-governance")
            scripts_dir.mkdir(parents=True, exist_ok=True)
            script_copy = scripts_dir / "manage_skill.py"
            shutil.copy2(SCRIPT_PATH, script_copy)
            project_root.mkdir(parents=True, exist_ok=True)

            result = self.run_script_from_path(
                script_copy,
                project_root,
                "--bootstrap-project-layout",
            )

            canonical_dir = project_root / "_skill-library" / "skill-governance"
            project_link = project_root / ".agents" / "skills" / "skill-governance"

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Bootstrap source cleanup (removed)", result.stdout)
            self.assertTrue(canonical_dir.exists())
            self.assertFalse(source_dir.exists())
            self.assertTrue(project_link.is_symlink())
            self.assertEqual(project_link.resolve(), canonical_dir.resolve())

    def test_bootstrap_project_layout_removes_duplicate_source_when_canonical_exists(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "demo-project"
            source_dir = project_root / "skill-governance"
            canonical_dir = project_root / "_skill-library" / "skill-governance"
            scripts_dir = source_dir / "scripts"
            write_skill_dir(source_dir, skill_name="skill-governance")
            write_skill_dir(canonical_dir, skill_name="skill-governance")
            scripts_dir.mkdir(parents=True, exist_ok=True)
            script_copy = scripts_dir / "manage_skill.py"
            shutil.copy2(SCRIPT_PATH, script_copy)
            project_root.mkdir(parents=True, exist_ok=True)

            result = self.run_script_from_path(
                script_copy,
                project_root,
                "--bootstrap-project-layout",
            )

            project_link = project_root / ".agents" / "skills" / "skill-governance"

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Keeping", result.stdout)
            self.assertIn("Bootstrap source cleanup (removed)", result.stdout)
            self.assertTrue(canonical_dir.exists())
            self.assertFalse(source_dir.exists())
            self.assertTrue(project_link.is_symlink())
            self.assertEqual(project_link.resolve(), canonical_dir.resolve())

    def test_add_task_creates_project_owned_skill(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "demo-project"
            project_root.mkdir(parents=True, exist_ok=True)

            result = self.run_script(
                "add",
                "demo-skill",
                "--project-root",
                str(project_root),
                "--purpose",
                "Use this skill when the user wants help with demo-skill tasks.",
            )

            canonical_dir = project_root / "_skill-library" / "demo-skill"
            project_exposure = project_root / ".agents" / "skills" / "demo-skill"

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(canonical_dir.exists())
            self.assertTrue(project_exposure.is_symlink())
            self.assertEqual(project_exposure.resolve(), canonical_dir.resolve())

    def test_enable_task_supports_copy_exposure_mode(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            project_root = Path(tmpdir) / "demo-project"
            canonical_dir = library_root / "demo-skill"
            write_skill_dir(canonical_dir, skill_name="demo-skill")
            project_root.mkdir(parents=True, exist_ok=True)

            result = self.run_script(
                "enable",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_root),
                "--exposure-mode",
                "copy",
            )

            project_exposure = project_root / ".agents" / "skills" / "demo-skill"

            list_result = self.run_script(
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_root),
                "--list-project-skills",
                "--format",
                "json",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(project_exposure.exists())
            self.assertFalse(project_exposure.is_symlink())
            payload = json.loads(list_result.stdout)
            self.assertEqual(payload["entries"][0]["status"], "managed copy")
            self.assertEqual(payload["entries"][0]["managed_mode"], "copy")

    def test_add_task_uses_repo_configured_paths(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir) / "demo-project"
            project_root.mkdir(parents=True, exist_ok=True)
            (project_root / "skill-governance.toml").write_text(
                "\n".join(
                    [
                        "[skill_registry]",
                        'project_root = ".platform/skills/project"',
                        'exposure_root = ".platform/skills/enabled"',
                        'exposure_mode = "copy"',
                        "",
                    ]
                )
            )

            result = self.run_script(
                "add",
                "demo-skill",
                "--project-root",
                str(project_root),
                "--purpose",
                "Use this skill when the user wants help with demo-skill tasks.",
            )

            canonical_dir = project_root / ".platform" / "skills" / "project" / "demo-skill"
            project_exposure = project_root / ".platform" / "skills" / "enabled" / "demo-skill"

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(canonical_dir.exists())
            self.assertTrue(project_exposure.exists())
            self.assertFalse(project_exposure.is_symlink())

    def test_repair_task_enables_missing_project_exposure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            project_root = Path(tmpdir) / "demo-project"
            canonical_dir = library_root / "demo-skill"
            write_skill_dir(canonical_dir, skill_name="demo-skill")
            project_root.mkdir(parents=True, exist_ok=True)

            result = self.run_script(
                "repair",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_root),
            )

            project_exposure = project_root / ".agents" / "skills" / "demo-skill"

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(project_exposure.exists() or project_exposure.is_symlink())
            self.assertIn("Safe auto-fix queue", result.stdout)
            self.assertIn("Task complete: repair", result.stdout)

    def test_repair_task_repairs_broken_workspace_exposure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)
            library_root = workspace_root / "_skill-library"
            canonical_dir = library_root / "demo-skill"
            project_root = workspace_root / "project-a"
            project_skills_dir = project_root / ".agents" / "skills"
            write_skill_dir(canonical_dir, skill_name="demo-skill")
            project_skills_dir.mkdir(parents=True, exist_ok=True)
            (project_root / ".git").mkdir(parents=True, exist_ok=True)
            broken_link = project_skills_dir / "demo-skill"
            broken_link.symlink_to(project_root / "missing-target")

            result = self.run_script(
                "repair",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--workspace-root",
                str(workspace_root),
            )

            resolved_target = Path(os.path.realpath(broken_link))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(broken_link.is_symlink())
            self.assertEqual(resolved_target, canonical_dir.resolve())
            self.assertIn("repair-broken-project-exposure", result.stdout)

    def test_repair_task_repairs_broken_current_project_exposure_without_workspace(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            canonical_dir = library_root / "demo-skill"
            project_root = Path(tmpdir) / "demo-project"
            project_skills_dir = project_root / ".agents" / "skills"
            write_skill_dir(canonical_dir, skill_name="demo-skill")
            project_skills_dir.mkdir(parents=True, exist_ok=True)
            broken_link = project_skills_dir / "demo-skill"
            broken_link.symlink_to(project_root / "missing-target")

            result = self.run_script(
                "repair",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_root),
            )

            resolved_target = Path(os.path.realpath(broken_link))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(broken_link.is_symlink())
            self.assertEqual(resolved_target, canonical_dir.resolve())

    def test_repair_task_dry_run_does_not_modify_exposure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            project_root = Path(tmpdir) / "demo-project"
            canonical_dir = library_root / "demo-skill"
            write_skill_dir(canonical_dir, skill_name="demo-skill")
            project_root.mkdir(parents=True, exist_ok=True)

            result = self.run_script(
                "repair",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_root),
                "--dry-run",
            )

            project_exposure = project_root / ".agents" / "skills" / "demo-skill"

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(project_exposure.exists() or project_exposure.is_symlink())
            self.assertIn("would", result.stdout.lower())

    def test_repair_rejects_unrelated_mutation_flags(self):
        result = self.run_script(
            "repair",
            "demo-skill",
            "--project-root",
            "/tmp/demo-project",
            "--purpose",
            "Use this skill when the user wants help.",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("repair only works with managed skill scope flags", result.stdout)

    def test_upgrade_task_refreshes_existing_canonical_skill_from_import_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            canonical_dir = library_root / "demo-skill"
            incoming_dir = Path(tmpdir) / "incoming-skill"
            write_skill_dir(canonical_dir, skill_name="demo-skill")
            write_skill_dir(incoming_dir, skill_name="demo-skill")
            update_skill_description(
                incoming_dir,
                "Use this skill when the user wants upgraded demo-skill behavior.",
            )

            result = self.run_script(
                "upgrade",
                str(incoming_dir),
                "--library-root",
                str(library_root),
            )

            canonical_content = (canonical_dir / "SKILL.md").read_text()

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Task complete: upgrade", result.stdout)
            self.assertIn("upgraded demo-skill behavior", canonical_content)

    def test_upgrade_task_reports_workspace_impact_summary(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)
            library_root = workspace_root / "_skill-library"
            canonical_dir = library_root / "demo-skill"
            incoming_dir = workspace_root / "incoming-skill"
            project_a = workspace_root / "project-a"
            project_b = workspace_root / "project-b"
            write_skill_dir(canonical_dir, skill_name="demo-skill")
            write_skill_dir(incoming_dir, skill_name="demo-skill")
            project_a.mkdir(parents=True, exist_ok=True)
            project_b.mkdir(parents=True, exist_ok=True)

            enable_a = self.run_script(
                "enable",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_a),
            )
            enable_b = self.run_script(
                "enable",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_b),
                "--exposure-mode",
                "copy",
            )
            self.assertEqual(enable_a.returncode, 0, enable_a.stderr)
            self.assertEqual(enable_b.returncode, 0, enable_b.stderr)

            result = self.run_script(
                "upgrade",
                str(incoming_dir),
                "--library-root",
                str(library_root),
                "--workspace-root",
                str(workspace_root),
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[IMPACT] Active projects using demo-skill: 2", result.stdout)
        self.assertIn("copy-based project exposure", result.stdout)

    def test_enable_task_accepts_project_alias_flag(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            project_root = Path(tmpdir) / "demo-project"
            canonical_dir = library_root / "demo-skill"
            write_skill_dir(canonical_dir, skill_name="demo-skill")
            project_root.mkdir(parents=True, exist_ok=True)

            result = self.run_script(
                "enable",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project",
                str(project_root),
            )

            project_exposure = project_root / ".agents" / "skills" / "demo-skill"

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(project_exposure.exists())

    def test_retire_task_reports_remaining_workspace_dependents(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)
            library_root = workspace_root / "_skill-library"
            project_a = workspace_root / "project-a"
            project_b = workspace_root / "project-b"
            canonical_dir = library_root / "demo-skill"
            write_skill_dir(canonical_dir, skill_name="demo-skill")
            project_a.mkdir(parents=True, exist_ok=True)
            project_b.mkdir(parents=True, exist_ok=True)

            enable_a = self.run_script(
                "enable",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_a),
            )
            enable_b = self.run_script(
                "enable",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_b),
            )
            self.assertEqual(enable_a.returncode, 0, enable_a.stderr)
            self.assertEqual(enable_b.returncode, 0, enable_b.stderr)

            retire_result = self.run_script(
                "retire",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_a),
                "--workspace-root",
                str(workspace_root),
            )

            project_a_exposure = project_a / ".agents" / "skills" / "demo-skill"
            project_b_exposure = project_b / ".agents" / "skills" / "demo-skill"

            self.assertEqual(retire_result.returncode, 0, retire_result.stderr)
            self.assertFalse(project_a_exposure.exists() or project_a_exposure.is_symlink())
            self.assertTrue(project_b_exposure.exists() or project_b_exposure.is_symlink())
            self.assertIn("[IMPACT] Remaining active projects for demo-skill: 1", retire_result.stdout)
            self.assertIn("canonical skill remains", retire_result.stdout.lower())

    def test_enable_task_infers_project_root_from_current_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            project_root = Path(tmpdir) / "demo-project"
            canonical_dir = library_root / "demo-skill"
            write_skill_dir(canonical_dir, skill_name="demo-skill")
            project_root.mkdir(parents=True, exist_ok=True)
            (project_root / ".git").mkdir(parents=True, exist_ok=True)

            result = self.run_script_from_path(
                SCRIPT_PATH,
                project_root,
                "enable",
                "demo-skill",
                "--library-root",
                str(library_root),
            )

            project_exposure = project_root / ".agents" / "skills" / "demo-skill"

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Project root was inferred from the current working directory", result.stdout)
            self.assertTrue(project_exposure.exists())

    def test_enable_task_uses_manifest_mode_in_ci_auto_mode(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            project_root = Path(tmpdir) / "demo-project"
            canonical_dir = library_root / "demo-skill"
            write_skill_dir(canonical_dir, skill_name="demo-skill")
            project_root.mkdir(parents=True, exist_ok=True)

            result = self.run_script_with_env(
                {"CI": "1"},
                "enable",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_root),
            )

            project_exposure = project_root / ".agents" / "skills" / "demo-skill"
            manifest_path = (
                project_root
                / ".agents"
                / "skill-governance"
                / "skills-manifest.json"
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(project_exposure.exists() or project_exposure.is_symlink())
            self.assertTrue(manifest_path.exists())

            doctor_result = self.run_script(
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_root),
                "--doctor",
                "--format",
                "json",
            )
            self.assertEqual(doctor_result.returncode, 0, doctor_result.stderr)
            doctor_payload = json.loads(doctor_result.stdout)
            self.assertEqual(doctor_payload["project_link"]["status"], "managed manifest")

            list_result = self.run_script(
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_root),
                "--list-project-skills",
                "--format",
                "json",
            )
            self.assertEqual(list_result.returncode, 0, list_result.stderr)
            list_payload = json.loads(list_result.stdout)
            self.assertEqual(list_payload["entries"][0]["status"], "managed manifest")

    def test_audit_sync_writes_registry_and_dependency_graph(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)
            library_root = workspace_root / "_skill-library"
            platform_root = workspace_root / ".skill-platform"
            project_root = workspace_root / "demo-project"
            canonical_dir = library_root / "demo-skill"
            write_skill_dir(canonical_dir, skill_name="demo-skill")
            project_root.mkdir(parents=True, exist_ok=True)

            enable_result = self.run_script(
                "enable",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_root),
                "--platform-root",
                str(platform_root),
            )
            self.assertEqual(enable_result.returncode, 0, enable_result.stderr)

            audit_result = self.run_script(
                "audit",
                "--library-root",
                str(library_root),
                "--workspace-root",
                str(workspace_root),
                "--platform-root",
                str(platform_root),
                "--sync-platform-state",
                "--format",
                "json",
            )

            registry_path = platform_root / "registry.json"
            dependency_graph_path = platform_root / "dependency-graph.json"

            self.assertEqual(audit_result.returncode, 0, audit_result.stderr)
            self.assertTrue(registry_path.exists())
            self.assertTrue(dependency_graph_path.exists())
            payload = json.loads(audit_result.stdout)
            self.assertEqual(payload["mode"], "audit")
            self.assertTrue(payload["drift"]["registry_matches"])
            self.assertTrue(payload["drift"]["dependency_graph_matches"])
            self.assertIn("demo-skill", payload["registry"]["skills"])
            self.assertEqual(
                payload["dependency_graph"]["skills"]["demo-skill"]["active_projects_total"],
                1,
            )

    def test_audit_detects_stale_dependency_graph(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)
            library_root = workspace_root / "_skill-library"
            platform_root = workspace_root / ".skill-platform"
            project_root = workspace_root / "demo-project"
            canonical_dir = library_root / "demo-skill"
            write_skill_dir(canonical_dir, skill_name="demo-skill")
            project_root.mkdir(parents=True, exist_ok=True)

            enable_result = self.run_script(
                "enable",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_root),
                "--platform-root",
                str(platform_root),
            )
            self.assertEqual(enable_result.returncode, 0, enable_result.stderr)

            dependency_graph_path = platform_root / "dependency-graph.json"
            graph_payload = json.loads(dependency_graph_path.read_text())
            graph_payload["projects"] = {}
            graph_payload["projects_total"] = 0
            dependency_graph_path.write_text(json.dumps(graph_payload, indent=2, sort_keys=True) + "\n")

            audit_result = self.run_script(
                "audit",
                "--library-root",
                str(library_root),
                "--workspace-root",
                str(workspace_root),
                "--platform-root",
                str(platform_root),
                "--format",
                "json",
            )

            self.assertNotEqual(audit_result.returncode, 0)
            payload = json.loads(audit_result.stdout)
            self.assertFalse(payload["drift"]["dependency_graph_matches"])
            self.assertTrue(
                any("Dependency graph is out of date" in issue for issue in payload["issues"])
            )

    def test_audit_reports_blocking_lifecycle_violation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)
            library_root = workspace_root / "_skill-library"
            platform_root = workspace_root / ".skill-platform"
            project_root = workspace_root / "demo-project"
            canonical_dir = library_root / "demo-skill"
            write_skill_dir(canonical_dir, skill_name="demo-skill")
            project_root.mkdir(parents=True, exist_ok=True)

            enable_result = self.run_script(
                "enable",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_root),
                "--platform-root",
                str(platform_root),
            )
            self.assertEqual(enable_result.returncode, 0, enable_result.stderr)

            registry_path = platform_root / "registry.json"
            registry_payload = json.loads(registry_path.read_text())
            registry_payload["skills"]["demo-skill"]["lifecycle_status"] = "archived"
            registry_path.write_text(json.dumps(registry_payload, indent=2, sort_keys=True) + "\n")

            audit_result = self.run_script(
                "audit",
                "--library-root",
                str(library_root),
                "--workspace-root",
                str(workspace_root),
                "--platform-root",
                str(platform_root),
                "--format",
                "json",
            )

            self.assertNotEqual(audit_result.returncode, 0)
            payload = json.loads(audit_result.stdout)
            self.assertTrue(
                any(
                    finding["type"] == "inactive-lifecycle-has-dependents"
                    for finding in payload["audit_findings"]
                )
            )

    def test_enable_task_auto_syncs_platform_state(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_root = Path(tmpdir)
            library_root = workspace_root / "_skill-library"
            platform_root = workspace_root / ".skill-platform"
            project_root = workspace_root / "demo-project"
            canonical_dir = library_root / "demo-skill"
            write_skill_dir(canonical_dir, skill_name="demo-skill")
            project_root.mkdir(parents=True, exist_ok=True)

            result = self.run_script(
                "enable",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--project-root",
                str(project_root),
                "--workspace-root",
                str(workspace_root),
                "--platform-root",
                str(platform_root),
            )

            registry_path = platform_root / "registry.json"
            dependency_graph_path = platform_root / "dependency-graph.json"

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Platform state sync", result.stdout)
            self.assertTrue(registry_path.exists())
            self.assertTrue(dependency_graph_path.exists())
            registry_payload = json.loads(registry_path.read_text())
            self.assertIn("demo-skill", registry_payload["skills"])

    def test_add_generates_richer_skill_md_draft(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            result = self.run_script(
                "add",
                "release-notes-skill",
                "--library-root",
                str(library_root),
                "--purpose",
                "Use this skill when the user wants help with release note workflows.",
                "--resources",
                "scripts,references",
            )

            skill_md = (library_root / "release-notes-skill" / "SKILL.md").read_text()

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("## Do Not Use This Skill When", skill_md)
            self.assertIn("## Inputs / Outputs", skill_md)
            self.assertIn("## Risks / Boundaries", skill_md)
            self.assertIn("`scripts/`", skill_md)
            self.assertIn("`references/`", skill_md)

    def test_document_task_previews_contextual_draft_as_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            skill_dir = library_root / "demo-skill"
            write_skill_dir(skill_dir, skill_name="demo-skill")
            (skill_dir / "scripts").mkdir(parents=True, exist_ok=True)
            (skill_dir / "scripts" / "summarize.py").write_text("print('ok')\n")

            result = self.run_script(
                "document",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--dry-run",
                "--format",
                "json",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["mode"], "document")
        self.assertTrue(payload["ok"])
        self.assertFalse(payload["applied"])
        self.assertIn("## Inputs / Outputs", payload["draft_content"])
        self.assertIn("scripts/", payload["draft_content"])

    def test_document_task_merges_missing_sections_by_default(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            skill_dir = library_root / "demo-skill"
            write_skill_dir(skill_dir, skill_name="demo-skill")
            (skill_dir / "SKILL.md").write_text(
                "\n".join(
                    [
                        "---",
                        "name: demo-skill",
                        'description: "Use this skill when the user wants help with demo-skill tasks."',
                        "---",
                        "",
                        "# Demo Skill",
                        "",
                        "## Purpose",
                        "",
                        "Old content.",
                        "",
                    ]
                )
                + "\n"
            )

            result = self.run_script(
                "document",
                "demo-skill",
                "--library-root",
                str(library_root),
            )

            merged = (skill_dir / "SKILL.md").read_text()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[DOCUMENT] Update style: merge-missing-sections", result.stdout)
        self.assertIn("[DOCUMENT] Added sections:", result.stdout)
        self.assertIn("Old content.", merged)
        self.assertIn("## Purpose", merged)
        self.assertIn("## Do Not Use This Skill When", merged)
        self.assertIn("## Risks / Boundaries", merged)
        self.assertNotIn("Use this skill when the user needs help with demo skill workflows.", merged)

    def test_document_task_preview_reports_merge_mode_and_preserves_existing_sections(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            skill_dir = library_root / "demo-skill"
            write_skill_dir(skill_dir, skill_name="demo-skill")
            (skill_dir / "SKILL.md").write_text(
                "\n".join(
                    [
                        "---",
                        "name: demo-skill",
                        'description: "Use this skill when the user wants help with demo-skill tasks."',
                        "---",
                        "",
                        "# Demo Skill",
                        "",
                        "## Purpose",
                        "",
                        "Old content.",
                        "",
                    ]
                )
                + "\n"
            )

            result = self.run_script(
                "document",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--dry-run",
                "--format",
                "json",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["rewrite_mode"], "merge-missing-sections")
        self.assertIn("Do Not Use This Skill When", payload["missing_sections_added"])
        self.assertIn("Purpose", payload["preserved_sections"])
        self.assertIn("Old content.", payload["draft_content"])

    def test_document_task_rewrites_existing_skill_md_when_overwrite_requested(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            library_root = Path(tmpdir) / "_skill-library"
            skill_dir = library_root / "demo-skill"
            write_skill_dir(skill_dir, skill_name="demo-skill")
            (skill_dir / "SKILL.md").write_text(
                "\n".join(
                    [
                        "---",
                        "name: demo-skill",
                        'description: "Use this skill when the user wants help with demo-skill tasks."',
                        "---",
                        "",
                        "# Demo Skill",
                        "",
                        "## Purpose",
                        "",
                        "Old content.",
                        "",
                    ]
                )
                + "\n"
            )

            result = self.run_script(
                "document",
                "demo-skill",
                "--library-root",
                str(library_root),
                "--overwrite-skill-md",
            )

            rewritten = (skill_dir / "SKILL.md").read_text()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[DOCUMENT] SKILL.md:", result.stdout)
        self.assertIn("[DOCUMENT] Update style: full-rewrite", result.stdout)
        self.assertNotIn("Old content.", rewritten)
        self.assertIn("[DOCUMENT] SKILL.md:", result.stdout)
        self.assertIn("## Do Not Use This Skill When", rewritten)
        self.assertIn("## Risks / Boundaries", rewritten)


if __name__ == "__main__":
    unittest.main()
