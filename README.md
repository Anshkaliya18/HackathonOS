# HackathonOS

HackathonOS is a Markdown-first AI hackathon mentor skill. It helps teams move from idea selection through implementation, verification, demo preparation, and submission readiness while grounding advice in project evidence and preserving human approval gates.

## Capabilities

- Idea discovery, evaluation, comparison, and red-team review.
- Project planning, implementation guidance, status, and next-action workflows.
- Configuration and secret checks, testing/security reviews, demo and submission preparation.
- Markdown templates, reusable rules, Python routing/configuration/evaluation utilities.
- Distribution CLI for version, updates, uninstall, diagnostics, and output audit.

## Agent support

Integration files exist for Claude Code, OpenCode, and Kilo Code. The global installer currently targets Claude Code and OpenCode. Runtime loading is marked **NOT VERIFIED** in `commands/manifest.json`; Codex CLI, Qwen Code, and Gemini CLI have no verified adapter. See [AGENT-COMPATIBILITY.md](AGENT-COMPATIBILITY.md).

## Install status

Install the latest published release from PowerShell:

```powershell
irm https://raw.githubusercontent.com/Anshkaliya18/HackathonOS/main/distribution/install.ps1 | iex
```

Or from Linux/macOS:

```bash
curl -fsSL https://raw.githubusercontent.com/Anshkaliya18/HackathonOS/main/distribution/install.sh | bash
```

These install the Claude Code and OpenCode integrations. Runtime loading is not yet verified; see [AGENT-COMPATIBILITY.md](AGENT-COMPATIBILITY.md).

## Quick use from this repository

Open the repo in an agent that can load its skill files, then invoke:

```text
/hackathonos help
/hackathonos status
/hackathonos suggest
```

CLI management examples (after a valid release install):

```text
hackathonos --version
hackathonos doctor
hackathonos audit
hackathonos clean --dry-run
```

## Project structure

```text
SKILL.md             Canonical behavior and routing guidance
commands/            Command manifest and command definitions
core/                Router, configuration manager, idea engine
workflows/ rules/    Lifecycle workflows and shared safety rules
templates/           Project artifacts and configuration examples
adapters/ .claude/ .opencode/ .kilo/  Agent integrations
distribution/        Installers, CLI, release metadata
tests/               Regression and installer tests
```

## Documentation

- [Quickstart](QUICKSTART.md) · [Installation](INSTALLATION.md) · [Configuration](CONFIGURATION.md)
- [Agent compatibility](AGENT-COMPATIBILITY.md) · [Commands](COMMANDS.md) · [Workflows](WORKFLOWS.md)
- [Architecture](ARCHITECTURE.md) · [Troubleshooting](TROUBLESHOOTING.md) · [Contributing](CONTRIBUTING.md)
- [Release process](RELEASE.md) · [Security](SECURITY.md) · [Changelog](CHANGELOG.md)

No license file is present; no license is inferred here.
