# HackathonOS — Presentation Rules

Official judging criteria define how the project will be evaluated. Use official judging criteria when available. Do not invent official judging criteria.

**Lifecycle Phase:** Phase 17 — PPT / Presentation Intelligence  
**Purpose:** Authoritative rules for presentation preparation. Phase 17 reviews and recommends; it does not implement, replace prior phases, or modify locked artifacts. Phase 17 optimizes for judge comprehension, credibility, and evidence coverage within presentation constraints, not visual decoration alone.

---

## 1. Purpose and Boundaries

Phase 17 converts validated project evidence into a coherent, evidence-backed presentation plan. It answers:

> "What should the presentation communicate? Which slides are necessary? What evidence proves each claim? Is the presentation ready?"

### Phase 17 MAY:

- Inspect official judging criteria
- Inspect Phase 11 testing/security evidence
- Inspect Phase 12 UX evidence
- Inspect Phase 13 red-team evidence
- Inspect Phase 14 judge simulation evidence
- Inspect Phase 15 score optimization priorities
- Inspect Phase 16 demo preparation evidence
- Inspect repository/project evidence
- Build presentation strategy
- Build slide architecture
- Build slide ordering
- Define slide objectives
- Map slides to judging criteria
- Map claims to evidence
- Build presentation narrative
- Plan slide content
- Place evidence on slides
- Design judge takeaways
- Calculate presentation timing
- Assign slide priorities
- Identify presentation risks
- Prepare speaker guidance
- Prepare Q&A inputs
- Determine presentation readiness gate
- Prioritize presentation-critical issues
- Create prioritized presentation preparation tasks
- Recommend what to present next
- Update Phase 17 artifacts and project state

### Phase 17 MUST NOT:

- Reselect the idea
- Redesign product architecture
- Perform core implementation work
- Execute testing or security verification
- Execute red-team attacks
- Execute demo
- Perform final audit
- Perform submission
- Perform post-mortem
- Silently modify application code
- Silently modify Phase 1–16 artifacts
- Silently redesign architecture
- Replace Phase 11 testing/security
- Replace Phase 12 UX review
- Replace Phase 13 red-team
- Replace Phase 14 judge simulation
- Replace Phase 15 score optimization
- Replace Phase 16 demo preparation
- Claim presentation readiness without evidence
- Fabricate judge feedback
- Present unsupported presentation claims
- Treat presentation readiness as official judging score

---

## 2. Evidence Model

Every important presentation claim must identify its evidence status.

Allowed evidence labels:

| Label | Definition |
|-------|------------|
| FACT | Directly observed from repository inspection, verified execution, or external source |
| INFERENCE | Logical conclusion drawn from observed facts |
| ASSUMPTION | Not yet verified; requires confirmation |
| UNKNOWN | No information available; not observed |

Rules:

- Never convert UNKNOWN into FACT.
- A feature existing in code does not prove a slide claim.
- Generated documentation is not proof of runtime behavior.
- A screenshot is evidence of what the screenshot shows, not necessarily current live behavior.
- Every observation cites reproducible evidence: path/line, route/screen, steps, result, or evidence artifact.
- Generated HackathonOS artifacts are not independent evidence.

Presentation evidence types:

| Type | Definition |
|------|------------|
| UI | User interface element or screen |
| output | Program output or result |
| test | Test execution result |
| log | Log or trace output |
| artifact | Generated file or artifact |
| live behavior | Observed live runtime behavior |
| screenshot | Static screenshot image |
| recording | Recorded video or demo |
| documentation | Documented claim |
| benchmark | Benchmark or measurement result |
| source/code inspection | Direct source code inspection |

---

## 3. Presentation Evidence vs Product Evidence

Keep these distinct:

- Product exists — The feature exists in code
- Product works — The feature functions correctly
- Product tested — The feature was verified through testing
- Product demonstrated — The feature was shown in a demo
- Product presented — The feature appears on a slide
- Product claim supported — Evidence backs the claim

A polished slide does not prove a capability.

---

## 4. Presentation Readiness vs Other Readiness

Keep separate:

- Product readiness — The product works
- Technical readiness — The architecture and implementation are sound
- Demo readiness — The demo can be reliably presented
- Presentation readiness — The slides and pitch are ready
- Submission readiness — The project is ready for submission

Do not merge these scores or statuses.

---

## 5. Presentation Score Separation

If Phase 17 produces any score or rating, explicitly label it:

```
INTERNAL PRESENTATION READINESS INDICATOR
NOT OFFICIAL JUDGING SCORE
```

