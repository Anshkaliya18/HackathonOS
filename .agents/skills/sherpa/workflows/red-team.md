# sherpa — Red Team Workflow

**Operation:** RED-TEAM  
**Purpose:** Actively attempt to disprove project readiness. Identify weaknesses, construct adversarial scenarios, challenge claims, and produce a prioritized red-team review. Phase 8 is an adversarial intelligence layer — it reviews and recommends; it does not implement fixes or replace other phases.

**Pipeline:**
Read Project State → Verify Readiness → Read Phase 2 Idea Evidence → Read Phase 3 Project Plan → Read Phase 4 Implementation Evidence → Read Phase 5 Testing/Security Evidence → Read Phase 7 UX Evidence → Inspect Current Repository → Identify Critical Claims → Identify Assumptions → Construct Adversarial Scenarios → Attempt to Break / Disprove Claims → Record Evidence → Classify Findings → Assign Severity + Confidence → Prioritize Findings → Propose Mitigations → Determine Required Owner / Phase → Verify Applicable Mitigations → Re-test Relevant Risks → Red Team Quality Gate → Update Project State → Return Exactly ONE Primary Next Action

---

## When to Use

Use RED-TEAM when:
- A hackathon idea has been selected and implementation baseline exists
- You need an adversarial review of the project before judging
- You want to identify weaknesses that could cause the project to lose

**Prerequisite:** `.sherpa/project-state.md` must exist with `selected idea` known, Phase 3 project plan, Phase 4 implementation state, Phase 5 testing/security evidence, and Phase 7 UX evidence.

---

## Pipeline Stages

### Stage 1: Read Project State

Read `.sherpa/project-state.md`:
- Hackathon name, deadline, time remaining
- Judging criteria and weights
- Problem statement, target users
- Selected idea (must be known)
- Phase 2 decision outcome
- Phase 3 architecture status
- Phase 4 implementation status
- Phase 5 test/security evidence
- Phase 7 UX evidence

If `selected idea` is UNKNOWN:
- STOP normal red team review.
- Do not invent a selected idea.
- Return: selected idea is unknown, RED-TEAM cannot produce a normal review yet, exactly one primary next action: confirm the selected idea.

If implementation baseline is incomplete:
- Set Red Team Status to BLOCKED or LIMITED.
- Report RED TEAM REVIEW = BLOCKED or LIMITED.
- Perform bounded review of known artifacts only.
- Clearly state limitations.

### Stage 2: Verify Readiness

Check:
- Phase 3 project plan exists
- Phase 4 implementation status is known
- Phase 5 testing/security evidence exists
- Phase 7 UX evidence exists

If required information is missing:
- Mark as UNKNOWN
- Report RED TEAM REVIEW = BLOCKED or LIMITED
- Do not invent readiness

### Stage 3: Read Phase 2 Idea Evaluation

Read `.sherpa/decisions.md` and `.sherpa/evaluations/<idea-name>.md`:
- Selected idea name
- Evaluation scores
- Red-team outcomes from Phase 2
- Rejected ideas and reasons
- MVP scope

### Stage 4: Read Phase 3 Project Plan

Read `.sherpa/evidence/project-plan-*.md`:
- Current architecture
- Proposed architecture
- MVP scope (MUST/SHOULD/OPTIONAL/EXCLUDED)
- Implementation workstreams
- Dependencies
- Critical path
- Technical risks
- Time strategy

### Stage 5: Read Phase 4 Implementation Evidence

Read `.sherpa/evidence/` implementation artifacts:
- Repository baseline
- Components implemented
- Tests executed
- Deployment configuration
- Known issues

### Stage 6: Read Phase 5 Testing/Security Evidence

Read `.sherpa/evidence/` testing/security artifacts:
- Test results
- Security findings
- Blocked tests
- Regression risks
- Known failures

Do not duplicate the Phase 5 testing/security engine. Consume its evidence only.

### Stage 7: Read Phase 7 UX Evidence

