# HackathonOS — Testing + Security Rules

Defines authoritative Phase 5 behavior. Phase 5 inspects the implemented project, creates test/security plans, executes applicable checks, records evidence, and evaluates quality. Phase 4 is a frozen dependency: never modify its rules, templates, or workflow. Phase 5 does not replace Phase 4 or silently modify application code or architecture.

## 1. Readiness and evidence first

Read `.hackathon/project-state.md`, the Phase 3 project plan, and `.hackathon/implementation-plan.md` before normal testing. Read artifacts at explicitly referenced stable paths when needed. Inspect the actual repository and test baseline before making claims.

- If `Implementation status = NOT_STARTED`, report `Testing blocked until implementation exists.` Do not run a normal project test campaign.
- If implementation status, selected idea, or required plans are missing/UNKNOWN, mark readiness `UNKNOWN` or `BLOCKED`; do not infer readiness from an artifact alone.
- If status is `IN_PROGRESS`, test implemented scope only and label incomplete flows accordingly. If status is `BLOCKED`, tests may be run only for an explicitly bounded existing scope; overall quality cannot be READY while the blocker remains unexplained.
- Implementation status `COMPLETE` permits testing; it does not prove quality.

Every test/security assertion uses one status: `PLANNED`, `EXECUTED`, `PASSED`, `FAILED`, `BLOCKED`, or `UNKNOWN`. A pass requires direct execution evidence (command/procedure, scope, result, and output or report). An unexecuted check is never PASSED. A missing test framework is `UNKNOWN` or `NOT PRESENT`, not FAILED. A broken/unavailable environment is `BLOCKED`.

Generated plans, reviews, and finding records are not independent execution evidence. Do not invent tool availability, test results, vulnerabilities, scan results, CI status, or dependency audit results.

## 2. Test baseline and categories

Record observed test framework/runner, test directories/files, scripts, build/lint/typecheck commands, API/E2E setup, CI, runtime, application structure, configuration/environment names, test data, fixtures, mocks, and known failures. Do not expose secret values. For each item state the evidence source or UNKNOWN.

Use only applicable categories: `UNIT`, `INTEGRATION`, `E2E`, `UI`, `API`, `SECURITY`, `PERFORMANCE`, `ACCESSIBILITY`, and `MANUAL`. No project must use all categories. Do not describe a script or test file as passing until it has actually been run.

Prioritize in order: critical user flows; MUST HAVE MVP behavior; authentication/authorization where applicable; data validation/integrity; API boundaries; error handling; security-sensitive paths; regression-prone areas; secondary features; optional features. Do not spend limited time on optional checks while critical flows remain unverified.

## 3. Test execution and failures

Use `templates/test-plan.md` at `.hackathon/test-plan.md` and `templates/test-result.md` at `.hackathon/testing/test-NNN.md`. Record planned tests separately from executed results. Before execution, state expected result and relevant scope. After execution, capture exact command/procedure, exit/result, relevant output, date/time, and affected revision when available.

- Mark a check `EXECUTED` while evidence is being recorded; mark `PASSED` only when observed results meet its expected result.
- Preserve failures as `FAILED` with output, impact, and affected component. Do not relabel them PASSED without a rerun that succeeds.
- If a test cannot run due to absent tools, dependencies, data, or environment, mark `BLOCKED` and identify the blocker. Do not install dependencies merely to make a test possible.
- Record tests not applicable with a reason; do not fabricate coverage.

## 4. Bounded security review

Use `templates/security-review.md` at `.hackathon/security-review.md` and `templates/security-finding.md` at `.hackathon/security/finding-NNN.md`. Every review states scope, files/areas inspected, method, limitations, and unknowns. Never claim a complete security audit from bounded inspection. Use the phrase `No confirmed vulnerabilities identified within the inspected scope.` only when it is accurate; it does not imply the whole application is safe.

