# OpenCode Adapter — Stage 1

Native project command: `.opencode/commands/hackathonos.md`, invoked as `/hackathonos`. The documented `$ARGUMENTS` placeholder passes forms such as `/hackathonos status` to the canonical router in root `SKILL.md`.

Official discovery convention: project command Markdown files live under `.opencode/commands/`; the filename defines the command name and `$ARGUMENTS` receives trailing user input ([official docs](https://opencode.ai/docs/commands)).

Runtime discovery: **VERIFIED** in OpenCode 1.19.4. The interactive slash picker displayed `/hackathonos` and its command description. The command was not selected or invoked; no model request, MCP authentication, or project operation occurred.
