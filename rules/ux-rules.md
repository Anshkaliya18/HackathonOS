# UX Review Rules

These rules are authoritative for the UX-REVIEW capability. UX review is lifecycle Phase 12; this is engineering capability Phase 7. Do not renumber or edit the 20-phase lifecycle.

## Purpose and boundaries

Evaluate whether the strongest user journeys are understandable, usable, reliable, accessible within a defined scope, responsive where tested, and convincing in a demo. Prioritize user outcomes over aesthetic preference. Review and recommend; do not change product scope, selected idea, approved Phase 3 architecture, Phase 4 implementation plan, or application source. Do not replace Phase 5 testing/security, judge simulation, score optimization, presentation, submission, or post-mortem work.

If a proposed remediation needs database/API redesign, authentication redesign, major frontend restructuring, service restructuring, or a major dependency change, record **ARCHITECTURE CHANGE REQUIRED**, why, evidence, impact, estimated effort, alternative, risk, and recommendation. Stop that remediation pending human-controlled architecture approval.

## Readiness and source of truth

Read `.hackathon/project-state.md`, the Phase 3 project plan, Phase 4 implementation plan/tasks, and Phase 5 test results/security review/findings before inspecting UX. UX review normally requires implementation READY/COMPLETE (or the project's explicit equivalent) and Phase 5 evidence showing the relevant scope is tested/reviewed. If implementation is NOT_STARTED, incomplete, or readiness cannot be established, report **UX review BLOCKED** or **NOT_READY**; do not imply a review occurred. A bounded static baseline may be offered only when clearly separated from a UX review and dynamic claims remain UNKNOWN.

Use the selected idea as context only. Never change it. Consume existing Phase 5 failures, blocked tests, security findings, and regression risks. If a UX question requires an automated or functional test, mark **TEST REQUIRED** and route it to the Phase 5 process; do not execute or duplicate that engine.

## Evidence model

Every claim is labeled FACT, INFERENCE, ASSUMPTION, or UNKNOWN. FACT identifies inspected source, UI, state, test, or direct observation. INFERENCE states its evidence and reasoning. ASSUMPTION is an explicit provisional premise. UNKNOWN includes what is missing and why. Every finding cites reproducible evidence: path/line, route/screen, viewport/device, steps, result, or evidence artifact. Never claim an interaction, viewport, assistive technology, or state was tested when it was not.

Never convert UNKNOWN into FACT. If evidence is unavailable, record UNKNOWN and explain what is missing and why.

Finding observation status is one of: OBSERVED, SUPPORTED, INFERRED, UNKNOWN, NOT_TESTED.
- OBSERVED: Directly visible or reproducible UX behavior.
- SUPPORTED: Strongly supported by available evidence such as screenshots, tests, source inspection, or runtime evidence.
- INFERRED: Reasonable conclusion based on available evidence but not directly verified.
- UNKNOWN: Insufficient evidence.
- NOT_TESTED: The relevant interaction or condition was not actually exercised.

Do not collapse these states. Finding workflow status is OPEN, IN_PROGRESS, FIXED, ACCEPTED_RISK, BLOCKED, or UNKNOWN. Do not confuse these status sets. A proposed change is not a fix. FIXED requires focused verification evidence and relevant regression consideration.

## Baseline and flow review

Inspect the actual project and record root/revision, frontend and backend relationship, routes/entry points, page/component structure, styles/design system/UI libraries, responsive CSS/breakpoints, forms/validation, loading/error/empty/success/disabled/retry/progress/confirmation states, navigation, authentication where applicable, accessibility semantics, test infrastructure, existing screenshots/evidence, known UX issues, and limitations. Mark absent or unavailable details UNKNOWN. If there is no frontend, record **UI = NOT PRESENT / UNKNOWN** and state the limited UX scope.

Review information architecture: content organization, page structure, grouping, terminology, discoverability, information density, and logical sequencing. Evaluate whether users can understand what belongs together, whether important information is easy to find, whether labels are meaningful, and whether the structure is predictable.

Identify and review relevant journeys in this order: first entry; primary value proposition; critical MVP action; result/output; error recovery; return/repeat use; demo/judge flow. For each flow record goal, target user, entry, preconditions, ordered steps, expected/observed outcome, friction, severity, evidence, observation status, and recommended action. A flow can be UNKNOWN or BLOCKED; never fabricate observed behavior.

Review clarity, labels, terminology, navigation/location, discoverability, actions, destructive intent, feedback, forms/validation/preserved input/defaults, content grouping, hierarchy, cognitive load, concrete visual hierarchy/usability consequences, and all applicable feedback states. Distinguish confirmed omissions from uninspected states.

## Accessibility and responsive boundaries

Record accessibility scope and limitations. Check applicable keyboard order and operability, visible focus, semantics, names/labels/form associations, contrast, zoom/text scaling, alternative text, ARIA correctness, error announcements, reduced motion, and touch target usability. Do not claim WCAG compliance without evaluation against a named version/level and defined scope. Prefer bounded language such as “No confirmed issue identified within the inspected scope.”

For responsive behavior record tested viewports and examine overflow/clipping, navigation, forms, controls, cards/tables/modals, touch behavior, spacing, and typography. Review mobile/tablet/desktop only when actually inspected. Untested sizes are UNKNOWN, never PASS.

## Findings and severity

Each finding includes a stable ID, title, category, severity, affected flow and component, concrete observation, evidence, user impact, reproduction steps, remediation, architecture impact, verification method, workflow status, and verification evidence. Categories: USABILITY, NAVIGATION, ACCESSIBILITY, RESPONSIVE, VISUAL_HIERARCHY, FORM, FEEDBACK, ERROR_HANDLING, ONBOARDING, CONTENT, CONSISTENCY, DEMO_FLOW, OTHER.

Confidence is recorded separately from severity as HIGH, MEDIUM, LOW, or UNKNOWN.

Severity considers flow criticality, frequency, blockage/confusion, accessibility and demo impact, recovery cost, and evidence confidence. CRITICAL blocks the primary journey or makes the demo fundamentally unusable; HIGH is major friction in a critical MVP flow; MEDIUM is meaningful with a workaround; LOW is minor friction/polish; INFO is an opportunity; UNKNOWN means evidence is insufficient. Do not inflate severity.

Priority uses P0, P1, P2, P3:
- P0: Critical UX blocker that prevents the primary task or demo; must be fixed or explicitly accepted.
- P1: High user/demo impact; fix before submission if time permits.
- P2: Meaningful UX weakness; fix after P0/P1 if time remains.
- P3: Minor polish; only if all higher priorities are complete.

Do not confuse severity and priority. HIGH severity does not automatically mean P0 if the fix cannot be safely completed within remaining time.

Conflicting UX evidence is recorded as a separate finding; do not silently reconcile contradictions between observations.

## Remediation, regression, and human authority

For each finding connect evidence → impact → recommendation → human/implementation decision when required → implementation through the existing Phase 4 process → focused UX verification → regression consideration (and Phase 5 test when needed) → evidence. Do not implement fixes as part of UX review. Do not mark FIXED without evidence. Do not mark a risk accepted without explicit human acceptance recorded in the project's decision evidence.

Phase 7 never changes architecture or selected idea. It may recommend and size a change; explicit human approval and the existing architecture/implementation processes are required. Do not claim regression passed without an executed check and result.

## Time strategy

- `>24h`: broad UX, accessibility, responsive review, then targeted polish.
- `12–24h`: critical flows, major usability, accessibility, demo polish.
- `6–12h`: critical journey, demo flow, obvious blockers, responsive essentials.
- `2–6h`: demo flow, navigation, forms, obvious breakage.
- `<2h`: freeze features; fix only demo blockers, critical usability/accessibility blockers, broken navigation/forms, or demo-device responsive failure.
- Unknown time: `TIME STRATEGY = UNKNOWN`; do not infer a deadline or remaining hours.

Within any window, critical blockers outrank low-impact visual polish.

## State, artifacts, and quality gate

Keep detailed evidence in `.hackathon/ux-review.md` and `.hackathon/ux/{flow-NNN,finding-NNN,verification-NNN}.md`. Add only these compact fields to the project's `.hackathon/project-state.md`, and only if the file already exists / is being legitimately updated by the workflow: UX status (`NOT_STARTED | IN_PROGRESS | BLOCKED | COMPLETE`); UX baseline (`UNKNOWN | VERIFIED`); Critical flows (`UNKNOWN | IDENTIFIED | REVIEWED`); Critical UX status (`UNKNOWN | PASS | FAIL | BLOCKED`); Accessibility status (`UNKNOWN | PASS | FAIL | BLOCKED`); Responsive status (`UNKNOWN | PASS | FAIL | BLOCKED`); UX quality gate (`NOT_READY | REVIEW_IN_PROGRESS | BLOCKED | CONDITIONAL | READY`). Do not change Phase 1 template/workflow files or add other state fields. Do not set UX COMPLETE merely because a review document exists.

Gate values: NOT_READY, REVIEW_IN_PROGRESS, BLOCKED, CONDITIONAL, READY. READY requires critical flows reviewed; no unexplained critical blocker; critical accessibility issues resolved or explicitly accepted; applicable critical responsive issues resolved or explicitly accepted; major navigation/usability issues addressed or accepted; findings evidence-backed; every claimed fix verified; and limitations documented. Unknown applicability or missing evidence prevents READY and may yield CONDITIONAL/BLOCKED. A polished appearance alone is insufficient.

Return exactly one **PRIMARY NEXT ACTION**, chosen from the highest-impact unresolved blocker or next required human decision. Do not create another NEXT/lifecycle engine. Never silently change scope or fabricate observations, tests, fixes, approvals, or remaining time.
