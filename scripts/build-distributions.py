#!/usr/bin/env python3
"""Build deterministic native Sherpa distributions from canonical sources.

Authored inputs stay at the repository root and in commands/manifest.json.
Only distribution/generated/ is replaced by this command.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "distribution" / "generated"
RESOURCE_DIRS = ("commands", "core", "workflows", "rules", "templates", "src", "docs")
CLIENTS = ("claude", "opencode", "codex", "kilo")
FRONTMATTER = re.compile(r"\A---\s*\n(?P<meta>.*?)\n---\s*\n", re.S)


def clean_text(value: str) -> str:
    return " ".join(value.split())


def validate_sources() -> tuple[dict, list[dict]]:
    root_skill = ROOT / "SKILL.md"
    skill_text = root_skill.read_text(encoding="utf-8")
    if not skill_text.startswith("---\n"):
        raise ValueError("Root SKILL.md must start with YAML metadata")
    manifest = json.loads((ROOT / "commands" / "manifest.json").read_text(encoding="utf-8"))
    commands = manifest.get("implemented")
    if not isinstance(commands, list) or not commands:
        raise ValueError("commands/manifest.json has no implemented commands")
    names: set[str] = set()
    for item in commands:
        name = item.get("command", "")
        if not re.fullmatch(r"sherpa-[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError(f"Invalid command name: {name!r}")
        if name in names:
            raise ValueError(f"Duplicate command name: {name}")
        names.add(name)
        workflow = item.get("workflow", "")
        if workflow.startswith("workflows/") and not (ROOT / workflow).is_file():
            raise ValueError(f"{name} points to missing resource: {workflow}")
        if not item.get("description") or not item.get("router_key"):
            raise ValueError(f"{name} is missing description or router_key")
        item["capabilities"] = {
            "core_workflow": True,
            "agent_skill": list(CLIENTS),
            "native_slash_command": ["claude", "opencode", "kilo"],
        }
    return manifest, commands


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def skill_entry(name: str, description: str, args_text: str, client: str) -> str:
    if client == "claude":
        argument_clause = "The user's supplied arguments are `$ARGUMENTS`; pass them unchanged as focus/context to the registered workflow."
    else:
        argument_clause = "Use the user's current request and all focus details and constraints from the invocation context."
    return f'''---
name: {name}
description: {description} Use this skill when the user invokes {name} or asks for this Sherpa operation.
---

This is a command-specific entry point for the Sherpa skill.

1. Read `../sherpa/SKILL.md` and follow its shared mentor, safety, and project-state rules.
2. Read `../sherpa/commands/manifest.json` and resolve `{name}`. Confirm it is implemented and use only its registered operation and workflow.
3. Read the referenced workflow and supporting resources relative to `../sherpa/`; never resolve Sherpa resources relative to the consuming project's working directory.
4. Route the operation as `{args_text}`. {argument_clause} Preserve approval gates, phase locks, evidence requirements, and scope limits. If a referenced resource is missing, stop and report its exact expected path.
'''


def native_prompt(client: str, item: dict) -> str:
    name = item["command"]
    aliases = item.get("legacy_aliases", [])
    operation = aliases[0].removeprefix("/sherpa ") if aliases else name.removeprefix("sherpa-")
    if client == "opencode":
        header = f"---\ndescription: {item['description']}\n---\n\n"
        return header + f"Load and follow the installed Agent Skill `sherpa`. Command: `{name}`. Route operation: `{item['router_key']}`. Resolve only that command through the bundled manifest, then execute its registered workflow and resources relative to the skill directory. User arguments: `$ARGUMENTS`. If the skill or any resource is unavailable, report the missing name/path and stop. Do not infer a fallback operation.\n"
    if client == "kilo":
        header = f"---\ndescription: {item['description']}\n---\n\n"
        # Kilo's official workflow docs do not document an argument placeholder.
        return header + f"Load the installed Agent Skill `sherpa`. Command: `{name}`. Route operation: `{item['router_key']}`. Execute only this manifest entry using the workflow/resources relative to the installed skill directory. Kilo's documented workflow format does not specify argument substitution; do not assume trailing text is available. If focus details are needed, ask the user to invoke the Sherpa skill and include them there. If a resource is missing, report its exact name/path and stop.\n"
    return skill_entry(name, item["description"], operation, client)


def build(output: Path) -> dict:
    manifest, commands = validate_sources()
    temp_parent = output.parent
    temp_parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix="sherpa-build-", dir=temp_parent))
    try:
        package_manifest = dict(manifest)
        package_manifest["implemented"] = commands
        package_manifest["version"] = (ROOT / "distribution" / "VERSION").read_text(encoding="utf-8").strip()
        shared = stage / "shared" / "sherpa"
        shared.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / "SKILL.md", shared / "SKILL.md")
        for directory in RESOURCE_DIRS:
            source = ROOT / directory
            if source.is_dir():
                shutil.copytree(source, shared / directory, dirs_exist_ok=True,
                                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", "node_modules"))
        (shared / "commands" / "manifest.json").write_text(
            json.dumps(package_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        shutil.copy2(ROOT / "distribution" / "VERSION", shared / "VERSION")
        for client in CLIENTS:
            base = stage / "clients" / client
            skills = base / "skills"
            skills.mkdir(parents=True, exist_ok=True)
            if client in {"claude", "codex"}:
                for item in commands:
                    dest = skills / item["command"] / "SKILL.md"
                    write(dest, skill_entry(item["command"], item["description"], item.get("router_key", ""), client))
            if client == "opencode":
                write(base / "commands" / "sherpa.md",
                      "---\ndescription: Route a Sherpa request to its registered workflow.\n---\n\nLoad and follow the installed Agent Skill `sherpa`. Forward the complete user arguments unchanged to its canonical router. Resolve the operation only from the bundled command manifest and read supporting resources relative to the skill directory; never infer a fallback for unknown commands. Arguments: `$ARGUMENTS`. If a skill or resource is missing, report its expected name/path and stop.\n")
                for item in commands:
                    write(base / "commands" / f"{item['command']}.md", native_prompt(client, item))
            elif client == "kilo":
                write(base / "commands" / "sherpa.md",
                      "---\ndescription: Route a Sherpa request to its registered workflow.\n---\n\nLoad and follow the installed Agent Skill `sherpa`. Resolve the user's request through its bundled command manifest and read workflow resources relative to the skill directory. The documented Kilo workflow format does not specify argument substitution, so do not assume trailing arguments are available. Ask the user to invoke the Agent Skill directly if arguments or focus details must be forwarded. If a resource is missing, report its expected name/path and stop.\n")
                for item in commands:
                    write(base / "commands" / f"{item['command']}.md", native_prompt(client, item))
        source_files = [ROOT / "SKILL.md", ROOT / "commands" / "manifest.json"]
        for folder in RESOURCE_DIRS:
            if (ROOT / folder).exists():
                source_files.extend(p for p in (ROOT / folder).rglob("*") if p.is_file() and p.suffix not in {".pyc", ".pyo"})
        digest = hashlib.sha256()
        for file in sorted(set(source_files)):
            digest.update(file.relative_to(ROOT).as_posix().encode())
            digest.update(b"\0")
            digest.update(file.read_bytes())
            digest.update(b"\0")
        metadata = {
            "generated": True,
            "generator": "scripts/build-distributions.py",
            "source_sha256": digest.hexdigest(),
            "clients": list(CLIENTS),
            "command_count": len(commands),
            "capabilities": {
                "claude": {"skills": True, "native_slash_commands": True},
                "opencode": {"skills": True, "native_slash_commands": True},
                "codex": {"skills": True, "native_slash_commands": False},
                "kilo": {"skills": True, "native_slash_commands": True, "argument_substitution": False},
            },
        }
        write(stage / "README.generated.md", "# Generated Sherpa distributions\n\nGenerated by `scripts/build-distributions.py`. Edit canonical root `SKILL.md`, resources, or `commands/manifest.json`; never edit files here directly.\n")
        write(stage / "build-manifest.json", json.dumps(metadata, indent=2) + "\n")
        if output.exists():
            shutil.rmtree(output)
        # Windows may hold a transient handle on the staged directory (for
        # example, virus scanning); copy into the dedicated generated path.
        # The stage is fully built before the old output is removed.
        if output.exists():
            shutil.rmtree(output)
        shutil.copytree(stage, output)
        return metadata
    finally:
        if stage.exists():
            shutil.rmtree(stage)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="build into a temporary directory and compare outputs")
    args = parser.parse_args()
    output = args.output.resolve()
    if args.check:
        with tempfile.TemporaryDirectory(prefix="sherpa-check-") as temp:
            expected = Path(temp) / "generated"
            build(expected)
            if not output.exists():
                raise SystemExit(f"Generated output is missing: {output}. Run the build first.")
            expected_files = {p.relative_to(expected) for p in expected.rglob("*") if p.is_file()}
            actual_files = {p.relative_to(output) for p in output.rglob("*") if p.is_file()}
            if expected_files != actual_files:
                raise SystemExit("Generated distribution file list is stale; run the build.")
            for rel in expected_files:
                if (expected / rel).read_bytes() != (output / rel).read_bytes():
                    raise SystemExit(f"Generated distribution is stale: {rel}. Run the build.")
            print(f"Distribution check passed ({len(expected_files)} files).")
        return 0
    metadata = build(output)
    print(f"Built deterministic client distributions: {', '.join(metadata['clients'])}; {metadata['command_count']} commands.")
    print(f"Source SHA-256: {metadata['source_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
