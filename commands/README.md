# HackathonOS Native Command Layer — Stage 1

`SKILL.md` remains the canonical router. Native command entrypoints provide host-discovered invocations and pass an operation to that router. They do not duplicate phase logic.

## Core command set

| Canonical command | Operation passed to `SKILL.md` | Claude Code | Kilo Code | OpenCode |
|---|---|---|---|---|
| `/hackathonos` | Default intent router | `/hackathonos` | `/hackathonos` | `/hackathonos` |
| `/hackathonos status` | STATUS | `/hackathonos status` | `/hackathonos-status` | `/hackathonos status` |
| `/hackathonos next` | NEXT | `/hackathonos next` | `/hackathonos-next` | `/hackathonos next` |
| `/hackathonos help` | HELP | `/hackathonos help` | `/hackathonos-help` | `/hackathonos help` |
| `/hackathonos init` | INIT | `/hackathonos init` | `/hackathonos-init` | `/hackathonos init` |
| `/hackathonos phase` | PHASE | `/hackathonos phase` | `/hackathonos-phase` | `/hackathonos phase` |

Kilo aliases are used because its official workflow contract documents filename-based commands but not argument substitution for one command. The supported-platform list is exactly Claude Code, Kilo Code, and OpenCode; this is not a universal-agent-support claim.

## Native discovery and verification status

| Platform | Native path | Runtime status | Evidence |
|---|---|---|---|
| Claude Code | `.claude/skills/hackathonos/SKILL.md` | NOT VERIFIED | CLI 2.1.316 displayed workspace trust gate; it was declined before command discovery. |
| Kilo Code | `.kilo/commands/*.md` | NOT VERIFIED | CLI 7.8.8 available; terminal picker output was not readable. |
| OpenCode | `.opencode/commands/hackathonos.md` | VERIFIED | CLI 1.19.4 slash picker displayed `/hackathonos`; command not invoked. |

All entrypoints are prompt-only and do not execute shell commands, install packages, perform network operations, or autonomously mutate a project. Static manifest checks are separate from runtime discovery.
