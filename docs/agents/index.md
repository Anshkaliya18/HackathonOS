# Agent compatibility

Compatibility has two parts: files may be present, and the host may successfully discover and run them. The repository does not treat file presence as proof of runtime support.

| Agent | Repository integration files | Global installer | Runtime status in manifest |
|---|---|---|---|
| Claude Code | `.claude/skills/` | Yes | NOT VERIFIED |
| OpenCode | `.opencode/commands/` and package metadata | Yes | NOT VERIFIED |
| Kilo Code | `.kilo/commands/` | No | NOT VERIFIED |
| Codex CLI | No verified native adapter | No | Not verified / unsupported |
| Qwen Code | No verified native adapter | No | Not supported |
| Gemini CLI | No verified native adapter | No | Not supported |
| Generic host | Manually load `SKILL.md` if supported | No | Host-dependent |

The exact host evidence for Claude, OpenCode, and Kilo is in `commands/manifest.json`. Those entries currently record **NOT VERIFIED**.

## Claude Code

Integration files are checked in under `.claude/skills/`; the global installer targets `~/.claude/skills/hackathonos/`. Install using the [standard installer](/installation/), open a project repository, and try `/hackathonos help`. Runtime discovery has not been verified. If it does not appear, check the host's skill discovery rules and reload the agent.

## OpenCode

Command and package files are checked in under `.opencode/`; the global installer targets `~/.config/opencode/skills/hackathonos/`. Use the standard installer and try `/hackathonos help`. Runtime loading is not verified; consult the adapter README and host documentation if the command is not discovered.

## Kilo Code

`.kilo/commands/` files exist, but the global installer does not install them. Runtime loading is `NOT VERIFIED` in the manifest. Use repository-local files only if the host supports them, and validate in a disposable project before relying on the integration.

## Codex CLI, Qwen Code, and Gemini CLI

There is no verified native adapter or installer target for these agents. Do not assume a slash command will work. A generic host may use the root `SKILL.md` only when it supports manually supplied instruction files; behavior is host-dependent.

## Adapter developer notes

Keep adapter assets distinct, route only to commands in the shared manifest, preserve approval and evidence constraints, and record runtime smoke-test evidence before changing a compatibility claim. See [contributing](/contributing/) and [architecture](/architecture/).
