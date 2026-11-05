# Presentation Plan

**Project:** <project name or UNKNOWN>  
**Repository:** <repository root or UNKNOWN>  
**Plan date:** <UTC date/time>  
**Plan status:** NOT_STARTED | IN_PROGRESS | COMPLETE  
**Hackathon:** <name or UNKNOWN>  
**Time remaining:** <hours or UNKNOWN>  
**Time-aware strategy:** <category or UNKNOWN>  
**Selected idea:** <idea name or UNKNOWN>  
**Presentation duration:** <minutes or UNKNOWN>  
**Presentation readiness gate:** NOT_READY | PREPARING | BLOCKED | CONDITIONAL | READY  

---

## 1. Evidence Base Consumed

| Phase | Evidence Source | Status | Evidence Type |
|-------|----------------|--------|---------------|
| Phase 11 | `.sherpa/evidence/` testing/security artifacts | | FACT / INFERENCE / ASSUMPTION / UNKNOWN |
| Phase 12 | `.sherpa/ux-review.md`, `.sherpa/ux/` | | FACT / INFERENCE / ASSUMPTION / UNKNOWN |
| Phase 13 | `.sherpa/red-team.md`, `.sherpa/red-team/` | | FACT / INFERENCE / ASSUMPTION / UNKNOWN |
| Phase 14 | `.sherpa/judge-simulation.md` | | FACT / INFERENCE / ASSUMPTION / UNKNOWN |
| Phase 15 | `.sherpa/score-optimization.md` | | FACT / INFERENCE / ASSUMPTION / UNKNOWN |
| Phase 16 | `.sherpa/demo-preparation.md` | | FACT / INFERENCE / ASSUMPTION / UNKNOWN |
| Repository | Direct repository inspection | | FACT / INFERENCE / ASSUMPTION / UNKNOWN |

**Rule:** Do not claim evidence was consumed unless the artifact was actually read.

---

## 2. Presentation Objective

**Presentation objective:** <concise statement of what the judge should understand by the end of the presentation>

---

## 3. Presentation Narrative

| Section | Content | Included? | Time Estimate |
|---------|---------|-----------|---------------|
| Problem | | YES / NO / UNKNOWN | |
| Why it matters | | YES / NO / UNKNOWN | |
| Current gap | | YES / NO / UNKNOWN | |
| Solution | | YES / NO / UNKNOWN | |
| How it works | | YES / NO / UNKNOWN | |
| Why it is different | | YES / NO / UNKNOWN | |
| Proof | | YES / NO / UNKNOWN | |
| Demo | | YES / NO / UNKNOWN | |
| Impact | | YES / NO / UNKNOWN | |
| Closing | | YES / NO / UNKNOWN | |

**Rule:** Do not force all sections into the live presentation if time constraints make that harmful.

---

## 4. Slide Architecture

| Slide ID | Title | Purpose | Primary Message | Judge Takeaway | Content | Evidence | Target Criterion | Priority | Time | Speaker Guidance | Visual Requirement | Risk | Verification | Status |
|----------|-------|---------|-----------------|----------------|---------|----------|------------------|----------|------|------------------|--------------------|------|--------------|--------|
| | | | | | | | | PPT-P0 / P1 / P2 / P3 / DROP | | | | | | PLANNED / EXECUTED / PASSED / FAILED / BLOCKED / UNKNOWN / NOT_APPLICABLE |

Store detailed slides in `.sherpa/presentation/slide-NNN.md`.

---

## 5. Presentation Claims

| Claim ID | Claim | Evidence Source | Evidence Type | Evidence Status | Verification Method | Slide | Target Criterion | Confidence |
|----------|-------|-----------------|---------------|-----------------|---------------------|-------|------------------|------------|
| | | | UI / output / test / log / artifact / live behavior / screenshot / recording / documentation / benchmark / source/code inspection | FACT / INFERENCE / ASSUMPTION / UNKNOWN | | | | HIGH / MEDIUM / LOW / UNKNOWN |

