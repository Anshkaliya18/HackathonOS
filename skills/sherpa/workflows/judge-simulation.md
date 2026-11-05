# sherpa — Judge Simulation Workflow

**Operation:** JUDGE-SIM  
**Purpose:** Simulate how a realistic hackathon judge would perceive the project. Identify what judges would notice, question, misunderstand, praise, distrust, or penalize. Phase 9 is a judge simulation intelligence engine — it reviews and recommends; it does not optimize scores or change the project.

**Pipeline:**
Read Project State → Verify Readiness → Read Hackathon Rules / Criteria → Read Phase 2 Evaluation → Read Phase 3 Project Plan → Read Phase 4 Implementation Evidence → Read Phase 5 Testing/Security Evidence → Read Phase 7 UX Evidence → Read Phase 8 Red Team Evidence → Inspect Actual Repository → Inspect Actual Demo Flow → Build Judge Perspective → Evaluate Each Criterion → Simulate Judge Questions → Challenge Claims → Assess Judge Confidence → Identify Judge Concerns → Prioritize Preparation Needs → Produce Judge Simulation Report → Update Project State → Return Exactly ONE Primary Next Action

---

## When to Use

Use JUDGE-SIM when:
- A hackathon idea has been selected and implementation baseline exists
- You want to anticipate how judges would perceive the project
- You need to understand what judges would question, trust, or distrust

**Prerequisite:** `.sherpa/project-state.md` must exist with `selected idea` known, Phase 2 idea evaluation, Phase 3 project plan, Phase 4 implementation evidence, Phase 5 testing/security evidence, Phase 7 UX evidence, and Phase 8 Red Team evidence.

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
- Phase 8 Red Team evidence

If `selected idea` is UNKNOWN:
- STOP normal judge simulation.
- Do not invent a selected idea.
- Return: selected idea is unknown, JUDGE-SIM cannot produce a normal simulation yet, exactly one primary next action: confirm the selected idea.

If required information is missing:
- Mark as UNKNOWN
- Report JUDGE-SIM = BLOCKED or LIMITED
- Do not invent readiness

### Stage 2: Verify Readiness

Check:
- Hackathon rules / judging criteria exist (or mark UNKNOWN)
- Phase 2 idea evaluation exists
- Phase 3 project plan exists
- Phase 4 implementation status is known
- Phase 5 testing/security evidence exists
- Phase 7 UX evidence exists
- Phase 8 Red Team evidence exists

If required information is missing:
- Mark as UNKNOWN
- Report JUDGE-SIM = BLOCKED or LIMITED
- Do not invent readiness

### Stage 3: Read Hackathon Rules / Criteria

Read the hackathon's official judging criteria and weights:
- Capture each criterion name and weight
- If criteria/weights are UNKNOWN, mark UNKNOWN
- Do NOT invent criteria or weights
- Do NOT invent weights

### Stage 4: Read Phase 2 Idea Evaluation

Read `.sherpa/decisions.md` and `.sherpa/evaluations/<idea-name>.md`:
- Selected idea name
- Evaluation scores
- Red-team outcomes from Phase 2
- Rejected ideas and reasons
- MVP scope

### Stage 5: Read Phase 3 Project Plan

Read `.sherpa/evidence/project-plan-*.md`:
- Current architecture
- Proposed architecture
- MVP scope (MUST/SHOULD/OPTIONAL/EXCLUDED)
- Implementation workstreams
- Dependencies
- Critical path
- Technical risks
- Time strategy

### Stage 6: Read Phase 4 Implementation Evidence

Read `.sherpa/evidence/` implementation artifacts:
- Repository baseline
- Components implemented
- Tests executed
- Deployment configuration
- Known issues

### Stage 7: Read Phase 5 Testing/Security Evidence

Read `.sherpa/evidence/` testing/security artifacts:
- Test results
- Security findings
- Blocked tests
- Regression risks
- Known failures

Do not duplicate the Phase 5 testing/security engine. Consume its evidence only.

### Stage 8: Read Phase 7 UX Evidence

Read `.sherpa/ux-review.md` and `.sherpa/ux/` artifacts:
- UX baseline
- Critical flows
- Findings
- Quality gate status
- Limitations

Do not duplicate the Phase 7 UX engine. Consume its evidence only.

### Stage 9: Read Phase 8 Red Team Evidence

Read `.sherpa/red-team.md` and `.sherpa/red-team/` artifacts:
- Red team findings
- Risks
- Mitigations
- Quality gate status
- Limitations

Do not duplicate the Phase 8 Red Team engine. Consume its evidence only.

### Stage 10: Inspect Current Repository

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

### Stage 11: Inspect Actual Demo Flow

Inspect the actual demo path if available:
- Judge opens project
- Initial understanding
- First interaction
- Core action
- Result
- Secondary behavior
- Error/recovery
- Completion

Record:
- Steps
- Time
- Visible output
- Confusion points
- Failure points
- Recovery
- Missing context
- Judge-visible value

Do not claim a demo was executed unless it was actually executed. If dynamic execution is unavailable:

```text
Demo execution = NOT_TESTED
```

### Stage 12: Build Judge Perspective

