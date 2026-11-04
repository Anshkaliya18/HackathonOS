# sherpa — Project Planning Workflow

**Operation:** PROJECT-PLAN  
**Purpose:** Turn the selected hackathon idea into an implementation-ready engineering plan. Phase 3 is an engineering analysis and planning engine, NOT a coding engine.

**Pipeline:**
INPUT → Read project state → Verify selected idea → Read Phase 2 artifacts → Inspect repository → Create repository analysis → Identify engineering gaps → Design architecture → Define MVP → Create implementation plan → Analyze risks → Apply time-aware prioritization → Write project plan → Update permitted project state → Return exactly ONE primary next action

---

## When to Use

Use PROJECT-PLAN when:
- A hackathon idea has been selected (confirmed in `.sherpa/project-state.md`)
- You need an implementation-ready project plan
- You want to analyze the repository, define architecture, scope the MVP, and plan implementation work

**Prerequisite:** `.sherpa/project-state.md` must exist with `selected idea` known.

---

## Pipeline Stages

### Stage 1: Input

**Accept from user:**
- Confirmation to proceed with project planning for the selected idea
- Any additional context about team skills, constraints, or preferences

**Read from `.sherpa/project-state.md`:**
- Hackathon name, deadline, time remaining
- Judging criteria and weights
- Problem statement, target users
- Selected idea (must be known)
- Planning status, architecture status, MVP status

### Stage 2: Verify Selected Idea (Selected Idea Gate)

**Check:** Is `selected idea` known in `.sherpa/project-state.md`?

**If UNKNOWN:**
- STOP normal planning.
- Do not invent a selected idea.
- Return:
  - Selected idea is unknown
  - Phase 3 cannot produce a normal project plan yet
  - Exactly one primary next action: confirm the selected idea (via human confirmation of Phase 2 recommendation)

**If known:**
- Continue to Stage 3.
- Record the selected idea name in the project plan.

**Rule:** Phase 3 consumes the Phase 2 result. It does not silently reopen idea selection. If the selected idea is technically infeasible, record the engineering concern, explain the evidence, recommend scope reduction or reconsideration, and route the human back to Phase 2. Never silently switch ideas.

### Stage 3: Read Phase 2 Artifacts

**Read from `.sherpa/decisions.md`:**
- Selected idea name
- Evaluation scores and reasoning
- Red-team outcomes
- Recommended next action from Phase 2

**Read from `.sherpa/evaluations/<idea-name>.md`:**
- Full per-idea evaluation
- Category scores
- Feasibility gate result
- Minimum viable version scope

**Read from `.sherpa/evidence/`:**
- Any existing evidence files

**Rule:** Do not treat Phase 2 AI-generated recommendations as independent facts. Use them as input, but verify against repository evidence where applicable.

### Stage 4: Inspect Repository

**Analysis scope:** TARGETED (declare explicitly)

**Inspect in priority order:**
1. Project metadata (package.json, requirements.txt, pyproject.toml, README.md)
2. Dependency manifests
3. Top-level project structure
4. Application entry points
5. Frontend
6. Backend
7. Database/data layer
8. API layer
9. AI/ML layer
10. Tests
11. Deployment/configuration
12. Documentation
13. Targeted deeper inspection where necessary

**Evidence classification (for every observation):**
- FACT: Directly observed
- INFERENCE: Logical conclusion from facts
- ASSUMPTION: Not yet verified
- UNKNOWN: No information available

**Rules:**
- Never fabricate repository facts.
- Execution claims require execution evidence.
- Seeing a test file does NOT mean tests pass.
- Seeing package.json does NOT mean dependencies are installed.
- Seeing deployment configuration does NOT mean deployment works.
- Seeing an API route does NOT mean the API is operational.
- sherpa-generated artifacts are NOT independent evidence.

**Save repository analysis to:** `.sherpa/evidence/repo-analysis-<timestamp>.md`

Use `templates/repo-analysis.md` as the record format.

**Analysis scope declaration:** This analysis is TARGETED. <explanation of what was and was not inspected>.

### Stage 5: Identify Engineering Gaps

Compare repository state against the selected idea requirements:

| Gap | Description | Impact | Evidence Type | Source |
|-----|-------------|--------|---------------|--------|
| | | | | |

**Gaps to check:**
- Missing entry points
- Missing frontend/backend components
- Missing database/schema
- Missing API routes
- Missing AI/ML pipeline
- Missing tests
- Missing deployment configuration
- Missing environment variables
- Incomplete areas
- TODOs/placeholders
- Security observations
- Deployment risks

### Stage 6: Design Architecture

**Current architecture:** Document what exists in the repository (or UNKNOWN if none).

**Proposed architecture:** Document what should exist for the selected idea.

**Rules:**
- Always distinguish CURRENT STATE from PROPOSED TARGET STATE.
- Do not describe proposed architecture as if it already exists.
- If migration is required, explicitly identify: MIGRATION REQUIRED.
- Document architecture decision rationale.

**Architecture status:** DRAFT (not APPROVED until human confirmation)

### Stage 7: Define MVP

Define MVP with explicit categories:

| Category | Features |
|----------|----------|
| MUST HAVE | |
| SHOULD HAVE | |
| OPTIONAL | |
| EXCLUDED | |

