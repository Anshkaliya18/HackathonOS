# Command reference

Commands are generated from [commands/manifest.json](https://github.com/Anshkaliya18/HackathonOS/blob/main/commands/manifest.json). Rebuild this page with `npm run docs:commands` after changing the manifest. Runtime support is recorded separately in that file; a registered command does not prove the agent host loads it.

## Syntax

The native command name is listed below. Legacy invocations use `/hackathonos <operation> [focus]`. For example:

```text
/hackathonos status
/hackathonos suggest focus on accessibility for campus teams
/hackathonos config check
```

There are no structured command flags for agent workflows. Optional natural-language context is passed as focus. Unknown explicit commands are unavailable. The host's actual invocation format depends on its adapter.

## Index

- CORE
- CONFIGURATION
- INTELLIGENCE
- ENGINEERING
- PRODUCT QUALITY
- FINALIZATION

| Native command | Description | Router key | Procedure |
|---|---|---|---|
| `hackathonos-status` | Show evidence-backed project status. | `status` | [workflows/status.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/status.md) |
| `hackathonos-next` | Identify the single highest-priority next action. | `next` | [workflows/next.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/next.md) |
| `hackathonos-help` | List implemented HackathonOS commands and limitations. | `help` | [SKILL.md#help](https://github.com/Anshkaliya18/HackathonOS/blob/main/SKILL.md#help) |
| `hackathonos-init` | Initialize project-local HackathonOS state safely. | `init` | [workflows/init.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/init.md) |
| `hackathonos-phase` | Show current lifecycle phase and evidence. | `phase` | [SKILL.md#phase](https://github.com/Anshkaliya18/HackathonOS/blob/main/SKILL.md#phase) |
| `hackathonos-config` | Show a redacted project configuration overview. | `config` | [workflows/configuration.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/configuration.md) |
| `hackathonos-config-check` | Validate project configuration and secret protections. | `config check` | [workflows/configuration.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/configuration.md) |
| `hackathonos-suggest` | Discover, evaluate, and red-team idea candidates; human selection required. | `suggest` | [workflows/idea-intelligence.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/idea-intelligence.md) |
| `hackathonos-evaluate` | Evaluate and compare candidate ideas with evidence. | `evaluate` | [workflows/idea-evaluation.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/idea-evaluation.md) |
| `hackathonos-compare` | Compare candidate ideas using the existing idea-evaluation workflow. | `compare` | [workflows/idea-evaluation.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/idea-evaluation.md) |
| `hackathonos-redteam` | Challenge project assumptions and readiness using the red-team workflow. | `redteam` | [workflows/red-team.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/red-team.md) |
| `hackathonos-optimize` | Prioritize score-improving work against evidence and criteria. | `optimize` | [workflows/score-optimization.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/score-optimization.md) |
| `hackathonos-judge-me` | Simulate judge perception using the judge-simulation workflow. | `judge-me` | [workflows/judge-simulation.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/judge-simulation.md) |
| `hackathonos-repo` | Inspect repository evidence as part of project planning. | `repo` | [workflows/project-planning.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/project-planning.md) |
| `hackathonos-architecture` | Plan architecture from the selected idea and repository evidence. | `architecture` | [workflows/project-planning.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/project-planning.md) |
| `hackathonos-techstack` | Assess technology choices within the project plan. | `techstack` | [workflows/project-planning.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/project-planning.md) |
| `hackathonos-plan` | Create an implementation-ready project plan. | `plan` | [workflows/project-planning.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/project-planning.md) |
| `hackathonos-build` | Execute an approved implementation task using the existing implementation workflow. | `build` | [workflows/implementation.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/implementation.md) |
| `hackathonos-verify` | Verify implementation through the existing testing and security workflow. | `verify` | [workflows/testing-security.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/testing-security.md) |
| `hackathonos-test` | Test implemented scope using the testing and security workflow. | `test` | [workflows/testing-security.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/testing-security.md) |
| `hackathonos-security` | Review security using the testing and security workflow. | `security` | [workflows/testing-security.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/testing-security.md) |
| `hackathonos-ux` | Review product usability and accessibility readiness. | `ux` | [workflows/ux-review.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/ux-review.md) |
| `hackathonos-accessibility` | Review accessibility within the existing UX-review scope. | `accessibility` | [workflows/ux-review.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/ux-review.md) |
| `hackathonos-demo` | Prepare an evidence-backed judge-oriented demo plan. | `demo` | [workflows/demo-preparation.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/demo-preparation.md) |
| `hackathonos-audit` | Run the existing final-audit workflow after its prerequisites are met. | `audit` | [workflows/final-audit.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/final-audit.md) |
| `hackathonos-submission` | Prepare and verify submission materials without submitting. | `submission` | [workflows/submission.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/submission.md) |
| `hackathonos-postmortem` | Run the final-phase evidence-based retrospective. | `postmortem` | [workflows/postmortem.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/postmortem.md) |
| `hackathonos-research` | Research competitors, markets, technologies, and evidence with verifiable sources. | `research` | [workflows/research.md](https://github.com/Anshkaliya18/HackathonOS/blob/main/workflows/research.md) |

## Distribution management CLI

This separate executable manages installed files; these are not agent workflows.

| Command | Arguments | Behavior |
|---|---|---|
| `hackathonos --version` | none | Prints installed CLI version. |
| `hackathonos update` | optional `--yes` / `-y` | Fetches a release and updates managed skill files after checksum verification. |
| `hackathonos uninstall` | optional `--yes` / `-y` | Removes recognized managed skill and CLI files; preserves project state. |
| `hackathonos doctor` | none | Reports runtime/install information and manifest reachability. |
| `hackathonos audit` | none | Reports debris, duplicates, empty directories, and file count in managed skill folders. |
| `hackathonos clean` | `--dry-run` by default; `--yes` to remove | Lists recognized generated debris; deletion requires confirmation and is scoped to managed skill folders. |
| `hackathonos help` | none | Prints CLI usage. |

Agent workflows return evidence-based reports or artifacts; they do not promise one fixed output schema. See [installation](/installation/) and [source command notes](https://github.com/Anshkaliya18/HackathonOS/blob/main/COMMANDS.md).
