# sherpa — Final Audit Rules

**Lifecycle Phase:** Phase 18 — Final Audit Intelligence  
**Purpose:** Authoritative rules for final audit. Phase 18 performs verification and final readiness audit. It does not implement, replace prior phases, or modify locked artifacts. Phase 18 audits and recommends; it does not execute submission.

---

## 1. Purpose and Boundaries

Phase 18 converts validated project evidence into a final audit report and readiness determination. It answers:

> "Based on the available evidence, what is actually ready, what is not ready, and what must happen before submission?"

Phase 18 may inspect:

- All prior-phase evidence
- Official judging criteria and weights
- Project evidence
- Demo evidence
- Presentation evidence
- Repository evidence
- Deployment evidence
- Submission requirements

Phase 18 MUST NOT:

- Implement new product features
- Modify application source code
- Silently redesign architecture
- Change the selected idea
- Reselect the idea
- Perform final submission
- Perform post-mortem
- Create PPT
- Perform demo execution
- Replace Phase 11 testing/security
- Replace Phase 12 UX review
- Replace Phase 13 red-team
- Replace Phase 14 judge simulation
- Replace Phase 15 score optimization
- Replace Phase 16 demo preparation
- Claim submission readiness without evidence
- Fabricate judge feedback
- Present unsupported presentation claims
- Treat presentation readiness as official judging score
- Invent judging criteria
- Fabricate evidence
- Treat framework validation as live project validation

---

## 2. Evidence Model

Every important audit claim must identify its evidence status.

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
- Code presence does not prove runtime behavior.
- A passing test does not prove unrelated functionality.
- A screenshot does not prove current live behavior.
- A demo rehearsal does not prove production reliability.
- Generated sherpa artifacts are not independent evidence.
- Evidence must trace back to repository inspection, actual execution, external verification, or explicit human-provided information.
- Do not treat previous AI-generated recommendations as facts.

Evidence types:

| Type | Definition |
|------|------------|
| source code | Application source code inspection |
| test result | Test execution result |
| runtime output | Program runtime output |
| log | Log or trace output |
| artifact | Generated file or artifact |
| screenshot | Static screenshot image |
| recording | Recorded video or demo |
| documentation | Documented claim |
| benchmark | Benchmark or measurement result |
| source/code inspection | Direct source code inspection |
| deployment | Deployment configuration or result |
| judge simulation | Judge simulation evidence |
| demo rehearsal | Demo rehearsal evidence |
| presentation artifact | Presentation artifact |
| security review | Security review finding |
| UX review | UX review finding |
| red-team result | Red-team finding |

---

## 3. Audit Status Model

Each audited item receives:

| Status | Definition |
|--------|------------|
| PASS | Evidence supports the requirement |
| PASS_WITH_LIMITATION | Requirement substantially satisfied but has documented limitation |
| FAIL | Evidence demonstrates requirement not satisfied |
| BLOCKED | Verification cannot proceed; dependency unavailable |
| UNKNOWN | Insufficient evidence to determine status |
| NOT_APPLICABLE | Requirement genuinely does not apply |

Rules:

- UNKNOWN never becomes PASS without new evidence.
- UNKNOWN never becomes PASS_WITH_LIMITATION.
- UNKNOWN never becomes FAIL.
- UNKNOWN never becomes BLOCKED.
- UNKNOWN never becomes NOT_APPLICABLE.
- An artifact existing does not prove its claims.
- Documentation does not automatically prove implementation.
- Code presence does not prove runtime behavior.
- A passing test does not prove unrelated functionality.
- A screenshot does not prove current live behavior.
- A demo rehearsal does not prove production reliability.
- A presentation claim does not prove product capability.

---

## 4. Final Audit Evidence Record

Each evidence record:

| Field | Description |
|-------|-------------|
| Evidence ID | Unique identifier |
| Source Phase | Phase that produced evidence |
| Artifact | Artifact name or path |
| Claim / Requirement | What is being evidenced |
| Evidence Type | Source type |
| Evidence Status | FACT / INFERENCE / ASSUMPTION / UNKNOWN |
| Verification Method | How verified |
| Observed Result | Observed result |
| Confidence | HIGH / MEDIUM / LOW / UNKNOWN |
| Related Finding | Related finding ID |

Evidence types may include:

- source code
- test result
- runtime output
- log
- artifact
- screenshot
- recording
- deployment
- configuration
- documentation
- judge simulation
- demo rehearsal
- presentation artifact
- security review
- UX review
- red-team result

---

## 5. Audit Domains

Audit domains:

