#!/usr/bin/env python3
"""Refresh portable skill bundles before npm packing."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLES = (ROOT / "skills/sherpa", ROOT / ".agents/skills/sherpa")
DIRECTORIES = ("commands", "core", "workflows", "rules", "templates", "src")
DOC_FILES = (
    "docs/commands/README.md",
    "docs/configuration/runtime-verification.md",
)


def ignore_generated(_directory: str, names: list[str]) -> set[str]:
    return {name for name in names if name == "__pycache__" or name.endswith((".pyc", ".pyo"))}


def main() -> None:
    version = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["version"]
    for bundle in BUNDLES:
        bundle.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / "SKILL.md", bundle / "SKILL.md")
        for name in DIRECTORIES:
            shutil.copytree(ROOT / name, bundle / name, dirs_exist_ok=True, ignore=ignore_generated)
        for relative in DOC_FILES:
            source = ROOT / relative
            destination = bundle / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        for cache in bundle.rglob("__pycache__"):
            shutil.rmtree(cache)
        for artifact in bundle.rglob("*"):
            if artifact.is_file() and artifact.suffix in {".pyc", ".pyo"}:
                artifact.unlink()

    manifests = (
        ROOT / "plugin.json",
        ROOT / ".claude-plugin/plugin.json",
        ROOT / ".codex-plugin/plugin.json",
        ROOT / "gemini-extension.json",
        ROOT / "qwen-extension.json",
    )
    for path in manifests:
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["version"] = version
        path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    marketplace_path = ROOT / ".claude-plugin/marketplace.json"
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    for plugin in marketplace["plugins"]:
        if plugin.get("source", {}).get("source") == "npm" and plugin["source"].get("package") == "sherpa-skill":
            plugin["source"]["version"] = version
    marketplace_path.write_text(json.dumps(marketplace, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