Do not present a simulated presentation score as the competition's official score.

Do not use arbitrary hidden multipliers.

---

## 6. Presentation Is Not a Marketing Brochure

Prioritize:

- clarity
- evidence
- judge relevance
- differentiation
- technical credibility
- measurable value

Avoid:

- unsupported superlatives
- fake statistics
- fabricated traction
- invented user numbers
- invented market size
- invented performance
- unsupported claims

---

## 7. Judging Criteria

Use official judging criteria when available.

- use their exact terminology
- preserve official weights
- map slides to criteria
- identify uncovered criteria

If official criteria are unavailable:

```text
CRITERIA = UNKNOWN
```

Do not fabricate a rubric.

Any provisional framework must be explicitly labeled:

```
PROVISIONAL PRESENTATION FRAMEWORK
```

---

## 8. Slide Architecture

Each slide must contain:

| Field | Description |
|-------|-------------|
| Slide ID | Unique identifier |
| Title | Slide title |
| Purpose | Why this slide exists |
| Primary Message | The core message to communicate |
| Judge Takeaway | What the judge should remember |
| Content | Slide content description |
| Evidence | Evidence supporting claims |
| Target Criterion | Judging criterion this slide addresses |
| Priority | PPT-P0 / PPT-P1 / PPT-P2 / PPT-P3 / DROP |
| Time | Target time in minutes/seconds |
| Speaker Guidance | What the presenter should say |
| Visual Requirement | What should appear on screen |
| Risk | Presentation risk |
| Verification | How claims are verified |
| Status | PLANNED / EXECUTED / PASSED / FAILED / BLOCKED / UNKNOWN / NOT_APPLICABLE |

Slide types:

- Title
- Problem
- User
- Existing gap
- Solution
- Product flow
- Core features
- Differentiation
- Innovation
- Technical architecture
- AI/ML methodology
- Security/privacy
- Results
- Validation
- Impact
- Business/use case
- Demo transition
- Roadmap
- Closing
- Q&A

Do not force every project to use every slide type.

---

## 9. Slide Priority System

| Priority | Definition |
|----------|------------|
| PPT-P0 | Essential / judging-critical |
| PPT-P1 | High-value |
| PPT-P2 | Useful |
| PPT-P3 | Optional |
| DROP | Remove |

Priority must consider: judging value, evidence strength, judge visibility, time, redundancy, risk, complexity.

Every slide must receive exactly one priority.

---

## 10. Presentation Narrative

Build a coherent narrative:

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

Adapt structure to project type, judging rubric, available time, evidence, and demo flow.

Avoid generic slide stuffing.

---

# 11. Time-Aware Presentation Strategy

| Time Remaining | Priority Focus |
|----------------|----------------|
| >24 hours | Comprehensive slide structure, multiple review cycles, visual refinement, rehearsal, Q&A preparation |
| 12–24 hours | Essential slides, evidence, timing, judge criteria, speaker notes |
| 6–12 hours | P0 slides, P1 judge-visible content, evidence, rehearsal, clarity |
| 2–6 hours | Freeze content, remove redundancy, timing, claims, evidence, readability, rehearsal |
| <2 hours | Freeze slide structure, only critical corrections, evidence corrections, factual corrections, timing fixes, final verification |

If presentation time is UNKNOWN:

```
PRESENTATION TIME = UNKNOWN
```

Never invent presentation duration.

---

# 12. Slide-to-Criterion Mapping

Mapping:

```text
Judging Criterion
    → Presentation Slide
    → Claim
    → Evidence
    → Judge Takeaway
```

Mapping statuses: SUPPORTED / PARTIALLY_SUPPORTED / UNKNOWN / CONTRADICTED / NOT_APPLICABLE

Identify:

- uncovered criteria
- weakly supported criteria
- overrepresented criteria
- redundant slides

Do not create unsupported evidence to fill gaps.

If judging criteria are unavailable:

```text
CRITERION = UNKNOWN
```

Do not invent judging criteria.

---

# 13. Claim Credibility

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

---

# 14. Numbers and Metrics

For each metric record:

| Field | Description |
|-------|-------------|
| Metric | Metric name |
| Value | Metric value |
| Unit | Unit of measurement |
| Source | Where the value came from |
| Measurement Method | How it was measured |
| Date | When it was measured |
| Evidence Status | FACT / INFERENCE / ASSUMPTION / UNKNOWN |
| Confidence | HIGH / MEDIUM / LOW / UNKNOWN |

Before using: user counts, accuracy, latency, revenue, savings, growth, adoption, performance, benchmark results, market size, percentage improvements — all require evidence.