| Domain | Description |
|--------|-------------|
| A | Lifecycle Integrity |
| B | Idea / Problem Alignment |
| C | Product / MVP Alignment |
| D | Architecture / Implementation Alignment |
| E | Testing |
| F | Security |
| G | UX / Accessibility |
| H | Red Team |
| I | Judge Simulation |
| J | Score Optimization |
| K | Demo |
| L | Presentation |
| M | Evidence Integrity |
| N | Documentation |
| O | Repository / Deployment |
| P | Submission Requirements |
| Q | Known Risks |
| R | Final Readiness |

Do not silently omit a domain.

If evidence is unavailable:

> UNKNOWN

---

## 6. Final Blocker Rule

A CRITICAL finding must prevent unconditional final readiness unless:

- VERIFIED_MITIGATED
- ACCEPTED_RISK with human authority
- NOT_APPLICABLE with evidence

Do not hide critical findings.
Do not silently downgrade them.

---

# 7. Cross-Phase Consistency

Build consistency audit:

```text
Selected Idea
    → Problem
    → MVP
    → Architecture
    → Implementation
    → Testing
    → UX
    → Red Team
    → Judge Simulation
    → Score Optimization
    → Demo
    → Presentation
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

Every contradiction becomes an explicit finding.

---

# 8. Selected Idea Stability

Verify selected idea remains stable. Do not silently reselect.

If material divergence exists:

> IDEA_ALIGNMENT = FAIL

Do not silently change idea.

---

# 9. Requirement Coverage

Extract requirements from:

- Hackathon rules
- Judging criteria
- Project requirements
- Phase 1 outputs
- Selected idea
- MVP definition
- Implementation plan
- Testing/security requirements
- Demo requirements
- Presentation requirements

If official rules unavailable:

> RULES = UNKNOWN

Do not fabricate compliance.

---

# 10. Judging Criteria Coverage

Use official criteria when available:

| Criterion | Weight | Evidence | Implementation Support | Demo Support | Presentation Support | Coverage | Confidence |

Use exact official terminology.

If weights unavailable:

> WEIGHT = UNKNOWN

Do not invent weights.

Do not calculate official score unless official judging mathematics known.

---

# 11. Score Separation

Phase 18 summarizes prior internal estimates but keeps separate:

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

# 12. Claim Audit

Audit claims from README, documentation, UI, demo, PPT, speaker notes, judge answers, project description, marketing text.

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

# 13. Metric Audit

Audit numerical claims:

| Metric | Value | Unit | Source | Measurement Method | Date | Evidence Status | Confidence |

Before using: user counts, accuracy, latency, revenue, savings, growth, adoption, performance, benchmark results, market size, percentage improvements — all require evidence.

Never fabricate precision.

If metric cannot be verified:

> UNKNOWN

---

# 14. Testing Audit

Verify Phase 11 evidence:

- tests actually executed
- PASS has evidence
- critical paths tested
- failure cases addressed
- regression evidence exists
- blocked tests remain blocked
- UNKNOWN remains UNKNOWN

Do not infer full project quality from passing framework test.

Distinguish framework validation from live project validation.

---

# 15. Security Audit

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

# 16. UX / Accessibility Audit

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

# 17. Red Team Closure Audit

Review Phase 13 findings:

| Finding | Severity | Evidence | Status | Mitigation | Verification | Owner | Final Disposition |

Open CRITICAL finding blocks unconditional readiness.

---

# 18. Judge Simulation Closure

Review Phase 14:

- critical judge questions
- skeptical follow-ups
- weak claims
- unsupported answers
- evidence gaps
- unresolved credibility concerns

Answer readiness:

- READY
- PARTIALLY_READY
- WEAK
- UNKNOWN
- NOT_APPLICABLE

Do not convert weak answers into READY without new evidence.

---

# 19. Score Optimization Closure

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

# 20. Demo Closure

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

# 21. Presentation Closure

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

# 22. Repository Audit

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

# 23. Secret / Sensitive Data Audit

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

> No secret indicators identified within inspected scope.

---

# 24. Documentation Consistency

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

# 25. Deployment Audit

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

# 26. Submission Requirements Audit

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

# 27. Last-Minute Change Protection

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

# 28. Final Risk Register

Each risk:

| Risk ID | Description | Source Phase | Severity | Likelihood | Confidence | Impact | Mitigation | Owner | Status | Final Disposition |

Confidence separate from severity.

---

# 29. Final Readiness Gate

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
- but important live verification still unavailable
- non-critical evidence incomplete

BLOCKED when critical requirement prevents progression.

NOT_READY when meaningful preparation remains.

Never mark READY simply because audit framework passed tests.

---

# 30. Final Audit Score

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

# 31. Final Audit Finding Model

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

# 32. Human Authority

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

# 33. Project State Fields

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

# 34. Failure Cases

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
- Present unsupported claims

---

# 35. Determinism

Same evidence, criteria, time remaining, and audit scope → same audit report and readiness determination every time. No randomness. No LLM-generated scores without explicit numeric input.
