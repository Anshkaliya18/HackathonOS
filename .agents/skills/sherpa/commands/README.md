# Sherpa Native Command Layer

The authoritative registry for working and planned native commands is [`manifest.json`](manifest.json). The implemented command adapters are generated thin prompts mapped there. See [`docs/commands/README.md`](../docs/commands/README.md) for the full command list, workflow mappings, backward compatibility, and host verification state.

`SKILL.md` remains the canonical router. Native command entrypoints provide host-discovered invocations and pass an operation to that router. They do not duplicate phase logic.

## Core command set

The original master router remains available. Preferred hyphenated commands are registered separately for implemented workflows; see the manifest rather than inferring availability from this legacy syntax table.

| Canonical command | Operation passed to `SKILL.md` | Claude Code | Kilo Code | OpenCode |
|---|---|---|---|---|
| `/sherpa` | Default intent router | `/sherpa` | `/sherpa` | `/sherpa` |
| `/sherpa status` | STATUS | `/sherpa status` | `/sherpa-status` | `/sherpa status` |
| `/sherpa next` | NEXT | `/sherpa next` | `/sherpa-next` | `/sherpa next` |
| `/sherpa help` | HELP | `/sherpa help` | `/sherpa-help` | `/sherpa help` |
| `/sherpa init` | INIT | `/sherpa init` | `/sherpa-init` | `/sherpa init` |
| `/sherpa phase` | PHASE | `/sherpa phase` | `/sherpa-phase` | `/sherpa phase` |
| `/sherpa config` | CONFIG | `/sherpa config` | `/sherpa config` | `/sherpa config` |
| `/sherpa config check` | CONFIG CHECK | `/sherpa config check` | `/sherpa config check` | `/sherpa config check` |
| `/sherpa suggest [focus]` | SUGGEST | `/sherpa suggest [focus]` | `/sherpa suggest [focus]` | `/sherpa suggest [focus]` |

Stage 2 adds redacted configuration overview and validation operations through the single `/sherpa` entrypoint. `core/commands/router.py` resolves the complete normalized argument string, whether the host supplies only trailing text or the full invocation, with exact `config check` and `config` routes to `workflows/configuration.md`. Explicit configuration requests never fall back to STATUS. Kilo's docs do not specify argument substitution; a current root invocation did identify CONFIG and CONFIG CHECK, but each operation was stopped by Kilo's permission gate before a report. No nested command discovery is assumed. The Python standard-library utility is run only against the consuming project root. No application runtime or provider API is invoked.

Kilo's Stage 1 aliases remain available as before. At the original Stage 2 routing change, config operations used the root router without separate Kilo aliases. The current hyphenated command system now registers config aliases from `manifest.json`; runtime remains unverified as documented below. Repository integration files currently target exactly Claude Code, Kilo Code, and OpenCode; this is not a universal-agent-support claim.

Stage 3 adds idea-intelligence-only routing through the same root command. Optional focus text is forwarded as context; it does not create native subcommands. The workflow produces 10–20 problem territories and 15–25 candidates, calls the standard-library engine to validate evidence fields, calculate the internal (non-official) score, red-team each candidate, rank the Top 5/Top 3, detect duplicates, and persist immutable reports under `.sherpa/ideas/runs/`. Final selection remains pending human approval. No source generation, deployment, lifecycle update, or Phase 4 behavior is part of SUGGEST. Host runtime for SUGGEST has not yet been verified.

## Native discovery and verification status

| Platform | Native path | Runtime status | Evidence |
|---|---|---|---|
| Claude Code | `.claude/skills/sherpa/SKILL.md` | NOT VERIFIED | Earlier master-router invocations were user-confirmed, but this renamed distribution and its current command adapters have not been verified. |
| Kilo Code | `.kilo/commands/*.md` | NOT VERIFIED | Earlier root routing was observed, but operations stopped at the host permission gate; see runtime record. |
| OpenCode | `.opencode/commands/sherpa.md` | NOT VERIFIED | Historical discovery was observed; the current renamed command adapter has not completed a runtime invocation. |

## Adapter argument contracts

- **Claude Code:** registered through the skill name `sherpa`; its documented `$ARGUMENTS` placeholder forwards trailing input. After syncing the current repository skill, successful CONFIG, CONFIG CHECK, PHASE, and NEXT runtime output was confirmed in Claude Code; see `docs/configuration/runtime-verification.md`.
- **Kilo Code:** registered by `.kilo/commands/sherpa.md`; Stage 1 filename aliases remain. Kilo documents filename-derived command names but does not document a trailing-argument substitution token. Current `config` and `config check` root invocations reached the corresponding operations; required commands were auto-rejected by the permission gate before reports were produced.
- **OpenCode:** registered by `.opencode/commands/sherpa.md`; `$ARGUMENTS` forwards trailing input. The root command directs that input to the shared router. Runtime invocation did not complete in the recorded attempt.

Native adapter manifests remain prompt-based and do not embed shell execution or dependency installation. The SUGGEST workflow explicitly invokes the standard-library engine for context, validation, and persistence; its runtime is not inferred from static checks. Routing tests verify the resolver and adapter forwarding contract, not successful host execution.
