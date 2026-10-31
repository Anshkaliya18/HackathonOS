# Kilo Code Adapter — Stage 1

Native project command directory: `.kilo/commands/`.

Entrypoints:

- `/hackathonos` — root intent router
- `/hackathonos-status`
- `/hackathonos-next`
- `/hackathonos-help`
- `/hackathonos-init`
- `/hackathonos-phase`

These Stage 1 aliases are retained. At the original Stage 2 routing implementation, CONFIG and CONFIG CHECK used the root `/hackathonos` entrypoint; the current hyphenated system also registers explicit config aliases from `commands/manifest.json`. The official workflow guide documents filename-derived command names but does not document argument substitution. The aliases do not require trailing arguments. Root `SKILL.md` is canonical; `core/commands/router.py` defines exact command resolution.

Official discovery convention: Kilo reads Markdown workflow commands from `.kilo/commands/`, with the filename used as the slash-command name ([official docs](https://kilo.ai/docs/customize/workflows)).

Hyphenated aliases are registered as `.kilo/commands/hackathonos-<action>.md`. No trailing-argument placeholder is assumed. Runtime attempt from an isolated temporary project: `kilo run --pure --command hackathonos-status` resolved the global adapter and read the global skill, manifest, router, and status workflow; the permission gate auto-rejected a read-only `Test-Path` call before a report was produced. Global command discovery and dispatch were observed for STATUS; completed runtime behavior is **NOT VERIFIED**. No auto-approval was enabled.

Stage 1 runtime discovery: **NOT VERIFIED**. The earlier inspection reported Kilo 7.8.8. A CLI session was opened, but its slash-command picker was not readable through the available terminal output; no command was invoked in that Stage 1 session.

Historical Stage 2 alias runtime: **BLOCKED**. In an isolated temporary project, the CLI recognized the then-existing separate Stage 2 aliases, but headless runs auto-rejected the Python command permission and interactive attempts did not return a report. Those aliases were removed when Stage 2 routing moved to the single `/hackathonos` entrypoint. Current root argument delivery for `config` and `config check` is **UNKNOWN** pending a live host invocation. No broad auto-approval was enabled. The CLI reported version 7.8.18 during the historical attempts.
