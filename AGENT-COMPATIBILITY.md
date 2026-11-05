# Agent compatibility

Compatibility means integration files exist; runtime loading is a separate verification. The command manifest records status and evidence.

| Agent | Integration | Scope | Runtime status |
|---|---|---|---|
| Claude Code | `.claude/skills/` skill and command files | Repo; global installer targets `~/.claude/skills/sherpa/` | NOT VERIFIED |
| OpenCode | `.opencode/commands/` and package metadata | Repo; global installer targets `~/.config/opencode/skills/sherpa/` | NOT VERIFIED |
| Kilo Code | `kilo.jsonc`, `.kilo/rules/`, `.kilo/commands/` | Repository project configuration | NOT VERIFIED |
| Codex CLI | No verified native adapter | Not supported by installer | Not verified |
| Qwen Code | No verified native adapter | Not supported | Not verified |
| Gemini CLI | No verified native adapter | Not supported | Not verified |
| Generic | Manually load root `SKILL.md` if host supports instruction files | Host-dependent | Host-dependent |

## Installation check evidence

On 2026-11-04, the earlier v1.0.0 Windows package was installed with PowerShell into a temporary user profile using `-Both -NoCli -NoPath -Yes`. The installer reported successful validation, and both skill directories contained `SKILL.md` and a parseable command manifest. This historical result does not verify the Sherpa v2.0.0 package or runtime loading.

This verifies installation and basic file structure only. It does not verify that either agent loads the skill or dispatches its commands at runtime. See `commands/manifest.json` for the separate runtime-check evidence. Do not infer runtime compatibility from the presence of Markdown command files.
