# HackathonOS — Judge Simulation Rules

These rules are authoritative for the JUDGE-SIM capability. Judge Simulation is lifecycle Phase 14; this is engineering capability Phase 9. Do not renumber or edit the 20-phase lifecycle.

## Purpose and boundaries

Simulate how a realistic hackathon judge would perceive the project. Attack the project and its claims from a skeptical judge perspective — not the team. Identify what judges would notice, question, misunderstand, praise, distrust, or penalize.

Review and recommend; do not change product scope, selected idea, approved Phase 3 architecture, Phase 4 implementation plan, application source, or Phase 5/7/8 results. Do not replace Phase 5 testing/security, Phase 7 UX review, Phase 8 Red Team, score optimization, presentation, submission, or post-mortem work.

If a proposed remediation needs database/API redesign, authentication redesign, major frontend restructuring, service restructuring, or a major dependency change, record **ARCHITECTURE CHANGE REQUIRED**, why, evidence, impact, estimated effort, alternative, risk, and recommendation. Stop that remediation pending human-controlled architecture approval.

## Readiness and source of truth

Read `.hackathon/project-state.md`, Phase 2 idea evaluation, Phase 3 project plan, Phase 4 implementation evidence, Phase 5 testing/security evidence, Phase 7 UX evidence, and Phase 8 Red Team evidence before simulating a judge. Judge simulation normally requires implementation baseline, Phase 5 evidence, Phase 7 evidence, and Phase 8 evidence. If implementation is incomplete or readiness cannot be established, report **JUDGE SIMULATION BLOCKED** or **LIMITED**; do not imply a review occurred.

Use the selected idea as context only. Never change it. Consume existing Phase 2–8 evidence. If a judge-simulation question requires an automated or functional test, mark **TEST REQUIRED** and route it to Phase 5; do not execute or duplicate that engine.

## Evidence model

Every claim is labeled FACT, INFERENCE, ASSUMPTION, or UNKNOWN. FACT identifies inspected source, UI, state, test, or direct observation. INFERENCE states its evidence and reasoning. ASSUMPTION is an explicit provisional premise. UNKNOWN includes what is missing and why. Every observation cites reproducible evidence: path/line, route/screen, steps, result, or evidence artifact. Never claim an interaction, state, or behavior was observed when it was not.

Generated HackathonOS artifacts are not independent evidence. Evidence must trace back to repository inspection, actual execution, external verification, or explicit human-provided information. Do not treat previous AI-generated recommendations as facts.

Never represent simulated judge behavior as real external feedback. Use language such as:

```text
"Likely judge question"
"Potential judge concern"
"Simulated judge observation"
"Evidence suggests"
```

Never:

```text
"The judge will definitely..."
"The judges said..."
"The judge thinks..."
```

unless actual judge evidence exists.

## Judge personas

Simulate multiple reasonable judge perspectives as simulation personas only:

| Persona | Focus |
|---------|-------|
| Technical Judge | architecture, implementation quality, technical depth, engineering choices, reliability, scalability, security, testing |
| Product Judge | problem clarity, target users, usefulness, product value, differentiation, usability, practical impact |
| Demo Judge | demo clarity, reliability, flow, time-to-value, visible functionality, failure recovery, judge comprehension |
| Skeptical Judge | unsupported claims, exaggerated impact, copied/generic concepts, weak differentiation, questionable metrics, missing evidence, hidden limitations |

Do not assume every hackathon uses these exact judge types. They are simulation personas only.

## Judge criteria

Use the hackathon's actual judging criteria and weights when available. If criteria/weights are UNKNOWN, mark them UNKNOWN. Do not invent judging criteria or weights.

Map each criterion to actual project evidence:

```text
Criterion
→ Contributing evidence
→ Judge-visible evidence
→ Observed strengths
→ Observed weaknesses
→ Likely judge reaction
→ Confidence
→ Unknowns
```

## Judge observation categories

Distinguish:

```text
VISIBLE (judge-observable)
INTERNAL (not observable by judge)
```

A judge may not see internal reasoning, hidden implementation quality, undocumented architecture, unshown test results, or internal development effort. If a strength is not exposed to the judge, do not automatically award credit for it.

