# Sherpa

**Build the right thing. Prove it works. Show why it matters.**

Sherpa is a portable Agent Skill and plugin for Claude Code, Codex, Gemini CLI, Qwen Code, OpenCode, and Kilo Code. It mentors hackathon projects from rules and idea selection through planning, implementation, testing, and submission.

```bash
npm install -g sherpa-skill
sherpa install
```

Then in your agent:
```text
/sherpa suggest
/sherpa plan
/sherpa demo
/sherpa submission
```

**What you get right away:**
- **One install:** works in Claude Code and OpenCode; project state lives in `.sherpa/` and survives restarts and context switches.
- **Evidence-led:** facts vs assumptions, with `UNKNOWN` when information is missing — no invented details.
- **Human approval gates:** Sherpa recommends, never silently picks an idea or writes code without you confirming.
- **Full lifecycle:** idea → plan → build → verify → demo → submission → postmortem.

[![npm version](https://img.shields.io/npm/v/sherpa-skill)](https://www.npmjs.com/package/sherpa-skill)
[![MIT License](https://img.shields.io/badge/license-MIT-244d47.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Anshkaliya18/sherpa)](https://github.com/Anshkaliya18/sherpa/stargazers)
[![Agent files: Claude · Codex · Gemini · Qwen · OpenCode · Kilo](https://img.shields.io/badge/agent%20files-Claude%20%7C%20Codex%20%7C%20Gemini%20%7C%20Qwen-9a4f2e)](AGENT-COMPATIBILITY.md)

![sherpa](docs/public/sherpa.gif)

## Install

The npm package is published as `sherpa-skill` (the name `sherpa` is already taken on npm).

### Option 1: npm (recommended)

```bash
npm install -g sherpa-skill
sherpa install
```

This installs the Sherpa skill for both Claude Code and OpenCode, plus the `sherpa` distribution CLI. To preview without writing files:

```bash
sherpa install --dry-run
```

To install only the skill (skip the CLI):

```bash
sherpa install --no-cli
```

To remove:

```bash
sherpa uninstall
```

The npm `sherpa` launcher supports `install`, `migrate`, and `uninstall`, and forwards `update`, `doctor`, `audit`, `clean`, `help`, and `--version` to the bundled management CLI. Management commands require Python 3.

Install with `--global` to call `sherpa` directly. For a local install, prefix commands with `npx sherpa-skill`, for example `npx sherpa-skill doctor`.

Node.js is required to run the npm package. `package.json` does not declare an `engines` field, so no specific Node version is pinned — use a current LTS release.

### Option 2: Other install methods (release installers)

The release installers download a versioned GitHub Releases archive, verify its SHA-256 checksum, and install the skill and CLI:

macOS / Linux:
```bash
curl -fsSL https://github.com/Anshkaliya18/sherpa/releases/latest/download/install.sh | bash
```

Windows PowerShell:
```powershell
irm https://github.com/Anshkaliya18/sherpa/releases/latest/download/install.ps1 | iex
```

Both installers target `~/.claude/skills/sherpa/` (Claude Code) and `~/.config/opencode/skills/sherpa/` (OpenCode) by default and never touch your project data or `.sherpa/` directories.

## See it in action

The following is an illustrative example, not a guaranteed transcript. It shows how a vague team idea becomes a scoped plan using real `/sherpa` operations.

**Before** — a vague team idea:
> "We should build something for campus accessibility. Maybe an app?"

**After** — walking the idea through Sherpa operations:

```text
/sherpa suggest ideas for campus accessibility
# -> Surfaces candidate ideas with pros/cons, risks, and judging-impact notes.
#    Human picks one; Sherpa never auto-selects.

/sherpa evaluate the chosen idea
# -> Compares candidates against evidence and criteria, then recommends.

/sherpa plan
# -> Writes an implementation-ready engineering plan to .sherpa/.
#    Architecture is not auto-approved and no code is written yet.

/sherpa demo
# -> Produces a judge-oriented demo preparation plan from validated evidence.

/sherpa submission
# -> Verifies and freezes submission materials without submitting.

/sherpa status
# -> Shows where you are, what's complete, what's broken, and the risks.
```

Each operation maps to a real workflow in `workflows/` (e.g. `idea-intelligence.md`, `project-planning.md`, `demo-preparation.md`, `submission.md`) and is registered in `commands/manifest.json`. Invoke as `/sherpa <operation> [focus]`.

## Supported agents

| Agent | Integration files | Global installer | Runtime status |
|---|---|---:|---|
| Claude Code | Claude plugin marketplace and Agent Skill | npm installer | NOT VERIFIED |
| Codex CLI / Codex app | Codex plugin manifest and Agent Skill | shared skill | NOT VERIFIED |
| Gemini CLI | Gemini extension and Agent Skill | shared skill | NOT VERIFIED |
| Qwen Code | Qwen extension and Agent Skill | shared skill | NOT VERIFIED |
| OpenCode | Agent Skill and legacy commands | npm installer | NOT VERIFIED |
| Kilo Code | Agent Skill and project commands | shared skill | NOT VERIFIED |

Details and evidence: [agent compatibility](AGENT-COMPATIBILITY.md).

Sherpa keeps one shared skill and packages host-specific manifests around it. These manifests establish install formats, not runtime support. Compatibility claims remain NOT VERIFIED until the current host discovers and runs Sherpa.

Install from Claude Code with `/plugin marketplace add Anshkaliya18/Sherpa` and `/plugin install sherpa@sherpa`. Gemini CLI and Qwen Code can install this repository with `gemini extensions install https://github.com/Anshkaliya18/Sherpa` and `qwen extensions install https://github.com/Anshkaliya18/Sherpa`. Codex, Gemini CLI, Qwen Code, Kilo Code, and OpenCode can also load `.agents/skills/sherpa/` through the shared Agent Skills directory. See the [agent guide](docs/agents/index.md) for Codex setup and verification limits.

Help us verify: install Sherpa on your agent, run `/sherpa status` and `/sherpa next`, and open an issue with your results.

## Why Sherpa

- **Evidence-led:** facts, assumptions, and unknowns are kept distinct; `UNKNOWN` is used when information is unavailable.
- **Human approval gates:** recommendations never silently choose ideas or approve consequential work — you confirm each step.
- **Project-local notes:** project context and generated records live in `.sherpa/` inside your repo, not in the skill directory.
- **Full lifecycle coverage:** idea selection → planning → implementation → testing/security → demo prep → submission → postmortem.

## Contributing / Community

- [Contributing guide](CONTRIBUTING.md) — pull requests welcome.
- Look for issues labeled **good first issue**.
- [Open an issue](https://github.com/Anshkaliya18/sherpa/issues) for bugs or verification reports.
- [GitHub Discussions](https://github.com/Anshkaliya18/sherpa/discussions) for questions and ideas.

## Documentation

Field guide: https://anshkaliya18.github.io/Sherpa/ · Project references: [installation](INSTALLATION.md) · [commands](COMMANDS.md) · [workflows](WORKFLOWS.md) · [configuration](CONFIGURATION.md) · [architecture](ARCHITECTURE.md) · [security](SECURITY.md) · [migration](MIGRATION.md) · [contributing](CONTRIBUTING.md) · [changelog](CHANGELOG.md).
