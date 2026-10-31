# HackathonOS — Phase 19 Submission Rules

**Lifecycle Phase:** Phase 19 — Submission Intelligence  
**Operation:** `SUBMISSION-PREPARE`  
**Purpose:** Discover, verify, and freeze a submission package. Phase 19 prepares; the human submits.

## Authority and evidence

Use sources in this order: official rules; official portal instructions; organizer communications; official judging criteria; explicit project requirements; project-specific instructions; user information; internal artifacts. Preserve conflicts, identify authority, and request human verification where needed. An undocumented requirement is not mandatory absent evidence.

Classify evidence as FACT, INFERENCE, ASSUMPTION, or UNKNOWN. Each VERIFIED claim must cite its actual source and verification method. A file's existence does not prove its contents, accessibility, permissions, correctness, freshness, or format. UNKNOWN never becomes verified by inference. Do not use fabricated test, build, dependency, API, URL, access, submission, or deployment claims.

## Requirement and status models

Each requirement records ID, requirement, source, mandatory flag, evidence, artifact/field, status, owner, deadline, and notes. Status: VERIFIED, READY, MISSING, INVALID, BLOCKED, UNKNOWN, NOT_APPLICABLE.

Deadline record: deadline, timezone, source, confidence, current status, time remaining. Deadline states: UPCOMING, URGENT, DUE_SOON, DEADLINE_PASSED, UNKNOWN. Never assume a timezone or invent a deadline.

Artifact record: ID, name, type, location, version, required flag, accessibility, verification, last checked, hash/identifier, status. Field record: ID, field, required flag, value, source, evidence, character limit, format, status, notes. Unknown values stay UNKNOWN.

Link states: VERIFIED_ACCESSIBLE, ACCESSIBLE_WITH_AUTH, BROKEN, REDIRECTED, UNKNOWN, NOT_APPLICABLE. Access states: PUBLIC, RESTRICTED, AUTH_REQUIRED, EXPIRED, UNKNOWN. Verify syntax, destination, expected content, permissions, authentication, and expiry when possible. Do not expose credentials or recommend public exposure of sensitive data.

## Verification boundaries

Inspect the actual repository and available package. Check repository/branch/intended commit, README and setup documentation, required files, links, accidental private data, debug artifacts, and configuration. Verify deployment, demo/video, PPT and file limits only when actual artifacts and authoritative requirements are available. Never imply setup works without executing it. Secret checks use bounded scope language: “No secret indicators were detected within the audited submission scope.”

Keep submission form, README, PPT, demo, repository, deployment, project description, selected idea, and final audit claims consistent. Audit claims as VERIFIED, SUPPORTED, PARTIALLY_SUPPORTED, UNSUPPORTED, CONTRADICTED, UNKNOWN. Unsupported claims must be corrected or removed; contradicted claims must not be submitted; metrics require evidence.

## Snapshot, freeze, and readiness

Create a submission snapshot with snapshot ID, timestamp/timezone, repository commit, branch, frontend/backend/PPT/video/documentation versions, deployment URL, and status. Mark missing values UNKNOWN. After snapshot, classify changes REQUIRED, SAFE, RISKY, or FORBIDDEN_AFTER_FREEZE. Freeze is ACTIVE only after critical artifacts are verified; unresolved required unknowns prevent claiming complete verification. After freeze, only critical submission fixes, broken-link fixes, required metadata corrections, access fixes, and organizer-required changes are routine. Destructive changes, idea changes, major architecture changes, replacing the submission artifact, and scope changes require explicit human approval.

Readiness values: NOT_READY, CONDITIONAL, BLOCKED, READY_TO_SUBMIT. READY_TO_SUBMIT requires all mandatory requirements verified, required artifacts and formats verified, links accessible, critical claims supported, no unresolved critical blockers, a consistent package and final snapshot, deadline known or explicitly verified, and human confirmation still pending. Framework validation alone never yields live READY_TO_SUBMIT. Human submission remains external and unchecked.

Each risk records ID, description, severity, likelihood, confidence, impact, mitigation, owner, status. Keep severity and confidence separate. Critical risk blocks READY unless VERIFIED_MITIGATED or ACCEPTED_RISK with human authority.

## Human control and prohibited operations

Always surface `FINAL HUMAN CONFIRMATION REQUIRED` before the eventual human submission, including package, destination, deadline/timezone, risks, snapshot, unresolved noncritical issues, and irreversible consequences. The system must NEVER click a final submit button, submit a form or entry, publish private information, change repository visibility, upload to the portal, or accept irreversible terms. It never performs the actual submission. The final checklist item “Submission performed” remains unchecked in Phase 19.

Do not develop features, redesign architecture/demo/PPT/final audit, change the selected idea, perform post-mortem, install dependencies, deploy, or modify application code. Preserve locked Phase 1–18 behavior and exactly one `PRIMARY NEXT ACTION`.
