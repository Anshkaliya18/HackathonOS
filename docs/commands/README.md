# HackathonOS Native Commands

`commands/manifest.json` is the single authoritative registry. It lists only commands mapped to an existing workflow as implemented. Planned commands are not registered in host adapters or advertised as usable.

## Preferred syntax

Use `/hackathonos-<action>` for direct invocation. The master `/hackathonos` command and its existing nested forms remain available for backward compatibility. Both forms resolve through `core/commands/router.py` to the same workflow; adapters contain no business logic.

## Implemented commands

### Core

- `/hackathonos-status` — Show evidence-backed project status. Maps to `STATUS` → `workflows/status.md`.
- `/hackathonos-next` — Identify the single highest-priority next action. Maps to `NEXT` → `workflows/next.md`.
- `/hackathonos-help` — List implemented HackathonOS commands and limitations. Maps to `HELP` → `SKILL.md#help`.
- `/hackathonos-init` — Initialize project-local HackathonOS state safely. Maps to `INIT` → `workflows/init.md`.
- `/hackathonos-phase` — Show current lifecycle phase and evidence. Maps to `PHASE` → `SKILL.md#phase`.

### Configuration

- `/hackathonos-config` — Show a redacted project configuration overview. Maps to `CONFIG` → `workflows/configuration.md`.
- `/hackathonos-config-check` — Validate project configuration and secret protections. Maps to `CONFIG CHECK` → `workflows/configuration.md`.

### Intelligence

- `/hackathonos-suggest` — Discover, evaluate, and red-team idea candidates; human selection required. Maps to `SUGGEST` → `workflows/idea-intelligence.md`.
- `/hackathonos-evaluate` — Evaluate and compare candidate ideas with evidence. Maps to `IDEA-EVALUATE` → `workflows/idea-evaluation.md`.
- `/hackathonos-compare` — Compare candidate ideas using the existing idea-evaluation workflow. Maps to `IDEA-EVALUATE` → `workflows/idea-evaluation.md`.
- `/hackathonos-redteam` — Challenge project assumptions and readiness using the red-team workflow. Maps to `RED-TEAM` → `workflows/red-team.md`.
- `/hackathonos-optimize` — Prioritize score-improving work against evidence and criteria. Maps to `SCORE-OPTIMIZE` → `workflows/score-optimization.md`.
- `/hackathonos-judge-me` — Simulate judge perception using the judge-simulation workflow. Maps to `JUDGE-SIM` → `workflows/judge-simulation.md`.

### Engineering

- `/hackathonos-repo` — Inspect repository evidence as part of project planning. Maps to `PROJECT-PLAN` → `workflows/project-planning.md`.
- `/hackathonos-architecture` — Plan architecture from the selected idea and repository evidence. Maps to `PROJECT-PLAN` → `workflows/project-planning.md`.
- `/hackathonos-techstack` — Assess technology choices within the project plan. Maps to `PROJECT-PLAN` → `workflows/project-planning.md`.
- `/hackathonos-plan` — Create an implementation-ready project plan. Maps to `PROJECT-PLAN` → `workflows/project-planning.md`.
- `/hackathonos-build` — Execute an approved implementation task using the existing implementation workflow. Maps to `IMPLEMENT` → `workflows/implementation.md`.
- `/hackathonos-verify` — Verify implementation through the existing testing and security workflow. Maps to `TESTING-SECURITY` → `workflows/testing-security.md`.
- `/hackathonos-test` — Test implemented scope using the testing and security workflow. Maps to `TESTING-SECURITY` → `workflows/testing-security.md`.
- `/hackathonos-security` — Review security using the testing and security workflow. Maps to `TESTING-SECURITY` → `workflows/testing-security.md`.
- `/hackathonos-ux` — Review product usability and accessibility readiness. Maps to `UX-REVIEW` → `workflows/ux-review.md`.

### Product Quality

- `/hackathonos-accessibility` — Review accessibility within the existing UX-review scope. Maps to `UX-REVIEW` → `workflows/ux-review.md`.

### Finalization

