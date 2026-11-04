# Demo Plan

**Project:** <project name or UNKNOWN>  
**Repository:** <repository root or UNKNOWN>  
**Plan date:** <UTC date/time>  
**Plan status:** NOT_STARTED | IN_PROGRESS | COMPLETE  
**Hackathon:** <name or UNKNOWN>  
**Time remaining:** <hours or UNKNOWN>  
**Time-aware strategy:** <category or UNKNOWN>  
**Selected idea:** <idea name or UNKNOWN>  
**Demo duration:** <hours/minutes or UNKNOWN>  
**Demo readiness gate:** NOT_READY | PREPARING | BLOCKED | CONDITIONAL | READY  

---

## 1. Evidence Base Consumed

| Phase | Evidence Source | Status | Evidence Type |
|-------|----------------|--------|---------------|
| Phase 11 | `.sherpa/evidence/` testing/security artifacts | | FACT / INFERENCE / ASSUMPTION / UNKNOWN |
| Phase 12 | `.sherpa/ux-review.md`, `.sherpa/ux/` | | FACT / INFERENCE / ASSUMPTION / UNKNOWN |
| Phase 13 | `.sherpa/red-team.md`, `.sherpa/red-team/` | | FACT / INFERENCE / ASSUMPTION / UNKNOWN |
| Phase 14 | `.sherpa/judge-simulation.md` | | FACT / INFERENCE / ASSUMPTION / UNKNOWN |
| Phase 15 | `.sherpa/score-optimization.md` | | FACT / INFERENCE / ASSUMPTION / UNKNOWN |
| Repository | Direct repository inspection | | FACT / INFERENCE / ASSUMPTION / UNKNOWN |

**Rule:** Do not claim evidence was consumed unless the artifact was actually read.

---

## 2. Demo Objective

**Demo objective:** <concise statement of what the judge should understand by the end of the demo>

---

## 3. Demo Narrative

| Section | Content | Included? | Time Estimate |
|---------|---------|-----------|---------------|
| Problem | | YES / NO / UNKNOWN | |
| User/context | | YES / NO / UNKNOWN | |
| Solution | | YES / NO / UNKNOWN | |
| Core interaction | | YES / NO / UNKNOWN | |
| Differentiator | | YES / NO / UNKNOWN | |
| Technical credibility | | YES / NO / UNKNOWN | |
| Result | | YES / NO / UNKNOWN | |
| Impact | | YES / NO / UNKNOWN | |
| Closing takeaway | | YES / NO / UNKNOWN | |

**Rule:** Do not force all sections into the live demo if time constraints make that harmful.

---

## 4. Demo Flow

| Step ID | Step Name | Purpose | Presenter Action | System Action | Expected Result | Evidence | Time Estimate | Reliability | Failure Risk | Recovery | Fallback | Status |
|---------|-----------|---------|------------------|---------------|---------------|----------|---------------|-------------|--------------|----------|----------|--------|
| | | | | | | | | HIGH / MEDIUM / LOW / UNKNOWN | LOW / MEDIUM / HIGH / UNKNOWN | | | | PLANNED / EXECUTED / PASSED / FAILED / BLOCKED / UNKNOWN / NOT_APPLICABLE |

Store detailed steps in `.sherpa/demo/flow-NNN.md`.

---

## 5. Demo Evidence

| Claim ID | Claim | Evidence | Evidence Type | Evidence Status | Verification | Demo Step | Confidence |
|----------|-------|----------|---------------|-----------------|--------------|-----------|------------|
| | | | UI / output / test / log / artifact / live behavior / documentation | FACT / INFERENCE / ASSUMPTION / UNKNOWN | | | HIGH / MEDIUM / LOW / UNKNOWN |

**Rule:** No evidence → UNKNOWN. Weak evidence cannot be upgraded merely because the feature exists.

---

## 6. Demo Claim Matrix

| Judging Criterion | Project Claim | Demo Step | Evidence | Mapping State | Expected Judge Takeaway |
|-------------------|---------------|-----------|----------|---------------|-------------------------|
| | | | | SUPPORTED / PARTIALLY_SUPPORTED / UNKNOWN / CONTRADICTED / NOT_APPLICABLE | |

If judging criteria are unavailable:

```
CRITERION = UNKNOWN
```

---

## 7. Judge-Visible Moments

| Moment ID | What Judge Should Notice | How Demonstrated | Evidence | Expected Takeaway | Confidence | Time Cost | Risk |
|-----------|-------------------------|------------------|----------|-------------------|------------|-----------|------|
| | | | | | HIGH / MEDIUM / LOW / UNKNOWN | | |

---

## 8. Presenter Talking Points

| Step ID | ACTION | SAY | SHOW | PROVE | TRANSITION |
|---------|--------|-----|------|-------|------------|
| | | | | | |

