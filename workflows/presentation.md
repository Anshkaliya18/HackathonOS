# HackathonOS — PRESENTATION-PREPARE Workflow

**Operation:** PRESENTATION-PREPARE  
**Lifecycle Phase:** Phase 17 — PPT / Presentation Intelligence  
**Purpose:** Convert validated project evidence into a coherent, evidence-backed presentation plan. Phase 17 optimizes for judge comprehension, credibility, and evidence coverage within presentation constraints, not visual decoration alone.

## Prerequisites

- `.hackathon/project-state.md` must exist
- `selected idea` must be known (not UNKNOWN)
- Phase 16 demo preparation evidence must exist
- Phase 15 score optimization evidence must exist
- Phase 14 judge simulation evidence must exist
- Phase 13 red-team evidence must exist
- Phase 12 UX evidence must exist
- Phase 11 testing/security evidence must exist

If any prerequisite is missing, mark it UNKNOWN, report PRESENTATION-PREPARE = BLOCKED or LIMITED, and do not invent criteria, evidence, or presentation readiness.

## Pipeline

### Stage 1: Read Project State

Read `.hackathon/project-state.md` and capture:

- Hackathon name, deadline, time remaining
- Phase
- Selected idea
- Judging criteria and weights
- Current estimated score, potential score
- Demo preparation evidence
- Presentation readiness gate
- Time-aware strategy category

### Stage 2: Read Prior-Phase Evidence

Consume (do not duplicate or replace) the following evidence:

| Phase | Source | What to consume |
|-------|--------|-----------------|
| Phase 11 | `.hackathon/evidence/` testing/security artifacts | Verified tests, critical failures, security findings, quality gate, evidence |
| Phase 12 | `.hackathon/ux-review.md`, `.hackathon/ux/` artifacts | Critical UX issues, usability findings, accessibility findings, demo flow observations |
| Phase 13 | `.hackathon/red-team.md`, `.hackathon/red-team/` artifacts | Critical findings, adversarial failures, recoverability, unresolved risks |
| Phase 14 | `.hackathon/judge-simulation.md` | Judge questions, skeptical follow-ups, weak claims, evidence gaps, expected judge concerns |
| Phase 15 | `.hackathon/score-optimization.md` | P0/P1 improvements, judge-visible priorities, evidence weaknesses, criterion gaps |
| Phase 16 | `.hackathon/demo-preparation.md` | Demo objective, primary flow, judge-visible moments, evidence, fallback info, timing |

Do not re-run Phase 11–16 engines. Consume their evidence only.

Flag contradictory claims between phases:

```text
Documentation says X
Repository does Y
Phase 14 simulation says Z
```

Do not silently reconcile contradictions. Record them as separate findings.

### Stage 3: Inspect Current Repository

Inspect the actual repository:

- Project metadata
- Dependency manifests
- Top-level project structure
- Application entry points
- Frontend/backend/database/AI components
- APIs
- Tests
- Deployment configuration
- Documentation
- Environment configuration

Classify every observation as FACT, INFERENCE, ASSUMPTION, or UNKNOWN. Cite repository path/line or execution result.

Rules:

- Never fabricate repository facts.
- Seeing a file does not prove a slide claim.
- Generated HackathonOS artifacts are not independent evidence.

### Stage 4: Build Presentation Objective

Define the presentation objective:

> "By the end of the presentation, the judge should understand that [PROJECT] solves [PROBLEM] for [USER] by [CORE MECHANISM], producing [VERIFIABLE RESULT]."

Every slide should contribute to this objective. Flag unnecessary slides.

### Stage 5: Build Presentation Narrative

Build the presentation narrative from these sections:

1. Problem
2. Why it matters
3. Current gap
4. Solution
5. How it works
6. Why it is different
7. Proof
8. Demo
9. Impact
10. Closing

Use time-aware selection. Do not force all sections into the live presentation.

### Stage 6: Build Slide Architecture

Construct slides:

| Slide ID | Title | Purpose | Primary Message | Judge Takeaway | Content | Evidence | Target Criterion | Priority | Time | Speaker Guidance | Visual Requirement | Risk | Verification | Status |

Every slide must have a status: PLANNED / EXECUTED / PASSED / FAILED / BLOCKED / UNKNOWN / NOT_APPLICABLE.

Do not mark PASSED without evidence.

### Stage 7: Map Presentation Evidence

For every presentation claim:

| Claim ID | Claim | Evidence Source | Evidence Type | Evidence Status | Verification Method | Slide | Target Criterion | Confidence |

Evidence types: UI / output / test / log / artifact / live behavior / screenshot / recording / documentation / benchmark / source/code inspection

Evidence statuses: FACT / INFERENCE / ASSUMPTION / UNKNOWN

No evidence → UNKNOWN.