Read `.sherpa/ux-review.md` and `.sherpa/ux/` artifacts:
- UX baseline
- Critical flows
- Findings
- Quality gate status
- Limitations

Do not duplicate the Phase 7 UX engine. Consume its evidence only.

### Stage 8: Inspect Current Repository

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

Evidence classification (for every observation):
- FACT: Directly observed
- INFERENCE: Logical conclusion from facts
- ASSUMPTION: Not yet verified
- UNKNOWN: No information available

Rules:
- Never fabricate repository facts.
- Execution claims require execution evidence.
- Seeing a test file does NOT mean tests pass.
- Generated sherpa artifacts are not independent evidence.

If conflicting evidence is found between sources (e.g., source code suggests one behavior but observed runtime shows another), record the contradiction as a separate finding; do not silently reconcile it.

### Stage 9: Identify Critical Claims

Identify important project claims. Each claim:
- Claim ID
- Claim text
- Source
- Evidence
- Evidence type
- Confidence

Distinguish "the application performs the algorithm" from "the algorithm produces high-quality outcomes."

### Stage 10: Identify Assumptions

Identify assumptions underlying the project:
- User behavior assumptions
- Technical assumptions
- Dependency assumptions
- Environment assumptions
- Performance assumptions

### Stage 11: Construct Adversarial Scenarios

Construct scenarios designed to break the project. Each scenario:
- Scenario ID
- Attack Surface
- Attacker/Skeptical Judge Perspective
- Preconditions
- Attack
- Expected Failure
- Actual Result
- Evidence
- Severity
- Confidence
- Finding
- Mitigation
- Verification Method
- Status

Only execute scenarios applicable to the actual project. Mark non-applicable scenarios NOT_APPLICABLE with justification.

Attack surfaces to consider:
- invalid input
- empty data
- duplicate input
- missing required field
- unexpected user behavior
- refresh during critical flow
- network failure
- backend failure
- dependency failure
- API timeout
- stale data
- unauthorized access
- privacy exposure
- misleading output
- poor recommendation quality
- weak differentiation
- unsupported claim
- demo failure
- judge confusion
- mobile/responsive issue
- accessibility barrier
- performance bottleneck
- deployment/runtime failure
- environment mismatch
- missing fallback
- recovery failure
- data corruption
- repeated use
- adversarial/abnormal input
- "Why should this win?" challenge

### Stage 12: Attempt to Break / Disprove Claims

For each critical claim, construct and execute adversarial attempts to disprove it. Record actual results.

### Stage 13: Record Evidence

Record all evidence for each finding, scenario, and claim. Evidence must be reproducible: path/line, route/screen, steps, result, or evidence artifact.

### Stage 14: Classify Findings

Classify each finding:
- Category: PRODUCT, DIFFERENTIATION, TECHNICAL, RELIABILITY, SECURITY, PRIVACY, UX, ACCESSIBILITY, RESPONSIVE, DEMO, PERFORMANCE, EVIDENCE, CREDIBILITY, DEPLOYMENT, OTHER
- Severity: CRITICAL, HIGH, MEDIUM, LOW, INFO, UNKNOWN
- Confidence: HIGH, MEDIUM, LOW, UNKNOWN

Severity rules:
- CRITICAL: primary flow cannot work, demo can fundamentally fail, severe security/trust issue, core claim demonstrably false
- HIGH: major MVP weakness, significant reliability issue, major unsupported claim
- MEDIUM: meaningful weakness with workaround
- LOW: minor friction
- INFO: observation without material risk
- UNKNOWN: insufficient evidence

Do not inflate severity.

### Stage 15: Prioritize Findings

Priority order:
1. CRITICAL MVP failure
2. CRITICAL demo failure
3. confirmed security/trust issue
4. HIGH reliability risk
5. HIGH differentiation weakness
6. unsupported major claim
7. HIGH UX/demo friction
8. important technical risk
9. evidence gaps
10. medium risks
11. low-risk polish

Do not prioritize cosmetic issues over project-breaking risks.

### Stage 16: Propose Mitigations

