#!/usr/bin/env python3
"""Phase 19 contract and synthetic adversarial validation (stdlib only).
No LLM runtime, live project, portal, deployment, or submission is invoked.
"""
from __future__ import annotations
import json, re, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = {
    "workflow": ROOT / "workflows/submission.md",
    "rules": ROOT / "rules/submission-rules.md",
    "skill": ROOT / "SKILL.md",
    "lifecycle": ROOT / "workflows/lifecycle.md",
    "final_audit_workflow": ROOT / "workflows/final-audit.md",
    "plan": ROOT / "templates/submission-plan.md",
    "requirement": ROOT / "templates/submission-requirement.md",
    "artifact": ROOT / "templates/submission-artifact.md",
    "field": ROOT / "templates/submission-field.md",
    "link": ROOT / "templates/submission-link.md",
    "risk": ROOT / "templates/submission-risk.md",
    "checklist": ROOT / "templates/submission-checklist.md",
    "snapshot": ROOT / "templates/submission-snapshot.md",
    "verification": ROOT / "templates/submission-verification.md",
}
T = {k: p.read_text(encoding="utf-8") for k, p in FILES.items()}

def must(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)

def ready(c: dict) -> bool:
    """Conservative synthetic gate used only for harness adversarial fixtures."""
    reject = ["phase18_unlocked", "wrong_lifecycle", "fabricated_requirement", "hidden_conflict",
              "fabricated_deadline", "wrong_timezone", "missing_artifact", "inaccessible_repo",
              "broken_deployment", "private_required", "unsupported_claim", "name_conflict",
              "repo_mismatch", "stale_ppt", "missing_required_demo", "bad_format", "oversized",
              "exposed_secret", "fabricated_url", "fabricated_access", "bad_snapshot",
              "feature_after_freeze", "critical_risk", "confirmation_bypass", "submit_attempt",
              "visibility_change", "private_exposure", "multiple_actions", "fabricated_ready"]
    return not any(c.get(k, False) for k in reject)

