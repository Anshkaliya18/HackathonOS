# HackathonOS — Engineering Rules

Defines Phase 3 engineering analysis and planning rules. All rules enforce evidence discipline, human authority, and time-aware prioritization.

---

## 1. Evidence Classification

Every repository observation and claim must be classified:

| Type | Definition |
|------|------------|
| FACT | Directly observed from repository inspection or verified execution |
| INFERENCE | Logical conclusion drawn from observed facts |
| ASSUMPTION | Not yet verified; requires confirmation |
| UNKNOWN | No information available; not observed |

**Rules:**
- Never fabricate repository facts.
- Execution claims require execution evidence.
- Seeing a test file does NOT mean tests pass.
- Seeing package.json does NOT mean dependencies are installed.
- Seeing deployment configuration does NOT mean deployment works.
- Seeing an API route does NOT mean the API is operational.
- HackathonOS-generated artifacts are NOT independent evidence.
- Evidence must trace back to repository inspection, actual execution, external verification, or explicit human-provided information.
- Do not treat previous AI-generated recommendations as facts.

---

## 2. Time-Aware Engineering Strategy

Use the existing Phase 1 time strategy. Do not invent a deadline if it is unknown.

| Time Remaining | Focus |
|----------------|-------|
| > 24 hours | Core implementation + differentiation + quality |
| 12–24 hours | Finish MVP + one strong differentiator + testing |
| 6–12 hours | MVP completion + stability + UX polish |
| 2–6 hours | Freeze major features + fix critical issues + demo reliability |
| < 2 hours | NO NEW FEATURES, NO ARCHITECTURE REWORK, NO EXPERIMENTAL DEPENDENCIES. Focus on reliability, demo, submission |

If remaining time is UNKNOWN:
- Mark it UNKNOWN
- Produce a time-neutral plan
- Recommend establishing the deadline if necessary

---

## 3. MVP Requirements

Every project plan must explicitly define:

| Category | Definition |
|----------|------------|
| MUST HAVE | Features required for the core deliverable to function |
| SHOULD HAVE | Important features that add significant value |
| OPTIONAL | Nice-to-have features if time permits |
| EXCLUDED | Explicitly out of scope for this hackathon |

**Rule:** Aggressively protect the MVP from unnecessary scope. Time pressure must influence these decisions.

---

## 4. Architecture Freeze Rule

Once architecture is explicitly approved, treat it as frozen.

It may only be reopened if a material blocker exists.

A reopening recommendation must contain:
- blocker
- evidence
- impact
- time cost
- alternative
- reason existing architecture is no longer viable

Human approval is required before changing the approved architecture.

Prevent endless architecture churn.

---

## 5. Architecture Approval Gate

Architecture approval is human-controlled.

The AI may recommend approval but MUST NOT change:
- Architecture: DRAFT → Architecture: APPROVED

without explicit human confirmation.

The project-plan artifact must distinguish:
- CURRENT STATE (what exists now)
- PROPOSED TARGET STATE (what is recommended)

Do not describe proposed architecture as if it already exists. If migration is required, explicitly identify: MIGRATION REQUIRED.

---

## 6. Project State Rules

Keep `.hackathon/project-state.md` compact.

Add only compact planning status fields:

| Field | Values |
|-------|--------|
| Planning status | NOT_STARTED | IN_PROGRESS | COMPLETE |
| Repository analysis | UNKNOWN | COMPLETE |
| Architecture | UNKNOWN | DRAFT | APPROVED |
| MVP | UNKNOWN | DRAFT | APPROVED |
| Implementation plan | UNKNOWN | READY |
| Engineering risk | UNKNOWN | LOW | MEDIUM | HIGH |

Do NOT put detailed repository analysis or architecture inside project-state.md. Detailed artifacts go to `.hackathon/evidence/`.

---

## 7. Selected Idea Gate

Before normal Phase 3 execution:

1. Read `.hackathon/project-state.md`.
2. If `selected idea = UNKNOWN`:
   - STOP normal planning.
   - Do not invent a selected idea.
   - Return: selected idea is unknown, Phase 3 cannot produce a normal project plan yet, exactly one primary next action: confirm the selected idea.
3. If `selected idea` is known, continue.

Phase 3 consumes the selected idea and Phase 2 artifacts. It does not silently reopen idea selection.

If Phase 3 discovers the selected idea is technically infeasible:
- DO NOT automatically select another idea.
- Record the engineering concern, explain the evidence, recommend scope reduction or architecture revision.
- If reconsideration is necessary, route the human back to Phase 2.
- Human authority remains absolute.

---

## 8. Repository Analysis Scope

Analysis must be targeted and structured. Prioritize inspection in this order:

1. Project metadata
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

The analysis must declare its scope. Do not claim exhaustive repository analysis unless the repository was actually analyzed exhaustively.

Repository analysis artifacts go to `.hackathon/evidence/`.

---

## 9. Implementation-Ready Definition

The plan can only be marked `Implementation plan: READY` when ALL of the following are true:

- selected idea is known
- repository baseline analyzed sufficiently
- current architecture identified
- proposed architecture documented
- architecture explicitly approved
- MVP defined
- exclusions defined
- implementation workstreams defined
- dependencies identified
- critical path identified
- technical risks documented
- testing priorities documented
- security priorities documented
- time strategy defined or explicitly marked UNKNOWN
- unresolved unknowns documented
- exactly one primary next action exists

Otherwise keep the plan in DRAFT/IN_PROGRESS state.

---

## 10. Failure Cases

| Case | Behavior |
|------|----------|
| No selected idea | Stop and request confirmation |
| Empty repository | Do not fabricate architecture. Report insufficient evidence. |
| Broken repository | Document observed problems, impact, blocking status, recommended remediation |
| Missing tests | Report test coverage/status as UNKNOWN or NOT PRESENT |
| Missing environment variables | Do not invent values |
| Unknown deadline | Do not assume one |
| Architecture rejected by human | Capture rejection/reason, return architecture to DRAFT |
| Approved architecture blocked | Require material blocker + human approval before reopening |
| Insufficient repository evidence | Lower planning confidence, mark unknowns explicitly |

Phase 3 MUST NOT:
- write application code
- modify application source files
- modify frontend/backend implementation
- install dependencies
- deploy the application
- automatically select an idea
- automatically change the selected idea
- automatically approve architecture
- perform final judge scoring
- perform final presentation generation
- claim tests passed without execution evidence
- claim deployment works without verification evidence
- claim security is complete without evidence
- silently override Phase 2 decisions

If a Phase 3 recommendation requires changing the selected idea, route the issue back to the human / Phase 2. Never silently switch ideas.
