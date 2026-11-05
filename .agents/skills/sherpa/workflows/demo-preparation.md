# sherpa — DEMO PREPARE Workflow

**Operation:** DEMO-PREPARE  
**Lifecycle Phase:** Phase 16 — Demo Preparation Intelligence  
**Purpose:** Convert validated project evidence into a reliable, judge-oriented, time-bounded demonstration plan. Phase 16 optimizes for reliable judge comprehension and credible proof under real demo constraints, not feature quantity.

## Prerequisites

- `.sherpa/project-state.md` must exist
- `selected idea` must be known (not UNKNOWN)
- Phase 15 score optimization evidence must exist
- Phase 14 judge simulation evidence must exist
- Phase 13 red-team evidence must exist
- Phase 12 UX evidence must exist
- Phase 11 testing/security evidence must exist

If any prerequisite is missing, mark it UNKNOWN, report DEMO-PREPARE = BLOCKED or LIMITED, and do not invent criteria, evidence, or demo readiness.

## Pipeline

### Stage 1: Read Project State

Read `.sherpa/project-state.md` and capture:

- Hackathon name, deadline, time remaining
- Phase
- Selected idea
- Judging criteria and weights
- Current estimated score, potential score
- Demo objective
- Demo readiness gate
- Time-aware strategy category

### Stage 2: Read Prior-Phase Evidence

Consume (do not duplicate or replace) the following evidence:

| Phase | Source | What to consume |
|-------|--------|-----------------|
| Phase 11 | `.sherpa/evidence/` testing/security artifacts | Verified tests, critical failures, security findings, quality gate, evidence |
| Phase 12 | `.sherpa/ux-review.md`, `.sherpa/ux/` artifacts | Critical UX issues, usability findings, accessibility findings, demo flow observations |
| Phase 13 | `.sherpa/red-team.md`, `.sherpa/red-team/` artifacts | Critical findings, adversarial failures, recoverability, unresolved risks |
| Phase 14 | `.sherpa/judge-simulation.md` | Judge questions, skeptical follow-ups, weak claims, evidence gaps, expected judge concerns |
| Phase 15 | `.sherpa/score-optimization.md` | P0/P1 improvements, judge-visible priorities, evidence weaknesses |

Do not re-run Phase 11–15 engines. Consume their evidence only.

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
- Seeing a file does not mean it works during a demo.
- Generated sherpa artifacts are not independent evidence.

### Stage 4: Build Demo Objective

Define the demo objective:

> "By the end of the demo, the judge should understand that [PROJECT] solves [PROBLEM] for [USER] by [CORE MECHANISM], producing [VERIFIABLE RESULT]."

Every demo step should contribute to this objective. Flag unnecessary steps.

### Stage 5: Build Demo Narrative

Build the demo narrative from these sections:

1. Problem
2. User/context
3. Solution
4. Core interaction
5. Differentiator
6. Technical credibility
7. Result
8. Impact
9. Closing takeaway

Use time-aware selection. Do not force all sections into the live demo.

### Stage 6: Build Demo Flow

Construct demo steps:

| Step ID | Step Name | Purpose | Presenter Action | System Action | Expected Result | Evidence | Time Estimate | Reliability | Failure Risk | Recovery | Fallback | Status |

Every step must have a status: PLANNED / EXECUTED / PASSED / FAILED / BLOCKED / UNKNOWN / NOT_APPLICABLE.

Do not mark PASSED without evidence.

### Stage 7: Map Demo Evidence

For every demo claim:

| Claim ID | Claim | Evidence | Evidence Type | Evidence Status | Verification | Demo Step | Confidence |

Evidence types: UI / output / test / log / artifact / live behavior / documentation

Evidence statuses: FACT / INFERENCE / ASSUMPTION / UNKNOWN

No evidence → UNKNOWN. Weak evidence cannot be upgraded merely because the feature exists.

### Stage 8: Build Demo Claim Matrix

Map judging criteria to project claims to demo steps to evidence:

| Judging Criterion | Project Claim | Demo Step | Evidence | Mapping State | Expected Judge Takeaway |

Mapping states: SUPPORTED / PARTIALLY_SUPPORTED / UNKNOWN / CONTRADICTED / NOT_APPLICABLE

If judging criteria are unavailable:

```
CRITERION = UNKNOWN
```

### Stage 9: Identify Judge-Visible Moments

Identify moments where the judge should clearly notice:

- Problem relevance
- Solution value
- Innovation
- Differentiation
- Technical sophistication
- Reliability
- UX quality
- Security/privacy
- Measurable result
- Real-world usefulness

Each moment: Moment ID / What judge should notice / How demonstrated / Evidence / Expected takeaway / Confidence / Time cost / Risk

### Stage 10: Build Presenter Talking Points

For each major demo step:

```text
ACTION: What the presenter does.
SAY: What the presenter says.
SHOW: What the judge sees.
PROVE: What evidence supports the claim.
TRANSITION: How to move to the next step.
```

Phase 16 only prepares demo-specific speaking guidance. Phase 17 owns presentation construction.

### Stage 11: Build Demo Timing Model

Create timing plan:

| Segment | Target Time | Priority |

Derive timing from competition constraints, available demo time, project complexity, reliability, judge attention, and number of critical steps.

If demo duration is UNKNOWN:

```
DEMO DURATION = UNKNOWN
```

### Stage 12: Assess Demo Reliability

Every demo step receives:

| Dimension | Scale |
|-----------|-------|
| Reliability | HIGH / MEDIUM / LOW / UNKNOWN |
| Failure likelihood | LOW / MEDIUM / HIGH / UNKNOWN |
| Recoverability | IMMEDIATE / SIMPLE / MANUAL / DIFFICULT / NONE / UNKNOWN |

