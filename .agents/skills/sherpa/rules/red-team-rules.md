# sherpa — Red Team Rules

These rules are authoritative for the RED-TEAM capability. Red Team is lifecycle Phase 13; this is engineering capability Phase 8. Do not renumber or edit the 20-phase lifecycle.

## Purpose and boundaries

Actively attempt to disprove project readiness. Attack the project and its claims — not the team. Identify hidden weaknesses, technical weaknesses, product weaknesses, UX weaknesses, differentiation weaknesses, judging weaknesses, demo weaknesses, evidence weaknesses, credibility risks, and failure modes.

Review and recommend; do not change product scope, selected idea, approved Phase 3 architecture, Phase 4 implementation plan, application source, or Phase 5/Phase 7 results. Do not replace Phase 5 testing/security, Phase 7 UX review, judge simulation, score optimization, presentation, submission, or post-mortem work.

If a proposed remediation needs database/API redesign, authentication redesign, major frontend restructuring, service restructuring, or a major dependency change, record **ARCHITECTURE CHANGE REQUIRED**, why, evidence, impact, estimated effort, alternative, risk, and recommendation. Stop that remediation pending human-controlled architecture approval.

## Readiness and source of truth

Read `.sherpa/project-state.md`, the Phase 2 idea evaluation, Phase 3 project plan, Phase 4 implementation evidence, Phase 5 testing/security evidence, and Phase 7 UX evidence before inspecting UX. Red Team review normally requires implementation baseline, Phase 5 evidence, and Phase 7 evidence. If implementation is incomplete or readiness cannot be established, report **RED TEAM REVIEW = BLOCKED** or **LIMITED**; do not imply a review occurred.

Use the selected idea as context only. Never change it. Consume existing Phase 2 idea evaluation, Phase 3 project plan, Phase 4 implementation state, Phase 5 test/security findings, and Phase 7 UX findings. If a red-team question requires an automated or functional test, mark **TEST REQUIRED** and route it to the Phase 5 process; do not execute or duplicate that engine.

## Evidence model

Every claim is labeled FACT, INFERENCE, ASSUMPTION, or UNKNOWN. FACT identifies inspected source, UI, state, test, or direct observation. INFERENCE states its evidence and reasoning. ASSUMPTION is an explicit provisional premise. UNKNOWN includes what is missing and why. Every finding cites reproducible evidence: path/line, route/screen, steps, result, or evidence artifact. Never claim an interaction, state, or behavior was tested when it was not.

Generated sherpa artifacts are not independent evidence. Evidence must trace back to repository inspection, actual execution, external verification, or explicit human-provided information. Do not treat previous AI-generated recommendations as facts.

## Attack surfaces

Inspect applicable attack surfaces: Product, Differentiation, Technical, Reliability, Security/Trust, Privacy, UX, Accessibility, Responsive, Demo, Performance, Evidence, Credibility, Deployment.

Challenge every important project claim. Distinguish "the application performs the algorithm" from "the algorithm produces high-quality outcomes." Challenge unsupported statistics, unsupported performance claims, unsupported user claims, unsupported AI claims, "production-ready" claims, "secure" claims, "scalable" claims, "real-time" claims, and "zero vulnerabilities" claims.

Functional abuse scenarios include invalid input, missing input, duplicate actions, repeated submissions, unexpected navigation, invalid sequences, and unsupported actions.

## Adversarial actors

The system considers applicable perspectives:

| Actor | Perspective |
|-------|-------------|
| Malicious User | Attempts to abuse the product |
| Careless User | Makes realistic mistakes |
| Curious User | Explores unsupported behavior |
| Skeptical Judge | Challenges claims and asks difficult questions |
| Unlucky Runtime | Produces timing, network, storage, or dependency failures |
| Invalid Input | Provides malformed or unexpected data |
| Empty Environment | Removes expected data/resources |
| Partial Failure | Breaks one component while others remain operational |
| Repeated Action | Performs the same action multiple times |
| Boundary Condition | Uses minimum, maximum, zero, empty, unusually large, or unusual values |

Every applicable actor must be considered at least once. Actors not applicable to the project are marked NOT_APPLICABLE with justification.

## Adversarial scenarios

Each scenario contains: Scenario ID, Attack Surface, Attacker/Skeptical Judge Perspective, Preconditions, Attack, Expected Failure, Actual Result, Evidence, Severity, Confidence, Finding, Mitigation, Verification Method, Status.

Only scenarios applicable to the actual project should be executed. Non-applicable scenarios are marked NOT_APPLICABLE with justification.

## Finding model

Each finding contains: Finding ID, Title, Attack Surface, Category, Severity, Confidence, Affected Flow/Component, Claim Challenged, Observation, Evidence, Attack/Reproduction Steps, User Impact, Judge Impact, Technical Impact, Recommended Mitigation, Required Owner, Required Phase, Architecture Impact, Verification Method, Status, Verification Evidence.