### Stage 8: Build Slide-to-Criterion Mapping

Map judging criteria to slides to claims to evidence:

| Judging Criterion | Presentation Slide | Claim | Evidence | Mapping State | Expected Judge Takeaway |

Mapping states: SUPPORTED / PARTIALLY_SUPPORTED / UNKNOWN / CONTRADICTED / NOT_APPLICABLE

If judging criteria are unavailable:

```
CRITERION = UNKNOWN
```

### Stage 9: Assess Claim Credibility

Every major claim status:

| Status | Definition |
|--------|------------|
| VERIFIED | Claim is fully supported by evidence |
| SUPPORTED | Claim is backed by reasonable evidence |
| PARTIALLY_SUPPORTED | Claim has some evidence but gaps remain |
| UNSUPPORTED | Claim has no evidence |
| CONTRADICTED | Claim contradicts available evidence |
| UNKNOWN | Insufficient evidence to classify |

Rules:

- UNSUPPORTED claims should be removed, weakened, or explicitly qualified.
- CONTRADICTED claims must not be presented as facts.
- UNKNOWN claims must remain UNKNOWN.
- Do not increase confidence because a claim sounds plausible.

### Stage 10: Define Metrics and Numbers

For each presentation metric:

| Metric | Value | Unit | Source | Measurement Method | Date | Evidence Status | Confidence |

Before using: user counts, accuracy, latency, revenue, savings, growth, adoption, performance, benchmark results, market size, percentage improvements — all require evidence.

Never fabricate precision.

If a number cannot be verified:

```
UNKNOWN
```

### Stage 11: Build Technical Presentation

Technical slides must communicate credibility without unnecessary complexity.

Use evidence from Phase 3/4 and verified implementation:

- architecture
- data flow
- API structure
- model pipeline
- database
- security controls
- testing
- deployment
- performance
- failure handling

Do not claim technologies not actually used.

Do not invent architecture diagrams.

### Stage 12: Address AI / ML Claims

If the project uses AI/ML, separate:

- model used
- training data
- preprocessing
- inference
- evaluation
- measured performance
- limitations

Never claim:

- "100% accurate"
- "production ready"
- "industry-leading"
- "state-of-the-art"

unless evidence actually supports the claim.

If no AI exists:

```
AI = NOT_APPLICABLE
```

### Stage 13: Integrate Demo

Connect presentation to demo:

- demo objective
- primary demo flow
- judge-visible moments
- demo claims
- evidence
- fallback information
- timing

Do not duplicate the entire demo inside the PPT.

The presentation should prepare the judge to understand the demo.

### Stage 14: Incorporate Judge Simulation Evidence

Consume Phase 14:

- judge questions
- skeptical follow-ups
- weak claims
- evidence gaps
- credibility concerns

For important presentation claims, anticipate:

> "How do you know?"

and:

> "Can you prove it?"

The slide plan should make those questions easier to answer.

### Stage 15: Incorporate Score Optimization Evidence

Consume Phase 15:

- P0 improvements
- P1 improvements
- evidence weaknesses
- differentiation opportunities
- criterion gaps

Do not recreate the score optimization system. Phase 17 consumes its outputs.

### Stage 16: Incorporate UX, Security, Red Team Evidence

Consume from Phase 11, Phase 12, Phase 13:

Only include findings relevant to presentation credibility.

Do not hide critical known issues.

If a limitation materially affects a claim, surface it appropriately.

### Stage 17: Build Demo Timing Model

Create timing plan:

| Segment | Target Time | Priority |

Derive timing from actual competition constraint, available presentation time, project complexity, reliability, judge attention, and number of critical slides.

If presentation duration is UNKNOWN:

```
PRESENTATION TIME = UNKNOWN
```

Total slide duration must be checked against available presentation time.

### Stage 18: Prepare Speaker Guidance

For every major slide:

```text
SHOW:   What appears on screen.
SAY:    What presenter communicates.
PROVE:  Evidence supporting the claim.
EMPHASIZE: What judge should remember.
AVOID:  Potential misleading or unnecessary claims.
TRANSITION: How to move to the next slide.
```

Phase 17 only prepares presentation-specific speaking guidance.

### Stage 19: Plan Visual Evidence

For each slide identify whether it needs:

- screenshot
- architecture diagram
- chart
- UI flow
- table
- metric
- code excerpt
- test evidence
- demo frame
- no visual

Do not add visuals merely for decoration.

Every visual should improve comprehension or credibility.

### Stage 20: Perform Redundancy Analysis

Detect:

- duplicate claims
- repeated screenshots
- repeated metrics
- repeated explanations
- unnecessary technical details
- slides with no unique value

Each redundant slide should be:

- merged
- simplified
- removed

unless the judging rubric explicitly requires separate coverage.

