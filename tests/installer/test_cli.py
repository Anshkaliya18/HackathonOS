#!/usr/bin/env python3
"""Tests for the HackathonOS distribution CLI.

External downloads are mocked. Tests run in disposable directories and never
touch the real user skill installation or any `.hackathon/` project state.
Runs standalone with unittest.mock (no pytest required).
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import platform
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path
from unittest import mock

# Load the CLI module (no .py extension) by path.
import importlib.util
from importlib.machinery import SourceFileLoader

CLI_PATH = Path(__file__).resolve().parents[2] / "distribution" / "cli" / "hackathonos"
spec = importlib.util.spec_from_file_location(
    "hackathonos_cli", CLI_PATH, loader=SourceFileLoader("hackathonos_cli", str(CLI_PATH))
)
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


def patch(obj, attr, new):
    return mock.patch.object(obj, attr, new)


def make_skill_dir(root: Path, name: str = "hackathonos", version: str | None = "1.0.0") -> Path:
    """Build a minimal valid skill tree in a disposable directory."""
    skill = root / name
    (skill / "commands").mkdir(parents=True)
    (skill / "core" / "commands").mkdir(parents=True)
    (skill / "workflows").mkdir()
    (skill / "workflows" / "status.md").write_text("# status\n")
    (skill / "SKILL.md").write_text("# skill\n")
    (skill / "commands" / "manifest.json").write_text(json.dumps({"schema_version": 1}))
    (skill / "core" / "commands" / "router.py").write_text("x = 1\n")
    if version is not None:
        (skill / "VERSION").write_text(version + "\n")
    return skill


def make_tarball(path: Path, files: dict[str, bytes]) -> None:
    with tarfile.open(path, "w:gz") as tar:
        for name, data in files.items():
            info = tarfile.TarInfo(name=name)
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))


def make_zipball(path: Path, files: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path, "w") as zf:
        for name, data in files.items():
            zf.writestr(name, data)


# ---------------------------------------------------------------------------
# Version / detection
# ---------------------------------------------------------------------------

def test_cli_version():
    assert cli.cli_version() == "1.0.0"


def test_installed_version_reads_file():
    with tempfile.TemporaryDirectory() as tmp:
        skill = make_skill_dir(Path(tmp), version="2.0.0")
        assert cli.installed_version(skill) == "2.0.0"


def test_installed_version_missing_file():
    with tempfile.TemporaryDirectory() as tmp:
        skill = make_skill_dir(Path(tmp), version=None)
        assert cli.installed_version(skill) is None


def test_detect_installed():
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        claude = base / ".claude" / "skills"
        opencode = base / ".config" / "opencode" / "skills"
        make_skill_dir(claude)
        make_skill_dir(opencode)

        with patch(cli, "CLAUDE_SKILL_DIR", claude / "hackathonos"), \
             patch(cli, "OPENCODE_SKILL_DIR", opencode / "hackathonos"), \
             patch(cli, "SKILL_DIRS", {"claude": claude / "hackathonos", "opencode": opencode / "hackathonos"}):
            found = cli.detect_installed()
        assert set(found) == {"claude", "opencode"}


def test_detect_installed_none():
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        with patch(cli, "CLAUDE_SKILL_DIR", base / "nope" / "claude"), \
             patch(cli, "OPENCODE_SKILL_DIR", base / "nope" / "opencode"), \
             patch(cli, "SKILL_DIRS", {"claude": base / "nope" / "claude", "opencode": base / "nope" / "opencode"}):
            assert cli.detect_installed() == {}


# ---------------------------------------------------------------------------
# Manifest URL
# ---------------------------------------------------------------------------

def test_manifest_url_default():
    with mock.patch.dict(os.environ, {}, clear=True):
        os.environ.pop("HACKATHONOS_RELEASE_MANIFEST_URL", None)
        assert cli.manifest_url() == cli.DEFAULT_MANIFEST_URL


def test_manifest_url_env():
    with mock.patch.dict(os.environ, {"HACKATHONOS_RELEASE_MANIFEST_URL": "https://example.com/manifest.json"}):
        assert cli.manifest_url() == "https://example.com/manifest.json"


# ---------------------------------------------------------------------------
# Checksum
# ---------------------------------------------------------------------------

def test_sha256_file():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "file.txt"
        p.write_bytes(b"hello world")
        expected = hashlib.sha256(b"hello world").hexdigest()
        assert cli.sha256_file(p) == expected


# ---------------------------------------------------------------------------
# Safe extraction (path traversal protection)
# ---------------------------------------------------------------------------

def test_safe_extract_tar_path_traversal_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        archive = Path(tmp) / "evil.tar.gz"
        make_tarball(archive, {
            "good.txt": b"good",
            "../../etc/evil": b"evil",
        })
        dest = Path(tmp) / "dest"
        dest.mkdir()
        try:
            cli.safe_extract_tar(archive, dest)
        except cli.HackathonOSError as exc:
            assert "path traversal" in str(exc)
        else:
            raise AssertionError("path traversal tar was not rejected")


def test_safe_extract_tar_safe():
    with tempfile.TemporaryDirectory() as tmp:
        archive = Path(tmp) / "safe.tar.gz"
        make_tarball(archive, {"a/b.txt": b"x", "c.md": b"y"})
        dest = Path(tmp) / "dest"
        cli.safe_extract_tar(archive, dest)
        assert (dest / "a" / "b.txt").read_bytes() == b"x"
        assert (dest / "c.md").read_bytes() == b"y"


def test_safe_extract_zip_path_traversal_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        archive = Path(tmp) / "evil.zip"
        make_zipball(archive, {
            "good.txt": b"good",
            "../evil": b"evil",
        })
        dest = Path(tmp) / "dest"
        dest.mkdir()
        try:
            cli.safe_extract_zip(archive, dest)
        except cli.HackathonOSError as exc:
            assert "path traversal" in str(exc)
        else:
            raise AssertionError("path traversal zip was not rejected")


# ---------------------------------------------------------------------------
# Archive selection by platform
# ---------------------------------------------------------------------------

def test_platform_archive_name_windows_amd64():
    manifest = {
        "archives": [
            {"os": "windows", "arch": "amd64", "format": "zip", "url": "https://example.com/w.zip"},
            {"os": "linux", "arch": "amd64", "format": "tar.gz", "url": "https://example.com/l.tar.gz"},
        ]
    }
    with mock.patch.object(platform, "system", return_value="Windows"), \
         mock.patch.object(platform, "machine", return_value="AMD64"):
        entry = cli.platform_archive_name(manifest)
    assert entry is not None
    assert entry["url"].endswith("w.zip")


def test_platform_archive_name_linux_arm64():
    manifest = {
        "archives": [
            {"os": "linux", "arch": "arm64", "format": "tar.gz", "url": "https://example.com/l-arm.tar.gz"},
        ]
    }
    with mock.patch.object(platform, "system", return_value="Linux"), \
         mock.patch.object(platform, "machine", return_value="aarch64"):
        entry = cli.platform_archive_name(manifest)
    assert entry is not None
    assert entry["url"].endswith("l-arm.tar.gz")


def test_platform_archive_name_no_match():
    manifest = {"archives": [{"os": "linux", "arch": "amd64", "format": "tar.gz", "url": "x"}]}
    with mock.patch.object(platform, "system", return_value="Windows"), \
         mock.patch.object(platform, "machine", return_value="x86_64"):
        assert cli.platform_archive_name(manifest) is None


# ---------------------------------------------------------------------------
# validate_skill_tree
# ---------------------------------------------------------------------------

def test_validate_skill_tree_ok():
    with tempfile.TemporaryDirectory() as tmp:
        skill = make_skill_dir(Path(tmp))
        assert cli.validate_skill_tree(skill) == []


def test_validate_skill_tree_missing():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "bad"
        root.mkdir()
        (root / "SKILL.md").write_text("x")
        problems = cli.validate_skill_tree(root)
        assert any("manifest" in p for p in problems)
        assert any("router" in p for p in problems)


# ---------------------------------------------------------------------------
# Update flow (mocked download)
# ---------------------------------------------------------------------------

MANIFEST = {
    "latest": {"version": "2.0.0"},
    "archives": [
        {"os": "linux", "arch": "amd64", "format": "tar.gz",
         "url": "https://example.com/hackathonos-2.0.0-linux-amd64.tar.gz",
         "checksum": "0" * 64},
    ],
    "cli": {"url": "", "checksum": ""},
}


def build_update_environment():
    tmp = Path(tempfile.mkdtemp())
    claude = make_skill_dir(tmp / ".claude" / "skills", version="1.0.0")
    opencode = make_skill_dir(tmp / ".config" / "opencode" / "skills", version="1.0.0")
    return tmp, claude, opencode


def fake_download_success(url, dest):
    dest_path = Path(dest)
    files = {
        "SKILL.md": b"# skill\n",
        "commands/manifest.json": b"{}",
        "commands/hackathonos-status.md": b"---\n---\n",
        "core/commands/router.py": b"x = 1\n",
        "workflows/status.md": b"# status\n",
        "templates/project-state.md": b"# state\n",
        "rules/mentor-rules.md": b"# rules\n",
        "src/verification.py": b"v = 1\n",
        "src/config_manager.py": b"c = 1\n",
        "scripts/evaluate.py": b"e = 1\n",
        "adapters/claude/README.md": b"# claude\n",
        "docs/configuration/overview.md": b"# docs\n",
        "VERSION": b"2.0.0\n",
    }
    make_tarball(dest_path, files)
    return dest_path


def test_update_installs_and_reports_version():
    tmp, claude, opencode = build_update_environment()

    with mock.patch.object(cli, "manifest_url", lambda: "https://example.com/manifest.json"), \
         mock.patch.object(cli, "fetch_json", lambda url, timeout=30: MANIFEST), \
         mock.patch.object(cli, "download_file", fake_download_success), \
         mock.patch.object(cli, "sha256_file", lambda p: "0" * 64), \
         mock.patch.object(cli, "platform_archive_name", lambda m: MANIFEST["archives"][0]), \
         mock.patch.object(cli, "SKILL_DIRS", {"claude": claude, "opencode": opencode}), \
         mock.patch.object(cli, "log", lambda m, level="info": None):

        rc = cli.cmd_update(mock.MagicMock())
    assert rc == 0
    assert (claude / "VERSION").read_text().strip() == "2.0.0"
    assert (opencode / "VERSION").read_text().strip() == "2.0.0"
    assert (claude / "SKILL.md").exists()


def test_update_up_to_date():
    tmp, claude, opencode = build_update_environment()
    (claude / "VERSION").write_text("2.0.0\n")
    (opencode / "VERSION").write_text("2.0.0\n")

    with mock.patch.object(cli, "manifest_url", lambda: "https://example.com/manifest.json"), \
         mock.patch.object(cli, "fetch_json", lambda url, timeout=30: MANIFEST), \
         mock.patch.object(cli, "log", lambda m, level="info": None), \
         mock.patch.object(cli, "SKILL_DIRS", {"claude": claude, "opencode": opencode}):

        rc = cli.cmd_update(mock.MagicMock())
    assert rc == 0


def test_update_checksum_mismatch():
    tmp, claude, opencode = build_update_environment()

    manifest_bad = json.loads(json.dumps(MANIFEST))
    manifest_bad["archives"][0]["checksum"] = "f" * 64

    with mock.patch.object(cli, "manifest_url", lambda: "https://example.com/manifest.json"), \
         mock.patch.object(cli, "fetch_json", lambda url, timeout=30: manifest_bad), \
         mock.patch.object(cli, "download_file", fake_download_success), \
         mock.patch.object(cli, "sha256_file", lambda p: "0" * 64), \
         mock.patch.object(cli, "platform_archive_name", lambda m: manifest_bad["archives"][0]), \
         mock.patch.object(cli, "SKILL_DIRS", {"claude": claude, "opencode": opencode}):

        try:
            cli.cmd_update(mock.MagicMock())
        except cli.HackathonOSError as exc:
            assert "checksum" in str(exc).lower()
        else:
            raise AssertionError("checksum mismatch was not raised")


def test_update_rolls_back_on_invalid_archive():
    tmp, claude, opencode = build_update_environment()

    def bad_download(url, dest):
        dest_path = Path(dest)
        make_tarball(dest_path, {"commands/manifest.json": b"{}"})
        return dest_path

    with mock.patch.object(cli, "manifest_url", lambda: "https://example.com/manifest.json"), \
         mock.patch.object(cli, "fetch_json", lambda url, timeout=30: MANIFEST), \
         mock.patch.object(cli, "download_file", bad_download), \
         mock.patch.object(cli, "sha256_file", lambda p: "0" * 64), \
         mock.patch.object(cli, "platform_archive_name", lambda m: MANIFEST["archives"][0]), \
         mock.patch.object(cli, "SKILL_DIRS", {"claude": claude, "opencode": opencode}):

        try:
            cli.cmd_update(mock.MagicMock())
        except cli.HackathonOSError:
            pass
        else:
            raise AssertionError("invalid archive was not rejected")

    # Original installation must be preserved (rollback).
    assert (claude / "VERSION").read_text().strip() == "1.0.0"
    assert (opencode / "VERSION").read_text().strip() == "1.0.0"


def test_update_preserves_project_state():
    tmp, claude, opencode = build_update_environment()
    project_state = tmp / ".hackathon" / "project-state.md"
    project_state.parent.mkdir(parents=True)
    project_state.write_text("my project state\n")

    with mock.patch.object(cli, "manifest_url", lambda: "https://example.com/manifest.json"), \
         mock.patch.object(cli, "fetch_json", lambda url, timeout=30: MANIFEST), \
         mock.patch.object(cli, "download_file", fake_download_success), \
         mock.patch.object(cli, "sha256_file", lambda p: "0" * 64), \
         mock.patch.object(cli, "platform_archive_name", lambda m: MANIFEST["archives"][0]), \
         mock.patch.object(cli, "SKILL_DIRS", {"claude": claude, "opencode": opencode}):

        cli.cmd_update(mock.MagicMock())
    assert project_state.read_text() == "my project state\n"


# ---------------------------------------------------------------------------
# Uninstall (mocked)
# ---------------------------------------------------------------------------

def test_uninstall_removes_skills_preserves_project_state():
    tmp, claude, opencode = build_update_environment()
    project_state = tmp / ".hackathon" / "project-state.md"
    project_state.parent.mkdir(parents=True)
    project_state.write_text("preserve me\n")

    cli_bin = tmp / "bin"
    cli_bin.mkdir()
    fake_cli = cli_bin / "hackathonos"
    fake_cli.write_text("#!/usr/bin/env python3\n")

    with mock.patch.object(cli, "SKILL_DIRS", {"claude": claude, "opencode": opencode}), \
         mock.patch.object(cli, "detect_installed", lambda: {"claude": claude, "opencode": opencode}), \
         mock.patch.object(cli, "cli_bin_dir", lambda: cli_bin), \
         mock.patch.object(cli, "log", lambda m, level="info": None):

        rc = cli.cmd_uninstall(mock.MagicMock(assume_yes=True))
    assert rc == 0
    assert not (claude / "SKILL.md").exists()
    assert not (opencode / "SKILL.md").exists()
    assert not fake_cli.exists()
    # Project state preserved.
    assert project_state.read_text() == "preserve me\n"


# ---------------------------------------------------------------------------
# doctor
# ---------------------------------------------------------------------------

def test_doctor_runs():
    with mock.patch.object(cli, "manifest_url", lambda: "https://example.com/manifest.json"), \
         mock.patch.object(cli, "fetch_json", lambda url, timeout=10: {"latest": {"version": "2.0.0"}}):

        rc = cli.cmd_doctor(mock.MagicMock())
    assert rc == 0


if __name__ == "__main__":
    import traceback

    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception:
            failed += 1
            print(f"FAIL {test.__name__}")
            traceback.print_exc()
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
