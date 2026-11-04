# Sherpa Native Commands

[`commands/manifest.json`](https://github.com/Anshkaliya18/sherpa/blob/main/commands/manifest.json) is the single authoritative registry. It lists only commands mapped to an existing workflow as implemented. Planned commands are not registered in host adapters or advertised as usable.

## Preferred syntax

Use `/sherpa-<action>` for direct invocation. The master `/sherpa` command and its existing nested forms remain available for backward compatibility. Both forms resolve through `core/commands/router.py` to the same workflow; adapters contain no business logic.

## Implemented commands

### Core

- `/sherpa-status` — Show evidence-backed project status. Maps to `STATUS` → `workflows/status.md`.
- `/sherpa-next` — Identify the single highest-priority next action. Maps to `NEXT` → `workflows/next.md`.
- `/sherpa-help` — List implemented sherpa commands and limitations. Maps to `HELP` → `SKILL.md#help`.
- `/sherpa-init` — Initialize project-local sherpa state safely. Maps to `INIT` → `workflows/init.md`.
- `/sherpa-phase` — Show current lifecycle phase and evidence. Maps to `PHASE` → `SKILL.md#phase`.

### Configuration

- `/sherpa-config` — Show a redacted project configuration overview. Maps to `CONFIG` → `workflows/configuration.md`.
- `/sherpa-config-check` — Validate project configuration and secret protections. Maps to `CONFIG CHECK` → `workflows/configuration.md`.

### Intelligence

- `/sherpa-suggest` — Discover, evaluate, and red-team idea candidates; human selection required. Maps to `SUGGEST` → `workflows/idea-intelligence.md`.
- `/sherpa-evaluate` — Evaluate and compare candidate ideas with evidence. Maps to `IDEA-EVALUATE` → `workflows/idea-evaluation.md`.
- `/sherpa-compare` — Compare candidate ideas using the existing idea-evaluation workflow. Maps to `IDEA-EVALUATE` → `workflows/idea-evaluation.md`.
- `/sherpa-research` — Investigate a research question with source and evidence constraints. Maps to `RESEARCH` → `workflows/research.md`.
- `/sherpa-redteam` — Challenge project assumptions and readiness using the red-team workflow. Maps to `RED-TEAM` → `workflows/red-team.md`.
- `/sherpa-optimize` — Prioritize score-improving work against evidence and criteria. Maps to `SCORE-OPTIMIZE` → `workflows/score-optimization.md`.
- `/sherpa-judge-me` — Simulate judge perception using the judge-simulation workflow. Maps to `JUDGE-SIM` → `workflows/judge-simulation.md`.

### Engineering

- `/sherpa-repo` — Inspect repository evidence as part of project planning. Maps to `PROJECT-PLAN` → `workflows/project-planning.md`.
- `/sherpa-architecture` — Plan architecture from the selected idea and repository evidence. Maps to `PROJECT-PLAN` → `workflows/project-planning.md`.
- `/sherpa-techstack` — Assess technology choices within the project plan. Maps to `PROJECT-PLAN` → `workflows/project-planning.md`.
- `/sherpa-plan` — Create an implementation-ready project plan. Maps to `PROJECT-PLAN` → `workflows/project-planning.md`.
- `/sherpa-build` — Execute an approved implementation task using the existing implementation workflow. Maps to `IMPLEMENT` → `workflows/implementation.md`.
- `/sherpa-verify` — Verify implementation through the existing testing and security workflow. Maps to `TESTING-SECURITY` → `workflows/testing-security.md`.
- `/sherpa-test` — Test implemented scope using the testing and security workflow. Maps to `TESTING-SECURITY` → `workflows/testing-security.md`.
- `/sherpa-security` — Review security using the testing and security workflow. Maps to `TESTING-SECURITY` → `workflows/testing-security.md`.
- `/sherpa-ux` — Review product usability and accessibility readiness. Maps to `UX-REVIEW` → `workflows/ux-review.md`.

### Product Quality

- `/sherpa-accessibility` — Review accessibility within the existing UX-review scope. Maps to `UX-REVIEW` → `workflows/ux-review.md`.

### Finalization

- `/sherpa-demo` — Prepare an evidence-backed judge-oriented demo plan. Maps to `DEMO-PREPARE` → `workflows/demo-preparation.md`.
- `/sherpa-audit` — Run the existing final-audit workflow after its prerequisites are met. Maps to `FINAL-AUDIT` → `workflows/final-audit.md`.
- `/sherpa-submission` — Prepare and verify submission materials without submitting. Maps to `SUBMISSION-PREPARE` → `workflows/submission.md`.
- `/sherpa-postmortem` — Run the final-phase evidence-based retrospective. Maps to `POSTMORTEM` → `workflows/postmortem.md`.

### Emergency

No implemented command currently belongs to this group.

## Planned, not available

These names are intentionally absent from native adapters and command help until a corresponding workflow exists:

- `/sherpa-improve` — PLANNED. No general improvement workflow exists; score optimization is narrower.
- `/sherpa-polish` — PLANNED. No standalone polish workflow exists.
- `/sherpa-performance` — PLANNED. No performance-review workflow exists.
- `/sherpa-experience` — PLANNED. No standalone experience workflow exists.
- `/sherpa-video` — PLANNED. No video workflow exists.
- `/sherpa-emergency` — PLANNED. No emergency workflow exists.
- `/sherpa-freeze` — PLANNED. No freeze workflow exists.
- `/sherpa-reality-check` — PLANNED. No dedicated reality-check workflow exists.
- `/sherpa-health` — PLANNED. No standalone health workflow exists.

## Host registration and argument behavior

| Host | Registration | Argument handling | Hyphenated runtime |
|---|---|---|---|
| Claude Code | `.claude/skills/<command>/SKILL.md`; the skill name is slash-invocable. | `$ARGUMENTS` is passed into each thin adapter. | NOT VERIFIED — global invocation stopped before dispatch because the configured model was unrecognized. |
| OpenCode | `.opencode/commands/<command>.md`; filename defines the slash command. | `$ARGUMENTS` is supported by the command template. | NOT VERIFIED — global invocation produced no output after 15 seconds and was interrupted. |
| Kilo | `.kilo/commands/<command>.md`; filename defines the workflow command. | No argument substitution is assumed; adapters do not depend on trailing input. | NOT VERIFIED — global status command loaded its workflow, then a read-only tool call was auto-rejected by the permission gate. |

Runtime attempt evidence recorded in the manifest:

- Claude Code: `NOT VERIFIED` — `claude --print --permission-mode plan /sherpa-status` from an isolated temporary project stopped before dispatch because Claude Code rejected the configured model as unrecognized.
- OpenCode: `NOT VERIFIED` — `opencode run --pure --log-level DEBUG --command sherpa-status` from an isolated temporary project produced no output after 15 seconds and was interrupted; the earlier project-root attempt also waited without workflow output.
- Kilo: `NOT VERIFIED` — `kilo run --pure --command sherpa-status` from an isolated temporary project resolved the global adapter and read the global SKILL.md, manifest, router, and status workflow; the permission gate auto-rejected a read-only Test-Path call before a report was produced.

Runtime status is also recorded in `commands/manifest.json`. A file or static test proves registration structure, not that a host discovers or executes it. The existing master router has historical host-specific verification recorded in [`commands/README.md`](https://github.com/Anshkaliya18/sherpa/blob/main/commands/README.md); those results do not verify the newly added hyphenated commands.

Official host references: [Claude Code skills](https://code.claude.com/docs/en/skills), [OpenCode commands](https://opencode.ai/docs/commands), and [Kilo workflows](https://kilo.ai/docs/customize/workflows).

## Compatibility and safety

Existing `/sherpa`, `/sherpa status`, `/sherpa next`, `/sherpa config`, `/sherpa config check`, `/sherpa suggest`, and `/sherpa verify` are retained in the shared resolver. Native aliases share the same router and workflow. Config output remains redacted; the consuming project state is read in place and is not synchronized from this framework repository. Human approval, prerequisites, evidence labels, and lifecycle boundaries remain owned by the existing workflows. Stage 3 remains BLOCKED / NOT LOCKED until `/sherpa-suggest` has been run in a supported host against the actual consuming project. No Stage 4 action is invoked by registering `/sherpa-build`.

