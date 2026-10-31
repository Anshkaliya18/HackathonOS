# HackathonOS — POSTMORTEM Workflow

**Lifecycle Phase:** 20 — Post-Mortem Intelligence (final phase)  
**Purpose:** Preserve evidence-based lessons from the completed hackathon cycle.

## Prerequisites

1. Read `SKILL.md` and `workflows/lifecycle.md`; require exactly 20 phases with Phase 18 Final Audit, Phase 19 Submission, Phase 20 Post-Mortem. Never extend or renumber.
2. Read `audits/phase19-final-report.md`; require `PHASE 19 COMPLETE & LOCKED`, 35/35 acceptance, 30/30 adversarial, regression, scope and evidence integrity PASS. If not, stop with the exact blocker.
3. Inspect Phase 19 rules, workflow, templates, harness and audit. Preserve every locked prior-phase artifact and behavior.
4. Read `.hackathon/project-state.md` if present. If absent, record no live project state. Do not write project state into this framework repository.

## Procedure

1. Determine evidence scope: LIVE POST-MORTEM only with sufficient actual project history; otherwise `CONDITIONAL — FRAMEWORK VALIDATION ONLY`.
2. Inventory available historical artifacts and their provenance. Distinguish framework tests from live project records.
3. Label every significant statement FACT, INFERENCE, ASSUMPTION, or UNKNOWN. Cite evidence. Never fill history gaps with typical or synthetic events.
4. Review all 20 phases. For each, record purpose, usage, evidence, value, problems, redundancy, missing capability, contract gap and recommendation; unavailable project effectiveness is UNKNOWN.
5. Build timeline and plan-vs-actual tables. Missing planned/actual dates, durations and events remain UNKNOWN. Classify time variance only when evidenced.
6. Review planned/added/removed/deferred/accidental scope. Call scope creep only with evidence.
7. Review important decisions with contemporaneous context, evidence, options, authority, expected/actual outcome, quality and lesson. Do not infer decision ownership.
8. Record incidents only when supported by artifacts. Analyze observed outcome separately from cause; include counterevidence, alternatives, confidence and causality status.
9. Review original risks against observed outcomes. Unknown exposure remains UNKNOWN, not AVOIDED.
10. Review Phases 11–19 outcomes (testing/security, UX, red team, judge simulation, score optimization, demo, presentation, submission) only against actual records. Keep simulated judging/optimization separate from actual judging results.
11. Record official result only from official evidence. Otherwise result = UNKNOWN. Do not infer participation/result from framework status.
12. Identify evidence-backed wins and failures without blame. Extract lessons and reusable assets without modifying prior locked assets.
13. Evaluate HackathonOS Phases 1–19, bottlenecks, process debt, contract gaps, and proposed internal improvement backlog. Label its priorities as internal, not judging scores.
14. Add `postmortem` state only in the actual project's `.hackathon/project-state.md`, with listed fields and UNKNOWN where evidence is absent. Preserve all existing state. Never create project state in this skill repository.
15. Run evidence-integrity and historical-integrity checks; ensure no prior evidence was edited, no unsupported causality/result/score/judge statement appears, and no Phase 21 exists.
16. Produce the post-mortem artifact and exactly one `PRIMARY NEXT ACTION`. For framework-only validation this may be archival preservation of this completed cycle.

## Project state extension (actual project repository only)

```yaml
postmortem:
  status: UNKNOWN
  evidence_scope: UNKNOWN
  outcome: UNKNOWN
  result: UNKNOWN
  timeline_status: UNKNOWN
  decision_review: UNKNOWN
  incident_count: UNKNOWN
  risk_outcome_status: UNKNOWN
  lessons_count: UNKNOWN
  reusable_assets_count: UNKNOWN
  process_bottlenecks: UNKNOWN
  process_debt: UNKNOWN
  hackathonos_effectiveness: UNKNOWN
  contract_gaps: UNKNOWN
  improvement_backlog: UNKNOWN
  human_review: UNKNOWN
  final_status: UNKNOWN
  primary_next_action: UNKNOWN
```

Do not insert these values into the skill repository or overwrite prior state.

## Required report sections

Use `templates/postmortem.md` and include all 35 numbered sections listed there. Keep actual project claims UNKNOWN where evidence is missing. The framework audit belongs at `audits/phase20-final-report.md`; the post-mortem artifact for a real project belongs under that project's `.hackathon/` directory.

## Boundaries

Do not modify application source, dependencies, deployments, submissions, repository visibility, prior phase artifacts, or the lifecycle map. Do not implement a Phase 21. Recommendations are recorded for future human-authorized work only.

## Explicit review matrix

For all phase reviews, use this record: Phase; Purpose; Used?; Evidence; Value; Problems; Redundancy; Missing Capability; Contract Gap; Recommendation; Effectiveness. Review Phase 1 Rules, 2 Problem, 3 Ideas, 4 Validation, 5 Research, 6 Idea Selection, 7 MVP, 8 Architecture, 9 Development Plan, 10 Implementation, 11 Testing + Security, 12 UX, 13 Red Team, 14 Judge Simulation, 15 Score Optimization, 16 Demo Preparation, 17 Presentation, 18 Final Audit, and 19 Submission. Framework tests are not evidence of live project effectiveness.

The plan-vs-actual matrix has rows for timeline, scope, architecture, implementation, testing, security, UX, demo, presentation, and submission. Each row captures planned, actual, variance, evidence, reason, and impact. Unavailable values are UNKNOWN.

Record observed outcome separately from possible causes. For every cause include evidence supporting and against it, alternatives, confidence, and causality status. Record the official result only in a separate outcome section with source evidence; otherwise UNKNOWN.

Record explicit human approvals, rejected recommendations, scope and architecture decisions, risk acceptance, and final submission confirmation only when documented. Ownership otherwise UNKNOWN.

Bottleneck categories are TOOLING, PROCESS, KNOWLEDGE, TIME, DEPENDENCY, HUMAN_DECISION, COMMUNICATION, UNKNOWN. Reusable assets must include asset, location, purpose, quality, reuse recommendation, and required changes. Internal improvement priority is not official hackathon scoring.