**Rules:**
- Aggressively protect the MVP from unnecessary scope.
- Time pressure must influence these decisions.
- Time-aware strategy based on remaining time:
  - >24h: Core implementation + differentiation + quality
  - 12–24h: Finish MVP + one strong differentiator + testing
  - 6–12h: MVP completion + stability + UX polish
  - 2–6h: Freeze major features + fix critical issues + demo reliability
  - <2h: NO NEW FEATURES, NO ARCHITECTURE REWORK, NO EXPERIMENTAL DEPENDENCIES. Focus on reliability, demo, submission.

If time remaining is UNKNOWN: mark UNKNOWN, produce time-neutral plan, recommend establishing deadline.

### Stage 8: Create Implementation Plan

Define:

| Element | Content |
|---------|---------|
| Implementation workstreams | List with descriptions, dependencies, effort, priority |
| Dependencies | List with install status |
| Critical path | Ordered steps with time estimates |
| Technical risks | List with likelihood, impact, mitigation |
| Security priorities | List with evidence type |
| Testing priorities | List with execution evidence status |
| UX priorities | List |

**Rules:**
- Do not claim tests passed without execution evidence.
- Do not claim deployment works without verification evidence.
- Do not claim security is complete without evidence.
- Do not invent environment variable values.

### Stage 9: Analyze Risks

Document:

| Risk | Likelihood | Impact | Mitigation | Evidence Type |
|------|------------|--------|------------|---------------|
| | | | | |

Include:
- Technical risks
- Security risks
- Deployment risks
- Time risks

### Stage 10: Apply Time-Aware Prioritization

Based on remaining time, prioritize workstreams:

| Time remaining | Priority focus |
|----------------|---------------|
| > 24 hours | Core implementation + differentiation + quality |
| 12–24 hours | Finish MVP + one strong differentiator + testing |
| 6–12 hours | MVP completion + stability + UX polish |
| 2–6 hours | Freeze major features + fix critical issues + demo reliability |
| < 2 hours | NO NEW FEATURES, NO ARCHITECTURE REWORK, NO EXPERIMENTAL DEPENDENCIES |

If time remaining is UNKNOWN: produce time-neutral plan, mark UNKNOWN.

### Stage 11: Write Project Plan Artifact

Use `templates/project-plan.md` as the record format.

**Save to:** `.sherpa/evidence/project-plan-<timestamp>.md` or a stable path

Include all sections:
- Project
- Hackathon criteria
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
- MVP (MUST/SHOULD/OPTIONAL/EXCLUDED)
- Implementation workstreams
- Dependencies
- Critical path
- Technical risks
- Security priorities
- Testing priorities
- UX priorities
- Time strategy
- Architecture decisions
- Unknowns
- Recommended next action

**Plan status:** DRAFT (not READY until all implementation-ready criteria met)

### Stage 12: Update Permitted Project State

Update ONLY these compact fields in `.sherpa/project-state.md`:

| Field | New value |
|-------|-----------|
| Planning status | IN_PROGRESS | COMPLETE |
| Repository analysis | COMPLETE (if analysis done) |
| Architecture | DRAFT (not APPROVED) |
| MVP | DRAFT (not APPROVED) |
| Implementation plan | UNKNOWN (not READY until all criteria met) |
| Engineering risk | LOW | MEDIUM | HIGH |

**Rules:**
- Do NOT put detailed repository analysis or architecture inside project-state.md.
- Architecture cannot become APPROVED without explicit human confirmation.
- MVP cannot become APPROVED without explicit human confirmation.
- Implementation plan cannot become READY until all implementation-ready criteria are met.

**Do NOT change:**
- `selected idea` (remains as set by Phase 2 + human confirmation)
- Problem statement
- Hackathon criteria/weights
- Deadline/time remaining (unless correcting an error)

### Stage 13: Return Exactly One Primary Next Action

**Output format:**

```
PRIMARY NEXT ACTION: <exactly one action>

WHY: <explanation based on impact, time, risk, and criteria>

DONE WHEN: <clear definition of done>

Time remaining: <hours or UNKNOWN>

Blocked by: <blocker or "None">
```

**Rule:** Exactly one primary next action. Do not produce competing alternatives.

**Examples:**
- "Implement the authentication MVP flow" — WHY: on critical path — DONE WHEN: login/logout/session verified
- "Create repository analysis" — WHY: need baseline before architecture — DONE WHEN: repo-analysis artifact written
- "Confirm selected idea" — WHY: Phase 3 gate requires it — DONE WHEN: human confirms in project-state.md

---

## Validation Checklist

After PROJECT-PLAN completes:

- [ ] Selected idea verified (or gate triggered)
- [ ] Repository analysis declared its scope
- [ ] Evidence classification used (FACT/INFERENCE/ASSUMPTION/UNKNOWN)
- [ ] No execution claims without execution evidence
- [ ] sherpa artifacts not treated as independent evidence
- [ ] Current architecture and proposed architecture separated
- [ ] MVP contains MUST HAVE / SHOULD HAVE / OPTIONAL / EXCLUDED
- [ ] Time-aware strategy applied
- [ ] Unknown deadline not assumed
- [ ] Architecture status = DRAFT (not auto-APPROVED)
- [ ] No application source code modified
- [ ] No dependencies installed
- [ ] No deployment performed
- [ ] Phase 2 scoring logic unchanged
- [ ] Phase 1 INIT/STATUS/NEXT unchanged
- [ ] project-state.md remains compact
- [ ] Exactly ONE primary next action returned
- [ ] Implementation plan READY only when all criteria met + architecture approved
