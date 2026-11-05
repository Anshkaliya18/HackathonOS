#!/usr/bin/env python3
"""Build Sherpa release archives and their truthful checksum manifest."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tarfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def tracked_files() -> list[Path]:
    result = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True)
    entries = result.stdout.decode().split("\0")
    excluded = {".git", ".claude", ".opencode", ".kilo", ".sherpa", "node_modules", "tests", "distribution", "package.json", "package-lock.json"}
    allowed_directories = {"commands", "core", "workflows", "rules", "templates", "src", "scripts", "adapters", "docs"}
    allowed_root_files = {"SKILL.md", "README.md", "LICENSE", ".env.sherpa.example"}
    paths = []
    for name in entries:
        if not name:
            continue
        path = Path(name)
        if path.parts[0] in excluded or any(part in {"__pycache__", ".pytest_cache"} for part in path.parts):
            continue
        if len(path.parts) == 1 and path.name not in allowed_root_files:
            continue
        if len(path.parts) > 1 and path.parts[0] not in allowed_directories:
            continue
        full = ROOT / path
        if full.is_file():
            paths.append(path)
    return paths


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    tag = os.environ.get("GITHUB_REF_NAME", "v2.0.0")
    version = tag[1:] if tag.startswith("v") else tag
    output = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "release-assets").resolve()
    output.mkdir(parents=True, exist_ok=True)
    for child in output.iterdir():
        if child.is_file(): child.unlink()
        elif child.is_dir():
            import shutil
            shutil.rmtree(child)
    files = tracked_files()
    archives = []
    for os_name, arch, fmt in (("linux", "amd64", "tar.gz"), ("darwin", "amd64", "tar.gz"),
                               ("darwin", "arm64", "tar.gz"), ("windows", "amd64", "zip")):
        name = f"sherpa-{version}-{os_name}-{arch}.{fmt}"
        dest = output / name
        if fmt == "tar.gz":
            with tarfile.open(dest, "w:gz", compresslevel=9) as archive:
                for rel in files:
                    archive.add(ROOT / rel, arcname=rel.as_posix(), recursive=False)
                archive.add(ROOT / "distribution/VERSION", arcname="VERSION", recursive=False)
        else:
            with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
                for rel in files:
                    archive.write(ROOT / rel, rel.as_posix())
                archive.write(ROOT / "distribution/VERSION", "VERSION")
        archives.append({"os": os_name, "arch": arch, "format": fmt, "name": name,
                         "url": f"https://github.com/Anshkaliya18/Sherpa/releases/download/{tag}/{name}",
                         "size": dest.stat().st_size, "checksum": digest(dest)})
    cli_name = f"sherpa-cli-{version}.zip"
    cli_path = output / cli_name
    with zipfile.ZipFile(cli_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for rel in ("distribution/cli/sherpa", "distribution/cli/sherpa.bat"):
            archive.write(ROOT / rel, Path(rel).name)
    for filename in ("install.sh", "install.ps1", "uninstall.sh", "uninstall.ps1"):
        source = ROOT / "distribution" / filename
        (output / filename).write_bytes(source.read_bytes())
    manifest = {
        "schema_version": 1, "project": "Sherpa",
        "description": "AI agent skill that mentors hackathon teams for Claude Code and OpenCode",
        "latest": {"version": version, "channel": "stable"}, "archives": archives,
        "cli": {"name": "sherpa", "url": f"https://github.com/Anshkaliya18/Sherpa/releases/download/{tag}/{cli_name}",
                "checksum": digest(cli_path), "size": cli_path.stat().st_size},
        "notes": f"Sherpa {version} release. See CHANGELOG.md.",
        "published_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    checksums = []
    for file in sorted(output.iterdir()):
        if file.name not in {"manifest.json", "checksums.txt"}:
            checksums.append(f"{digest(file)}  {file.name}")
    (output / "checksums.txt").write_text("\n".join(checksums) + "\n", encoding="utf-8")
    print(f"Built {len(archives)} skill archives and one CLI archive in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