**Rule:** No evidence → UNKNOWN. Weak evidence cannot be upgraded merely because a slide exists.

---

## 6. Slide-to-Criterion Mapping

| Judging Criterion | Presentation Slide | Claim | Evidence | Mapping State | Expected Judge Takeaway |
|-------------------|--------------------|-------|----------|---------------|-------------------------|
| | | | | SUPPORTED / PARTIALLY_SUPPORTED / UNKNOWN / CONTRADICTED / NOT_APPLICABLE | |

If judging criteria are unavailable:

```
CRITERION = UNKNOWN
```

---

## 7. Claim Credibility

| Claim ID | Claim | Credibility Status | Reasoning | Evidence | Action |
|----------|-------|-------------------|-----------|----------|--------|
| | | VERIFIED / SUPPORTED / PARTIALLY_SUPPORTED / UNSUPPORTED / CONTRADICTED / UNKNOWN | | | REMOVE / WEAKEN / QUALIFY / KEEP |

---

## 8. Numbers and Metrics

| Metric | Value | Unit | Source | Measurement Method | Date | Evidence Status | Confidence |
|--------|-------|------|--------|--------------------|------|-----------------|------------|
| | | | | | | FACT / INFERENCE / ASSUMPTION / UNKNOWN | HIGH / MEDIUM / LOW / UNKNOWN |

**Rule:** Never fabricate precision. If a number cannot be verified: UNKNOWN.

---

## 9. Technical Presentation

| Technical Element | Description | Evidence | Evidence Status | Confidence |
|-------------------|-------------|----------|-----------------|--------------|
| Architecture | | | FACT / INFERENCE / ASSUMPTION / UNKNOWN | HIGH / MEDIUM / LOW / UNKNOWN |
| Data Flow | | | | |
| API Structure | | | | |
| Model Pipeline | | | | |
| Database | | | | |
| Security Controls | | | | |
| Testing | | | | |
| Deployment | | | | |
| Performance | | | | |
| Failure Handling | | | | |

**Rule:** Do not claim technologies not actually used. Do not invent architecture diagrams.

---

## 10. AI / ML Claims

**AI Present:** YES / NO / UNKNOWN

| AI Element | Description | Evidence | Evidence Status | Confidence |
|------------|-------------|----------|-----------------|------------|
| Model Used | | | | |
| Training Data | | | | |
| Preprocessing | | | | |
| Inference | | | | |
| Evaluation | | | | |
| Measured Performance | | | | |
| Limitations | | | | |

**Rule:** Never claim "100% accurate", "production ready", "industry-leading", "state-of-the-art" unless evidence supports it. If no AI: AI = NOT_APPLICABLE.

---

## 11. Demo Integration

| Demo Element | Value |
|--------------|-------|
| Demo Objective | |
| Primary Demo Flow | |
| Judge-Visible Moments | |
| Demo Claims | |
| Demo Evidence | |
| Demo Fallback Information | |
| Demo Timing | |

**Rule:** Do not duplicate the entire demo inside the PPT. The presentation should prepare the judge to understand the demo.

---

## 12. Judge Simulation Integration

| Judge Simulation Element | Value |
|--------------------------|-------|
| Judge Questions | |
| Skeptical Follow-ups | |
| Weak Claims | |
| Evidence Gaps | |
| Credibility Concerns | |

---

## 13. Score Optimization Integration

| Score Opt Element | Value |
|-------------------|-------|
| P0 Improvements | |
| P1 Improvements | |
| Evidence Weaknesses | |
| Differentiation Opportunities | |
| Criterion Gaps | |

---

## 14. UX / Security / Red Team Integration

| Finding Source | Finding | Relevance to Presentation | Evidence Status |
|----------------|---------|---------------------------|-----------------|
| Phase 11 Testing/Security | | | |
| Phase 12 UX | | | |
| Phase 13 Red Team | | | |