For each finding, propose mitigation:
- Recommended mitigation
- Required owner (PHASE 4 / PHASE 5 / PHASE 7 / PHASE 8 / HUMAN ARCHITECTURE APPROVAL / FUTURE PHASE / ACCEPTED RISK)
- Required phase
- Architecture impact
- Time estimate/confidence

### Stage 17: Determine Required Owner / Phase

Route each finding:
- Technical code bug → PHASE 4 — IMPLEMENTATION
- Missing security verification → PHASE 5 — TESTING / SECURITY
- UX issue → PHASE 7 — UX
- Architecture limitation → HUMAN ARCHITECTURE APPROVAL
- Judge/pitch issue → FUTURE PHASE
- Red-team-specific mitigation → PHASE 8 — RED TEAM
- Explicitly accepted risk → ACCEPTED RISK

Do not fix issues by silently modifying another phase.

### Stage 18: Verify Applicable Mitigations

For mitigations that have been implemented:
- Record verification evidence
- Mark VERIFIED only after actual verification
- Never mark VERIFIED merely because a recommendation was written

### Stage 19: Re-test Relevant Risks

Re-test risks that were mitigated to confirm mitigation effectiveness.

### Stage 20: Red Team Quality Gate

Evaluate gate:
- NOT_READY
- RED_TEAM_IN_PROGRESS
- BLOCKED
- CONDITIONAL
- READY

READY requires:
- critical attack surfaces reviewed
- no unresolved critical project-breaking finding
- critical demo path challenged
- major claims challenged
- high-severity findings resolved or explicitly accepted
- security/UX dependencies clearly routed
- verification evidence for claimed mitigations
- limitations documented
- remaining risks visible
- evidence-backed conclusions

A project can be RED TEAM READY while still having accepted medium/low risks.

### Stage 21: Update Project State

Update ONLY these compact fields in `.sherpa/project-state.md`:

| Field | New Value |
|-------|-----------|
| Red Team Status | NOT_STARTED | IN_PROGRESS | BLOCKED | COMPLETE |
| Red Team Baseline | UNKNOWN | VERIFIED |
| Critical Attack Surfaces | UNKNOWN | IDENTIFIED | REVIEWED |
| Critical Findings | UNKNOWN | PASS | FAIL | BLOCKED |
| High Findings | UNKNOWN | PASS | FAIL | BLOCKED |
| Red Team Quality Gate | NOT_READY | RED_TEAM_IN_PROGRESS | BLOCKED | CONDITIONAL | READY |

Rules:
- Do NOT put detailed red team analysis inside project-state.md.
- Detailed material goes to `.sherpa/red-team.md` and `.sherpa/red-team/`.
- Do not change `selected idea`.
- Do not silently change architecture.
- Human approval required for architecture changes and CRITICAL/HIGH risk acceptance.

### Stage 22: Return Exactly One Primary Next Action

Output format:

```
PRIMARY NEXT ACTION: <exactly one action>

WHY: <explanation based on impact, time, risk, and judging criteria>

DONE WHEN: <clear definition of done>

Time remaining: <hours or UNKNOWN>

Blocked by: <blocker or "None">
```

Rule: Exactly one primary next action. Do not produce competing alternatives.

---

## Validation Checklist

After RED-TEAM completes:

- [ ] Selected idea verified (or gate triggered)
- [ ] Readiness verified (or BLOCKED/LIMITED reported)
- [ ] Phase 2, 3, 4, 5, 7 evidence consumed
- [ ] Repository inspected
- [ ] Critical claims identified
- [ ] Adversarial scenarios constructed
- [ ] Findings classified with severity and confidence
- [ ] Findings prioritized
- [ ] Mitigations proposed with owner/phase
- [ ] Mitigations verified where implemented
- [ ] Quality gate evaluated
- [ ] Project state updated (compact fields only)
- [ ] Exactly ONE primary next action returned
- [ ] No application source code modified
- [ ] No Phase 1–7 files modified
- [ ] No Phase 5 or Phase 7 engine duplicated
- [ ] No idea silently changed
- [ ] No architecture silently redesigned
