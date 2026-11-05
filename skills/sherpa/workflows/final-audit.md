# sherpa — FINAL AUDIT Workflow

**Operation:** FINAL-AUDIT  
**Lifecycle Phase:** Phase 18 — Final Audit Intelligence  
**Purpose:** Convert validated project evidence into a final audit report and readiness determination. Phase 18 performs verification and decision support. It does not implement, replace prior phases, or modify locked artifacts. Phase 18 audits and recommends; it does not execute submission.

## Prerequisites

- Confirm `workflows/lifecycle.md` has exactly 20 ordered phases and Phase 17 is PPT / Presentation, Phase 18 is Final Audit, Phase 19 is Submission, and Phase 20 is Post-Mortem.
- If the lifecycle map differs, stop FINAL-AUDIT and record Lifecycle Integrity = FAIL; do not repair or renumber the lifecycle.
- Verify Phase 17 is `COMPLETE & LOCKED` from its final audit evidence before proceeding. If not, stop Phase 18 and report the exact prerequisite blocker; do not modify Phase 17.
- `.sherpa/project-state.md` must exist
- `selected idea` must be known (not UNKNOWN)
- Phase 17 presentation evidence must exist
- Phase 16 demo preparation evidence must exist
- Phase 15 score optimization evidence must exist
- Phase 14 judge simulation evidence must exist
- Phase 13 red-team evidence must exist
- Phase 12 UX evidence must exist
- Phase 11 testing/security evidence must exist

If project evidence is missing, mark the affected project audit areas UNKNOWN and report live project readiness as BLOCKED, NOT_READY, or CONDITIONAL as supported; do not invent evidence or readiness. Missing Phase 17 lock is a hard stop.

## Pipeline

### Stage 1: Read Project State

Read `.sherpa/project-state.md` and capture:

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
| Phase 11 | `.sherpa/evidence/` testing/security artifacts | Verified tests, critical failures, security findings, quality gate, evidence |
| Phase 12 | `.sherpa/ux-review.md`, `.sherpa/ux/` artifacts | Critical UX issues, usability findings, accessibility findings, demo flow observations |
| Phase 13 | `.sherpa/red-team.md`, `.sherpa/red-team/` artifacts | Critical findings, adversarial failures, recoverability, unresolved risks |
| Phase 14 | `.sherpa/judge-simulation.md` | Judge questions, skeptical follow-ups, weak claims, evidence gaps, expected judge concerns |
| Phase 15 | `.sherpa/score-optimization.md` | P0/P1 improvements, judge-visible priorities, evidence weaknesses, criterion gaps |
| Phase 16 | `.sherpa/demo-preparation.md` | Demo objective, primary flow, judge-visible moments, evidence, fallback info, timing |
| Phase 17 | `.sherpa/presentation.md` | Presentation objective, slide architecture, claims evidence, timing, speaker guidance |

Do not re-run Phase 11–17 engines. Consume their evidence only.

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
- Generated sherpa artifacts are not independent evidence.

### Stage 4: Build Evidence Record

Create final audit evidence record for each claim:

| Evidence ID | Source Phase | Artifact | Claim / Requirement | Evidence Type | Evidence Status | Verification Method | Observed Result | Confidence | Related Finding |

Evidence types: source code / test result / runtime output / log / artifact / screenshot / recording / deployment / configuration / documentation / judge simulation / demo rehearsal / presentation artifact / security review / UX review / red-team result

### Stage 5: Audit Domains

Audit each domain:

- Domain A: Lifecycle Integrity
- Domain B: Idea / Problem Alignment
- Domain C: Product / MVP Alignment
- Domain D: Architecture / Implementation Alignment
- Domain E: Testing
- Domain F: Security
- Domain G: UX / Accessibility
- Domain H: Red Team
- Domain I: Judge Simulation
- Domain J: Score Optimization
- Domain K: Demo
- Domain L: Presentation
- Domain M: Evidence Integrity
- Domain N: Documentation
- Domain O: Repository / Deployment
- Domain P: Submission Requirements
- Domain Q: Known Risks
- Domain R: Final Readiness

Do not silently omit a domain. If evidence unavailable: UNKNOWN.

### Stage 6: Cross-Phase Consistency Audit

Build cross-phase consistency chain:

```text
Selected Idea → Problem → MVP → Architecture → Implementation → Testing → UX → Red Team → Judge Simulation → Score Optimization → Demo → Presentation
```

