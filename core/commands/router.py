"""Deterministic command argument routing shared by HackathonOS adapters."""
from __future__ import annotations

from dataclasses import dataclass


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


def resolve(arguments: str) -> Route | None:
    """Resolve explicit command arguments or a full root-command invocation.

    None means no supported explicit operation. Empty arguments are left to the
    canonical SKILL.md intent router; unknown explicit commands stay unavailable.
    """
    normalized = " ".join(arguments.strip().lower().split())
    for command in ("/hackathonos", "\\hackathonos", "hackathonos"):
        if normalized == command:
            normalized = ""
            break
        if normalized.startswith(command + " "):
            normalized = normalized[len(command):].strip()
            break
    route = ROUTES.get(normalized)
    if route:
        return route
    if normalized.startswith("suggest "):
        return Route("SUGGEST", "workflows/idea-intelligence.md")
    return None
