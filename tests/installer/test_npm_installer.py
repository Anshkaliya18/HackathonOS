import os
import json
import subprocess
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ENTRY = ROOT / "distribution" / "npm" / "sherpa.mjs"


class NpmInstallerTests(unittest.TestCase):
    def run_npm_cli(self, *args, profile=None, env_overrides=None):
        env = os.environ.copy()
        if profile is not None:
            env["HOME"] = str(profile)
            env["USERPROFILE"] = str(profile)
        if env_overrides:
            env.update(env_overrides)
        return subprocess.run(
            ["node", str(ENTRY), *args],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_dry_run_lists_both_targets_without_creating_them(self):
        with tempfile.TemporaryDirectory(prefix="sherpa-npm-dry-run-") as profile:
            env = os.environ.copy()
            env["HOME"] = profile
            env["USERPROFILE"] = profile
            result = subprocess.run(
                ["node", str(ENTRY), "install", "--dry-run"],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(str(Path(profile) / ".claude" / "skills" / "sherpa"), result.stdout)
            self.assertIn(str(Path(profile) / ".config" / "opencode" / "skills" / "sherpa"), result.stdout)
            self.assertIn("no files were changed", result.stdout)
            self.assertFalse((Path(profile) / ".claude").exists())
            self.assertFalse((Path(profile) / ".config").exists())

    def test_help_exits_without_installing(self):
        result = subprocess.run(
            ["node", str(ENTRY), "--help"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--dry-run", result.stdout)
        self.assertIn("--no-cli", result.stdout)
        self.assertIn("--uninstall", result.stdout)
        self.assertIn("doctor", result.stdout)
        self.assertIn("audit", result.stdout)
        self.assertIn("clean", result.stdout)
        self.assertIn("--version", result.stdout)

    def test_management_cli_commands_are_forwarded(self):
        with tempfile.TemporaryDirectory(prefix="sherpa-npm-cli-") as profile:
            version = self.run_npm_cli("--version")
            self.assertEqual(version.returncode, 0, version.stderr)
            self.assertIn("sherpa 2.0.7", version.stdout)

            help_result = self.run_npm_cli("help")
            self.assertEqual(help_result.returncode, 0, help_result.stderr)
            self.assertIn("distribution CLI", help_result.stdout)
            self.assertIn("sherpa audit", help_result.stdout)
            self.assertIn("sherpa clean", help_result.stdout)

            for command, expected in (("audit", "Sherpa output audit"), ("clean", "Dry run")):
                args = (command, "--dry-run") if command == "clean" else (command,)
                result = self.run_npm_cli(*args, profile=profile)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(expected, result.stdout)

            update = self.run_npm_cli("update", profile=profile)
            self.assertEqual(update.returncode, 1)
            self.assertIn("No Sherpa skill installation found", update.stdout)

    def test_doctor_is_forwarded_and_reads_manifest(self):
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                body = json.dumps({"project": "Sherpa", "latest": {"version": "2.0.7"}}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_args):
                pass

        with tempfile.TemporaryDirectory(prefix="sherpa-npm-doctor-") as profile:
            server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                url = f"http://127.0.0.1:{server.server_port}/manifest.json"
                result = self.run_npm_cli(
                    "doctor",
                    profile=profile,
                    env_overrides={"SHERPA_RELEASE_MANIFEST_URL": url},
                )
            finally:
                server.shutdown()
                thread.join(timeout=2)
                server.server_close()
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("=== sherpa doctor ===", result.stdout)
            self.assertIn("Manifest reachable: yes (latest 2.0.7)", result.stdout)

    def test_migrate_is_forwarded_and_preserves_legacy_state(self):
        with tempfile.TemporaryDirectory(prefix="sherpa-npm-migrate-") as project:
            legacy = Path(project) / ".hackathon"
            legacy.mkdir()
            (legacy / "notes.md").write_text("keep this\n", encoding="utf-8")
            result = self.run_npm_cli("migrate", "--project-root", project, "--yes")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((Path(project) / ".sherpa" / "notes.md").read_text(encoding="utf-8"), "keep this\n")
            self.assertEqual((legacy / "notes.md").read_text(encoding="utf-8"), "keep this\n")

    def test_uninstall_remains_available_in_isolated_profile(self):
        with tempfile.TemporaryDirectory(prefix="sherpa-npm-uninstall-") as profile:
            result = self.run_npm_cli("uninstall", profile=profile)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("No sherpa installation found", result.stdout)

    def test_unknown_commands_show_management_cli_usage(self):
        result = self.run_npm_cli("not-a-command")
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage: sherpa", result.stderr.lower())

    def test_package_does_not_publish_python_caches(self):
        package = __import__("json").loads((ROOT / "package.json").read_text(encoding="utf-8"))
        self.assertNotIn("distribution/cli/", package["files"])
        self.assertIn("distribution/cli/sherpa", package["files"])


if __name__ == "__main__":
    unittest.main()
