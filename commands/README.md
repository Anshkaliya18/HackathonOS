# HackathonOS Native Command Layer

The authoritative registry for working and planned native commands is [`manifest.json`](manifest.json). The implemented command adapters are generated thin prompts mapped there. See [`docs/commands/README.md`](../docs/commands/README.md) for the full command list, workflow mappings, backward compatibility, and host verification state.

`SKILL.md` remains the canonical router. Native command entrypoints provide host-discovered invocations and pass an operation to that router. They do not duplicate phase logic.

## Core command set

The original master router remains available. Preferred hyphenated commands are registered separately for implemented workflows; see the manifest rather than inferring availability from this legacy syntax table.

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
| `/hackathonos suggest [focus]` | SUGGEST | `/hackathonos suggest [focus]` | `/hackathonos suggest [focus]` | `/hackathonos suggest [focus]` |

Stage 2 adds redacted configuration overview and validation operations through the single `/hackathonos` entrypoint. `core/commands/router.py` resolves the complete normalized argument string, whether the host supplies only trailing text or the full invocation, with exact `config check` and `config` routes to `workflows/configuration.md`. Explicit configuration requests never fall back to STATUS. Kilo's docs do not specify argument substitution; a current root invocation did identify CONFIG and CONFIG CHECK, but each operation was stopped by Kilo's permission gate before a report. No nested command discovery is assumed. The Python standard-library utility is run only against the consuming project root. No application runtime or provider API is invoked.

Kilo's Stage 1 aliases remain available as before. At the original Stage 2 routing change, config operations used the root router without separate Kilo aliases. The current hyphenated command system now registers config aliases from `manifest.json`; runtime remains unverified as documented below. The supported-platform list is exactly Claude Code, Kilo Code, and OpenCode; this is not a universal-agent-support claim.

Stage 3 adds idea-intelligence-only routing through the same root command. Optional focus text is forwarded as context; it does not create native subcommands. The workflow produces 10–20 problem territories and 15–25 candidates, calls the standard-library engine to validate evidence fields, calculate the internal (non-official) score, red-team each candidate, rank the Top 5/Top 3, detect duplicates, and persist immutable reports under `.hackathon/ideas/runs/`. Final selection remains pending human approval. No source generation, deployment, lifecycle update, or Phase 4 behavior is part of SUGGEST. Host runtime for SUGGEST has not yet been verified.

## Native discovery and verification status

| Platform | Native path | Runtime status | Evidence |
|---|---|---|---|
| Claude Code | `.claude/skills/hackathonos/SKILL.md` | STAGE 1/2 VERIFIED; STAGE 3 UNVERIFIED | After syncing the current repository skill to the active installation, the user confirmed successful `/hackathonos config`, `config check`, `phase`, and `next` runs. SUGGEST was added in Stage 3 and has not yet been invoked in a host. |
| Kilo Code | `.kilo/commands/*.md` | RUNTIME BLOCKED | Stage 2 aliases were recognized, but command permission was rejected or the interactive model stalled; see runtime record. |
| OpenCode | `.opencode/commands/hackathonos.md` | RUNTIME BLOCKED | Picker discovery was verified earlier; Stage 2 invocation stalled and the host bootstrapped local plugin dependencies; see runtime record. |

## Adapter argument contracts

- **Claude Code:** registered through the skill name `hackathonos`; its documented `$ARGUMENTS` placeholder forwards trailing input. After syncing the current repository skill, successful CONFIG, CONFIG CHECK, PHASE, and NEXT runtime output was confirmed in Claude Code; see `docs/configuration/runtime-verification.md`.
- **Kilo Code:** registered by `.kilo/commands/hackathonos.md`; Stage 1 filename aliases remain. Kilo documents filename-derived command names but does not document a trailing-argument substitution token. Current `config` and `config check` root invocations reached the corresponding operations; required commands were auto-rejected by the permission gate before reports were produced.
- **OpenCode:** registered by `.opencode/commands/hackathonos.md`; `$ARGUMENTS` forwards trailing input. The root command directs that input to the shared router. Runtime invocation did not complete in the recorded attempt.

Native adapter manifests remain prompt-based and do not embed shell execution or dependency installation. The SUGGEST workflow explicitly invokes the standard-library engine for context, validation, and persistence; its runtime is not inferred from static checks. Routing tests verify the resolver and adapter forwarding contract, not successful host execution.
