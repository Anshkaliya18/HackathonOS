# HackathonOS — Demo Preparation Rules

**Lifecycle Phase:** Phase 16 — Demo Preparation Intelligence  
**Purpose:** Authoritative rules for demo preparation. Phase 16 reviews and recommends; it does not implement, replace prior phases, or modify locked artifacts. Phase 16 optimizes for reliable judge comprehension and credible proof under real demo constraints, not feature quantity.

---

## 1. Purpose and Boundaries

Phase 16 converts validated project evidence into a reliable, judge-oriented, time-bounded demonstration plan. It answers:

> "What exactly should be demonstrated, in what order, what evidence proves each claim, what happens if something fails, and is the demo ready?"

### Phase 16 MAY:

- Inspect official judging criteria
- Inspect Phase 11 testing/security evidence
- Inspect Phase 12 UX evidence
- Inspect Phase 13 red-team evidence
- Inspect Phase 14 judge simulation evidence
- Inspect Phase 15 score optimization priorities
- Inspect repository/project evidence
- Build demo objective
- Build demo narrative
- Build demo flow
- Identify demo checkpoints
- Map demo evidence
- Identify demo risks
- Build fallback strategy
- Build rehearsal plan
- Determine demo readiness gate
- Prioritize demo-critical issues
- Create prioritized demo preparation tasks
- Recommend what to demonstrate next
- Update Phase 16 artifacts and project state

### Phase 16 MUST NOT:

- Reselect the idea
- Redesign product architecture
- Core implementation work
- Create official judging scores
- Create PPT / presentation materials
- Perform final submission
- Perform post-mortem
- Silently modify application code
- Silently modify Phase 1–15 artifacts
- Silently redesign architecture
- Replace Phase 11 testing/security
- Replace Phase 12 UX review
- Replace Phase 13 red-team
- Replace Phase 14 judge simulation
- Replace Phase 15 score optimization
- Claim demo readiness without evidence
- Fabricate judge feedback
- Present unsupported demo claims
- Treat demo readiness as official judging score

---

## 2. Evidence Model

Every demo claim must identify its evidence status.

Allowed evidence labels:

| Label | Definition |
|-------|------------|
| FACT | Directly observed from repository inspection, verified execution, or external source |
| INFERENCE | Logical conclusion drawn from observed facts |
| ASSUMPTION | Not yet verified; requires confirmation |
| UNKNOWN | No information available; not observed |

Rules:

- Never convert UNKNOWN into FACT.
- A feature existing in code does not prove that it works during the demo.
- Generated documentation is not proof of runtime behavior.
- A screenshot is evidence of what the screenshot shows, not necessarily current live behavior.
- A successful previous run does not automatically prove current runtime reliability.
- Every observation cites reproducible evidence: path/line, route/screen, steps, result, or evidence artifact.
- Generated HackathonOS artifacts are not independent evidence.

Demo evidence types:

| Type | Definition |
|------|------------|
| UI | User interface element or screen |
| output | Program output or result |
| test | Test execution result |
| log | Log or trace output |
| artifact | Generated file or artifact |
| live behavior | Observed live runtime behavior |
| documentation | Documented claim |

---

## 3. Demo Evidence vs Product Evidence

Keep these distinct:

- Product capability — The feature exists
- Demonstrated capability — The feature works in a demo context
- Evidence-backed capability — Evidence proves the capability
- Claimed capability — The project claims the capability

A feature existing in code does not prove demo readiness.

---

## 4. Demo Readiness vs Other Readiness

Keep separate:

- Product readiness — The product works
- Technical readiness — The architecture and implementation are sound
- Demo readiness — The demo can be reliably presented
- Presentation readiness — The PPT and pitch are ready

Do not merge these scores or statuses.

---

## 5. Demo Score Separation

If Phase 16 produces any score or rating, explicitly label it:

```
SIMULATED DEMO ASSESSMENT
NOT OFFICIAL JUDGING SCORE
```

Do not present a simulated demo score as the competition's official score.

Do not use hidden multipliers or arbitrary scoring formulas.

---

## 6. Reliability Beats Complexity

When two demo flows communicate similar value:

- Prefer the more reliable flow.
- Do not recommend fragile features merely because they are technically impressive.

---

## 7. Demo Objective Model

Template:

> "By the end of the demo, the judge should understand that [PROJECT] solves [PROBLEM] for [USER] by [CORE MECHANISM], producing [VERIFIABLE RESULT]."

Every demo step should contribute to this objective. Flag unnecessary steps.

---

## 8. Demo Narrative Model

Structured narrative sections:

1. Problem
2. User/context
3. Solution
4. Core interaction
5. Differentiator
6. Technical credibility
7. Result
8. Impact
9. Closing takeaway

Do not force all nine sections into the live demo if time constraints make that harmful. Use time-aware selection.

---

## 9. Time-Aware Demo Strategy

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

Never fabricate a demo duration or competition limit.

---

## 10. Demo Priority System

| Priority | Definition |
|----------|------------|
| DEMO-P0 | Demo blocker / critical — must be fixed or explicitly accepted |
| DEMO-P1 | Judge-visible high value |
| DEMO-P2 | Useful but non-critical |
| DEMO-P3 | Optional polish |
| DROP | Remove from demo |

Priority must consider: judge visibility, value, reliability, evidence strength, time, risk, dependencies.

Every demo item must receive exactly one priority.

---

## 11. Demo Reliability Model

Every demo step receives:

| Dimension | Scale |
|-----------|-------|
| Reliability | HIGH / MEDIUM / LOW / UNKNOWN |
| Failure likelihood | LOW / MEDIUM / HIGH / UNKNOWN |
| Recoverability | IMMEDIATE / SIMPLE / MANUAL / DIFFICULT / NONE / UNKNOWN |

A low-reliability, high-importance step must receive remediation, simplification, fallback, or explicit human approval.

---

## 12. Failure and Recovery Model

Failure classes:

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

Every failure must contain:

- Failure ID
- Trigger
- Expected impact
- Detection
- Immediate action
- Recovery path
- Fallback
- Presenter response
- Evidence requirement
- Severity
- Status

Never instruct the presenter to fabricate successful output.

---

## 13. Fallback Strategy

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

---

## 14. Demo Checkpoints

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

Each checkpoint must contain:

- Checkpoint ID
- Condition
- Verification method
- Expected result
- Status
- Evidence
- Owner
- Recovery action

---

## 15. Demo Claim Matrix

Mapping:

```text
Judging Criterion
    → Project Claim
    → Demo Step
    → Evidence
    → Expected Judge Takeaway
```

Mapping states: SUPPORTED / PARTIALLY_SUPPORTED / UNKNOWN / CONTRADICTED / NOT_APPLICABLE

If judging criteria are unavailable:

```
CRITERION = UNKNOWN
```

Do not invent judging criteria.

---

## 16. Judge-Visible Moments

Each moment must contain:

- Moment ID
- What judge should notice
- How it is demonstrated
- Evidence
- Expected takeaway
- Confidence
- Time cost
- Risk

Moments include: problem relevance, solution value, innovation, differentiation, technical sophistication, reliability, UX quality, security/privacy, measurable result, real-world usefulness.

---

## 17. Presenter Talking Points

For each major demo step:

```text
ACTION: What the presenter does.
SAY: What the presenter says.
SHOW: What the judge sees.
PROVE: What evidence supports the claim.
TRANSITION: How to move to the next step.
```

Phase 16 only prepares demo-specific speaking guidance. Phase 17 owns presentation construction.

---

## 18. Demo Timing Model

Example timing plan:

| Segment | Target Time | Priority |
|---------|-------------|----------|
| Problem | 30 sec | P0 |
| Solution | 30 sec | P0 |
| Core flow | 2 min | P0 |
| Differentiator | 1 min | P1 |
| Technical proof | 45 sec | P1 |
| Result | 30 sec | P0 |
| Closing | 30 sec | P0 |

Derive actual timing from competition constraints, available demo time, project complexity, reliability, judge attention, and number of critical steps.

---

## 19. Rehearsal System

Rehearsal statuses:

- NOT_STARTED
- PLANNED
- IN_PROGRESS
- PASSED
- FAILED
- BLOCKED
- UNKNOWN

Each rehearsal captures:

- Run ID
- Timestamp
- Duration
- Steps completed
- Failures
- Recovery attempts
- Observed delays
- Unexpected behavior
- Evidence
- Final result

A rehearsal marked PASSED must have actual evidence.

---

## 20. Demo Readiness Gate

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

---

## 21. Demo Readiness Score

If useful, a demo readiness score is an internal readiness indicator only.

```
SIMULATED DEMO ASSESSMENT
NOT OFFICIAL JUDGING SCORE
```

Do not use arbitrary hidden multipliers.

---

## 22. Integration with Previous Phases

Phase 16 consumes evidence from:

- Phase 11 — Testing + Security (verified tests, critical failures, security findings)
- Phase 12 — UX Review (critical UX issues, usability findings, demo flow observations)
- Phase 13 — Red Team (critical findings, adversarial failures, recoverability)
- Phase 14 — Judge Simulation (judge questions, skeptical follow-ups, weak claims, evidence gaps)
- Phase 15 — Score Optimization (P0/P1 improvements, judge-visible priorities)

Phase 16 does not replace those phases.

---

## 23. Human Authority

Human approval is required for:

- Removing an important feature from the demo
- Changing core demo scope
- Changing the primary user journey
- Major architecture changes
- Destructive changes
- Disabling production functionality
- Irreversible demo configuration
- Major dependency changes
- Claims that materially affect judging credibility

AI recommends. Human decides.

---

## 24. Project State Fields

Update ONLY these compact fields in `.hackathon/project-state.md`:

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
- Detailed material goes to `.hackathon/demo-preparation.md` and `.hackathon/demo/`.
- Do not change `selected idea`.
- Do not silently change architecture.
- Human approval required for major demo scope changes.

---

## 25. Failure Cases

| Case | Behavior |
|------|----------|
| No selected idea | Stop and request confirmation |
| Missing Phase 15 evidence | Report DEMO-PREPARE = LIMITED; proceed with available evidence |
| Missing demo evidence | Mark UNKNOWN |
| Unreliable core flow | Mark BLOCKED |
| No fallback available | Mark BLOCKED or CONDITIONAL |
| Unknown demo duration | DEMO DURATION = UNKNOWN |
| Human approval required for demo scope change | Route to HUMAN DECISION REQUIRED |

Phase 16 MUST NOT:

- Write application code
- Modify application source files
- Modify frontend/backend implementation
- Install dependencies
- Deploy the application
- Change the selected idea
- Silently redesign architecture
- Replace Phase 11/12/13/14/15 engines
- Perform final presentation generation
- Perform final submission
- Perform post-mortem
- Claim demo readiness without evidence
- Fabricate judge feedback
- Present unsupported demo claims

---

## 26. Determinism

Same evidence, criteria, time remaining, and demo constraints → same demo preparation plan and priority classifications every time. No randomness. No LLM-generated scores without explicit numeric input.
