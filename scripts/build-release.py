#!/usr/bin/env python3
"""Build Sherpa release archives and their truthful checksum manifest."""
from __future__ import annotations

import hashlib
import gzip
import io
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
    excluded = {".git", ".claude", ".opencode", ".kilo", ".agents", ".claude-plugin", ".codex-plugin", ".sherpa", "node_modules", "tests", "distribution", "package.json", "package-lock.json"}
    allowed_directories = {"commands", "core", "workflows", "rules", "templates", "src", "docs"}
    allowed_root_files = {"SKILL.md", "README.md", "LICENSE"}
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
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build-distributions.py")], cwd=ROOT, check=True)
    package_version = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["version"]
    tag = os.environ.get("GITHUB_REF_NAME", f"v{package_version}")
    version = tag[1:] if tag.startswith("v") else tag
    output = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "release-assets").resolve()
    output.mkdir(parents=True, exist_ok=True)
    for child in output.iterdir():
        if child.is_file(): child.unlink()
        elif child.is_dir():
            import shutil
            shutil.rmtree(child)
    files = tracked_files()
    files.extend(sorted((Path("distribution/generated") / path.relative_to(ROOT / "distribution/generated")
                         for path in (ROOT / "distribution/generated").rglob("*") if path.is_file()),
                        key=lambda p: p.as_posix()))
    files.extend((Path("distribution/cli/sherpa"), Path("distribution/cli/installer.py")))
    files = sorted(set(files), key=lambda p: p.as_posix())
    archives = []
    for os_name, arch, fmt in (("linux", "amd64", "tar.gz"), ("darwin", "amd64", "tar.gz"),
                               ("darwin", "arm64", "tar.gz"), ("windows", "amd64", "zip")):
        name = f"sherpa-{version}-{os_name}-{arch}.{fmt}"
        dest = output / name
        if fmt == "tar.gz":
            with dest.open("wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=0, compresslevel=9) as gz:
                with tarfile.open(fileobj=gz, mode="w") as archive:
                    for rel in files:
                        info = archive.gettarinfo(str(ROOT / rel), arcname=rel.as_posix())
                        info.mtime = 0
                        info.uid = info.gid = 0
                        info.uname = info.gname = ""
                        with (ROOT / rel).open("rb") as source:
                            archive.addfile(info, source)
                    info = archive.gettarinfo(str(ROOT / "distribution/VERSION"), arcname="VERSION")
                    info.mtime = 0
                    info.uid = info.gid = 0
                    info.uname = info.gname = ""
                    with (ROOT / "distribution/VERSION").open("rb") as source:
                        archive.addfile(info, source)
        else:
            with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
                for rel in files:
                    info = zipfile.ZipInfo(rel.as_posix(), date_time=(2020, 1, 1, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    archive.writestr(info, (ROOT / rel).read_bytes())
                info = zipfile.ZipInfo("VERSION", date_time=(2020, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, (ROOT / "distribution/VERSION").read_bytes())
        archives.append({"os": os_name, "arch": arch, "format": fmt, "name": name,
                         "url": f"https://github.com/Anshkaliya18/Sherpa/releases/download/{tag}/{name}",
                         "size": dest.stat().st_size, "checksum": digest(dest)})
    cli_name = f"sherpa-cli-{version}.zip"
    cli_path = output / cli_name
    with zipfile.ZipFile(cli_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for rel in ("distribution/cli/sherpa", "distribution/cli/sherpa.bat", "distribution/cli/installer.py"):
            info = zipfile.ZipInfo(Path(rel).name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, (ROOT / rel).read_bytes())
    for filename in ("install.sh", "install.ps1", "uninstall.sh", "uninstall.ps1"):
        source = ROOT / "distribution" / filename
        (output / filename).write_bytes(source.read_bytes())
    source_epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if not source_epoch:
        revision = os.environ.get("GITHUB_SHA", "HEAD")
        try:
            source_epoch = subprocess.run(
                ["git", "show", "-s", "--format=%ct", revision], cwd=ROOT,
                check=True, capture_output=True, text=True,
            ).stdout.strip()
        except subprocess.CalledProcessError:
            source_epoch = "0"
    published_at = datetime.fromtimestamp(int(source_epoch), tz=timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    manifest = {
        "schema_version": 1, "project": "Sherpa",
        "description": "AI hackathon mentor skill for Claude Code, Codex, Gemini CLI, Qwen Code, OpenCode, and Kilo Code",
        "latest": {"version": version, "channel": "stable"}, "archives": archives,
        "cli": {"name": "sherpa", "url": f"https://github.com/Anshkaliya18/Sherpa/releases/download/{tag}/{cli_name}",
                "checksum": digest(cli_path), "size": cli_path.stat().st_size},
        "notes": f"Sherpa {version} release. See CHANGELOG.md.",
        "published_at": published_at,
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
