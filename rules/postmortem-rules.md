# HackathonOS — Phase 20 Post-Mortem Rules

**Lifecycle Phase:** 20 — Post-Mortem Intelligence  
**Operation:** `POSTMORTEM`  
**Purpose:** Turn an evidenced completed hackathon cycle into reusable learning. This is the final lifecycle phase.

## Evidence and history

Classify each significant retrospective statement FACT, INFERENCE, ASSUMPTION, or UNKNOWN. Cite the source artifact and verification method. Never convert UNKNOWN or INFERENCE into FACT. Keep observed outcomes separate from possible causes. Correlation is not causation. Causality states: CONFIRMED, STRONGLY_SUPPORTED, PLAUSIBLE, UNCERTAIN, UNKNOWN, CONTRADICTED. Record evidence for and against each possible cause; alternatives; confidence; and why causation is or is not established.

Determine scope before analysis. LIVE POST-MORTEM requires sufficient actual project history. When only framework/test evidence exists, report `CONDITIONAL — FRAMEWORK VALIDATION ONLY`; explicitly say that workflow validation cannot establish a factual project retrospective. Do not invent results, ranks, winner/finalist status, judge feedback, scores, submissions, incidents, performance, user outcomes, timestamps, decisions, or time allocation. Missing facts remain UNKNOWN.

## Required retrospective coverage

Review Phases 1–20 without changing lifecycle count/order. Compare plan vs actual and cover timeline, scope (planned/added/removed/deferred/accidental), decisions and human authority, incidents, risk outcomes, testing/security, UX, red team, judge simulation, score optimization, demo, presentation, submission, result, wins, failures, causal explanations, KEEP/CHANGE/STOP/START, lessons, reusable assets, HackathonOS effectiveness, bottlenecks, process debt, contract gaps, and internal improvement backlog.

For unavailable project history, each domain is UNKNOWN; do not populate an illustrative event as if it happened. Framework validation evidence is clearly labeled and may support conclusions about the framework contract only, not about a live hackathon.

Decision quality: EXCELLENT, GOOD, ACCEPTABLE, WEAK, POOR, UNKNOWN. Evaluate using information available at decision time; do not judge only by outcome. Decision ownership and human approvals are UNKNOWN unless recorded. Do not attribute a human decision to AI.

Incidents require evidence. Root-cause categories: PROCESS, TECHNICAL, REQUIREMENT, TIME, COMMUNICATION, DECISION, DEPENDENCY, ENVIRONMENT, SCOPE, HUMAN FACTOR, UNKNOWN. Use 5 Whys or causal tree only when evidence supports it; otherwise mark root cause UNKNOWN and preserve alternatives. Never assign blame without evidence.

Risk outcomes: MATERIALIZED, PARTIALLY_MATERIALIZED, AVOIDED, MITIGATED, TRANSFERRED, IRRELEVANT, UNKNOWN. Distinguish severity from confidence. A risk not observed in available evidence is UNKNOWN, not AVOIDED.

## Learning and recommendations

Keep, Change, Stop, Start, lessons, assets, bottlenecks, process debt, contract gaps, and backlog records must have evidence, rationale, benefit/impact, priority, and target as applicable. Improvement priorities P0–P3 are INTERNAL HACKATHONOS IMPROVEMENT PRIORITY — NOT OFFICIAL HACKATHON SCORING. Recommendations do not authorize edits to locked prior phases.

HackathonOS effectiveness for each Phase 1–19 is HIGH, MEDIUM, LOW, NOT_USED, or UNKNOWN and must cite evidence. Test harness success establishes only framework contract assertions. It cannot prove workflow host behavior, live project effectiveness, hackathon outcome, or user/judge impact.

## Historical integrity and scope

Phase 20 analyzes and preserves. It does not rewrite prior artifacts, test results, decisions, scores, or timestamps. It may not build features, redesign architecture, modify application source, install dependencies, deploy, submit, change visibility, run score optimization, redesign PPT/demo, substitute reruns for retrospective evidence, or create Phase 21. Record future improvements instead of applying them. Preserve human authority and historical evidence.

## State and output

In the actual project repository only, add the Phase 20 `postmortem` state object from the workflow. Keep unavailable keys UNKNOWN; do not fabricate defaults. Do not create project state in the HackathonOS skill repository. Produce exactly one `PRIMARY NEXT ACTION`. Phase 20 is final, so the action is preservation/archive or another evidenced closure task, never a Phase 21 action.

## Quality and lock gates

Quality values: NOT_READY, ANALYSIS_IN_PROGRESS, BLOCKED, CONDITIONAL, COMPLETE. COMPLETE requires sufficient actual project history and a complete evidence-backed retrospective. CONDITIONAL is correct for framework-only validation.

Phase 20 framework lock requires 35/35 acceptance, 30/30 adversarial, regression PASS, scope PASS, evidence-integrity PASS, no framework-critical defect, exactly 20 phases, Phase 19 COMPLETE & LOCKED, and no Phase 21 route/artifact. Framework may be COMPLETE & LOCKED while live retrospective quality remains CONDITIONAL.

## Explicit retrospective records

### Outcome and cause record

For each outcome: record the observed outcome, evidence, confidence, possible causes, evidence for and against each cause, alternative explanation, and causality status. Outcomes and causes are separate records. Use `CONFIRMED`, `STRONGLY_SUPPORTED`, `PLAUSIBLE`, `UNCERTAIN`, `UNKNOWN`, or `CONTRADICTED`; do not use root cause when only correlation is known.

### Hackathon result states

`WINNER`, `FINALIST`, `SHORTLISTED`, `PARTICIPATED`, `NOT_SELECTED`, `NOT_SUBMITTED`, `CANCELLED`, `UNKNOWN`. Record the source and verification for any non-UNKNOWN result. No result may be inferred from project quality or framework completion.

### Process review models

Bottleneck categories: `TOOLING`, `PROCESS`, `KNOWLEDGE`, `TIME`, `DEPENDENCY`, `HUMAN_DECISION`, `COMMUNICATION`, `UNKNOWN`. Each record includes evidence, impact, frequency, resolution, and future prevention.

Process debt records: debt, origin, impact, risk, current status, recommended resolution, and priority. Contract gap records: gap ID, affected phase, problem, evidence, impact, recommended change, priority, and risk.

Reusable assets record asset, location, purpose, quality, reuse recommendation, and required changes. Keep/Change/Stop/Start recommendations include evidence, rationale, expected benefit, priority, and target.

### Explicit phase coverage

Review each phase individually: 1 Rules, 2 Problem, 3 Ideas, 4 Validation, 5 Research, 6 Selection, 7 MVP, 8 Architecture, 9 Plan, 10 Implementation, 11 Testing/Security, 12 UX, 13 Red Team, 14 Judge Simulation, 15 Score Optimization, 16 Demo, 17 Presentation, 18 Final Audit, 19 Submission. For each record purpose, whether used, evidence, value, problems, redundancy, missing capability, contract gap, recommendation, and effectiveness (`HIGH`, `MEDIUM`, `LOW`, `NOT_USED`, `UNKNOWN`). Missing live records yield UNKNOWN; framework contract evidence only supports framework-level observations.

## Never rewrite history

Never rewrite prior-phase history, evidence, test results, scores, decisions, or timestamps. Never convert UNKNOWN or INFERENCE to FACT, delete inconvenient failures, or fabricate success. Recommend historical-artifact improvements as future work without applying them during Phase 20.
