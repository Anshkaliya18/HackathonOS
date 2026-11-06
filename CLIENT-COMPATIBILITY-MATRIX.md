# Sherpa Client Compatibility Matrix

**Build:** 2.0.8 generated distribution  
**Evidence date:** 2026-11-07  
**Scope:** Windows host; compatibility statements are capability-specific.

| Client | Skill format and install target | Native command capability | Evidence | Status / limit |
|---|---|---|---|---|
| Claude Code | Agent Skill folders in `~/.claude/skills` or project `.claude/skills` | Skills can be invoked by name; generated Sherpa operation skills are skill entries, not separately registered slash-command files | Official [skills docs](https://code.claude.com/docs/en/skills); Windows project install and structural verification passed | Files and metadata verified. Interactive discovery/invocation not tested. |
| OpenCode | Agent Skills in `.opencode/skills` / global config skill location | Native custom slash commands in `.opencode/commands`; generated commands use `$ARGUMENTS` | Official [skills docs](https://opencode.ai/docs/skills/) and [commands docs](https://opencode.ai/docs/commands/); `opencode debug skill --pure` found installed project skill | Discovery passed on installed Windows CLI. Command execution/picker was not tested. |
| Codex CLI | Agent Skills in `~/.agents/skills` or project `.agents/skills` | This distribution does not register native slash commands; use skill discovery/invocation | Official [Codex skills docs](https://developers.openai.com/codex/skills); `codex debug prompt-input` on an isolated project included Sherpa | Skill discovery passed through CLI prompt-input inspection; model invocation not tested. |
| Kilo Code | Agent Skills under `.agents/skills`; Kilo-specific workflow commands under `.kilo/commands` or `~/.config/kilo/commands` | Native Markdown workflows; generated files avoid undocumented argument interpolation | Official [Kilo skills docs](https://kilo.ai/docs/customize/skills) and [workflow docs](https://kilo.ai/docs/customize/workflows); `kilo debug skill --pure` found installed project skill during test | Skill discovery passed in a Windows CLI run, but Windows cleanup was blocked by a lingering project-directory handle. Automated test skips this host. Native workflow execution not tested. |

## Cross-platform evidence

| Environment | Evidence |
|---|---|
| Windows / PowerShell | `install.ps1 -Codex -ProjectDir ... -NoCli -Yes` completed; installed files/resources validated; CLI discovery and runtime explicitly reported `NOT RUN`. PowerShell parser validation passed. |
| Windows / Git Bash | `bash -n distribution/install.sh` passed. A local project install into a path with spaces installed Codex files and passed structural/resource checks. |
| Linux | Not run in this environment. Linux destinations and shell behavior are covered by code paths and official client conventions, not claimed as runtime-tested. |

“Files and metadata verified” means filesystem and resource validation only. It does not assert the client loaded the skill. The installation engine reports these states separately.
