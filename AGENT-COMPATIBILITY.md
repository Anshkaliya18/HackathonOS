# Agent compatibility

Compatibility means integration files exist; runtime loading is a separate verification. The command manifest records status and evidence.

| Agent | Integration | Scope | Runtime status |
|---|---|---|---|
| Claude Code | `.claude-plugin/`, `.claude/skills/`, `skills/sherpa/` | npm installer or plugin | NOT VERIFIED |
| Codex CLI / Codex app | `.codex-plugin/`, `plugin.json`, `.agents/skills/` | shared skill directory or plugin | NOT VERIFIED |
| Gemini CLI | `gemini-extension.json`, `.agents/skills/` | shared skill directory or extension | NOT VERIFIED |
| Qwen Code | `qwen-extension.json`, `.agents/skills/` | shared skill directory or extension | NOT VERIFIED |
| OpenCode | `.opencode/commands/`, `.agents/skills/`, package metadata | npm installer or shared skill | NOT VERIFIED |
| Kilo Code | `kilo.jsonc`, `.kilo/`, `.agents/skills/` | shared skill directory | NOT VERIFIED |
| Generic | Manually load root `SKILL.md` if host supports instruction files | Host-dependent | Host-dependent |

## Installation check evidence

On 2026-11-04, the earlier v1.0.0 Windows package was installed with PowerShell into a temporary user profile using `-Both -NoCli -NoPath -Yes`. The installer reported successful validation, and both skill directories contained `SKILL.md` and a parseable command manifest. This historical result does not verify the Sherpa v2.0.0 package or runtime loading.

Sherpa packages one shared Agent Skill and native manifests for several hosts. The files establish packaging only, not discovery or workflow execution. See `commands/manifest.json` for separate runtime-check evidence. Do not infer runtime compatibility from the presence of Markdown command files or plugin manifests.

The generated installer targets Claude Code, OpenCode, Codex, and Kilo Code. It installs Agent Skills separately from native command files and reports filesystem checks separately from client discovery and execution. Gemini CLI and Qwen Code retain repository extension files but are not targets of the universal installer. See [the client compatibility matrix](CLIENT-COMPATIBILITY-MATRIX.md) for host-specific evidence and limits.