Identify contradictions:

- Presentation claims feature not in implementation
- Demo shows functionality not supported by evidence
- Architecture claims components that do not exist
- Tests claim coverage never executed
- Security claims exceed actual controls
- UX claims contradict observed behavior
- Judge answers contradict implementation
- Score optimization references unsupported weaknesses
- Presentation metrics do not match test results

Every contradiction becomes explicit finding.

### Stage 7: Selected Idea Stability Audit

Verify selected idea remains stable. Do not silently reselect.

If material divergence exists:

> IDEA_ALIGNMENT = FAIL

### Stage 8: Requirement Coverage Audit

Extract requirements from hackathon rules, judging criteria, project requirements, Phase 1 outputs, selected idea, MVP definition, implementation plan, testing/security requirements, demo requirements, presentation requirements.

For each requirement:

| Requirement ID | Requirement | Source | Importance | Evidence | Status | Owner | Finding |

If official criteria unavailable:

> RULES = UNKNOWN

Do not fabricate compliance.

### Stage 9: Judging Criteria Coverage Audit

Build criteria coverage map:

| Criterion | Weight | Evidence | Implementation Support | Demo Support | Presentation Support | Coverage | Confidence |

Use exact official terminology.

If weights unavailable:

> WEIGHT = UNKNOWN

Do not invent weights.

Do not calculate official score unless official judging mathematics known.

### Stage 10: Score Separation Audit

Verify Phase 15 keeps separate:

- OFFICIAL SCORE
- ESTIMATED SCORE
- PROVISIONAL SCORE
- SIMULATED JUDGE ASSESSMENT
- INTERNAL OPTIMIZATION HEURISTIC
- DEMO READINESS
- PRESENTATION READINESS
- FINAL AUDIT READINESS

Never combine into one misleading number.

Do not introduce hidden scoring multipliers or undisclosed transformations. A failed or blocked test is never represented as passed; PASS requires actual execution evidence.

If no official score:

> OFFICIAL SCORE = UNKNOWN

---

# 11. Claim Audit

Audit major claims from README, documentation, UI, demo, PPT, speaker notes, judge answers, project description, marketing text.

| Claim ID | Claim | Source | Evidence | Credibility | Risk | Action |

Credibility:

- VERIFIED
- SUPPORTED
- PARTIALLY_SUPPORTED
- UNSUPPORTED
- CONTRADICTED
- UNKNOWN

Rules:

- CONTRADICTED claims corrected or removed.
- UNSUPPORTED claims removed, weakened, or qualified.
- UNKNOWN claims not presented as facts.

---

# 12. Metric Audit

Audit all numerical claims:

| Metric | Value | Unit | Source | Measurement Method | Date | Evidence Status | Confidence |

Before using: user counts, accuracy, latency, revenue, savings, growth, adoption, performance, benchmark results, market size, percentage improvements — all require evidence.

Never fabricate precision.

If metric cannot be verified:

> UNKNOWN

---

# 13. Testing Audit

Verify Phase 11 evidence:

- tests actually executed
- PASS has evidence
- critical paths tested
- failure cases addressed
- regression evidence exists
- blocked tests remain blocked
- UNKNOWN remains UNKNOWN

Do not infer full project quality from passing framework test.

Distinguish:

> Framework validation

from:

> Live project validation.

---

# 14. Security Audit

Verify:

- secrets not exposed
- environment configuration appropriate
- credentials not committed
- authentication claims accurate
- authorization claims accurate
- input handling claims supported
- privacy claims supported
- security findings tracked
- critical security findings resolved or explicitly accepted

Never claim "zero vulnerabilities" unless genuinely justified by verified scope.

Prefer bounded language.

---

# 15. UX Audit

Verify Phase 12 findings:

- critical UX findings
- accessibility findings
- responsive behavior
- navigation
- forms
- error states
- loading states
- empty states
- success states
- demo flow

Do not claim accessibility compliance without evidence.

---

# 16. Red Team Closure Audit

Review Phase 13 findings:

| Finding | Severity | Evidence | Status | Mitigation | Verification | Owner | Final Disposition |

Open CRITICAL finding blocks unconditional readiness.

---

# 17. Judge Simulation Closure Audit

Review Phase 14:

- critical judge questions
- skeptical follow-ups
- weak claims
- unsupported answers
- evidence gaps
- unresolved credibility concerns

For each question:

- READY
- PARTIALLY_READY
- WEAK
- UNKNOWN
- NOT_APPLICABLE

Do not convert weak answers into READY without new evidence.

---

# 18. Score Optimization Closure Audit

Review Phase 15:

- P0 improvements
- P1 improvements
- unresolved evidence gaps
- reliability priorities
- differentiation priorities
- criterion gaps

For every unresolved P0:

| P0 Status | Owner | Reason | Impact | Verification | Final Disposition |

Do not silently delete unresolved P0 items.

---

# 19. Demo Closure Audit

Review Phase 16:

- primary flow
- critical demo steps
- demo evidence
- fallback
- rehearsal
- timing
- reliability
- judge-visible moments
- demo claims

Distinguish framework validation from live demo validation.

If no live project demo:

> LIVE DEMO READINESS = UNKNOWN / CONDITIONAL

Do not claim otherwise.

---

# 20. Presentation Closure Audit

Review Phase 17:

- essential slides
- judging criteria coverage
- claim evidence
- timing
- speaker guidance
- visual evidence
- Q&A readiness
- presentation risks

Distinguish presentation framework validated from live project presentation validated.

---

# 21. Repository Audit

Inspect repository where available:

- source files
- manifests
- README
- configuration
- environment templates
- tests
- documentation
- deployment configuration
- unused critical files
- suspicious generated files
- accidental credentials
- temporary artifacts
- debug code
- broken references
- inconsistent project names

Do not modify repository during audit unless explicitly required and human-approved.

---

# 22. Secret / Sensitive Data Audit

Search for likely secret indicators:

- API keys
- tokens
- passwords
- private keys
- credentials
- `.env`
- service account files
- OAuth secrets

Classify findings based on actual evidence.

Do not claim "no secrets exist anywhere" unless scope genuinely supports it.

Use bounded language:

> No secret indicators identified within audited scope.

---

# 23. Documentation Consistency Audit

Check:

- README
- project description
- setup instructions
- environment variables
- architecture documentation
- demo instructions
- screenshots
- API documentation
- installation commands
- deployment URLs
- license

Identify stale or contradictory documentation.

---

# 24. Deployment Audit

Where deployment evidence exists, verify:

- URL
- availability
- frontend
- backend
- API
- environment configuration
- expected routes
- critical flow

If live verification unavailable:

> DEPLOYMENT STATUS = UNKNOWN

Do not infer uptime.

---

# 25. Submission Requirements Audit

Determine prerequisites for Phase 19:

- repository
- live URL
- PPT
- demo video
- documentation
- team information
- forms
- screenshots
- required files
- license
- README
- project description

For each:

| Requirement | Known? | Evidence | Status | Missing Item | Owner |

Phase 18 does not submit anything.

---

# 26. Last-Minute Change Protection

Phase 18 explicitly warns against unnecessary changes.

Classify proposed changes:

- SAFE
- LOW_RISK
- MEDIUM_RISK
- HIGH_RISK
- IRREVERSIBLE

Near submission, default toward stability over feature expansion.

Do not recommend feature additions merely because possible.

---

# 27. Final Risk Register

Each risk:

| Risk ID | Description | Source Phase | Severity | Likelihood | Confidence | Impact | Mitigation | Owner | Status | Final Disposition |

Confidence separate from severity.

---

# 28. Final Readiness Gate

Gate values:

| Value | Meaning |
|-------|---------|
| NOT_READY | Insufficient evidence |
| READY | Critical items verified |
| BLOCKED | Critical dependency prevents validation |
| CONDITIONAL | Major unknowns remain |

READY requires:

- no unresolved critical blocker
- critical requirements verified
- critical claims supported
- judging criteria covered where known
- testing/security evidence sufficient
- demo evidence sufficient
- presentation evidence sufficient
- critical red-team findings resolved/accepted
- repository/submission prerequisites verified
- no known contradictory critical artifacts

CONDITIONAL when:

- no known critical blocker
- important live verification still unavailable
- non-critical evidence incomplete

BLOCKED when critical requirement prevents progression.

NOT_READY when meaningful preparation remains.

Never mark READY simply because audit framework passed tests.

---

# 29. Final Audit Score

Do not create misleading single project score.

If useful, report separate indicators:

- Evidence Completeness
- Requirement Coverage
- Claim Credibility
- Technical Readiness
- Demo Readiness
- Presentation Readiness
- Submission Readiness