**Rule:** Phase 16 only prepares demo-specific speaking guidance. Phase 17 owns presentation construction.

---

## 9. Demo Timing Model

| Segment | Target Time | Priority |
|---------|-------------|----------|
| | | |

**Rule:** Derive timing from competition constraints, available demo time, project complexity, reliability, judge attention, and number of critical steps. If demo duration is UNKNOWN, mark DEMO DURATION = UNKNOWN.

---

## 10. Demo Reliability

| Step ID | Reliability | Failure Likelihood | Recoverability |
|---------|-------------|-------------------|----------------|
| | HIGH / MEDIUM / LOW / UNKNOWN | LOW / MEDIUM / HIGH / UNKNOWN | IMMEDIATE / SIMPLE / MANUAL / DIFFICULT / NONE / UNKNOWN |

A low-reliability, high-importance step must receive remediation, simplification, fallback, or explicit human approval.

---

## 11. Failure and Recovery Model

| Failure ID | Trigger | Expected Impact | Detection | Immediate Action | Recovery Path | Fallback | Presenter Response | Evidence Requirement | Severity | Status |
|------------|---------|-----------------|-----------|------------------|---------------|----------|-------------------|----------------------|----------|--------|
| | | | | | | | | | CRITICAL / HIGH / MEDIUM / LOW / UNKNOWN | PLANNED / EXECUTED / PASSED / FAILED / BLOCKED / UNKNOWN |

Never instruct the presenter to fabricate successful output.

---

## 12. Fallback Strategy

| Flow | Fallback Category | Fallback Evidence | Labeled as Non-Live? |
|------|-------------------|-------------------|----------------------|
| | Live retry / Alternate route / Preloaded demo data / Local fallback / Static evidence / Recorded backup / Screenshot evidence / Test output / Secondary environment | | YES / NO |

Never present a recording or screenshot as live runtime behavior.

---

## 13. Demo Checkpoints

| Checkpoint ID | Condition | Verification Method | Expected Result | Status | Evidence | Owner | Recovery Action |
|---------------|-----------|---------------------|-----------------|--------|----------|-------|-----------------|
| | | | | PLANNED / EXECUTED / PASSED / FAILED / BLOCKED / UNKNOWN | | | |

---

## 14. Demo Priorities

| Item ID | Item | Category | Priority (DEMO-P0 / P1 / P2 / P3 / DROP) | Judge Visibility | Value | Reliability | Evidence Strength | Time | Risk | Dependencies |
|---------|------|----------|--------------------------------------------|------------------|-------|-------------|-------------------|------|------|--------------|
| | | | | LOW / MEDIUM / HIGH / VERY HIGH | | HIGH / MEDIUM / LOW / UNKNOWN | | | | |

Every demo item must receive exactly one priority.

---

## 15. Rehearsal Plan

| Rehearsal ID | Timestamp | Duration | Steps Completed | Failures | Recovery Attempts | Observed Delays | Unexpected Behavior | Evidence | Final Result |
|--------------|-----------|----------|-----------------|----------|-------------------|-----------------|---------------------|----------|--------------|
| | | | | | | | | | PLANNED / IN_PROGRESS / PASSED / FAILED / BLOCKED / UNKNOWN |

A rehearsal marked PASSED must have actual evidence.

---

## 16. Demo Readiness Gate

**Current Gate:** NOT_READY | PREPARING | BLOCKED | CONDITIONAL | READY

**Reason against every READY criterion:**

- Primary flow verified:
- Core output verified:
- Critical claims supported:
- Critical failures understood:
- Fallback available where needed:
- Timing known or explicitly UNKNOWN:
- Rehearsal completed:
- No unresolved critical demo blocker:

If any critical requirement is UNKNOWN, do not silently mark READY.

---

## 17. Demo Readiness Score

**SIMULATED DEMO ASSESSMENT**  
**NOT OFFICIAL JUDGING SCORE**

Do not use arbitrary hidden multipliers.

| Component | Value |
|-----------|-------|
| Core flow reliability | |
| Evidence coverage | |
| Recovery readiness | |
| Timing confidence | |
| Rehearsal evidence | |
| Judge-visible coverage | |

---

## 18. Unknowns

| Unknown | Why Unknown | Impact | Source |
|---------|-------------|--------|--------|
| | | | |

---

## 19. Recommended Next Action

**PRIMARY NEXT ACTION:** <exactly one action>

**WHY:** <explanation based on impact, time, risk, and judging criteria>

**DONE WHEN:** <clear definition of done>

**Time remaining:** <hours or UNKNOWN>

**Blocked by:** <blocker or "None">

**Rule:** Exactly one primary next action. Do not produce competing alternatives.

---

## 20. Validation Checklist

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