- `/hackathonos-demo` — Prepare an evidence-backed judge-oriented demo plan. Maps to `DEMO-PREPARE` → `workflows/demo-preparation.md`.
- `/hackathonos-audit` — Run the existing final-audit workflow after its prerequisites are met. Maps to `FINAL-AUDIT` → `workflows/final-audit.md`.
- `/hackathonos-submission` — Prepare and verify submission materials without submitting. Maps to `SUBMISSION-PREPARE` → `workflows/submission.md`.
- `/hackathonos-postmortem` — Run the final-phase evidence-based retrospective. Maps to `POSTMORTEM` → `workflows/postmortem.md`.

### Emergency

No implemented command currently belongs to this group.

## Planned, not available

These names are intentionally absent from native adapters and command help until a corresponding workflow exists:

- `/hackathonos-research` — PLANNED. No standalone research workflow exists; research is conditional within idea intelligence.
- `/hackathonos-improve` — PLANNED. No general improvement workflow exists; score optimization is narrower.
- `/hackathonos-polish` — PLANNED. No standalone polish workflow exists.
- `/hackathonos-performance` — PLANNED. No performance-review workflow exists.
- `/hackathonos-experience` — PLANNED. No standalone experience workflow exists.
- `/hackathonos-video` — PLANNED. No video workflow exists.
- `/hackathonos-emergency` — PLANNED. No emergency workflow exists.
- `/hackathonos-freeze` — PLANNED. No freeze workflow exists.
- `/hackathonos-reality-check` — PLANNED. No dedicated reality-check workflow exists.
- `/hackathonos-health` — PLANNED. No standalone health workflow exists.

## Host registration and argument behavior

| Host | Registration | Argument handling | Hyphenated runtime |
|---|---|---|---|
| Claude Code | `.claude/skills/<command>/SKILL.md`; the skill name is slash-invocable. | `$ARGUMENTS` is passed into each thin adapter. | NOT VERIFIED — global invocation stopped before dispatch because the configured model was unrecognized. |
| OpenCode | `.opencode/commands/<command>.md`; filename defines the slash command. | `$ARGUMENTS` is supported by the command template. | NOT VERIFIED — global invocation produced no output after 15 seconds and was interrupted. |
| Kilo | `.kilo/commands/<command>.md`; filename defines the workflow command. | No argument substitution is assumed; adapters do not depend on trailing input. | NOT VERIFIED — global status command loaded its workflow, then a read-only tool call was auto-rejected by the permission gate. |

Runtime attempt evidence recorded in the manifest:

- Claude Code: `NOT VERIFIED` — `claude --print --permission-mode plan /hackathonos-status` from an isolated temporary project stopped before dispatch because Claude Code rejected the configured model as unrecognized.
- OpenCode: `NOT VERIFIED` — `opencode run --pure --log-level DEBUG --command hackathonos-status` from an isolated temporary project produced no output after 15 seconds and was interrupted; the earlier project-root attempt also waited without workflow output.
- Kilo: `NOT VERIFIED` — `kilo run --pure --command hackathonos-status` from an isolated temporary project resolved the global adapter and read the global SKILL.md, manifest, router, and status workflow; the permission gate auto-rejected a read-only Test-Path call before a report was produced.

Runtime status is also recorded in `commands/manifest.json`. A file or static test proves registration structure, not that a host discovers or executes it. The existing master router has historical host-specific verification recorded in [`commands/README.md`](../../commands/README.md); those results do not verify the newly added hyphenated commands.

Official host references: [Claude Code skills](https://code.claude.com/docs/en/skills), [OpenCode commands](https://opencode.ai/docs/commands), and [Kilo workflows](https://kilo.ai/docs/customize/workflows).

## Compatibility and safety

Existing `/hackathonos`, `/hackathonos status`, `/hackathonos next`, `/hackathonos config`, `/hackathonos config check`, `/hackathonos suggest`, and `/hackathonos verify` are retained in the shared resolver. Native aliases share the same router and workflow. Config output remains redacted; the consuming project state is read in place and is not synchronized from this framework repository. Human approval, prerequisites, evidence labels, and lifecycle boundaries remain owned by the existing workflows. Stage 3 remains BLOCKED / NOT LOCKED until `/hackathonos-suggest` has been run in a supported host against the actual consuming project. No Stage 4 action is invoked by registering `/hackathonos-build`.