### Stage 21: Build Presentation Risk Model

Identify:

- unsupported claim risk
- missing evidence
- timing overflow
- excessive text
- technical complexity
- visual confusion
- judge misunderstanding
- demo disconnect
- contradictory information
- stale evidence
- unsupported metrics
- dependency on unavailable assets

Each risk receives:

- Severity
- Likelihood
- Detectability
- Recoverability
- Mitigation
- Owner
- Status

Do not collapse confidence and severity into one number.

### Stage 22: Prepare Q&A Inputs

For each likely question:

| Question | Related Slide | Evidence | Answer Readiness | Risk | Recommended Response |

Answer readiness: READY / PARTIALLY_READY / WEAK / UNKNOWN / NOT_APPLICABLE

Never fabricate an answer.

### Stage 23: Determine Presentation Readiness Gate

Gate values:

| Value | Meaning |
|-------|---------|
| NOT_READY | Insufficient evidence for meaningful review |
| PREPARING | Review is actively incomplete |
| BLOCKED | Critical dependency prevents validation |
| CONDITIONAL | Major unknowns remain, but review produced useful results |
| READY | Essential slides reviewed sufficiently |

READY requires:

- essential slides defined
- critical claims supported
- criteria mapped where available
- timing verified or explicitly UNKNOWN
- no critical unsupported claims
- demo transition defined
- speaker guidance available for critical slides
- presentation sequence coherent
- evidence available
- critical risks addressed

If these conditions are not satisfied:

> Do not mark READY.

### Stage 24: Calculate Internal Presentation Score

If useful, calculate an internal readiness indicator.

Possible dimensions:

- evidence coverage
- criterion coverage
- narrative clarity
- timing confidence
- claim credibility
- demo integration
- judge comprehension

Label it:

```
INTERNAL PRESENTATION READINESS INDICATOR
NOT OFFICIAL JUDGING SCORE
```

No arbitrary hidden multipliers.

### Stage 25: Update Project State

Update ONLY these compact fields in `.hackathon/project-state.md`:

| Field | Allowed Values |
|-------|---------------|
| Presentation Status | NOT_STARTED | IN_PROGRESS | BLOCKED | COMPLETE |
| Presentation Objective | UNKNOWN | DEFINED |
| Slide Count | UNKNOWN | DEFINED |
| Critical Slides | UNKNOWN | IDENTIFIED |
| Criterion Coverage | UNKNOWN | PARTIAL | COMPLETE |
| Evidence Coverage | UNKNOWN | PARTIAL | COMPLETE |
| Timing Status | UNKNOWN | DEFINED |
| Critical Presentation Risks | UNKNOWN | NONE | IDENTIFIED |
| Q&A Readiness | UNKNOWN | PARTIAL | COMPLETE |
| Presentation Readiness Gate | NOT_READY | PREPARING | BLOCKED | CONDITIONAL | READY |

Rules:

- Do NOT put detailed presentation analysis inside project-state.md.
- Detailed material goes to `.hackathon/presentation.md` and `.hackathon/presentation/`.
- Do not change `selected idea`.
- Do not silently change architecture.
- Human approval required for major presentation changes.

### Stage 26: Return Exactly One Primary Next Action

Output format:

```
PRIMARY NEXT ACTION: <exactly one action>

WHY: <explanation based on impact, time, risk, and judging criteria>

DONE WHEN: <clear definition of done>

Time remaining: <hours or UNKNOWN>

Blocked by: <blocker or "None">
```

Rule: Exactly one primary next action. Do not produce competing alternatives.

## Validation Checklist

After PRESENTATION-PREPARE completes:

- [ ] Project state read and verified
- [ ] Phase 11–16 evidence consumed (not duplicated)
- [ ] Repository inspected for evidence
- [ ] Presentation objective defined
- [ ] Presentation narrative built
- [ ] Slide architecture constructed
- [ ] Presentation evidence mapped
- [ ] Presentation claim matrix created
- [ ] Judge-visible moments identified
- [ ] Presenter talking points prepared
- [ ] Presentation timing model built
- [ ] Presentation reliability assessed
- [ ] Failure and recovery model built
- [ ] Fallback strategy created
- [ ] Presentation checkpoints defined
- [ ] Presentation priorities assigned
- [ ] Rehearsal plan built
- [ ] Presentation readiness gate evaluated
- [ ] Time-aware presentation strategy applied
- [ ] Project state updated with compact fields only
- [ ] No Phase 1–16 artifacts modified
- [ ] No application source code modified
- [ ] No PPT created
- [ ] No final presentation performed
- [ ] No final submission performed
- [ ] No postmortem performed
- [ ] No final audit performed
- [ ] No Phase 18 scope leakage
- [ ] No presentation claim fabricated
- [ ] Exactly ONE primary next action returned