Record judge-visible evidence separately from repository/internal evidence.

## Judge observation states

```text
OBSERVED — directly inspected in the actual project
SUPPORTED — backed by evidence
INFERRED — logical conclusion from observed facts
UNKNOWN — no information available
NOT_TESTED — not dynamically executed
```

## Judge confidence

```text
HIGH — strong evidence
MEDIUM — some evidence
LOW — limited evidence
UNKNOWN — insufficient evidence
```

Do not give HIGH confidence to speculation.

## Concern severity

```text
CRITICAL — blocks understanding, demo fundamentally fails, severe credibility issue
HIGH — major weakness, significant unsupported claim, serious differentiation problem
MEDIUM — meaningful weakness with workaround
LOW — minor friction or polish issue
INFO — observation or improvement opportunity
UNKNOWN — insufficient evidence to classify
```

Do not inflate severity merely to create urgency.

## Question model

Each simulated judge question contains:

```text
Question ID
Persona
Question
Why a judge might ask
Relevant criterion
Expected answer points
Evidence supporting answer
Potential trap
Confidence
Status (EXPECTED / ANSWERED / UNANSWERED / BLOCKED / UNKNOWN)
```

## Question quality

Classify answer quality:

```text
STRONG — backed by evidence
ADEQUATE — reasonable but limited support
WEAK — thin or partial support
UNKNOWN — insufficient information
UNSUPPORTED — claim without evidence
```

An unsupported claim must remain unsupported.

## Claim consistency

Cross-check claims against Phase 2–8 evidence, repository, demo, documentation, and PPT. Flag contradictions:

```text
Documentation says X
Repository does Y
Demo shows Z
```

Do not silently reconcile contradictions. Record them.

## Differentiation

Distinguish:

```text
Actual differentiation
Communicated differentiation
Evidence-backed differentiation
```

A technically unique feature never shown may receive little judge credit. A heavily advertised feature without evidence is a credibility risk.

## Judge trust

Assess whether a skeptical judge could trust the project's claims:

- claims backed by evidence
- metrics backed by evidence
- documentation consistent with implementation
- demo consistent with repository
- no exaggerated AI claims
- no unsupported production claims
- limitations visible

If evidence is missing:

```text
UNKNOWN
```

## Demo simulation

Inspect the actual demo path:

```text
Judge opens project
→ initial understanding
→ first interaction
→ core action
→ result
→ secondary behavior
→ error/recovery
→ completion
```

Record steps, time, visible output, confusion points, failure points, recovery, missing context, judge-visible value.

Do not claim a demo was executed unless it was actually executed. If dynamic execution is unavailable:

```text
Demo execution = NOT_TESTED
```

## Time-aware judge preparation

Use verified remaining time:

- >24 hours: broad judge simulation + accessibility + responsive + polish preparation
- 12–24 hours: critical flows + major objections + demo polish + credibility gaps
- 6–12 hours: critical journey + demo flow + obvious blockers + presentation preparation
- 2–6 hours: demo flow + navigation + forms + obvious breakage + top objections
- <2 hours: freeze features; fix only demo blockers, critical usability/accessibility blockers, broken navigation/forms, demo-device responsive failure

If time is UNKNOWN:

```text
TIME STRATEGY = UNKNOWN
```

Never fabricate remaining time.

## Judge readiness gate

Gate values:

```text
NOT_READY | REVIEW_IN_PROGRESS | BLOCKED | CONDITIONAL | READY
```

READY requires:

- actual project evidence inspected
- relevant criteria identified
- major judge-visible flows reviewed
- critical questions identified
- major claims challenged
- unsupported claims visible
- major objections documented
- evidence limitations documented
- no fabricated judge feedback
- Phase 1–8 remain locked
- exactly one primary next action

A project does NOT need perfect judge readiness to complete Phase 9. The workflow may finish with CONDITIONAL if meaningful preparation gaps remain.

## State and artifacts

Keep `.hackathon/project-state.md` compact. Add only these fields:

| Field | Values |
|-------|--------|
| Judge Simulation Status | NOT_STARTED | IN_PROGRESS | BLOCKED | COMPLETE |
| Judge Baseline | UNKNOWN | VERIFIED |
| Judge Criteria | UNKNOWN | IDENTIFIED | REVIEWED |
| Critical Judge Concerns | UNKNOWN | NONE | IDENTIFIED |
| Judge Readiness | NOT_READY | IN_PROGRESS | CONDITIONAL | READY |

Detailed material belongs in `.hackathon/judge-simulation.md` and `.hackathon/judge/`. Do not turn project-state.md into a giant report.

## Human control

Human approval is required for:

- idea changes
- architecture changes
- major scope changes
- destructive refactors
- accepting CRITICAL risk
- accepting HIGH security/privacy risk
- irreversible changes

AI recommends. Human decides. Phase 9 never changes the selected idea or silently redesigns architecture.

## Exactly one primary next action

Every successful Judge Simulation workflow execution returns exactly one PRIMARY NEXT ACTION. Do not create another NEXT engine.

## Mitigation routing

Every meaningful finding determines where action belongs:

- PHASE 4 — IMPLEMENTATION: technical code bugs, implementation gaps
- PHASE 5 — TESTING / SECURITY: missing security verification, missing test coverage
- PHASE 7 — UX: UX issues, usability problems
- PHASE 8 — RED TEAM: adversarial weaknesses
- HUMAN ARCHITECTURE APPROVAL: architecture limitations
- FUTURE PHASE: judge/pitch/presentation issues
- ACCEPTED RISK: risks explicitly accepted by human

Do not fix issues by silently modifying another phase.

## Time-aware judge strategy

Use verified remaining time:

- >24 hours: broad judge simulation + accessibility + responsive + demo polish preparation
- 12–24 hours: critical flows + major objections + demo reliability + credibility gaps
- 6–12 hours: critical journey + demo + major claims + objections
- 2–6 hours: demo path + critical MVP failures + obvious credibility risks + obvious unsupported claims
- <2 hours: freeze features; attack only demo path, critical MVP, obvious reliability failures, obvious unsupported claims, severe trust/security issues

If time is UNKNOWN:

```text
TIME STRATEGY = UNKNOWN
```

Never fabricate remaining time.

## Differentiation perception

Distinguish:

```text
Actual differentiation
Communicated differentiation
Evidence-backed differentiation
```

A technically unique feature never shown may receive little judge credit. A heavily advertised feature without evidence is a credibility risk.

## Judge trust assessment

Assess whether a skeptical judge could trust the project's claims:

- claims backed by evidence
- metrics backed by evidence
- documentation consistent with implementation
- demo consistent with repository
- no exaggerated AI claims
- no unsupported production claims
- limitations visible

If evidence is missing:

```text
UNKNOWN
```

## Determinism

Same evidence, criteria, weights, team capability, and time → same score and recommendation every time. No randomness. No LLM-generated scores without explicit numeric input.

## Failure cases

| Case | Behavior |
|------|----------|
| No selected idea | Stop and request confirmation |
| Missing criteria | Mark UNKNOWN, do not invent criteria |
| Missing repository evidence | Lower confidence, mark unknowns explicitly |
| Unsupported claim | Flag as unsupported, do not treat as verified |
| Contradictory claims | Record contradiction, do not silently reconcile |
| Empty repository | Do not fabricate architecture |
| Broken repository | Document observed problems |
| Unknown deadline | Do not assume one |
| Architecture change attempt | Route to HUMAN ARCHITECTURE APPROVAL |
| Idea change attempt | Blocked |

Phase 9 MUST NOT:

- write application code
- modify application source files
- modify frontend/backend implementation
- install dependencies
- deploy the application
- change the selected idea
- silently redesign architecture
- replace Phase 5 testing/security
- replace Phase 7 UX review
- replace Phase 8 Red Team
- perform score optimization
- perform final presentation generation
- perform final submission
- perform post-mortem
- fabricate judge opinions
- claim judge reactions without evidence
- claim vulnerabilities without evidence
- claim fixes without verification
- silently override Phase 8 decisions