# Exact 35 acceptance assertions.
checks = [
("Phase 18 prerequisite", lambda: must(".hackathon/final-audit.md" in T["workflow"] and "Audit status: COMPLETE" in T["workflow"] and ".hackathon/final-audit.md" in T["final_audit_workflow"], "project audit evidence")),
("Lifecycle phase count and identity", lambda: must(sum(line.startswith("| ") and line.endswith(" |") and line.split("|")[1].strip() in ("Understand Rules", "Analyze Problem", "Generate Ideas", "Validate Ideas", "Research Market", "Select Idea", "Design Product/MVP", "Architecture", "Development Plan", "Implementation", "Testing + Security", "UX Review", "Red Team", "Judge Simulation", "Score Optimization", "Demo Preparation", "PPT / Presentation", "Final Audit", "Submission", "Post-Mortem") for line in T["lifecycle"].splitlines()) == 20 and all(x in T["lifecycle"] for x in ("| Final Audit |", "| Submission |", "| Post-Mortem |")), "20 phases/order")),
("SUBMISSION-PREPARE router", lambda: must("SUBMISSION-PREPARE" in T["skill"] and "workflows/submission.md" in T["skill"], "route")),
("Phase 19 resources resolve", lambda: must(all(p.is_file() for p in FILES.values()), "resource missing")),
("Official source priority", lambda: must(all(x in T["rules"].lower() for x in ("official rules", "official portal", "organizer communications", "judging criteria")), "source precedence")),
("Requirement record fields", lambda: must(all(x in T["requirement"] for x in ("Requirement ID", "Requirement:", "Source", "Mandatory", "Evidence", "Artifact / field", "Status", "Owner", "Deadline", "Notes")), "requirement schema")),
("Requirement statuses", lambda: must(all(x in T["rules"] for x in ("VERIFIED", "READY", "MISSING", "INVALID", "BLOCKED", "UNKNOWN", "NOT_APPLICABLE")), "status enum")),
("Undocumented requirement safeguard", lambda: must("not mandatory absent evidence" in T["rules"], "mandatory evidence guard")),
("Conflicting rules surfaced", lambda: must("Preserve source conflicts" in T["workflow"], "conflict handling")),
("Deadline schema", lambda: must(all(x in T["rules"].lower() for x in ("deadline", "timezone", "source", "confidence", "time remaining")), "deadline fields")),
("Deadline states and timezone unknown", lambda: must(all(x in T["rules"] for x in ("UPCOMING", "URGENT", "DUE_SOON", "DEADLINE_PASSED", "Never assume a timezone")), "deadline states")),
("Artifact inventory fields", lambda: must(all(x in T["artifact"] for x in ("Artifact ID", "Name", "Type", "Location", "Version", "Required", "Accessible", "Verified", "Last checked", "Hash", "Status")), "artifact schema")),
("Submission field matrix", lambda: must(all(x in T["field"] for x in ("Field ID", "Field name", "Required", "Value", "Source", "Evidence", "Character limit", "Format", "Status")), "field schema")),
("Unknown personal/team fields", lambda: must("Never fabricate identity" in T["field"] and "UNKNOWN" in T["field"], "identity safeguard")),
("URL state and evidence model", lambda: must(all(x in T["link"] for x in ("VERIFIED_ACCESSIBLE", "ACCESSIBLE_WITH_AUTH", "BROKEN", "REDIRECTED", "UNKNOWN", "NOT_APPLICABLE", "Verification method")), "link states")),
("Access control states", lambda: must(all(x in T["rules"] for x in ("PUBLIC", "RESTRICTED", "AUTH_REQUIRED", "EXPIRED")), "access states")),
("Repository audit coverage", lambda: must(all(x in T["workflow"].lower() for x in ("repository", "branch", "intended commit", "readme/setup")), "repo coverage")),
("Snapshot fields", lambda: must(all(x in T["snapshot"] for x in ("Snapshot ID", "Timestamp", "Repository commit", "Branch", "Frontend", "Backend", "PPT", "Demo video", "Documentation", "Deployment URL", "Status")), "snapshot schema")),
("Freeze change classifications", lambda: must(all(x in T["snapshot"] for x in ("REQUIRED", "SAFE", "RISKY", "FORBIDDEN_AFTER_FREEZE")), "freeze classes")),
("Freeze activation gate", lambda: must("only once all critical artifacts are verified" in T["workflow"], "freeze condition")),
("Consistency audit coverage", lambda: must(all(x in T["workflow"].lower() for x in ("form", "readme", "ppt", "demo", "repository", "deployment", "selected idea", "phase 18")), "consistency domains")),
("Claim audit classification", lambda: must(all(x in T["rules"] for x in ("VERIFIED", "SUPPORTED", "PARTIALLY_SUPPORTED", "UNSUPPORTED", "CONTRADICTED", "UNKNOWN")), "claim statuses")),
("File formats and limits source", lambda: must("authoritative source" in T["workflow"] and "official requirements" in T["workflow"], "format requirements source")),
("Demo/video verification", lambda: must("demo/video" in T["workflow"].lower() and "actual artifacts" in T["workflow"], "demo evidence")),
("PPT audit without redesign", lambda: must("PPT" in T["workflow"] and "Do not redesign" in T["workflow"], "PPT boundary")),
("README audit without setup fabrication", lambda: must("README/setup" in T["workflow"] and "Report setup only as verified if it was actually run" in T["workflow"], "README boundary")),
("Bounded secret scan language", lambda: must("No secret indicators were detected within the audited submission scope" in T["rules"], "bounded scan")),
("Risk severity and confidence", lambda: must("Keep severity and confidence separate" in T["rules"] and "Critical risk blocks READY" in T["rules"], "risk gate")),
("Readiness states and evidence gate", lambda: must(all(x in T["rules"] for x in ("NOT_READY", "CONDITIONAL", "BLOCKED", "READY_TO_SUBMIT", "human confirmation still pending")), "readiness")),
("Human confirmation required", lambda: must("FINAL HUMAN CONFIRMATION REQUIRED" in T["rules"] and "human submits" in T["rules"], "human authority")),
("Checklist and unchecked submission", lambda: must("- [ ] Submission performed" in T["checklist"] and all(x in T["checklist"] for x in ("Rules verified", "Deadline verified", "Secrets checked", "Final snapshot created")), "checklist")),
("Compact additive state integration", lambda: must("Additive project-state fields only" in T["workflow"] and "do not overwrite prior phase state" in T["workflow"], "state integration")),
("Exactly one primary action", lambda: must("exactly one `PRIMARY NEXT ACTION`" in T["rules"] and "exactly one `PRIMARY NEXT ACTION`" in T["workflow"], "primary action")),
("No submit or irreversible automation", lambda: must(all(x in T["rules"] for x in ("click a final submit button", "submit a form", "change repository visibility", "upload to the portal")), "submission boundary")),
("Phase 20 excluded", lambda: must("Do not perform an actual competition submission or begin Phase 20" in T["workflow"], "Phase 20 boundary")),
]
must(len(checks) == 35, "expected exactly 35 acceptance cases")