Label as internal readiness indicators.

Not official judging scores.

---

# 30. Final Audit Finding Model

Each finding:

| Field | Description |
|-------|-------------|
| Finding ID | Unique identifier |
| Domain | Audit domain |
| Severity | CRITICAL / HIGH / MEDIUM / LOW |
| Description | Finding description |
| Evidence | Evidence supporting finding |
| Evidence Status | FACT / INFERENCE / ASSUMPTION / UNKNOWN |
| Confidence | HIGH / MEDIUM / LOW / UNKNOWN |
| Impact | Impact description |
| Recommendation | Recommended remediation |
| Owner Phase | Owning phase |
| Human Approval Required | YES / NO |
| Status | OPEN / IN_PROGRESS / VERIFIED_MITIGATED / ACCEPTED_RISK / BLOCKED / UNKNOWN / NOT_APPLICABLE |
| Verification | Verification evidence |
| Final Disposition | Final disposition |

Confidence separate from severity.

---

# 31. Human Authority

Human approval mandatory for:

- accepting critical risk
- changing selected idea
- changing project scope
- architecture changes
- destructive repository changes
- removing important evidence
- changing major claims
- removing judging-critical content
- submission decisions
- irreversible changes

AI recommends. Human decides.

---

# 32. Project State Fields

Update ONLY these compact fields in `.sherpa/project-state.md`:

| Field | Allowed Values |
|-------|---------------|
| Final Audit Status | NOT_STARTED | IN_PROGRESS | BLOCKED | COMPLETE |
| Final Readiness | NOT_READY | CONDITIONAL | BLOCKED | READY |
| Critical Findings | UNKNOWN | NONE | IDENTIFIED |
| Requirement Coverage | UNKNOWN | PARTIAL | COMPLETE |
| Criterion Coverage | UNKNOWN | PARTIAL | COMPLETE |
| Claim Audit Status | UNKNOWN | PARTIAL | COMPLETE |
| Demo Closure Status | UNKNOWN | COMPLETE | INCOMPLETE |
| Presentation Closure Status | UNKNOWN | COMPLETE | INCOMPLETE |
| Submission Prerequisites | UNKNOWN | PARTIAL | COMPLETE |
| Repository Audit Status | UNKNOWN | PARTIAL | COMPLETE |
| Security Audit Status | UNKNOWN | PARTIAL | COMPLETE |
| Documentation Audit Status | UNKNOWN | PARTIAL | COMPLETE |
| Final Risk Level | UNKNOWN | LOW | MEDIUM | HIGH | CRITICAL |
| Current Blocker | UNKNOWN | <blocker description> |
| Primary Next Action | UNKNOWN | <action> |

Rules:

- Do NOT put detailed audit inside project-state.md.
- Detailed material goes to `.sherpa/final-audit.md` and `.sherpa/final-audit/`.
- Do not change `selected idea`.
- Do not silently change architecture.
- Human approval required for critical risk acceptance.

---

# 33. Failure Cases

| Case | Behavior |
|------|----------|
| No selected idea | Stop and request confirmation |
| Missing Phase 17 evidence | Report FINAL-AUDIT = LIMITED; proceed with available evidence |
| Missing evidence | Mark UNKNOWN |
| Unsupported claim | Flag unsupported |
| Contradictory claims | Record contradiction; do not silently reconcile |
| Unknown deployment | DEPLOYMENT STATUS = UNKNOWN |
| Human approval required for critical risk | Route to HUMAN DECISION REQUIRED |

Phase 18 MUST NOT:

- Write application code
- Modify application source files
- Modify frontend/backend implementation
- Install dependencies
- Deploy application
- Change selected idea
- Silently redesign architecture
- Replace Phase 11–16 engines
- Perform final audit of live project without actual evidence
- Perform final submission
- Perform post-mortem
- Claim submission readiness without evidence
- Fabricate judge feedback
- Present unsupported presentation claims

Phase 18 does not perform final submission. Phase 19 owns submission execution.

## Final Output

Return the audit summary and exactly one **PRIMARY NEXT ACTION** addressing the highest-impact unresolved issue. Do not provide competing primary actions. Phase 18 does not execute Phase 19 submission or Phase 20 post-mortem.

---

# 34. Determinism

Same evidence, criteria, time remaining, and audit scope → same audit report and readiness determination every time. No randomness. No LLM-generated scores without explicit numeric input.
