# Agent compatibility

Compatibility means integration files exist; runtime loading is a separate verification. The command manifest records status and evidence.

| Agent | Integration | Scope | Runtime status |
|---|---|---|---|
| Claude Code | `.claude/skills/` skill and command files | Repo; global installer supports `~/.claude/skills/hackathonos/` | Install verified; runtime check pending |
| OpenCode | `.opencode/commands/` and package metadata | Repo; global installer supports `~/.config/opencode/skills/hackathonos/` | Install verified; runtime check pending |
| Kilo Code | `.kilo/commands/` | Repository files only | NOT VERIFIED |
| Codex CLI | No verified native adapter | Not supported by installer | Not verified |
| Qwen Code | No verified native adapter | Not supported | Not verified |
| Gemini CLI | No verified native adapter | Not supported | Not verified |
| Generic | Manually load root `SKILL.md` if host supports instruction files | Host-dependent | Host-dependent |

## Installation check evidence

On 2026-11-04, the v1.0.0 Windows release was installed with the PowerShell installer into a newly created temporary user profile using `-Both -NoCli -NoPath -Yes` and the v1.0.0 release manifest URL. The installer reported successful validation. Both target directories contained `SKILL.md`; each `commands/manifest.json` parsed as JSON and each command directory contained one Markdown command file.

This verifies installation and basic file structure only. It does not verify that either agent loads the skill or dispatches its commands at runtime. See `commands/manifest.json` for the separate runtime-check evidence. Do not infer runtime compatibility from the presence of Markdown command files.
