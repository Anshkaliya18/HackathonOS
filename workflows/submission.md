# HackathonOS — SUBMISSION-PREPARE Workflow

**Lifecycle Phase:** Phase 19 — Submission Intelligence  
**Purpose:** Prepare, verify, and freeze submission materials without submitting them.

## Hard prerequisites

1. Read `workflows/lifecycle.md`; require exactly 20 phases in order: Phase 18 Final Audit, Phase 19 Submission, Phase 20 Post-Mortem. Do not renumber or repair.
2. Read `audits/phase18-final-report.md`; require explicit `PHASE 18 COMPLETE & LOCKED`. If absent, stop and report the blocker.
3. Inspect Phase 18 implementation, report, and applicable Phase 1–18 contracts. Preserve all locked behavior.
4. Do not perform an actual competition submission or begin Phase 20.

## Procedure

1. Read `.hackathon/project-state.md` and prior phase evidence if present. If absent, record that no live project state was inspected; do not treat this framework repository as the project package.
2. Inspect the actual current repository and its metadata. Cite paths, command output, hashes, or captured evidence. Separate observed FACT from INFERENCE and UNKNOWN. Never simulate inspection.
3. Discover requirements using the authority order in `rules/submission-rules.md`. Record each in the requirement template. Preserve source conflicts; do not invent mandatory requirements.
4. Record deadline, timezone, source, confidence, status and time remaining. Unknown deadline/timezone stays UNKNOWN; use the documented deadline strategy only where actual time is known.
5. Inventory only existing/identified artifacts. Record version/location/access/verification independently. Do not claim an artifact exists because a template names it.
6. Map submission fields from evidence; unknown or personal/team data remain UNKNOWN. Apply limits/formats only when an authoritative source provides them.
7. Check each known URL for syntax, destination, content, access, authentication and expiry where actual verification can be performed. Record method/result/time. Unchecked links remain UNKNOWN.
8. Verify permissions for intended judges. Restricted required artifacts are blockers unless official rules permit restricted access. Do not expose secrets or change visibility.
9. Audit repository identity, branch, intended commit, README/setup, required files, links, sensitive data, debug artifacts and configuration. Report setup only as verified if it was actually run and evidence recorded; do not install dependencies or alter source.
10. Verify deployment, demo/video, presentation, formats and limits only against actual artifacts and official requirements. If not available, set UNKNOWN. Do not redesign these artifacts.
11. Build consistency and claim matrices across form, README, PPT, demo, repository, deployment, project description, selected idea and Phase 18 audit. Preserve contradictions as findings. Unsupported/contradicted claims are not submission-ready.
12. Run a bounded secret/sensitive-data check on the recorded scope. State the exact scope and method; never claim absolute absence.
13. Build the risk register, snapshot, and change classification. Values unavailable in repository metadata are UNKNOWN. Activate submission freeze only once all critical artifacts are verified.
14. Determine readiness from evidence using the gate in the rules. Missing live package or official requirements implies CONDITIONAL at best; do not claim READY_TO_SUBMIT from framework tests.
15. Present `FINAL HUMAN CONFIRMATION REQUIRED` and the final checklist. “Submission performed” must remain unchecked. Never invoke portal actions, upload, publish, change visibility, or submit.
16. Record exactly one `PRIMARY NEXT ACTION`.

## Required outputs

Use the Phase 19 templates for requirement records, inventory, field mapping, links, risks, checklist, snapshot, and verification. Produce `.hackathon/submission-plan.md` and detailed evidence under `.hackathon/submission/` only in the actual project repository. Framework validation evidence belongs in `audits/phase19-final-report.md`. Keep `.hackathon/project-state.md` compact and add only the Phase 19 fields specified below; do not overwrite prior phase state.

### Additive project-state fields only

Submission Status; Submission Readiness; Submission Deadline; Deadline Timezone; Submission Requirements; Artifact Inventory; Required Fields; URL Verification; Access Verification; Submission Snapshot; Freeze Status; Critical Submission Risks; Human Confirmation Status; Current Submission Blocker; Primary Next Action.

## Final report sections

Prerequisites; Lifecycle Integrity; Submission Requirements; Deadline Verification; Artifact Inventory; Field Verification; URL Verification; Access Verification; Repository Audit; Demo/Video Audit; PPT Audit; README Audit; Secret Audit; Consistency Audit; Claim Audit; Risk Register; Submission Snapshot; Freeze Status; Human Confirmation; Submission Readiness; Scope Compliance; Evidence Integrity; Primary Next Action; Final Decision.

## Readiness and phase lock are distinct

Phase 19 framework may be COMPLETE & LOCKED while live Submission Readiness remains CONDITIONAL. Framework contract tests do not verify live portal rules, package, links, artifact access, deployment, video, presentation, or deadline. Actual submission is a human action outside this workflow.
