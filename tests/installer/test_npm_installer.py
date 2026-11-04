import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ENTRY = ROOT / "distribution" / "npm" / "sherpa.mjs"


class NpmInstallerTests(unittest.TestCase):
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
        self.assertIn("--uninstall", result.stdout)


if __name__ == "__main__":
    unittest.main()