Categories: PRODUCT, DIFFERENTIATION, TECHNICAL, RELIABILITY, SECURITY, PRIVACY, UX, ACCESSIBILITY, RESPONSIVE, DEMO, PERFORMANCE, EVIDENCE, CREDIBILITY, DEPLOYMENT, OTHER.

Severity: CRITICAL / HIGH / MEDIUM / LOW / INFO / UNKNOWN. CRITICAL blocks the primary flow or makes the demo fundamentally unusable; HIGH is a major MVP weakness or significant reliability issue; MEDIUM is a meaningful weakness with a workaround; LOW is minor friction; INFO is an observation; UNKNOWN means insufficient evidence. Do not inflate severity.

Confidence: HIGH / MEDIUM / LOW / UNKNOWN. Depends on evidence quality. Do not give HIGH confidence to speculation.

## Likelihood

Use: VERY_HIGH / HIGH / MEDIUM / LOW / VERY_LOW / UNKNOWN. Never fabricate likelihood. If evidence is insufficient, record UNKNOWN.

## Recoverability

Use: AUTOMATIC / EASY / MANUAL / DIFFICULT / NONE / UNKNOWN. Evaluate whether the user/system can recover from the failure.

## Red Team Scoring

Do NOT create a fake official hackathon score. Red Team may calculate a risk-priority indicator for internal ordering. If used, explicitly label it:

```
INTERNAL RED TEAM PRIORITIZATION
NOT OFFICIAL JUDGING SCORE
```

Never mix it with Phase 10 score optimization.

## Critical Finding Rule

A CRITICAL finding must prevent unconditional RED_TEAM_QUALITY_GATE = READY unless it is VERIFIED_MITIGATED or explicitly ACCEPTED_RISK with human authority. Do not silently downgrade a CRITICAL finding.

## Findings and status

Finding status: OPEN / IN_PROGRESS / MITIGATED / VERIFIED / ACCEPTED_RISK / BLOCKED / UNKNOWN / NOT_APPLICABLE / WONT_FIX. A finding may only become VERIFIED after actual verification evidence exists. Never mark a mitigation verified merely because a recommendation was written.

## Mitigation routing

Every meaningful finding determines where action belongs:

- PHASE 4 — IMPLEMENTATION: technical code bugs, implementation gaps
- PHASE 5 — TESTING / SECURITY: missing security verification, missing test coverage
- PHASE 7 — UX: UX issues, usability problems
- PHASE 8 — RED TEAM: red-team-specific mitigations, scenario validation
- HUMAN ARCHITECTURE APPROVAL: architecture limitations
- FUTURE PHASE: judge/pitch issues, presentation issues
- ACCEPTED RISK: risks explicitly accepted by human

Do not fix issues by silently modifying another phase.

## Priority order

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

## Time-aware red team strategy

Use verified remaining time:

- >24 hours: Broad adversarial testing + mitigation + regression
- 12–24 hours: Critical flows + high-risk technical/product weaknesses + demo reliability
- 6–12 hours: Primary user journey + demo + critical reliability + major claims
- 2–6 hours: Demo-breaking scenarios + critical MVP failures + obvious credibility risks
- <2 hours: Freeze features. Attack only: demo path, critical MVP, obvious reliability failures, obvious unsupported claims, severe trust/security issues

If time is UNKNOWN: TIME STRATEGY = UNKNOWN. Never fabricate remaining time.

## Red team quality gate

Gate values: NOT_READY / RED_TEAM_IN_PROGRESS / BLOCKED / CONDITIONAL / READY.

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

A project can be RED TEAM READY while still having accepted medium/low risks. A strong red-team review should find weaknesses.

## State and artifacts

Keep `.sherpa/project-state.md` compact. Add only these fields:

| Field | Values |
|-------|--------|
| Red Team Status | NOT_STARTED | IN_PROGRESS | BLOCKED | COMPLETE |
| Red Team Baseline | UNKNOWN | VERIFIED |
| Critical Attack Surfaces | UNKNOWN | IDENTIFIED | REVIEWED |
| Critical Findings | UNKNOWN | PASS | FAIL | BLOCKED |
| High Findings | UNKNOWN | PASS | FAIL | BLOCKED |
| Red Team Quality Gate | NOT_READY | RED_TEAM_IN_PROGRESS | BLOCKED | CONDITIONAL | READY |

Detailed material belongs in `.sherpa/red-team.md` and `.sherpa/red-team/{claim-NNN,scenario-NNN,finding-NNN,verification-NNN}.md`. Do not turn project-state.md into a giant report.

## Human control

Human approval is required for:
- idea changes
- architecture changes
- major scope changes
- destructive refactors
- accepting CRITICAL risk
- accepting HIGH security/privacy risk
- irreversible changes

AI recommends. Human decides. Phase 8 never changes the selected idea or silently redesigns architecture.

## Exactly one primary next action

Every successful Red Team workflow execution returns exactly one PRIMARY NEXT ACTION. Do not create another NEXT engine.
