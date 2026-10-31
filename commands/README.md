# HackathonOS Native Command Layer — Stage 1 and Stage 2

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
| `/hackathonos config` | CONFIG | `/hackathonos config` | `/hackathonos config` | `/hackathonos config` |
| `/hackathonos config check` | CONFIG CHECK | `/hackathonos config check` | `/hackathonos config check` | `/hackathonos config check` |

Stage 2 adds redacted configuration overview and validation operations through the single `/hackathonos` entrypoint. `core/commands/router.py` resolves the complete normalized trailing argument string, with exact `config check` and `config` routes to `workflows/configuration.md`. The adapters forward trailing text to the canonical router; Kilo's documented workflow format is filename-based and does not specify argument substitution, so its root command's argument delivery still requires host runtime verification. No nested command discovery is assumed. The Python standard-library utility is run only against the consuming project root. No application runtime or provider API is invoked.

Kilo's Stage 1 aliases remain available as before. Stage 2 does not add separate Kilo config aliases; config operations are dispatched by the root router. The supported-platform list is exactly Claude Code, Kilo Code, and OpenCode; this is not a universal-agent-support claim.

## Native discovery and verification status

| Platform | Native path | Runtime status | Evidence |
|---|---|---|---|
| Claude Code | `.claude/skills/hackathonos/SKILL.md` | RUNTIME BLOCKED | Stage 2 command attempt returned model/provider errors; see `docs/configuration/runtime-verification.md`. |
| Kilo Code | `.kilo/commands/*.md` | RUNTIME BLOCKED | Stage 2 aliases were recognized, but command permission was rejected or the interactive model stalled; see runtime record. |
| OpenCode | `.opencode/commands/hackathonos.md` | RUNTIME BLOCKED | Picker discovery was verified earlier; Stage 2 invocation stalled and the host bootstrapped local plugin dependencies; see runtime record. |

## Adapter argument contracts

- **Claude Code:** registered through the skill name `hackathonos`; its documented `$ARGUMENTS` placeholder forwards trailing input. The root skill directs explicit operations to the shared router. Runtime config invocation has not succeeded in the recorded attempt.
- **Kilo Code:** registered by `.kilo/commands/hackathonos.md`; Stage 1 filename aliases remain. Kilo documents filename-derived command names but does not document a trailing-argument substitution token. The root command instructs routing the supplied text through the shared router, but delivery of `/hackathonos config check` remains unverified at runtime.
- **OpenCode:** registered by `.opencode/commands/hackathonos.md`; `$ARGUMENTS` forwards trailing input. The root command directs that input to the shared router. Runtime invocation did not complete in the recorded attempt.

All entrypoints are prompt-only and do not execute shell commands, install packages, perform network operations, or autonomously mutate a project. Static routing tests verify the shared resolver and adapter forwarding contract; they do not establish host runtime success.
