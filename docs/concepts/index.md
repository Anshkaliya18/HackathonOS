# Core concepts

HackathonOS separates the agent's instructions from a team's project state. The skill package contains reusable routing, workflows, rules, and templates. Each project stores its own decisions and evidence under `.hackathon/`.

## The main parts

| Part | What it means | Where it lives |
|---|---|---|
| Skill | The agent-facing behavior and operation routing | `SKILL.md` |
| Command manifest | Registered hyphenated names, descriptions, workflow routes, and adapter/runtime notes | `commands/manifest.json` |
| Router | Maps supported operation arguments to workflows | `core/commands/router.py` |
| Workflow | Steps, inputs, boundaries, and outputs for one operation | `workflows/` |
| Rule | Shared constraints such as evidence or approval requirements | `rules/` |
| Template | A reusable structure for project artifacts | `templates/` |
| Project state | Team-specific state and evidence | `<project>/.hackathon/` |

## Evidence and approvals

An **artifact** is a file a workflow creates or updates. An **evidence boundary** describes which inputs a workflow may rely on. HackathonOS is instructed to use `UNKNOWN` when information is unavailable. Recommendations do not automatically confirm the selected idea, approve architecture, or accept consequential risks.

## Commands and workflows

A command is the user-facing name. A workflow is the detailed procedure that command invokes. Several aliases can share one workflow; for example, `build` routes to implementation, while `test`, `verify`, and `security` route to testing and security.

## Rules and templates

Rules make constraints reusable across workflows. Templates provide consistent layouts for evidence such as plans, risks, test results, demo preparation, and submission readiness. These Markdown files are meant to be read and filled by the AI agent and team.

## Research and evaluation

Research is an implemented workflow for gathering evidence on questions such as competitors, markets, technologies, and hackathon rules. Idea evaluation compares candidates and makes recommendations; it does not select an idea on the team's behalf.

## Evaluation utilities

The repository includes a Python idea engine and verification/configuration utilities, plus evaluation scripts and regression checks. These are implementation modules, not a separately hosted evaluation service.

Next: [Lifecycle](/concepts/lifecycle) · [Architecture](/architecture/) · [Commands](/reference/commands).
