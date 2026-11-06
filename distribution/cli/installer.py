"""Transactional installation and verification for generated Sherpa bundles."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CLIENTS = ("claude", "opencode", "codex", "kilo")
CLIENT_BINARIES = {"claude": "claude", "opencode": "opencode", "codex": "codex", "kilo": "kilo"}
MARKER = ".sherpa-install.json"


def default_base(client: str, scope: str, project: Path | None) -> Path:
    home = Path.home()
    if scope == "project":
        if project is None:
            raise ValueError("--project-dir is required for a project install")
        return project.resolve() / {"claude": ".claude", "opencode": ".opencode", "codex": ".agents", "kilo": ".kilo"}[client]
    return home / {"claude": ".claude", "opencode": ".config/opencode", "codex": ".agents", "kilo": ".config/kilo"}[client]


def detect_clients() -> list[str]:
    found = []
    for client, binary in CLIENT_BINARIES.items():
        if shutil.which(binary):
            found.append(client)
    return found


def skill_root_for(client: str, base: Path, scope: str, destination: Path | None = None) -> Path:
    if client != "kilo":
        return base / "skills"
    if scope == "project":
        root = destination.parent if destination else base.parent
    else:
        root = destination.parent if destination else Path.home()
    return root / ".agents" / "skills"


def mappings(client: str, base: Path, scope: str, destination: Path | None = None) -> list[tuple[Path, Path]]:
    generated = Path(__file__).resolve().parents[1] / "generated"
    source = generated / "clients" / client
    if not source.is_dir() or not (generated / "shared" / "sherpa" / "SKILL.md").is_file():
        raise FileNotFoundError(f"Generated {client} distribution is missing at {source}; run scripts/build-distributions.py")
    result: list[tuple[Path, Path]] = []
    skill_root = skill_root_for(client, base, scope, destination)
    result.append((generated / "shared" / "sherpa", skill_root / "sherpa"))
    source_skills = source / "skills"
    for item in source_skills.iterdir():
        if item.is_dir():
            result.append((item, skill_root / item.name))
    source_commands = source / "commands"
    if source_commands.is_dir():
        command_root = base / ("commands" if client in {"opencode", "kilo"} else "commands")
        for item in source_commands.iterdir():
            if item.is_file():
                result.append((item, command_root / item.name))
    return result


def validate_skill(skill: Path) -> tuple[bool, list[str]]:
    errors = []
    main = skill / "SKILL.md"
    if not main.is_file():
        return False, [f"Missing {main}"]
    text = main.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\nname:" not in text or "\ndescription:" not in text:
        errors.append(f"Invalid Agent Skill metadata: {main}")
    else:
        frontmatter = text.split("---\n", 2)[1]
        name_match = re.search(r"^name:\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*$", frontmatter, re.M)
        description_match = re.search(r"^description:\s*(.+)$", frontmatter, re.M)
        if not name_match or name_match.group(1) != skill.name:
            errors.append(f"Skill name does not match directory {skill.name}: {main}")
        if not description_match or not 1 <= len(description_match.group(1)) <= 1024:
            errors.append(f"Skill description is missing or invalid: {main}")
    try:
        manifest = json.loads((skill / "commands/manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return False, [*errors, f"Invalid command manifest: {exc}"]
    for item in manifest.get("implemented", []):
        workflow = item.get("workflow", "")
        if workflow.startswith("workflows/") and not (skill / workflow).is_file():
            errors.append(f"Missing workflow resource for {item.get('command')}: {(skill / workflow).as_posix()}")
        for resource in item.get("resources", []):
            if not (skill / resource).is_file():
                errors.append(f"Missing resource for {item.get('command')}: {skill / resource}")
    return not errors, errors


def verify_install(client: str, base: Path, expected: int | None = None, scope: str = "global", destination: Path | None = None) -> dict[str, str | list[str]]:
    skill_root = skill_root_for(client, base, scope, destination)
    skill = skill_root / "sherpa"
    valid, errors = validate_skill(skill)
    manifest = json.loads((skill / "commands/manifest.json").read_text(encoding="utf-8")) if (skill / "commands/manifest.json").is_file() else {"implemented": []}
    commands = manifest.get("implemented", [])
    command_root = base / "commands"
    expected_names = {cmd["command"] for cmd in commands}
    native = [p for p in command_root.glob("sherpa-*.md") if p.is_file()] if client in {"opencode", "kilo"} else []
    if client in {"opencode", "kilo"}:
        native_names = {p.stem for p in command_root.glob("sherpa*.md") if p.is_file()}
        native_ok = native_names == expected_names | {"sherpa"}
    else:
        entry_names = {p.name for p in skill_root.glob("sherpa-*") if (p / "SKILL.md").is_file()}
        native_ok = entry_names == expected_names
        for name in expected_names & entry_names:
            entry = (skill_root / name / "SKILL.md").read_text(encoding="utf-8")
            if "../sherpa/" not in entry or "repository-root" in entry.lower():
                native_ok = False
                errors.append(f"Command skill {name} has an invalid resource reference")
    if client in {"opencode", "kilo"}:
        for path in native:
            content = path.read_text(encoding="utf-8")
            lower = content.lower()
            has_relative_reference = (
                "relative to the skill directory" in lower
                or "relative to the installed skill directory" in lower
            )
            if "repository-root" in lower or not has_relative_reference:
                native_ok = False
                errors.append(f"Native command has an unsafe resource reference: {path}")
    if expected is not None and len(commands) != expected:
        errors.append(f"Manifest command count changed: expected {expected}, got {len(commands)}")
    return {
        "FILES_INSTALLED": "PASS" if skill.is_dir() else "FAIL",
        "SKILL_VALIDATED": "PASS" if valid else "FAIL",
        "COMMANDS_INSTALLED": "PASS" if native_ok else "FAIL",
        "RESOURCES_VALIDATED": "PASS" if valid else "FAIL",
        "CLIENT_DISCOVERY_VERIFIED": "NOT RUN (requires client-specific live discovery test)",
        "RUNTIME_EXECUTION_VERIFIED": "NOT RUN (requires explicit invocation in the client)",
        "errors": errors,
    }


def install(client: str, scope: str, project: Path | None = None, destination: Path | None = None) -> list[dict]:
    base = destination.resolve() if destination else default_base(client, scope, project)
    file_map = mappings(client, base, scope, destination)
    manifest = json.loads((Path(__file__).resolve().parents[1] / "generated" / "shared" / "sherpa" / "commands/manifest.json").read_text(encoding="utf-8"))
    if not file_map:
        raise RuntimeError(f"No generated files for {client}")
    count = len(manifest.get("implemented", []))
    marker = base / MARKER
    if marker.is_file():
        previous = json.loads(marker.read_text(encoding="utf-8"))
        old_version = str(previous.get("version", "0"))
        new_version = str(manifest.get("version", "0"))
        try:
            old_parts = tuple(int(x) for x in old_version.split(".")[:3])
            new_parts = tuple(int(x) for x in new_version.split(".")[:3])
            if new_parts < old_parts:
                raise RuntimeError(f"Refusing downgrade from Sherpa {old_version} to {new_version}")
        except ValueError:
            pass
    transaction = Path(tempfile.mkdtemp(prefix="sherpa-install-"))
    backups: list[tuple[Path, Path]] = []
    installed: list[Path] = []
    prior_marker = marker.read_bytes() if marker.is_file() else None
    marker_written = False
    try:
        for source, target in file_map:
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                backup = transaction / f"backup-{len(backups)}"
                shutil.move(str(target), str(backup))
                backups.append((backup, target))
            installed.append(target)
            if source.is_dir():
                shutil.copytree(source, target)
            else:
                shutil.copy2(source, target)
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text(json.dumps({"client": client, "scope": scope, "version": manifest.get("version", "unknown"),
                                      "managed": [str(path) for path in installed]}, indent=2) + "\n", encoding="utf-8")
        marker_written = True
        result = verify_install(client, base, count, scope, destination)
        if any(result[k] == "FAIL" for k in ("FILES_INSTALLED", "SKILL_VALIDATED", "COMMANDS_INSTALLED", "RESOURCES_VALIDATED")):
            raise RuntimeError("Post-install validation failed: " + "; ".join(result["errors"]))
        result["base"] = str(base)
        result["version"] = manifest.get("version", "unknown")
        return [result]
    except Exception:
        if marker_written:
            if prior_marker is None:
                marker.unlink(missing_ok=True)
            else:
                marker.write_bytes(prior_marker)
        for target in reversed(installed):
            if target.is_dir(): shutil.rmtree(target, ignore_errors=True)
            elif target.exists(): target.unlink()
        for backup, target in reversed(backups):
            if backup.exists(): shutil.move(str(backup), str(target))
        raise
    finally:
        shutil.rmtree(transaction, ignore_errors=True)


def uninstall(client: str, scope: str, project: Path | None = None, destination: Path | None = None) -> list[str]:
    base = destination.resolve() if destination else default_base(client, scope, project)
    marker = base / MARKER
    if not marker.is_file():
        return [f"No managed Sherpa {client} installation found at {base}"]
    data = json.loads(marker.read_text(encoding="utf-8"))
    if data.get("client") != client:
        raise RuntimeError(f"Ownership marker at {marker} belongs to {data.get('client')}, not {client}")
    removed = []
    shared_paths: set[Path] = set()
    for other in CLIENTS:
        if other == client:
            continue
        other_marker = default_base(other, scope, project) / MARKER
        if other_marker.is_file():
            try:
                other_data = json.loads(other_marker.read_text(encoding="utf-8"))
                shared_paths.update(Path(value).resolve() for value in other_data.get("managed", []))
            except (OSError, json.JSONDecodeError):
                raise RuntimeError(f"Cannot safely determine shared installation ownership from {other_marker}")
    for entry in data.get("managed", []):
        target = Path(entry)
        if target.resolve() in shared_paths:
            removed.append(f"Preserved shared skill still used by another client: {target}")
            continue
        if target.is_dir(): shutil.rmtree(target)
        elif target.exists(): target.unlink()
        removed.append(str(target))
    marker.unlink()
    return removed


def add_parser(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("install", help="install a generated client distribution")
    p.add_argument("--client", choices=(*CLIENTS, "auto", "all"), default="auto")
    p.add_argument("--scope", choices=("global", "project"), default="global")
    p.add_argument("--project-dir", type=Path)
    p.add_argument("--destination", type=Path, help="custom client configuration root")
    p.add_argument("--dry-run", action="store_true", help="show native installation targets without writing files")
    p.add_argument("--yes", action="store_true")
    p.set_defaults(func=cmd_install)
    p = sub.add_parser("verify-install", help="verify managed files without claiming live discovery")
    p.add_argument("--client", choices=CLIENTS, required=True)
    p.add_argument("--scope", choices=("global", "project"), default="global")
    p.add_argument("--project-dir", type=Path)
    p.add_argument("--destination", type=Path)
    p.set_defaults(func=cmd_verify)
    p = sub.add_parser("remove-client", help="remove only files recorded by a Sherpa install")
    p.add_argument("--client", choices=(*CLIENTS, "all"), default="all")
    p.add_argument("--scope", choices=("global", "project"), default="global")
    p.add_argument("--project-dir", type=Path)
    p.add_argument("--destination", type=Path)
    p.add_argument("--yes", action="store_true")
    p.set_defaults(func=cmd_uninstall)


def selected(client: str) -> list[str]:
    if client == "auto":
        found = detect_clients()
        if not found:
            raise RuntimeError("No supported client CLI was detected. Select one explicitly with --client or install its CLI first.")
        return found
    return list(CLIENTS) if client == "all" else [client]


def cmd_install(args: argparse.Namespace) -> int:
    failures = 0
    try:
        clients = selected(args.client)
    except Exception as exc:
        print(f"INSTALL FAILED: {exc}", file=sys.stderr)
        return 1
    if args.destination and len(clients) > 1:
        print("--destination can be used with one --client at a time", file=sys.stderr)
        return 2
    if args.dry_run:
        for client in clients:
            try:
                base = args.destination.resolve() if args.destination else default_base(client, args.scope, args.project_dir)
                targets = [str(target) for _, target in mappings(client, base, args.scope, args.destination)]
                print(f"{client}: DRY RUN (no files were changed)")
                for target in targets:
                    print(f"  {target}")
            except Exception as exc:
                failures += 1
                print(f"{client}: DRY RUN FAILED: {exc}", file=sys.stderr)
        return 1 if failures else 0
    for client in clients:
        try:
            for result in install(client, args.scope, args.project_dir, args.destination):
                print(f"{client}: FILES_INSTALLED={result['FILES_INSTALLED']} SKILL_VALIDATED={result['SKILL_VALIDATED']} COMMANDS_INSTALLED={result['COMMANDS_INSTALLED']} RESOURCES_VALIDATED={result['RESOURCES_VALIDATED']}")
                print(f"{client}: CLIENT_DISCOVERY_VERIFIED={result['CLIENT_DISCOVERY_VERIFIED']}")
                print(f"{client}: RUNTIME_EXECUTION_VERIFIED={result['RUNTIME_EXECUTION_VERIFIED']}")
                print(f"Installed Sherpa {result['version']} at {result['base']}")
        except Exception as exc:
            failures += 1
            print(f"{client}: INSTALL FAILED: {exc}", file=sys.stderr)
    return 1 if failures else 0


def cmd_verify(args: argparse.Namespace) -> int:
    base = args.destination.resolve() if args.destination else default_base(args.client, args.scope, args.project_dir)
    result = verify_install(args.client, base, scope=args.scope, destination=args.destination)
    print(json.dumps(result, indent=2))
    return 1 if any(result[k] == "FAIL" for k in ("FILES_INSTALLED", "SKILL_VALIDATED", "COMMANDS_INSTALLED", "RESOURCES_VALIDATED")) else 0


def cmd_uninstall(args: argparse.Namespace) -> int:
    failures = 0
    for client in selected(args.client):
        try:
            result = uninstall(client, args.scope, args.project_dir, args.destination)
            print(f"{client}: " + ("\n  ".join(result) if result else "uninstalled"))
        except Exception as exc:
            failures += 1
            print(f"{client}: UNINSTALL FAILED: {exc}", file=sys.stderr)
    return 1 if failures else 0
