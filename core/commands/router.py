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
}


def resolve(arguments: str) -> Route | None:
    """Resolve explicit command arguments, preferring the longest exact route.

    None means no supported explicit operation. Empty arguments are left to the
    canonical SKILL.md intent router; unknown explicit commands stay unavailable.
    """
    normalized = " ".join(arguments.strip().lower().split())
    return ROUTES.get(normalized)
