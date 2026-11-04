# Agent compatibility

Compatibility means integration files exist; runtime loading is a separate verification. The command manifest records status and evidence.

| Agent | Integration | Scope | Runtime status |
|---|---|---|---|
| Claude Code | `.claude/skills/` skill and command files | Repo; global installer supports `~/.claude/skills/hackathonos/` | NOT VERIFIED |
| OpenCode | `.opencode/commands/` and package metadata | Repo; global installer supports `~/.config/opencode/skills/hackathonos/` | NOT VERIFIED |
| Kilo Code | `.kilo/commands/` | Repository files only | NOT VERIFIED |
| Codex CLI | No verified native adapter | Not supported by installer | Not verified |
| Qwen Code | No verified native adapter | Not supported | Not verified |
| Gemini CLI | No verified native adapter | Not supported | Not verified |
| Generic | Manually load root `SKILL.md` if host supports instruction files | Host-dependent | Host-dependent |

Do not infer support from Markdown command files. Verify against current official agent documentation and with a runtime smoke test before advertising compatibility.
