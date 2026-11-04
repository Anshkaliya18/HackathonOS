# sherpa — TESTING + SECURITY Workflow

**Operation:** TESTING-SECURITY (Phase 5)  
**Purpose:** Evaluate implemented scope using real test/security evidence and a time-aware quality gate.

## Routing

Use for TEST, TESTING, SECURITY, SECURITY REVIEW, RUN TESTS, CHECK SECURITY, TEST PROJECT, AUDIT SECURITY, or VERIFY IMPLEMENTATION. A general “what next?” remains owned by `workflows/next.md`. Follow `rules/testing-security-rules.md`. Phase 4 files are frozen; do not modify them. Do not start Phase 6.

## Deterministic Workflow

1. **Read state first.** Read `.sherpa/project-state.md`. Verify the selected idea and implementation status. If implementation is `NOT_STARTED`, return `Testing blocked until implementation exists.` Do not claim testing readiness.
2. **Read approved plans.** Read the Phase 3 project plan and Phase 4 implementation plan at their recorded paths. Identify the approved MVP, implemented scope, critical flows, architecture, and recent changes. Missing plans/status are `UNKNOWN`/`BLOCKED`; do not infer completion.
3. **Inspect actual baseline.** Record repository root/revision when available, runtime/framework, frontend/backend, test frameworks and files, scripts, build/lint/typecheck commands, API/E2E/CI setup, fixtures/mocks, config/environment names, and known failures. Mark unavailable items UNKNOWN. Do not install dependencies.
4. **Create/update test plan.** Use `templates/test-plan.md` at `.sherpa/test-plan.md`. Plan only applicable categories. Map critical user flows and MUST HAVE behavior first; include security-sensitive paths, regression-prone areas, then lower-priority checks. Include expected results, priority, dependencies, and status.
5. **Prioritize for available time.** Apply `rules/testing-security-rules.md` Section 7. If time is UNKNOWN, write `TIME STRATEGY = UNKNOWN` and keep priorities time-neutral.
6. **Execute applicable checks.** Run only checks supported by the observed environment and relevant to scope. Capture exact command/procedure and direct result. If unavailable, record BLOCKED/UNKNOWN. Never treat build success as full test/security success.
7. **Record each result.** Use `templates/test-result.md` under `.sherpa/testing/test-NNN.md`. Preserve failures and output. Mark unrun checks PLANNED/UNKNOWN/BLOCKED, never PASSED.
8. **Analyze failures.** Record affected flow, impact, blocking status, and likely cause separately from evidence. Do not hide or relabel a failure. Route source fixes through the Phase 4 implementation process; Phase 5 records remediation and verifies it after implementation.
9. **Perform bounded security review.** Use `templates/security-review.md` at `.sherpa/security-review.md`. State scope, method, limitations, unknowns, and findings. Inspect applicable security areas listed in the rules. Use FACT/INFERENCE/ASSUMPTION/UNKNOWN and severity/confidence separately. Do not claim no vulnerabilities beyond scope.
10. **Audit dependencies when possible.** Use an already-available project-native auditor, record exact command and output. If unavailable, record dependency security status UNKNOWN; do not install an auditor or upgrade packages.
11. **Record and prioritize findings.** Create `.sherpa/security/finding-NNN.md` from `templates/security-finding.md`. Prioritize by severity, exploitability, impact, surface, confidence, and MVP relevance. Do not call a proposed fix FIXED.
12. **Verify remediation and regressions.** For each implemented fix, run focused verification plus directly affected tests, related tests, critical-flow tests, and security regressions as applicable. Record evidence. If regression cannot run, finding remains BLOCKED/UNKNOWN and is not verified.
13. **Evaluate quality gate.** Set `READY` only under rules Section 6. Critical failures or unresolved/unverified critical findings prevent READY. Use BLOCKED/CONDITIONAL when critical evidence is missing or lower-severity/unknown issues remain material.
14. **Update compact state.** Update only Phase 5 fields allowed by rules Section 8. Keep detail in artifacts. Do not change idea, architecture, MVP, or Phase 4 fields.
15. **Return exactly one primary next action.** State scope, baseline, critical test/security outcomes, direct evidence, failures, unknowns, gate, and one next action. Do not begin Phase 6.

## Failure Cases

- `Implementation status = NOT_STARTED`: `Testing blocked until implementation exists.`
- Missing tests: `UNKNOWN` / `NOT PRESENT`, not FAILED.
- Test command fails: record FAILED and output; rerun after any fix.
- Test environment broken: BLOCKED.
- Security evidence insufficient: UNKNOWN, with scope/limitations.
- Dependency auditor unavailable: dependency security UNKNOWN.
- Unverified fix: finding remains OPEN/IN_PROGRESS/BLOCKED, never FIXED.
- Critical unresolved failure/finding: gate is not READY.
- Unknown time: `TIME STRATEGY = UNKNOWN`.
- Requested architecture redesign: `ARCHITECTURE CHANGE REQUIRED`; defer to human-controlled architecture process.
- Request to change selected idea: preserve it; human decision required.

## Output Contract

Return exactly one `PRIMARY NEXT ACTION`; do not create a parallel NEXT engine or continue to Phase 6.