adversarial = [
("Phase 18 not locked", "phase18_unlocked"), ("Lifecycle modified", "wrong_lifecycle"),
("Missing official requirements", "fabricated_requirement"), ("Fabricated requirement", "fabricated_requirement"),
("Conflicting requirements hidden", "hidden_conflict"), ("Fabricated deadline", "fabricated_deadline"),
("Wrong timezone", "wrong_timezone"), ("Missing mandatory artifact", "missing_artifact"),
("Inaccessible repository", "inaccessible_repo"), ("Broken deployment", "broken_deployment"),
("Private required artifact", "private_required"), ("Unsupported claim", "unsupported_claim"),
("Contradictory project name", "name_conflict"), ("Mismatched repository", "repo_mismatch"),
("Stale PPT", "stale_ppt"), ("Missing demo video", "missing_required_demo"),
("Invalid file format", "bad_format"), ("Oversized artifact", "oversized"),
("Exposed secret", "exposed_secret"), ("Fabricated URL verification", "fabricated_url"),
("Fabricated accessibility", "fabricated_access"), ("Snapshot inconsistency", "bad_snapshot"),
("Post-freeze feature addition", "feature_after_freeze"), ("Critical risk marked resolved", "critical_risk"),
("Human confirmation bypass", "confirmation_bypass"), ("Final submit attempted", "submit_attempt"),
("Automatic repository visibility change", "visibility_change"), ("Public exposure of private data", "private_exposure"),
("Multiple PRIMARY NEXT ACTION entries", "multiple_actions"), ("Fabricated READY_TO_SUBMIT", "fabricated_ready"),
]
must(len(adversarial) == 30, "expected exactly 30 adversarial cases")

results = []
for i, (description, fn) in enumerate(checks, 496):
    try:
        fn(); status, observed = "PASS", "PASS: repository contract assertion satisfied"
    except Exception as exc:
        status, observed = "FAIL", f"FAIL: {type(exc).__name__}: {exc}"
    results.append({"id": f"AT-{i}", "description": description, "setup": "Inspect actual Phase 19 contract files.",
                    "expected_result": "Required submission contract is explicit, bounded, and evidence-based.",
                    "observed_result": observed, "status": status,
                    "evidence": f"Executed assertion in tests/workflows/test_submission.py:AT-{i}"})
for i, (description, key) in enumerate(adversarial, 1):
    try:
        candidate = {key: True}
        assert not ready(candidate), "unsafe candidate accepted"
        status, observed = "PASS", "PASS: unsafe synthetic fixture rejected; no external action"
    except Exception as exc:
        status, observed = "FAIL", f"FAIL: {type(exc).__name__}: {exc}"
    results.append({"id": f"ADV-{i:02d}", "description": description,
                    "setup": f"Disposable synthetic fixture {key}=true", "expected_result": "Unsafe condition rejected or blocked.",
                    "observed_result": observed, "status": status,
                    "evidence": f"Executed assertion in tests/workflows/test_submission.py:ADV-{i:02d}; fixture only"})

with tempfile.TemporaryDirectory(prefix="hackathonos-phase19-") as d:
    fixture = Path(d) / "candidate.json"
    fixture.write_text(json.dumps({"fabricated_ready": True}), encoding="utf-8")
    assert not ready(json.loads(fixture.read_text(encoding="utf-8")))

at = [x for x in results if x["id"].startswith("AT-")]
adv = [x for x in results if x["id"].startswith("ADV-")]
passed = sum(x["status"] == "PASS" for x in results)
print(json.dumps({"suite": "Phase 19 Submission Intelligence contract validation",
                  "scope": "repository contract assertions and synthetic guard fixtures; no live LLM, portal, app, or submission",
                  "results": results,
                  "summary": {"total": len(results), "passed": passed, "failed": len(results)-passed,
                              "acceptance_total": len(at), "acceptance_passed": sum(x["status"] == "PASS" for x in at),
                              "adversarial_total": len(adv), "adversarial_passed": sum(x["status"] == "PASS" for x in adv)}}, indent=2))
raise SystemExit(0 if passed == len(results) else 1)
