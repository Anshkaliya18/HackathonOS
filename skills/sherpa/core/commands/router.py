"""Deterministic command argument routing shared by sherpa adapters."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re


@dataclass(frozen=True)
class Route:
    operation: str
    workflow: str


ROUTES = {
    "status": Route("STATUS", "workflows/status.md"),
    "next": Route("NEXT", "workflows/next.md"),
    "help": Route("HELP", "SKILL.md#help"),
    "init": Route("INIT", "workflows/init.md"),
    "phase": Route("PHASE", "SKILL.md#phase"),
    "config": Route("CONFIG", "workflows/configuration.md"),
    "config check": Route("CONFIG CHECK", "workflows/configuration.md"),
    "suggest": Route("SUGGEST", "workflows/idea-intelligence.md"),
}

MANIFEST_PATH = Path(__file__).resolve().parents[2] / "commands" / "manifest.json"
_MANIFEST = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
_ROOT = MANIFEST_PATH.parent.parent


def validate_manifest(manifest: dict, root: Path = _ROOT, check_adapter_files: bool = True) -> list[str]:
    """Validate command identity, route targets, adapter coverage and collisions."""
    errors: list[str] = []
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        return ["unsupported or malformed manifest"]
    if manifest.get("master_command") != "/sherpa":
        errors.append("master command must remain /sherpa")
    if not isinstance(manifest.get("implemented"), list) or not isinstance(manifest.get("planned"), list):
        return errors + ["implemented and planned must be lists"]
    required_adapters = {"claude", "opencode", "kilo"}
    group_values = manifest.get("groups")
    groups = set(group_values) if isinstance(group_values, list) else set()
    if not groups or len(groups) != len(group_values):
        errors.append("groups must be a non-empty unique list")
    commands: set[str] = set()
    router_keys: set[str] = set()
    aliases: set[str] = set()
    for index, item in enumerate(manifest["implemented"]):
        label = f"implemented[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object")
            continue
        command = item.get("command")
        if not isinstance(command, str) or not re.fullmatch(r"sherpa-[a-z0-9]+(?:-[a-z0-9]+)*", command):
            errors.append(f"{label} has an invalid canonical command name")
        elif command in commands:
            errors.append(f"duplicate canonical command: {command}")
        else:
            commands.add(command)
        if item.get("group") not in groups:
            errors.append(f"{label} has an invalid group")
        if item.get("status") != "implemented":
            errors.append(f"{label} must have implemented status")
        operation, key, workflow = item.get("operation"), item.get("router_key"), item.get("workflow")
        if not all(isinstance(value, str) and value for value in (operation, key, workflow)):
            errors.append(f"{label} is missing operation, router_key, or workflow")
        elif key in router_keys:
            errors.append(f"duplicate router key: {key}")
        else:
            router_keys.add(key)
        if isinstance(workflow, str) and workflow:
            target, _, anchor = workflow.partition("#")
            resolved = (root / target).resolve()
            if root.resolve() not in resolved.parents and resolved != root.resolve():
                errors.append(f"workflow escapes repository root: {workflow}")
            elif not resolved.is_file():
                errors.append(f"missing workflow: {workflow}")
            elif anchor and not re.search(rf"^##\s+{re.escape(anchor)}\s*$", resolved.read_text(encoding="utf-8-sig"), re.M | re.I):
                errors.append(f"missing workflow anchor: {workflow}")
        adapter_list = item.get("adapters")
        if not isinstance(adapter_list, list) or set(adapter_list) != required_adapters:
            errors.append(f"{label} must register all three host adapters")
        elif check_adapter_files:
            paths = {
                "claude": root / ".claude" / "skills" / str(command) / "SKILL.md",
                "opencode": root / ".opencode" / "commands" / f"{command}.md",
                "kilo": root / ".kilo" / "commands" / f"{command}.md",
            }
            for host, path in paths.items():
                if not path.is_file():
                    errors.append(f"missing {host} adapter: {command}")
        item_aliases = item.get("legacy_aliases")
        if not isinstance(item_aliases, list):
            errors.append(f"{label} legacy_aliases must be a list")
        else:
            for alias in item_aliases:
                if not isinstance(alias, str) or not alias.strip():
                    errors.append(f"{label} has an invalid legacy alias")
                elif alias.casefold() in aliases:
                    errors.append(f"duplicate command alias: {alias}")
                elif command and alias.casefold() == f"/{command}".casefold():
                    errors.append(f"native command collides with legacy alias: {alias}")
                else:
                    aliases.add(alias.casefold())
    planned_names: set[str] = set()
    for index, item in enumerate(manifest["planned"]):
        if not isinstance(item, dict):
            errors.append(f"planned[{index}] must be an object")
            continue
        command = item.get("command")
        if not isinstance(command, str) or not re.fullmatch(r"sherpa-[a-z0-9]+(?:-[a-z0-9]+)*", command):
            errors.append(f"planned[{index}] has an invalid canonical command name")
        elif command in planned_names or command in commands:
            errors.append(f"duplicate or colliding planned command: {command}")
        else:
            planned_names.add(command)
        if item.get("status") != "planned":
            errors.append(f"planned[{index}] must remain planned")
    statuses = manifest.get("host_runtime_status", {})
    if not isinstance(statuses, dict) or set(statuses) != required_adapters:
        errors.append("host runtime status must cover Claude Code, OpenCode, and Kilo")
    else:
        for host, record in statuses.items():
            if not isinstance(record, dict) or record.get("status") not in {"PASS", "FAIL", "UNKNOWN", "NOT VERIFIED"}:
                errors.append(f"invalid runtime status for {host}")
    return errors


# Host adapter files live beside the framework in the source repository, but
# in host-specific global directories after installation. Validate their names
# in every bundle; repository regression checks verify the physical files.
_MANIFEST_ERRORS = validate_manifest(_MANIFEST, check_adapter_files=False)
if _MANIFEST_ERRORS:
    raise ValueError("Invalid sherpa command manifest: " + "; ".join(_MANIFEST_ERRORS))

_NATIVE_ROUTES = {
    item["command"]: Route(item["operation"], item["workflow"])
    for item in _MANIFEST["implemented"]
}
_LEGACY_ROUTES = {
    item["router_key"]: Route(item["operation"], item["workflow"])
    for item in _MANIFEST["implemented"]
}


def resolve(arguments: str) -> Route | None:
    """Resolve explicit command arguments or a full root-command invocation.

    None means no supported explicit operation. Empty arguments are left to the
    canonical SKILL.md intent router; unknown explicit commands stay unavailable.
    """
    normalized = " ".join(arguments.strip().lower().split())
    for command in ("/sherpa", "\\sherpa", "sherpa"):
        if normalized == command:
            normalized = ""
            break
        if normalized.startswith(command + " "):
            normalized = normalized[len(command):].strip()
            break
    normalized = normalized.lstrip("/")
    native_name = normalized.partition(" ")[0]
    route = _NATIVE_ROUTES.get(native_name)
    if route:
        return route
    route = _LEGACY_ROUTES.get(normalized) or ROUTES.get(normalized)
    if route:
        return route
    if normalized.startswith("suggest "):
        return Route("SUGGEST", "workflows/idea-intelligence.md")
    return None
