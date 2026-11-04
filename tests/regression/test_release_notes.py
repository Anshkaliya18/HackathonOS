import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "release-notes.py"


class ReleaseNotesTests(unittest.TestCase):
    def test_tag_extracts_its_changelog_section(self):
        with tempfile.TemporaryDirectory(prefix="hackathonos-release-notes-") as folder:
            output = Path(folder) / "notes.md"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "v1.0.0", str(output)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            notes = output.read_text(encoding="utf-8")
            self.assertIn("CLI downloads use partial files", notes)
            self.assertNotIn("## Unreleased", notes)

    def test_missing_changelog_version_fails(self):
        with tempfile.TemporaryDirectory(prefix="hackathonos-release-notes-") as folder:
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "v9.9.9", str(Path(folder) / "notes.md")],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("no release section", result.stderr)


if __name__ == "__main__":
    unittest.main()
