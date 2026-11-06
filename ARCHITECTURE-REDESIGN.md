# Sherpa 2.x Distribution Architecture

## Canonical source

Authored product content has one source: repository-root `SKILL.md`, `commands/manifest.json`, and the root `commands/`, `core/`, `workflows/`, `rules/`, `templates/`, `src/`, and selected reference documentation. The directory `distribution/generated/` is build output and must never be edited directly. Run `python scripts/build-distributions.py` to regenerate it or `python scripts/build-distributions.py --check` to compare it with the canonical sources.

The build stores one shared resource tree at `distribution/generated/shared/sherpa/`. Native entrypoints are emitted separately under `distribution/generated/clients/<client>/`. Command metadata distinguishes the shared workflow capability, Agent Skill entries, and native slash-command files. Codex has skills and no generated slash commands. Kilo commands do not depend on trailing argument substitution because its official workflow documentation does not specify such a placeholder.

## Runtime resource resolution

The canonical skill and its resources are installed together as a single `sherpa/` directory under a client’s skills root. Every workflow, rule, template, Python helper, and command manifest reference is relative to that directory. Command skills refer to the sibling `../sherpa/` skill bundle. Native command prompts identify the canonical skill by its installed Agent Skill name and never assume that Sherpa files are at the consuming repository root or that the current working directory is the Sherpa checkout.

Missing workflows or explicitly registered resources fail validation with their expected installed path. The installer does not substitute generic content for missing resources.

## Client adapters

| Client | Skills | Native commands | Global roots | Project roots |
|---|---|---|---|---|
| Claude Code | Agent Skills, one skill per registered operation | Skill names are directly invocable as `/sherpa-*` | `~/.claude/skills/` | `.claude/skills/` |
| OpenCode | Agent Skills | `.md` command files using documented `$ARGUMENTS` | `~/.config/opencode/skills/`, `~/.config/opencode/commands/` | `.opencode/skills/`, `.opencode/commands/` |
| Codex | Agent Skills | Not claimed; no native slash command emitted | `~/.agents/skills/` | `.agents/skills/` |
| Kilo Code | Agent Skills | `.kilo/commands/*.md` workflows | `~/.agents/skills/`, `~/.config/kilo/commands/` | `.agents/skills/`, `.kilo/commands/` |

Official references: [Claude Code skills](https://code.claude.com/docs/en/skills), [OpenCode skills](https://opencode.ai/docs/skills/), [OpenCode commands](https://opencode.ai/docs/commands/), [Codex skills](https://developers.openai.com/codex/skills), [Kilo skills](https://kilo.ai/docs/customize/skills), and [Kilo workflows](https://kilo.ai/docs/customize/workflows). These establish format and path conventions; they do not establish runtime success for a specific Sherpa release.

## Installation model

The Python standard-library installer consumes generated output, copies the complete skill tree and native entrypoints into the selected client root, validates metadata/resources/command counts, and records the exact managed paths in `.sherpa-install.json`. Updates replace a prior managed target transactionally and restore backups if any copy or post-install validation fails. Uninstall removes only paths recorded by that marker. `--destination` chooses a custom client config root; `--scope project --project-dir <path>` uses that project’s native roots.

Installation states are separate: `FILES_INSTALLED`, `SKILL_VALIDATED`, `COMMANDS_INSTALLED`, and `RESOURCES_VALIDATED` are filesystem checks. `CLIENT_DISCOVERY_VERIFIED` and `RUNTIME_EXECUTION_VERIFIED` remain `NOT RUN` until a real client test proves them. A successful file installation is not represented as client runtime success.

The npm entrypoint invokes the generated installer from the package root. Standalone install scripts retain the release-download and checksum workflow; release archives must include `distribution/generated/` and `distribution/cli/installer.py` for the native installer path to be available.

## Build and release

`scripts/build-distributions.py` validates the manifest’s workflow references, generates the shared resource bundle and client adapters in a staging directory, writes stable metadata/source digests, and replaces only `distribution/generated/`. `npm pack` runs this deterministic build. The release builder includes generated distributions and normalizes archive timestamps/ownership. Release publication still requires release-level artifact and real-client acceptance checks; this architecture change does not publish a release.

## Compatibility limits

- Kilo’s documented workflow format does not specify a trailing-argument substitution token; generated workflows do not rely on one.
- Codex receives Agent Skills, not Sherpa-native slash commands.
- Installer filesystem validation cannot establish client picker visibility or model execution.
- Claude skills may be invoked as slash commands by the host, but actual runtime compatibility still depends on Claude Code version, settings, workspace trust, and model configuration.
- Existing legacy plugin/extension manifests are not proof that those clients are installed or validated by the universal installer.