A low-reliability, high-importance step must receive remediation, simplification, fallback, or explicit human approval.

### Stage 13: Build Failure and Recovery Model

Identify failure classes:

- Application fails to load
- API timeout
- Backend unavailable
- Authentication failure
- Database unavailable
- External service failure
- Invalid input
- Empty state
- Unexpected output
- Deployment issue
- Network interruption
- Browser issue
- Slow response
- Repeated action failure

For each failure: Failure ID / Trigger / Expected impact / Detection / Immediate action / Recovery path / Fallback / Presenter response / Evidence requirement / Severity / Status

Never instruct the presenter to fabricate successful output.

### Stage 14: Build Fallback Strategy

Every critical demo flow must have a fallback where practical.

Fallback categories:

- Live retry
- Alternate route
- Preloaded demo data
- Local fallback
- Static evidence
- Recorded backup
- Screenshot evidence
- Test output
- Secondary environment

Clearly label fallback evidence. Never present a recording or screenshot as live runtime behavior.

### Stage 15: Build Demo Checkpoints

Checkpoint categories:

- application loaded
- authentication ready
- database ready
- test data ready
- core action ready
- output verified
- differentiator ready
- evidence ready
- fallback ready
- final state ready

Each checkpoint: Checkpoint ID / Condition / Verification method / Expected result / Status / Evidence / Owner / Recovery action

### Stage 16: Assign Demo Priorities

Priority system:

| Priority | Definition |
|----------|------------|
| DEMO-P0 | Demo blocker / critical |
| DEMO-P1 | Judge-visible high value |
| DEMO-P2 | Useful but non-critical |
| DEMO-P3 | Optional polish |
| DROP | Remove from demo |

Every demo item must receive exactly one priority.

### Stage 17: Build Rehearsal Plan

Rehearsal statuses:

- NOT_STARTED
- PLANNED
- IN_PROGRESS
- PASSED
- FAILED
- BLOCKED
- UNKNOWN

Each rehearsal captures:

- Run ID / Timestamp / Duration / Steps completed / Failures / Recovery attempts / Observed delays / Unexpected behavior / Evidence / Final result

A rehearsal marked PASSED must have actual evidence.

### Stage 18: Determine Demo Readiness Gate

Gate values:

| Value | Meaning |
|-------|---------|
| NOT_READY | Insufficient evidence for meaningful review |
| PREPARING | Review is actively incomplete |
| BLOCKED | Critical dependency prevents validation |
| CONDITIONAL | Major unknowns remain, but review produced useful results |
| READY | Critical demo surfaces reviewed sufficiently |

READY requires:

- Primary flow verified
- Core output verified
- Critical claims supported
- Critical failures understood
- Fallback available where needed
- Timing known or explicitly UNKNOWN
- Rehearsal completed
- No unresolved critical demo blocker

If any critical requirement is UNKNOWN, do not silently mark READY.

### Stage 19: Apply Time-Aware Demo Strategy

| Time Remaining | Priority Focus |
|----------------|----------------|
| >24 hours | Full reliable demo, fallback infrastructure, multiple rehearsals, polished judge-visible flow, evidence capture |
| 12–24 hours | Complete happy path, reliability, one fallback, evidence mapping, rehearsal |
| 6–12 hours | Core demo, critical path, reliability, failure recovery, judge-visible differentiation, evidence |
| 2–6 hours | Freeze features, stabilize demo, remove fragile demo steps, rehearse, capture backup evidence |
| <2 hours | Freeze scope. Only demo-critical bug fixes, reliability fixes, deployment fixes, evidence verification, rehearsal, backup preparation |

If time is UNKNOWN:

```
DEMO DURATION = UNKNOWN
```

### Stage 20: Update Project State

Update ONLY these compact fields in `.sherpa/project-state.md`:

| Field | Allowed Values |
|-------|---------------|
| Demo Preparation Status | NOT_STARTED | IN_PROGRESS | BLOCKED | COMPLETE |
| Demo Objective | UNKNOWN | DEFINED |
| Demo Flow Status | UNKNOWN | DEFINED | REVIEWED |
| Demo Checkpoints | UNKNOWN | IDENTIFIED | REVIEWED |
| Demo Readiness Gate | NOT_READY | PREPARING | BLOCKED | CONDITIONAL | READY |
| Demo Critical Findings | UNKNOWN | NONE | IDENTIFIED |

Rules:

- Do NOT put detailed demo analysis inside project-state.md.
- Detailed material goes to `.sherpa/demo-preparation.md` and `.sherpa/demo/`.
- Do not change `selected idea`.
- Do not silently change architecture.
- Human approval required for major demo scope changes.

### Stage 21: Return Exactly One Primary Next Action

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

After DEMO-PREPARE completes:

- [ ] Project state read and verified
- [ ] Phase 11–15 evidence consumed (not duplicated)
- [ ] Repository inspected for evidence
- [ ] Demo objective defined
- [ ] Demo narrative built
- [ ] Demo flow constructed
- [ ] Demo evidence mapped
- [ ] Demo claim matrix created
- [ ] Judge-visible moments identified
- [ ] Presenter talking points prepared
- [ ] Demo timing model built
- [ ] Demo reliability assessed
- [ ] Failure and recovery model built
- [ ] Fallback strategy created
- [ ] Demo checkpoints defined
- [ ] Demo priorities assigned
- [ ] Rehearsal plan built
- [ ] Demo readiness gate evaluated
- [ ] Time-aware demo strategy applied
- [ ] Project state updated with compact fields only
- [ ] No Phase 1–15 artifacts modified
- [ ] No application source code modified
- [ ] No PPT created
- [ ] No final presentation performed
- [ ] No final submission performed
- [ ] No postmortem performed
- [ ] No demo claim fabricated
- [ ] Exactly ONE primary next action returned
