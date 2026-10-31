#!/usr/bin/env python3
"""Behavioral checks for explicit root-command argument routing."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("hackathonos_command_router", ROOT / "core/commands/router.py")
router = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = router
SPEC.loader.exec_module(router)


def main() -> int:
    cases = {
        "config": ("CONFIG", "workflows/configuration.md"),
        "config check": ("CONFIG CHECK", "workflows/configuration.md"),
        "status": ("STATUS", "workflows/status.md"),
        "next": ("NEXT", "workflows/next.md"),
        "help": ("HELP", "SKILL.md#help"),
        "init": ("INIT", "workflows/init.md"),
        "phase": ("PHASE", "SKILL.md#phase"),
    }
    assert set(router.ROUTES) == set(cases), f"unexpected route (possible out-of-scope command): {set(router.ROUTES) ^ set(cases)}"
    for args, expected in cases.items():
        route = router.resolve(args)
        assert route is not None and (route.operation, route.workflow) == expected, (args, route)
    assert router.resolve("  CONFIG   CHECK ") == router.resolve("config check")
    for invocation in ("/hackathonos config", "\\hackathonos config", "hackathonos config"):
        assert router.resolve(invocation) == router.resolve("config"), invocation
    for invocation in ("/hackathonos config check", "\\hackathonos config check", "hackathonos config check"):
        assert router.resolve(invocation) == router.resolve("config check"), invocation
    assert router.resolve("/hackathonos") is None
    assert router.resolve("suggest") is None
    assert router.resolve("/hackathonos suggest") is None
    assert router.resolve("config status") is None
    assert router.resolve("") is None

    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    for route in router.ROUTES.values():
        if "#" in route.workflow:
            path, anchor = route.workflow.split("#", 1)
            body = (ROOT / path).read_text(encoding="utf-8-sig").replace("\r\n", "\n")
            assert f"\n## {anchor.upper()}\n" in "\n" + body, f"route target missing: {route.workflow}"
        else:
            assert (ROOT / route.workflow).is_file(), f"route workflow missing: {route.workflow}"
        assert f"**{route.operation}**" in skill_text, f"operation not listed in SKILL.md: {route.operation}"
    assert router.resolve("config next") is None

    adapters = {
        ROOT / ".claude/skills/hackathonos/SKILL.md": "$ARGUMENTS",
        ROOT / ".kilo/commands/hackathonos.md": "text following `/hackathonos`",
        ROOT / ".opencode/commands/hackathonos.md": "$ARGUMENTS",
    }
    for path, forwarding in adapters.items():
        text = path.read_text(encoding="utf-8-sig")
        assert forwarding in text, f"argument forwarding missing: {path}"
        assert "core/commands/router.py" in text, f"canonical router missing: {path}"
        assert "full invocation" in text, f"full command invocation handling missing: {path}"
        assert "never STATUS" in text, f"explicit operation fallback guard missing: {path}"
    print(f"PASS: {len(cases)} explicit routes, normalization, unknown handling, and 3 adapter forwarding contracts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())