Build simulation from multiple judge personas:
- Technical Judge
- Product Judge
- Demo Judge
- Skeptical Judge

Do not assume every hackathon uses these exact judge types. They are simulation personas only.

### Stage 13: Evaluate Each Criterion

For each judging criterion:
- Map to actual evidence
- Identify strengths and weaknesses
- Determine likely judge reaction
- Assign confidence
- Identify unknowns

If official criteria exist, use them exactly. If UNKNOWN, mark UNKNOWN.

### Stage 14: Simulate Judge Questions

Construct questions a judge would ask:
- Each question: ID, persona, question text, why asked, relevant criterion, expected answer points, evidence, potential trap, confidence
- Map questions to criteria
- Do not fabricate judge answers

### Stage 15: Challenge Claims

Cross-check claims against:
- Phase 2 evidence
- Phase 3 project plan
- Phase 4 implementation
- Phase 5 testing/security
- Phase 7 UX
- Phase 8 Red Team
- repository
- demo

Flag contradictions:

```text
Documentation says X
Repository does Y
Demo shows Z
```

Do not silently reconcile contradictions. Record them.

### Stage 16: Assess Judge Confidence

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

### Stage 17: Identify Judge Concerns

Identify concerns judges would raise:
- unsupported claims
- weak differentiation
- demo failure risk
- technical credibility issues
- UX problems
- missing evidence
- hidden limitations

Assign severity:
- CRITICAL, HIGH, MEDIUM, LOW, INFO, UNKNOWN

Do not inflate severity.

### Stage 18: Prioritize Preparation Needs

Priority order:
1. CRITICAL demo failure
2. CRITICAL credibility issue
3. HIGH reliability risk
4. HIGH differentiation weakness
5. HIGH unsupported claim
6. HIGH UX/demo friction
7. important technical risk
8. evidence gaps
9. medium risks
10. low-risk polish

Do not prioritize cosmetic issues over project-breaking risks.

### Stage 19: Produce Judge Simulation Report

Use `templates/judge-simulation.md` as the record format.

Save to `.sherpa/judge-simulation.md`.

Include:
- Project
- Judge personas simulated
- Judging criteria and weights
- Current state
- Target outcome
- Current architecture
- Proposed architecture
- Components
- Data flow
- APIs/interfaces
- Database/storage
- AI/ML
- External services
- Deployment
- MVP
- MUST/SHOULD/OPTIONAL/EXCLUDED
- Implementation workstreams
- Dependencies
- Critical path
- Technical risks
- Security priorities
- Testing priorities
- UX priorities
- Time strategy
- Judge questions
- Expected answer quality
- Likely objections
- Technical credibility
- Product credibility
- Demo credibility
- Claim consistency
- Differentiation perception
- Judge trust
- Critical preparation risks
- Unknowns
- Time strategy
- Judge readiness
- Primary next action

### Stage 20: Update Project State

Update ONLY these compact fields in `.sherpa/project-state.md`:

| Field | New Value |
|-------|-----------|
| Judge Simulation Status | NOT_STARTED | IN_PROGRESS | BLOCKED | COMPLETE |
| Judge Baseline | UNKNOWN | VERIFIED |
| Judge Criteria | UNKNOWN | IDENTIFIED | REVIEWED |
| Critical Judge Concerns | UNKNOWN | NONE | IDENTIFIED |
| Judge Readiness | NOT_READY | IN_PROGRESS | BLOCKED | CONDITIONAL | READY |

Rules:
- Do NOT put detailed judge simulation inside project-state.md.
- Detailed material goes to `.sherpa/judge-simulation.md` and `.sherpa/judge/`.
- Do not change `selected idea`.
- Do not silently change architecture.
- Human approval required for architecture changes.

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

---

## Validation Checklist

After JUDGE-SIM completes:

- [ ] Selected idea verified (or gate triggered)
- [ ] Readiness verified (or BLOCKED/LIMITED reported)
- [ ] Phase 2–8 evidence consumed
- [ ] Repository inspected
- [ ] Judging criteria identified (or UNKNOWN)
- [ ] Judge personas identified
- [ ] First impression evaluated
- [ ] Judge-visible strengths and weaknesses identified
- [ ] Criterion-by-criterion observations made
- [ ] Simulated judge questions created
- [ ] Expected answer quality assessed
- [ ] Likely objections documented
- [ ] Technical credibility assessed
- [ ] Product credibility assessed
- [ ] Demo credibility assessed
- [ ] Claim consistency checked
- [ ] Differentiation perception evaluated
- [ ] Judge trust assessed
- [ ] Critical preparation risks identified
- [ ] Unknowns documented
- [ ] Time-aware strategy applied
- [ ] Unknown deadline not assumed
- [ ] Judge readiness gate evaluated
- [ ] No application source code modified
- [ ] No Phase 1–8 files modified
- [ ] No Phase 5/7/8 engines duplicated
- [ ] No score optimization performed
- [ ] No simulated score presented as official score
- [ ] No idea silently changed
- [ ] No architecture silently redesigned
- [ ] project-state.md remains compact
- [ ] Exactly ONE primary next action returned