Cover applicable areas: authentication, authorization/access control, input validation, output encoding, injection, secrets/environment, sensitive data, file/upload handling, API exposure, CORS, CSRF, XSS, SQL/NoSQL injection, command execution, path traversal, dependency vulnerabilities, rate limiting, logging, error leakage, and session/token handling. Mark uninspected or uncertain areas `UNKNOWN`. Classify observations `FACT`, `INFERENCE`, `ASSUMPTION`, or `UNKNOWN`, with source and confidence. Do not label a vulnerability without supporting evidence.

Use severity `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFO`, or `UNKNOWN`, based on exploitability, impact, affected surface, likelihood, and evidence. Do not inflate severity. Record confidence as `HIGH`, `MEDIUM`, `LOW`, or `UNKNOWN` separately from severity.

For dependency auditing, use an already-available project-native audit tool where practical. Record the exact command and results. If no appropriate tool is available, set dependency security status to `UNKNOWN`. Never install an auditor or automatically upgrade dependencies as part of review.

## 5. Remediation and regression

For each actionable finding record finding, impact, recommended remediation, approval/implementation decision required, focused verification method, and regression checks. Source changes and dependency upgrades are implementation work: route them through the approved Phase 4 process. Phase 5 may verify a fix after it exists; a proposed patch is not a fixed finding.

Mark a finding `FIXED` only after focused verification evidence passes. Meaningful fixes require identifying directly affected tests, related tests, critical user-flow checks, and security regression checks where applicable. If appropriate regression cannot run, status is `BLOCKED` or `UNKNOWN`, not verified.

## 6. Quality gate

Allowed quality gate values: `NOT_READY`, `TESTING_IN_PROGRESS`, `BLOCKED`, `CONDITIONAL`, `READY`.

`READY` requires all applicable critical tests to be executed and passed; critical failures resolved or explicitly accepted by a human; critical security findings fixed and verified or explicitly accepted by a human; no unexplained blocker; and evidence-backed status. A successful build alone is insufficient. Missing/unverified information, an open critical finding, or an unverified critical fix prevents READY. Keep the gate CONDITIONAL or BLOCKED when applicable tests, reviews, or regression evidence remain unavailable.

## 7. Time-aware testing

Use the existing project deadline/time. Do not calculate a false estimate or invent a deadline.

| Time remaining | Focus |
|---|---|
| >24h | Broad testing, security review, regression, and quality |
| 12–24h | MVP critical paths, security, high-value regression |
| 6–12h | Critical user flow, security-sensitive paths, demo reliability |
| 2–6h | Smoke tests, critical security checks, recent-change regression |
| <2h | Freeze features; test core demo, critical failures, obvious security risks, runtime-critical behavior |
| UNKNOWN | `TIME STRATEGY = UNKNOWN`; time-neutral prioritization |

## 8. Compact project state

Add/update only these Phase 5 fields in `.hackathon/project-state.md`:

| Field | Allowed values |
|---|---|
| Testing status | `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETE` |
| Test baseline | `UNKNOWN`, `VERIFIED` |
| Security review | `UNKNOWN`, `IN_PROGRESS`, `COMPLETE` |
| Critical test status | `UNKNOWN`, `PASS`, `FAIL`, `BLOCKED` |
| Critical security status | `UNKNOWN`, `PASS`, `FAIL`, `BLOCKED` |
| Quality gate | `NOT_READY`, `TESTING_IN_PROGRESS`, `BLOCKED`, `CONDITIONAL`, `READY` |

Do not add arbitrary fields or put detailed test/finding data in state. `Testing status = COMPLETE` means the defined Phase 5 test/review scope is complete, not that every test passed. Do not alter the selected idea, architecture, MVP, or Phase 4 implementation status.

## 9. Output

Return exactly one `PRIMARY NEXT ACTION`. Include readiness, scope, test/security status, executed evidence and failures, blockers/unknowns, quality gate, and one next action. Never start Phase 6.
