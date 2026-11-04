# Commands

This catalog is generated from `commands/manifest.json`; each command routes through the root `SKILL.md`. Invoke as `/sherpa <operation> [focus]`. Command file names vary by adapter. For behavioral details, follow the linked workflow. Runtime status per agent is recorded in the manifest.

## Syntax and results

The common syntax is `/sherpa <operation> [free-form focus or context]`. The operation must match a router key in the table. Workflows accept natural-language context as focus; the command manifest does not define structured positional flags. There is no guaranteed fixed response schema: each workflow produces an evidence-based report or requested project artifact, and writes project state only where the workflow permits. Unknown operations are unavailable. `/sherpa help` lists the live command set and limitations.

Examples:

```text
/sherpa status
/sherpa suggest focus on accessibility for campus teams
/sherpa config check
/sherpa submission
```

Expected results are respectively a current evidence-backed status, scoped idea candidates, configuration/secret validation findings, and submission readiness guidance. The agent may ask for missing evidence and must follow human approval gates.

| Operation | Purpose | Workflow |
|---|---|---|
| `status` | Show evidence-backed project status. | `workflows/status.md` |
| `next` | Identify the single highest-priority next action. | `workflows/next.md` |
| `help` | List implemented sherpa commands and limitations. | `SKILL.md#help` |
| `init` | Initialize project-local sherpa state safely. | `workflows/init.md` |
| `phase` | Show current lifecycle phase and evidence. | `SKILL.md#phase` |
| `config` | Show a redacted project configuration overview. | `workflows/configuration.md` |
| `config check` | Validate project configuration and secret protections. | `workflows/configuration.md` |
| `suggest` | Discover, evaluate, and red-team idea candidates; human selection required. | `workflows/idea-intelligence.md` |
| `evaluate` | Evaluate and compare candidate ideas with evidence. | `workflows/idea-evaluation.md` |
| `compare` | Compare candidate ideas using the existing idea-evaluation workflow. | `workflows/idea-evaluation.md` |
| `redteam` | Challenge project assumptions and readiness using the red-team workflow. | `workflows/red-team.md` |
| `optimize` | Prioritize score-improving work against evidence and criteria. | `workflows/score-optimization.md` |
| `judge-me` | Simulate judge perception using the judge-simulation workflow. | `workflows/judge-simulation.md` |
| `repo` | Inspect repository evidence as part of project planning. | `workflows/project-planning.md` |
| `architecture` | Plan architecture from the selected idea and repository evidence. | `workflows/project-planning.md` |
| `techstack` | Assess technology choices within the project plan. | `workflows/project-planning.md` |
| `plan` | Create an implementation-ready project plan. | `workflows/project-planning.md` |
| `build` | Execute an approved implementation task using the existing implementation workflow. | `workflows/implementation.md` |
| `verify` | Verify implementation through the existing testing and security workflow. | `workflows/testing-security.md` |
| `test` | Test implemented scope using the testing and security workflow. | `workflows/testing-security.md` |
| `security` | Review security using the testing and security workflow. | `workflows/testing-security.md` |
| `ux` | Review product usability and accessibility readiness. | `workflows/ux-review.md` |
| `accessibility` | Review accessibility within the existing UX-review scope. | `workflows/ux-review.md` |
| `demo` | Prepare an evidence-backed judge-oriented demo plan. | `workflows/demo-preparation.md` |
| `audit` | Run the existing final-audit workflow after its prerequisites are met. | `workflows/final-audit.md` |
| `submission` | Prepare and verify submission materials without submitting. | `workflows/submission.md` |
| `postmortem` | Run the final-phase evidence-based retrospective. | `workflows/postmortem.md` |
| `research` | Research competitors, markets, technologies, and evidence with verifiable sources. | `workflows/research.md` |

## Distribution CLI

The separate `sherpa` executable supports `--version`, `update`, `uninstall`, `doctor`, `audit`, and `clean`. See [INSTALLATION.md](INSTALLATION.md). These are installer management commands, not agent slash commands.

| CLI command | Arguments | Result |
|---|---|---|
| `sherpa --version` | None | Prints installed CLI semantic version. |
| `sherpa update` | Optional `--yes` / `-y` | Checks for a release and updates recognized global skills; release archive checksum is mandatory. |
| `sherpa uninstall` | Optional `--yes` / `-y` | Prompts unless confirmed, then removes recognized managed skill/CLI files; does not remove project `.sherpa/` data. |
| `sherpa doctor` | None | Reports runtime, known installs, and manifest reachability; returns nonzero if the manifest is unreachable. |
| `sherpa audit` | None | Reports debris, duplicates, empty dirs, and file count within recognized skill install folders. |
| `sherpa clean` | `--dry-run` (default behavior), optional `--yes` / `-y` | Lists generated debris; deletion requires `--yes` and remains scoped to recognized skill installation paths. |
| `sherpa help` | None | Prints CLI usage. |
