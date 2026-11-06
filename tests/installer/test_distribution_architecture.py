from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INSTALLER_PATH = ROOT / "distribution" / "cli" / "installer.py"
spec = importlib.util.spec_from_file_location("sherpa_installer", INSTALLER_PATH)
installer = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(installer)


class DistributionArchitectureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build-distributions.py")],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)

    def test_generated_distribution_is_current_and_has_native_adapter_sets(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build-distributions.py"), "--check"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        generated = ROOT / "distribution" / "generated"
        manifest = json.loads((generated / "shared/sherpa/commands/manifest.json").read_text(encoding="utf-8"))
        commands = manifest["implemented"]
        self.assertEqual(len(commands), 28)
        self.assertEqual(len(list((generated / "clients/opencode/commands").glob("*.md"))), len(commands) + 1)
        self.assertEqual(len(list((generated / "clients/kilo/commands").glob("*.md"))), len(commands) + 1)
        self.assertFalse(list((generated / "clients/codex").rglob("commands/*.md")))

    def test_installation_and_resource_resolution_from_external_path_with_spaces(self):
        with tempfile.TemporaryDirectory(prefix="sherpa external project ") as temp:
            outside = Path(temp) / "consuming project with spaces"
            outside.mkdir()
            base = outside / ".opencode"
            results = installer.install("opencode", "project", outside, base)
            self.assertEqual(results[0]["FILES_INSTALLED"], "PASS")
            self.assertEqual(results[0]["SKILL_VALIDATED"], "PASS")
            self.assertEqual(results[0]["COMMANDS_INSTALLED"], "PASS")
            self.assertEqual(results[0]["RESOURCES_VALIDATED"], "PASS")
            self.assertIn("NOT RUN", results[0]["CLIENT_DISCOVERY_VERIFIED"])
            skill = base / "skills/sherpa"
            workflow = skill / "workflows/status.md"
            self.assertTrue(workflow.is_file())
            self.assertEqual(workflow.resolve().parent.parent, skill.resolve())
            self.assertFalse((outside / "workflows/status.md").exists())

    def test_cli_dry_run_reports_targets_without_writing(self):
        with tempfile.TemporaryDirectory(prefix="sherpa dry run ") as temp:
            destination = Path(temp) / "unwritten client root"
            result = subprocess.run(
                [sys.executable, str(ROOT / "distribution/cli/sherpa"), "install", "--client", "codex",
                 "--destination", str(destination), "--dry-run"],
                cwd=ROOT, capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(str(destination / "skills/sherpa"), result.stdout)
            self.assertFalse(destination.exists())

    def test_idempotent_install_upgrade_and_owned_uninstall(self):
        with tempfile.TemporaryDirectory(prefix="sherpa-profile ") as temp:
            base = Path(temp) / "claude config"
            installer.install("claude", "global", destination=base)
            first = hashlib.sha256((base / "skills/sherpa/SKILL.md").read_bytes()).hexdigest()
            installer.install("claude", "global", destination=base)
            second = hashlib.sha256((base / "skills/sherpa/SKILL.md").read_bytes()).hexdigest()
            self.assertEqual(first, second)
            self.assertTrue((base / ".sherpa-install.json").is_file())
            removed = installer.uninstall("claude", "global", destination=base)
            self.assertTrue(any(path.endswith("sherpa") for path in removed))
            self.assertFalse((base / "skills/sherpa").exists())
            self.assertFalse((base / ".sherpa-install.json").exists())

    def test_missing_resources_fail_validation(self):
        with tempfile.TemporaryDirectory(prefix="sherpa-missing-resource-") as temp:
            skill = Path(temp) / "skills/sherpa"
            shutil.copytree(ROOT / "distribution/generated/shared/sherpa", skill)
            (skill / "workflows/status.md").unlink()
            valid, errors = installer.validate_skill(skill)
            self.assertFalse(valid)
            self.assertTrue(any("workflows/status.md" in error for error in errors))

    def test_partial_copy_failure_rolls_back_and_preserves_previous_marker(self):
        with tempfile.TemporaryDirectory(prefix="sherpa-rollback ") as temp:
            base = Path(temp) / "claude config"
            installer.install("claude", "global", destination=base)
            marker = base / ".sherpa-install.json"
            before_marker = marker.read_bytes()
            before_skill = (base / "skills/sherpa/SKILL.md").read_bytes()
            before_alias = (base / "skills/sherpa-status/SKILL.md").read_bytes()
            real_copytree = shutil.copytree
            calls = 0

            def fail_second_copy(src, dst, *args, **kwargs):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("simulated adapter copy failure")
                return real_copytree(src, dst, *args, **kwargs)

            with mock.patch.object(installer.shutil, "copytree", side_effect=fail_second_copy):
                with self.assertRaisesRegex(OSError, "simulated adapter copy failure"):
                    installer.install("claude", "global", destination=base)
            self.assertEqual(marker.read_bytes(), before_marker)
            self.assertEqual((base / "skills/sherpa/SKILL.md").read_bytes(), before_skill)
            self.assertEqual((base / "skills/sherpa-status/SKILL.md").read_bytes(), before_alias)

    def test_version_aware_install_refuses_a_downgrade_without_touching_files(self):
        with tempfile.TemporaryDirectory(prefix="sherpa-upgrade ") as temp:
            base = Path(temp) / "codex"
            installer.install("codex", "global", destination=base)
            skill = base / "skills/sherpa/SKILL.md"
            original = skill.read_bytes()
            marker = base / ".sherpa-install.json"
            data = json.loads(marker.read_text(encoding="utf-8"))
            data["version"] = "99.0.0"
            marker.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "Refusing downgrade"):
                installer.install("codex", "global", destination=base)
            self.assertEqual(skill.read_bytes(), original)
            self.assertEqual(json.loads(marker.read_text(encoding="utf-8"))["version"], "99.0.0")

    def test_codex_and_kilo_shared_global_skill_is_removed_after_last_owner(self):
        with tempfile.TemporaryDirectory(prefix="sherpa shared global ") as temp:
            home = Path(temp) / "user home"
            home.mkdir()
            with mock.patch.object(installer.Path, "home", return_value=home):
                installer.install("codex", "global")
                installer.install("kilo", "global")
                skill = home / ".agents/skills/sherpa/SKILL.md"
                self.assertTrue(skill.is_file())
                installer.uninstall("codex", "global")
                self.assertTrue(skill.is_file(), "Kilo still owns the shared Agent Skill")
                self.assertTrue((home / ".config/kilo/commands/sherpa.md").is_file())
                installer.uninstall("kilo", "global")
                self.assertFalse((home / ".agents/skills/sherpa").exists())

    def test_opencode_real_cli_discovers_project_skill(self):
        binary = shutil.which("opencode")
        if not binary:
            self.skipTest("OpenCode CLI is unavailable")
        with tempfile.TemporaryDirectory(prefix="sherpa opencode discovery ") as temp:
            project = Path(temp) / "consumer project"
            project.mkdir()
            installer.install("opencode", "project", project)
            result = subprocess.run(
                [binary, "debug", "skill", "--pure"],
                cwd=project, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("sherpa", result.stdout.lower())

    @unittest.skipIf(sys.platform == "win32", "Kilo CLI holds a handle on the project working directory after discovery on Windows")
    def test_kilo_real_cli_discovers_project_agent_skill(self):
        binary = shutil.which("kilo")
        if not binary:
            self.skipTest("Kilo CLI is unavailable")
        with tempfile.TemporaryDirectory(prefix="sherpa kilo discovery ") as temp:
            project = Path(temp) / "consumer project"
            project.mkdir()
            installer.install("kilo", "project", project)
            result = subprocess.run(
                [binary, "debug", "skill", "--pure"],
                cwd=project, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("sherpa", result.stdout.lower())

    def test_client_paths_follow_official_global_and_project_layouts(self):
        project = Path("C:/work/my project")
        self.assertEqual(installer.default_base("claude", "project", project), project.resolve() / ".claude")
        self.assertEqual(installer.default_base("opencode", "project", project), project.resolve() / ".opencode")
        self.assertEqual(installer.default_base("codex", "project", project), project.resolve() / ".agents")
        self.assertEqual(installer.default_base("kilo", "project", project), project.resolve() / ".kilo")

    def test_clean_npm_pack_install_invokes_generated_distribution(self):
        npm = shutil.which("npm") or shutil.which("npm.cmd")
        if not npm:
            self.skipTest("npm binary is unavailable")
        with tempfile.TemporaryDirectory(prefix="sherpa clean npm ") as temp:
            temp_path = Path(temp)
            pack = subprocess.run(
                [npm, "pack", "--silent", "--pack-destination", str(temp_path)],
                cwd=ROOT, capture_output=True, text=True, check=False,
            )
            self.assertEqual(pack.returncode, 0, pack.stdout + pack.stderr)
            tarball = temp_path / pack.stdout.strip().splitlines()[-1]
            npm_home = temp_path / "npm consumer space"
            installed = subprocess.run(
                [npm, "install", "--offline", "--ignore-scripts", "--no-audit", "--no-fund",
                 "--prefix", str(npm_home), str(tarball)],
                cwd=temp_path, capture_output=True, text=True, check=False,
            )
            self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
            entry = npm_home / "node_modules/sherpa-skill/distribution/npm/sherpa.mjs"
            destination = temp_path / "Codex config with spaces"
            result = subprocess.run(
                ["node", str(entry), "install", "--client", "codex", "--destination", str(destination), "--yes"],
                cwd=temp_path, capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((destination / "skills/sherpa/SKILL.md").is_file())
            self.assertTrue((destination / "skills/sherpa-status/SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
