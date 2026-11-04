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

The project has PowerShell and Bash installer scripts, but the checked-in release manifest is a template and release artifacts/checksums are not published. Therefore public one-command installation is not live yet. Do not use the placeholder `YOUR-DOMAIN` commands. See [INSTALLATION.md](INSTALLATION.md) for accurate current options and release publishing steps.

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