Never fabricate precision.

If a number cannot be verified:

```
UNKNOWN
```

or use a clearly qualitative statement.

---

# 15. Technical Presentation

Technical slides must communicate credibility without unnecessary complexity.

Potential technical evidence:

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

Do not claim technologies that were not actually used.

Do not invent architecture diagrams.

Architecture evidence must originate from Phase 3/4 and verified implementation evidence.

---

# 16. AI / ML Claims

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

---

# 17. Demo Integration

Consume Phase 16.

The presentation must connect naturally to the demo.

Use:

- demo objective
- primary demo flow
- judge-visible moments
- demo claims
- evidence
- fallback information
- timing

Do not duplicate the entire demo inside the PPT.

The presentation should prepare the judge to understand the demo.

---

# 18. Judge Simulation Integration

Consume Phase 14.

Use:

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

---

# 19. Score Optimization Integration

Consume Phase 15.

Use:

- P0 improvements
- P1 improvements
- evidence weaknesses
- differentiation opportunities
- criterion gaps

Do not recreate the score optimization system.

Phase 17 consumes its outputs.

---

# 20. UX / Security / Red Team Integration

Consume relevant evidence from:

- Phase 11 — Testing + Security
- Phase 12 — UX Review
- Phase 13 — Red Team

Only include findings relevant to presentation credibility.

Do not hide critical known issues.

If a limitation materially affects a claim, surface it appropriately.

---

# 21. Presentation Timing Model

Derive timing from actual competition constraint.

If presentation duration is UNKNOWN:

```
PRESENTATION TIME = UNKNOWN
```

Never invent presentation duration.

Total slide duration must be checked against available presentation time.

---

# 22. Speaker Guidance

For every important slide:

```text
SHOW:   What appears on screen.
SAY:    What presenter communicates.
PROVE:  Evidence supporting the claim.
EMPHASIZE: What judge should remember.
AVOID:  Potential misleading or unnecessary claims.
TRANSITION: How to move to the next slide.
```

Phase 17 only prepares presentation-specific speaking guidance. Phase 17 does not write a complete unrelated speech.

---

# 23. Visual Evidence

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

---

# 24. Redundancy Analysis

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

---

# 25. Presentation Risk Model

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

- Severity: CRITICAL / HIGH / MEDIUM / LOW / UNKNOWN
- Likelihood
- Detectability
- Recoverability
- Mitigation
- Owner
- Status

Do not collapse confidence and severity into one number.

---

# 26. Q&A Preparation Input

For each likely question:

| Field | Description |
|-------|-------------|
| Question | The question text |
| Related Slide | Slide that addresses this |
| Evidence | Supporting evidence |
| Answer Readiness | READY / PARTIALLY_READY / WEAK / UNKNOWN / NOT_APPLICABLE |
| Risk | Question risk |
| Recommended Response | Suggested answer |

Never fabricate an answer.

---

# 27. Presentation Readiness Gate

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

---

# 28. Internal Presentation Score

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

---

# 29. Unknown Handling

Unknown information must remain UNKNOWN.

Examples:

- unknown presentation duration
- unknown slide limit
- unknown judging rubric
- unknown audience
- unknown required format
- unknown metric
- unknown benchmark
- unknown evidence

Never silently infer.

---

# 30. Project State Fields

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

---

# 31. Failure Cases

| Case | Behavior |
|------|----------|
| No selected idea | Stop and request confirmation |
| Missing Phase 16 evidence | Report PRESENTATION-PREPARE = LIMITED; proceed with available evidence |
| Missing evidence | Mark UNKNOWN |
| No judging criteria | Mark UNKNOWN |
| Unknown presentation time | PRESENTATION TIME = UNKNOWN |
| No demo transition available | Mark CONDITIONAL or BLOCKED |
| Critical unsupported claim | Mark BLOCKED or CONDITIONAL |
| Human approval required for presentation scope change | Route to HUMAN DECISION REQUIRED |

Phase 17 MUST NOT:

- Write application code
- Modify application source files
- Modify frontend/backend implementation
- Install dependencies
- Deploy the application
- Change the selected idea
- Silently redesign architecture
- Replace Phase 11/12/13/14/15/16 engines
- Perform final audit
- Perform final submission
- Perform post-mortem
- Claim presentation readiness without evidence
- Fabricate judge feedback
- Present unsupported presentation claims

---

# 32. Determinism

Same evidence, criteria, time remaining, and presentation constraints → same presentation plan and priority classifications every time. No randomness. No LLM-generated scores without explicit numeric input.