**Rule:** Only include findings relevant to presentation credibility. Do not hide critical known issues.

---

## 15. Presentation Timing Model

| Segment | Target Time | Priority |
|---------|-------------|----------|
| | | |

**Rule:** Derive timing from actual competition constraint, available presentation time, project complexity, reliability, judge attention, and number of critical slides. Total slide duration must be checked against available presentation time. If demo duration is UNKNOWN: PRESENTATION TIME = UNKNOWN.

---

## 16. Speaker Guidance

| Slide ID | ACTION | SAY | PROVE | EMPHASIZE | AVOID | TRANSITION |
|----------|--------|-----|-------|-----------|-------|------------|
| | | | | | | |

**Rule:** Phase 17 only prepares presentation-specific speaking guidance.

---

## 17. Visual Evidence

| Slide ID | Visual Type | Description | Evidence Source | Improves Comprehension? | Improves Credibility? |
|----------|-------------|-------------|-----------------|------------------------|-----------------------|
| | screenshot / architecture diagram / chart / UI flow / table / metric / code excerpt / test evidence / demo frame / no visual | | | YES / NO / UNKNOWN | YES / NO / UNKNOWN |

**Rule:** Do not add visuals merely for decoration.

---

## 18. Redundancy Analysis

| Redundant Element | Occurrences | Action |
|-------------------|-------------|--------|
| | | merge / simplify / remove |

**Rule:** Unless the judging rubric explicitly requires separate coverage.

---

## 19. Presentation Risk Model

| Risk ID | Risk | Severity | Likelihood | Detectability | Recoverability | Mitigation | Owner | Status |
|---------|------|----------|------------|---------------|----------------|------------|-------|--------|
| | | CRITICAL / HIGH / MEDIUM / LOW / UNKNOWN | LOW / MEDIUM / HIGH / UNKNOWN | | | | | |

Do not collapse confidence and severity into one number.

---

## 20. Q&A Preparation Input

| Question ID | Question | Related Slide | Evidence | Answer Readiness | Risk | Recommended Response |
|-------------|----------|---------------|----------|------------------|------|----------------------|
| | | | | READY / PARTIALLY_READY / WEAK / UNKNOWN / NOT_APPLICABLE | | |

**Rule:** Never fabricate an answer.

---

## 21. Presentation Readiness Gate

**Current Gate:** NOT_READY | PREPARING | BLOCKED | CONDITIONAL | READY

**Reason against every READY criterion:**

- Essential slides defined:
- Critical claims supported:
- Criteria mapped where available:
- Timing verified or explicitly UNKNOWN:
- No critical unsupported claims:
- Demo transition defined:
- Speaker guidance available for critical slides:
- Presentation sequence coherent:
- Evidence available:
- Critical risks addressed:

---

## 22. Internal Presentation Score

**INTERNAL PRESENTATION READINESS INDICATOR**  
**NOT OFFICIAL JUDGING SCORE**

| Dimension | Value |
|-----------|-------|
| Evidence Coverage | |
| Criterion Coverage | |
| Narrative Clarity | |
| Timing Confidence | |
| Claim Credibility | |
| Demo Integration | |
| Judge Comprehension | |

**Rule:** No arbitrary hidden multipliers.

---

## 23. Unknowns

| Unknown | Why Unknown | Impact | Source |
|---------|-------------|--------|--------|
| | | | |

---

## 24. Recommended Next Action

**PRIMARY NEXT ACTION:** <exactly one action>

**WHY:** <explanation based on impact, time, risk, and judging criteria>

**DONE WHEN:** <clear definition of done>

**Time remaining:** <hours or UNKNOWN>

**Blocked by:** <blocker or "None">

**Rule:** Exactly one primary next action. Do not produce competing alternatives.

---

## 25. Validation Checklist

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
- [ ] No presentation claim fabricated
- [ ] Exactly ONE primary next action returned
