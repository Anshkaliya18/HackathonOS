# Kilo Code Adapter — Stage 1

Native project command directory: `.kilo/commands/`.

Entrypoints:

- `/hackathonos` — root intent router
- `/hackathonos-status`
- `/hackathonos-next`
- `/hackathonos-help`
- `/hackathonos-init`
- `/hackathonos-phase`

Aliases provide explicit commands because the current official workflow guide documents project-local `.kilo/commands/*.md` commands selected by filename but does not document argument substitution for `/hackathonos <operation>`. No argument-passing capability is claimed. Root `SKILL.md` is the canonical router.

Official discovery convention: Kilo reads Markdown workflow commands from `.kilo/commands/`, with the filename used as the slash-command name ([official docs](https://kilo.ai/docs/customize/workflows)).

Runtime discovery: **NOT VERIFIED**. Installed CLI reports Kilo 7.8.8. A CLI session was opened, but its slash-command picker was not readable through the available terminal output; no command was invoked and no project operation ran.
