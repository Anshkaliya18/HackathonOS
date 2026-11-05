# Sherpa

**Build the right thing. Prove it works. Show why it matters.**

Sherpa is a globally installed AI agent skill that mentors hackathon teams across projects, from idea selection through verification, demo preparation, and submission.

[![MIT License](https://img.shields.io/badge/license-MIT-244d47.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/Anshkaliya18/Sherpa)](https://github.com/Anshkaliya18/Sherpa/releases)
[![Stars](https://img.shields.io/github/stars/Anshkaliya18/Sherpa)](https://github.com/Anshkaliya18/Sherpa/stargazers)
[![Claude Code · OpenCode](https://img.shields.io/badge/agent%20files-Claude%20Code%20%7C%20OpenCode-9a4f2e)](AGENT-COMPATIBILITY.md)

![sherpa](docs/public/sherpa.gif)

## Install once

After the first Sherpa release is published, install from its version-pinned release asset:

```bash
curl -fsSL https://github.com/Anshkaliya18/Sherpa/releases/download/v2.0.0/install.sh | bash
```

The same release contains `install.ps1` for Windows PowerShell. The npm package name is `sherpa-skill` (`sherpa` is already taken on npm); its first publication is still pending.

## Try it now

```text
/sherpa help
/sherpa suggest
/sherpa next
```

The host's runtime command loading has not been verified; see the [supported agents table](AGENT-COMPATIBILITY.md).

## How Sherpa guides the work

- **Evidence-led:** keep facts, assumptions, and unknowns distinct.
- **Human approval gates:** recommendations do not silently choose ideas or approve consequential work.
- **Project-local notes:** project context and generated records live in `.sherpa/`.
- **Plain compatibility status:** integration files, installer coverage, and runtime checks are tracked separately.

## Supported agents

| Agent | Integration files | Global installer | Runtime status |
|---|---|---:|---|
| Claude Code | `.claude/skills/` | Yes | NOT VERIFIED |
| OpenCode | `.opencode/commands/` and package metadata | Yes | NOT VERIFIED |
| Kilo Code | `.kilo/commands/` | No | NOT VERIFIED |
| Codex CLI, Qwen Code, Gemini CLI | No verified native adapter | No | Not supported |

Details and evidence: [agent compatibility](AGENT-COMPATIBILITY.md).

## Documentation

The [Sherpa field guide](https://anshkaliya18.github.io/Sherpa/) includes installation, a first-ascent tutorial, lifecycle guides, and a searchable command explorer.

Useful project references: [installation](INSTALLATION.md) · [commands](COMMANDS.md) · [workflows](WORKFLOWS.md) · [configuration](CONFIGURATION.md) · [architecture](ARCHITECTURE.md) · [security](SECURITY.md) · [migration](MIGRATION.md) · [contributing](CONTRIBUTING.md) · [changelog](CHANGELOG.md).

## Repository map

| Path | Purpose |
|---|---|
| `SKILL.md` | Mentoring behavior and routing |
| `commands/` | Command definitions and compatibility metadata |
| `core/`, `workflows/`, `rules/` | Shared logic, lifecycle guides, and safety rules |
| `templates/` | Reusable project artifacts |
| `adapters/`, `.claude/`, `.opencode/`, `.kilo/` | Agent integration files |
| `distribution/` | Installers, CLI, and release tooling |
| `docs/` | VitePress field guide |
| `tests/` | Command, workflow, regression, and installer checks |
