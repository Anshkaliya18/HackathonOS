# Kilo Code Adapter — Stage 1

Native project command directory: `.kilo/commands/`.

Entrypoints:

- `/hackathonos` — root intent router
- `/hackathonos-status`
- `/hackathonos-next`
- `/hackathonos-help`
- `/hackathonos-init`
- `/hackathonos-phase`

These Stage 1 aliases are retained. Stage 2 CONFIG and CONFIG CHECK use the single `/hackathonos` root entrypoint and shared resolver; no separate Kilo config aliases or nested slash command discovery are assumed. The official workflow guide documents filename-derived command names but does not document argument substitution. The root prompt tells the model to use the trailing invocation text, but whether `/hackathonos config check` is delivered as trailing text is UNKNOWN until a host invocation verifies it. Root `SKILL.md` is canonical; `core/commands/router.py` defines exact argument resolution.

Official discovery convention: Kilo reads Markdown workflow commands from `.kilo/commands/`, with the filename used as the slash-command name ([official docs](https://kilo.ai/docs/customize/workflows)).

Stage 1 runtime discovery: **NOT VERIFIED**. The earlier inspection reported Kilo 7.8.8. A CLI session was opened, but its slash-command picker was not readable through the available terminal output; no command was invoked in that Stage 1 session.

Historical Stage 2 alias runtime: **BLOCKED**. In an isolated temporary project, the CLI recognized the then-existing separate Stage 2 aliases, but headless runs auto-rejected the Python command permission and interactive attempts did not return a report. Those aliases were removed when Stage 2 routing moved to the single `/hackathonos` entrypoint. Current root argument delivery for `config` and `config check` is **UNKNOWN** pending a live host invocation. No broad auto-approval was enabled. The CLI reported version 7.8.18 during the historical attempts.
