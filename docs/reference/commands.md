# Command reference

Commands are generated from [commands/manifest.json](https://github.com/Anshkaliya18/sherpa/blob/main/commands/manifest.json). Rebuild this page with `npm run docs:commands` after changing the manifest. Runtime support is recorded separately in that file; a registered command does not prove the agent host loads it.

## Syntax

The native command name is listed below. Legacy invocations use `/sherpa <operation> [focus]`. For example:

```text
/sherpa status
/sherpa suggest focus on accessibility for campus teams
/sherpa config check
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
| `sherpa-status` | Show evidence-backed project status. | `status` | [workflows/status.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/status.md) |
| `sherpa-next` | Identify the single highest-priority next action. | `next` | [workflows/next.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/next.md) |
| `sherpa-help` | List implemented sherpa commands and limitations. | `help` | [SKILL.md#help](https://github.com/Anshkaliya18/sherpa/blob/main/SKILL.md#help) |
| `sherpa-init` | Initialize project-local sherpa state safely. | `init` | [workflows/init.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/init.md) |
| `sherpa-phase` | Show current lifecycle phase and evidence. | `phase` | [SKILL.md#phase](https://github.com/Anshkaliya18/sherpa/blob/main/SKILL.md#phase) |
| `sherpa-config` | Show a redacted project configuration overview. | `config` | [workflows/configuration.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/configuration.md) |
| `sherpa-config-check` | Validate project configuration and secret protections. | `config check` | [workflows/configuration.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/configuration.md) |
| `sherpa-suggest` | Discover, evaluate, and red-team idea candidates; human selection required. | `suggest` | [workflows/idea-intelligence.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/idea-intelligence.md) |
| `sherpa-evaluate` | Evaluate and compare candidate ideas with evidence. | `evaluate` | [workflows/idea-evaluation.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/idea-evaluation.md) |
| `sherpa-compare` | Compare candidate ideas using the existing idea-evaluation workflow. | `compare` | [workflows/idea-evaluation.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/idea-evaluation.md) |
| `sherpa-redteam` | Challenge project assumptions and readiness using the red-team workflow. | `redteam` | [workflows/red-team.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/red-team.md) |
| `sherpa-optimize` | Prioritize score-improving work against evidence and criteria. | `optimize` | [workflows/score-optimization.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/score-optimization.md) |
| `sherpa-judge-me` | Simulate judge perception using the judge-simulation workflow. | `judge-me` | [workflows/judge-simulation.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/judge-simulation.md) |
| `sherpa-repo` | Inspect repository evidence as part of project planning. | `repo` | [workflows/project-planning.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/project-planning.md) |
| `sherpa-architecture` | Plan architecture from the selected idea and repository evidence. | `architecture` | [workflows/project-planning.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/project-planning.md) |
| `sherpa-techstack` | Assess technology choices within the project plan. | `techstack` | [workflows/project-planning.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/project-planning.md) |
| `sherpa-plan` | Create an implementation-ready project plan. | `plan` | [workflows/project-planning.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/project-planning.md) |
| `sherpa-build` | Execute an approved implementation task using the existing implementation workflow. | `build` | [workflows/implementation.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/implementation.md) |
| `sherpa-verify` | Verify implementation through the existing testing and security workflow. | `verify` | [workflows/testing-security.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/testing-security.md) |
| `sherpa-test` | Test implemented scope using the testing and security workflow. | `test` | [workflows/testing-security.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/testing-security.md) |
| `sherpa-security` | Review security using the testing and security workflow. | `security` | [workflows/testing-security.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/testing-security.md) |
| `sherpa-ux` | Review product usability and accessibility readiness. | `ux` | [workflows/ux-review.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/ux-review.md) |
| `sherpa-accessibility` | Review accessibility within the existing UX-review scope. | `accessibility` | [workflows/ux-review.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/ux-review.md) |
| `sherpa-demo` | Prepare an evidence-backed judge-oriented demo plan. | `demo` | [workflows/demo-preparation.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/demo-preparation.md) |
| `sherpa-audit` | Run the existing final-audit workflow after its prerequisites are met. | `audit` | [workflows/final-audit.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/final-audit.md) |
| `sherpa-submission` | Prepare and verify submission materials without submitting. | `submission` | [workflows/submission.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/submission.md) |
| `sherpa-postmortem` | Run the final-phase evidence-based retrospective. | `postmortem` | [workflows/postmortem.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/postmortem.md) |
| `sherpa-research` | Research competitors, markets, technologies, and evidence with verifiable sources. | `research` | [workflows/research.md](https://github.com/Anshkaliya18/sherpa/blob/main/workflows/research.md) |

## Distribution management CLI

This separate executable manages installed files; these are not agent workflows.

| Command | Arguments | Behavior |
|---|---|---|
| `sherpa --version` | none | Prints installed CLI version. |
| `sherpa update` | optional `--yes` / `-y` | Fetches a release and updates managed skill files after checksum verification. |
| `sherpa uninstall` | optional `--yes` / `-y` | Removes recognized managed skill and CLI files; preserves project state. |
| `sherpa doctor` | none | Reports runtime/install information and manifest reachability. |
| `sherpa audit` | none | Reports debris, duplicates, empty directories, and file count in managed skill folders. |
| `sherpa clean` | `--dry-run` by default; `--yes` to remove | Lists recognized generated debris; deletion requires confirmation and is scoped to managed skill folders. |
| `sherpa help` | none | Prints CLI usage. |

Agent workflows return evidence-based reports or artifacts; they do not promise one fixed output schema. See [installation](/installation/) and [source command notes](https://github.com/Anshkaliya18/sherpa/blob/main/COMMANDS.md).
