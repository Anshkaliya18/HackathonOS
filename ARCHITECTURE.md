# Architecture

HackathonOS is a Markdown-first agent skill with a small Python core and a separate distribution CLI.

- `SKILL.md`, `commands/`, `workflows/`, `rules/`, and `templates/` define mentor behavior and artifacts.
- `core/commands/router.py`, `core/configuration/manager.py`, and `core/ideas/engine.py` implement routing, configuration, and idea evaluation.
- `src/` contains verification/configuration utilities; `scripts/` contains evaluation tools.
- `.claude/`, `.opencode/`, `.kilo/`, and `adapters/` hold agent integration material.
- `distribution/` contains shell/PowerShell installers, uninstallers, the stdlib CLI, and release metadata.
- `tests/` contains regression and installer checks.

Adapters are currently separate checked-in assets, not outputs of a shared schema. Only Claude Code and OpenCode are targeted by the global installer. Release archives should include only the consumable skill tree; see `RELEASE.md` and `SECURITY.md`.
