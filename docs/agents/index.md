# Agent compatibility

Before you set out, check the integration files and the host’s runtime behavior as separate evidence. Files in a repository do not prove the agent discovers or runs them.

| Agent | Repository integration files | Global installer | Runtime status |
|---|---|---:|---|
| Claude Code | `.claude/skills/` | Yes | NOT VERIFIED |
| OpenCode | `.opencode/commands/` and package metadata | Yes | NOT VERIFIED |
| Kilo Code | `.kilo/commands/` | No | NOT VERIFIED |
| Codex CLI | No verified native adapter | No | Not supported |
| Qwen Code | No verified native adapter | No | Not supported |
| Gemini CLI | No verified native adapter | No | Not supported |
| Generic host | Root `SKILL.md`, only when manually supported | No | Host-dependent |

The status values follow [`commands/manifest.json`](https://github.com/Anshkaliya18/Sherpa/blob/main/commands/manifest.json). The global installer targets Claude Code and OpenCode. Kilo files are repository-local. Do not infer runtime support from adapter files or installer success.

## Claude Code

Files are checked in under `.claude/skills/`, and the installer targets `~/.claude/skills/sherpa/`. After installation, open a project and try `/sherpa help` only if the host exposes the skill. Runtime discovery has not been verified.

## OpenCode

Command files and package metadata are checked in under `.opencode/`; the installer targets `~/.config/opencode/skills/sherpa/`. Runtime loading is not verified.

## Kilo Code

`.kilo/commands/` files are present, but no global installer is provided and runtime loading is not verified. Validate in a disposable project before relying on them.

## Other agents

No verified native adapter or installer target is provided for Codex CLI, Qwen Code, or Gemini CLI. A generic host may accept the root `SKILL.md`, but behavior depends on that host.

## Updating a compatibility claim

Record the host and version, install/source method, exact invocation, project context, observed output, and limitations. Add that evidence to the manifest before changing status. See [contributing](/contributing/) and [architecture](/architecture/).
