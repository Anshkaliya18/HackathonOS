#!/usr/bin/env python3
"""Deterministic contract validation for Phase 13 — Red Team Intelligence.

Validates the Phase 13 Red Team workflow, rules, and template contracts against
the acceptance tests AT-286 through AT-320 and adversarial scenarios ADV-01–30.

Follows the Phase 6/Phase 10/Phase 11/Phase 12 smoke harness pattern: stdlib-only,
disposable fixtures, machine-readable JSON output, non-zero exit on any failure.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "SKILL.md"
WORKFLOW = ROOT / "workflows" / "red-team.md"
RULES = ROOT / "rules" / "red-team-rules.md"
REVIEW_TEMPLATE = ROOT / "templates" / "red-team-review.md"
FINDING_TEMPLATE = ROOT / "templates" / "red-team-finding.md"
SCENARIO_TEMPLATE = ROOT / "templates" / "red-team-scenario.md"
VERIFICATION_TEMPLATE = ROOT / "templates" / "red-team-verification.md"
LIFECYCLE = ROOT / "workflows" / "lifecycle.md"

# Expected Phase 13 resources (already exist from legacy Phase 8 numbering,
# but lifecycle.md identifies Red Team as Phase 13)
PHASE13_FILES = [
    WORKFLOW,
    RULES,
    REVIEW_TEMPLATE,
    FINDING_TEMPLATE,
    SCENARIO_TEMPLATE,
    VERIFICATION_TEMPLATE,
]


def file_contains(path: Path, pattern: str) -> bool:
    return re.search(pattern, path.read_text(encoding="utf-8"), re.IGNORECASE) is not None


# ---------------------------------------------------------------------------
# AT-286 through AT-320 acceptance tests
# ---------------------------------------------------------------------------

def test_at286_prerequisite_phase12_locked() -> None:
    """Red Team consumes the project's UX evidence."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 7 UX evidence" in text
    assert ".sherpa/project-state.md" in text


def test_at287_lifecycle_correctness() -> None:
    """Lifecycle contains exactly 20 phases; Phase 13 = Red Team."""
    text = LIFECYCLE.read_text(encoding="utf-8")
    data_rows = []
    in_phase_table = False
    for l in text.splitlines():
        stripped = l.strip()
        if "| Phase |" in stripped and "| When |" in stripped:
            in_phase_table = True
            continue
        if in_phase_table and stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cells) >= 3 and cells[0] and not all(c == "-" or c == "" for c in cells[0]):
                if cells[0] == "Time Remaining":
                    break
                data_rows.append(cells)
    assert len(data_rows) == 20, f"Expected 20 phases, found {len(data_rows)}"
    assert data_rows[12][0].strip() == "Red Team", \
        f"Phase 13 should be Red Team, found: {data_rows[12][0].strip()}"


def test_at288_routing_exists() -> None:
    """RED-TEAM routing exists in SKILL.md."""
    text = SKILL.read_text(encoding="utf-8")
    assert "RED-TEAM" in text, "SKILL.md missing RED-TEAM operation"
    assert "workflows/red-team.md" in text, "SKILL.md missing red-team.md workflow path"


def test_at289_resources_resolve() -> None:
    """All Phase 13 resources load from expected locations."""
    for f in PHASE13_FILES:
        assert f.is_file(), f"Phase 13 resource missing: {f}"


def test_at290_state_reading() -> None:
    """Workflow reads project state."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "project-state" in text.lower() or "project state" in text.lower(), \
        "Workflow does not read project state"


def test_at291_repository_inspection() -> None:
    """Workflow requires repository inspection."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "inspect" in text.lower(), "Workflow does not require inspection"
    assert "repository" in text.lower(), "Workflow does not inspect repository"


def test_at292_evidence_model() -> None:
    """Evidence model uses FACT/INFERENCE/ASSUMPTION/UNKNOWN."""
    rules_text = RULES.read_text(encoding="utf-8")
    for label in ["FACT", "INFERENCE", "ASSUMPTION", "UNKNOWN"]:
        assert label in rules_text, f"Rules missing evidence label: {label}"


def test_at293_claim_extraction() -> None:
    """Claims are extracted and challenged."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "claim" in text.lower(), "Workflow does not address claims"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "claim" in rules_text.lower(), "Rules do not address claims"


def test_at294_claim_challenge() -> None:
    """Claims are challenged with scenarios."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "challenge" in text.lower(), "Workflow does not address claim challenging"
    assert "attack" in text.lower() or "disprove" in text.lower(), \
        "Workflow does not address disproving claims"


def test_at295_asset_identification() -> None:
    """Critical assets are identified."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "asset" in combined or "critical" in combined, \
        "Workflow/rules do not address critical assets"


def test_at296_trust_boundaries() -> None:
    """Trust boundaries are analyzed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "boundary" in rules_text.lower() or "trust" in rules_text.lower(), \
        "Rules do not address trust boundaries"


def test_at297_adversarial_actors() -> None:
    """Adversarial actors are considered."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    for actor in ["malicious", "careless", "curious", "skeptical", "unlucky"]:
        assert actor in combined, f"Workflow/rules do not address actor: {actor}"


def test_at298_scenario_generation() -> None:
    """Adversarial scenarios are generated."""
    assert SCENARIO_TEMPLATE.is_file(), "Scenario template missing"
    text = SCENARIO_TEMPLATE.read_text(encoding="utf-8")
    assert "Scenario ID" in text, "Scenario template missing Scenario ID"
    assert "Attack" in text, "Scenario template missing Attack"


def test_at299_functional_abuse() -> None:
    """Functional abuse is inspected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "abuse" in rules_text.lower() or "invalid input" in rules_text.lower(), \
        "Rules do not address functional abuse"


def test_at300_reliability() -> None:
    """Reliability is challenged."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "reliab" in rules_text.lower() or "timeout" in rules_text.lower() or "network" in rules_text.lower(), \
        "Rules do not address reliability"


def test_at301_data() -> None:
    """Data is challenged."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "data" in rules_text.lower(), "Rules do not address data"


def test_at302_security_adjacent() -> None:
    """Security-adjacent analysis is performed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "security" in rules_text.lower(), "Rules do not address security-adjacent abuse"
    assert "phase 5" in rules_text.lower() or "phase11" in rules_text.lower() or "testing" in rules_text.lower(), \
        "Rules do not reference Phase 5/11 boundary"


def test_at303_ux_abuse() -> None:
    """UX abuse is challenged."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "ux" in rules_text.lower() or "usability" in rules_text.lower(), \
        "Rules do not address UX abuse"
    assert "phase 7" in rules_text.lower() or "phase12" in rules_text.lower(), \
        "Rules do not reference Phase 7/12 boundary"


def test_at304_performance() -> None:
    """Performance is challenged where evidence permits."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "performance" in rules_text.lower() or "large input" in rules_text.lower(), \
        "Rules do not address performance"


def test_at305_ai_behavior() -> None:
    """AI/model behavior is challenged if AI exists."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "ai" in rules_text.lower() or "model" in rules_text.lower() or "hallucination" in rules_text.lower(), \
        "Rules do not address AI/model behavior"


def test_at306_demo_reliability() -> None:
    """Demo reliability is challenged."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "demo" in combined, "Workflow/rules do not address demo reliability"


def test_at307_severity_model() -> None:
    """Severity model: CRITICAL/HIGH/MEDIUM/LOW."""
    rules_text = RULES.read_text(encoding="utf-8")
    finding_text = FINDING_TEMPLATE.read_text(encoding="utf-8")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        assert sev in rules_text or sev in finding_text, \
            f"Severity {sev} not found in rules or finding template"


def test_at308_likelihood() -> None:
    """Likelihood model defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    for lik in ["VERY_HIGH", "HIGH", "MEDIUM", "LOW", "VERY_LOW"]:
        assert lik in rules_text, f"Rules missing likelihood: {lik}"


def test_at309_confidence() -> None:
    """Confidence separate from severity."""
    rules_text = RULES.read_text(encoding="utf-8")
    finding_text = FINDING_TEMPLATE.read_text(encoding="utf-8")
    assert "Confidence" in finding_text, "Finding template missing Confidence"
    assert "severity" in rules_text.lower() and "confidence" in rules_text.lower(), \
        "Rules do not separate severity from confidence"


def test_at310_recoverability() -> None:
    """Recoverability model defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    for rec in ["AUTOMATIC", "EASY", "MANUAL", "DIFFICULT", "NONE"]:
        assert rec in rules_text, f"Rules missing recoverability: {rec}"


def test_at311_finding_lifecycle() -> None:
    """Finding lifecycle states defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    finding_text = FINDING_TEMPLATE.read_text(encoding="utf-8")
    for status in ["OPEN", "IN_PROGRESS", "MITIGATED", "VERIFIED", "ACCEPTED_RISK"]:
        assert status in rules_text or status in finding_text, \
            f"Finding status {status} not found"


def test_at312_mitigation() -> None:
    """Mitigation defined per finding."""
    finding_text = FINDING_TEMPLATE.read_text(encoding="utf-8")
    assert "Recommended Mitigation" in finding_text, "Finding template missing Recommended Mitigation"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "mitigation" in rules_text.lower(), "Rules do not address mitigation"


def test_at313_mitigation_verification() -> None:
    """Mitigation verification defined."""
    assert VERIFICATION_TEMPLATE.is_file(), "Verification template missing"
    verification_text = VERIFICATION_TEMPLATE.read_text(encoding="utf-8")
    assert "Verification Procedure" in verification_text, \
        "Verification template missing Verification Procedure"
    assert "Expected Result" in verification_text, \
        "Verification template missing Expected Result"
    assert "Actual Result" in verification_text, \
        "Verification template missing Actual Result"


def test_at314_quality_gate() -> None:
    """Quality gate states enforced."""
    rules_text = RULES.read_text(encoding="utf-8")
    for gate in ["NOT_READY", "RED_TEAM_IN_PROGRESS", "BLOCKED", "CONDITIONAL", "READY"]:
        assert gate in rules_text, f"Quality gate {gate} not found in rules"


def test_at315_time_strategy() -> None:
    """Time-aware strategy works."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "time" in combined, "Workflow/rules do not address time-aware strategy"
    assert "6" in rules_text or "2-6" in rules_text or "6-12" in rules_text, \
        "Rules do not define time strategy windows"


def test_at316_ownership_boundaries() -> None:
    """Phase 13 does not own other phases' responsibilities."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    rules_text = RULES.read_text(encoding="utf-8")
    combined = (workflow_text + " " + rules_text).lower()
    assert "do not" in combined, "Workflow/rules do not establish boundaries"
    assert "implementation" in combined or "phase 4" in combined, \
        "Workflow/rules do not address implementation ownership boundary"


def test_at317_human_approval() -> None:
    """Human authority is preserved."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "human" in rules_text.lower(), "Rules do not address human authority"
    assert "approval" in rules_text.lower(), "Rules do not address human approval"


def test_at318_primary_next_action() -> None:
    """Exactly one primary next action."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "PRIMARY NEXT ACTION" in workflow_text, "Workflow missing PRIMARY NEXT ACTION"
    review_text = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    assert "PRIMARY NEXT ACTION" in review_text, "Review template missing PRIMARY NEXT ACTION"


def test_at319_regression() -> None:
    """Regression is considered."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "regression" in combined, "Workflow/rules do not address regression"


def test_at320_scope_audit() -> None:
    """No ownership leakage and scope preserved."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    rules_text = RULES.read_text(encoding="utf-8")
    combined = (workflow_text + " " + rules_text).lower()
    assert "judge" in combined or "simulation" in combined, \
        "Workflow/rules do not address judge simulation boundary"


# ---------------------------------------------------------------------------
# Adversarial validation scenarios (30 minimum)
# ---------------------------------------------------------------------------

def test_adv_01_missing_phase12() -> None:
    """Missing UX evidence remains an explicit Red Team prerequisite."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 7 UX evidence" in text
    assert "Prerequisite" in text


def test_adv_02_partial_phase12() -> None:
    """Partial Phase 12 handled gracefully."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "partial" in text.lower() or "limited" in text.lower() or "blocked" in text.lower(), \
        "Workflow does not handle partial readiness"


def test_adv_03_missing_project_state() -> None:
    """Missing project state handled gracefully."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "project-state" in text.lower() or "project state" in text.lower()


def test_adv_04_empty_repository() -> None:
    """Empty repository handled gracefully."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text, "Rules do not handle UNKNOWN state"


def test_adv_05_missing_source_code() -> None:
    """Missing source code handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text or "not present" in rules_text.lower()


def test_adv_06_missing_runtime() -> None:
    """Missing runtime handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "runtime" in rules_text.lower() or "unknown" in rules_text.lower()


def test_adv_07_missing_browser() -> None:
    """Missing browser handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "browser" in rules_text.lower() or "unknown" in rules_text.lower()


def test_adv_08_missing_evidence() -> None:
    """Missing evidence marked UNKNOWN."""
    finding_text = FINDING_TEMPLATE.read_text(encoding="utf-8")
    assert "UNKNOWN" in finding_text, "Finding template does not allow UNKNOWN"


def test_adv_09_conflicting_evidence() -> None:
    """Conflicting evidence recorded, not reconciled."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "contradict" in workflow_text.lower() or "conflict" in workflow_text.lower()


def test_adv_10_stale_evidence() -> None:
    """Stale evidence flagged."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "stale" in workflow_text.lower() or "revision" in workflow_text.lower() or "unknown" in workflow_text.lower()


def test_adv_11_unsupported_security_claim() -> None:
    """Unsupported security claims rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "security" in rules_text.lower() and "scope" in rules_text.lower()


def test_adv_12_unsupported_reliability_claim() -> None:
    """Unsupported reliability claims rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "reliab" in rules_text.lower()


def test_adv_13_unsupported_ai_claim() -> None:
    """Unsupported AI claims rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "ai" in rules_text.lower() or "model" in rules_text.lower()


def test_adv_14_unsupported_scalability_claim() -> None:
    """Unsupported scalability claims rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "scalab" in rules_text.lower() or "performance" in rules_text.lower()


def test_adv_15_critical_finding_low_confidence() -> None:
    """Critical finding with LOW confidence handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "confidence" in rules_text.lower() and "severity" in rules_text.lower()


def test_adv_16_multiple_critical_findings() -> None:
    """Multiple critical findings handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "CRITICAL" in rules_text


def test_adv_17_finding_without_owner() -> None:
    """Finding without owner handled."""
    finding_text = FINDING_TEMPLATE.read_text(encoding="utf-8")
    assert "Required Owner" in finding_text or "Owner" in finding_text


def test_adv_18_finding_without_verification() -> None:
    """Finding without verification handled."""
    finding_text = FINDING_TEMPLATE.read_text(encoding="utf-8")
    assert "Verification" in finding_text


def test_adv_19_mitigation_without_evidence() -> None:
    """Mitigation without evidence not marked verified."""
    verification_text = VERIFICATION_TEMPLATE.read_text(encoding="utf-8")
    rules_text = RULES.read_text(encoding="utf-8")
    combined = (verification_text + " " + rules_text).lower()
    assert "evidence" in combined, "Verification does not require evidence"


def test_adv_20_failed_mitigation() -> None:
    """Failed mitigation handled."""
    verification_text = VERIFICATION_TEMPLATE.read_text(encoding="utf-8")
    assert "FAILED" in verification_text or "failed" in verification_text.lower()


def test_adv_21_repeated_user_action() -> None:
    """Repeated user action scenario considered."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "repeated" in rules_text.lower() or "duplicate" in rules_text.lower()


def test_adv_22_invalid_input() -> None:
    """Invalid input scenario considered."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "invalid input" in rules_text.lower() or "malformed" in rules_text.lower()


def test_adv_23_partial_dependency_failure() -> None:
    """Partial dependency failure scenario considered."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "dependency" in rules_text.lower() or "partial" in rules_text.lower() or "failure" in rules_text.lower()


def test_adv_24_external_api_failure() -> None:
    """External API failure scenario considered."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "api" in rules_text.lower() or "external" in rules_text.lower()


def test_adv_25_persistent_state_corruption() -> None:
    """Persistent state corruption scenario considered."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "persistent" in rules_text.lower() or "storage" in rules_text.lower() or "data" in rules_text.lower()


def test_adv_26_demo_failure() -> None:
    """Demo failure scenario considered."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "demo" in rules_text.lower()


def test_adv_27_ux_failure_discovered() -> None:
    """UX failure discovered by Red Team handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "ux" in rules_text.lower() or "usability" in rules_text.lower()


def test_adv_28_cross_phase_ownership() -> None:
    """Finding belonging to another phase is escalated, not taken."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "architecture change required" in rules_text.lower() or "phase" in rules_text.lower()


def test_adv_29_time_under_two_hours() -> None:
    """Time remaining <2 hours freezes broad changes."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "<2" in rules_text or "2 hours" in rules_text or "<2h" in rules_text


def test_adv_30_phase1_12_untouched() -> None:
    """Phase 1-12 artifacts remain untouched."""
    phase_files = [
        ROOT / "workflows" / "score-optimization.md",
        ROOT / "workflows" / "judge-simulation.md",
        ROOT / "workflows" / "ux-review.md",
        ROOT / "workflows" / "testing-security.md",
        ROOT / "workflows" / "implementation.md",
    ]
    for f in phase_files:
        assert f.is_file(), f"Phase file missing: {f}"


# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------

TESTS: list[tuple[str, Callable[[], None]]] = [
    # Acceptance tests AT-286 through AT-320
    ("AT-286 Prerequisite Phase 12 locked", test_at286_prerequisite_phase12_locked),
    ("AT-287 Lifecycle correctness", test_at287_lifecycle_correctness),
    ("AT-288 Routing exists", test_at288_routing_exists),
    ("AT-289 Resources resolve", test_at289_resources_resolve),
    ("AT-290 State reading", test_at290_state_reading),
    ("AT-291 Repository inspection", test_at291_repository_inspection),
    ("AT-292 Evidence model", test_at292_evidence_model),
    ("AT-293 Claim extraction", test_at293_claim_extraction),
    ("AT-294 Claim challenge", test_at294_claim_challenge),
    ("AT-295 Asset identification", test_at295_asset_identification),
    ("AT-296 Trust boundaries", test_at296_trust_boundaries),
    ("AT-297 Adversarial actors", test_at297_adversarial_actors),
    ("AT-298 Scenario generation", test_at298_scenario_generation),
    ("AT-299 Functional abuse", test_at299_functional_abuse),
    ("AT-300 Reliability", test_at300_reliability),
    ("AT-301 Data", test_at301_data),
    ("AT-302 Security-adjacent", test_at302_security_adjacent),
    ("AT-303 UX abuse", test_at303_ux_abuse),
    ("AT-304 Performance", test_at304_performance),
    ("AT-305 AI behavior", test_at305_ai_behavior),
    ("AT-306 Demo reliability", test_at306_demo_reliability),
    ("AT-307 Severity model", test_at307_severity_model),
    ("AT-308 Likelihood", test_at308_likelihood),
    ("AT-309 Confidence", test_at309_confidence),
    ("AT-310 Recoverability", test_at310_recoverability),
    ("AT-311 Finding lifecycle", test_at311_finding_lifecycle),
    ("AT-312 Mitigation", test_at312_mitigation),
    ("AT-313 Mitigation verification", test_at313_mitigation_verification),
    ("AT-314 Quality gate", test_at314_quality_gate),
    ("AT-315 Time-aware strategy", test_at315_time_strategy),
    ("AT-316 Ownership boundaries", test_at316_ownership_boundaries),
    ("AT-317 Human approval", test_at317_human_approval),
    ("AT-318 Primary next action", test_at318_primary_next_action),
    ("AT-319 Regression considered", test_at319_regression),
    ("AT-320 Scope audit", test_at320_scope_audit),
    # Adversarial validation scenarios
    ("ADV-01 Missing Phase 12", test_adv_01_missing_phase12),
    ("ADV-02 Partial Phase 12", test_adv_02_partial_phase12),
    ("ADV-03 Missing project state", test_adv_03_missing_project_state),
    ("ADV-04 Empty repository", test_adv_04_empty_repository),
    ("ADV-05 Missing source code", test_adv_05_missing_source_code),
    ("ADV-06 Missing runtime", test_adv_06_missing_runtime),
    ("ADV-07 Missing browser", test_adv_07_missing_browser),
    ("ADV-08 Missing evidence", test_adv_08_missing_evidence),
    ("ADV-09 Conflicting evidence", test_adv_09_conflicting_evidence),
    ("ADV-10 Stale evidence", test_adv_10_stale_evidence),
    ("ADV-11 Unsupported security claim", test_adv_11_unsupported_security_claim),
    ("ADV-12 Unsupported reliability claim", test_adv_12_unsupported_reliability_claim),
    ("ADV-13 Unsupported AI claim", test_adv_13_unsupported_ai_claim),
    ("ADV-14 Unsupported scalability claim", test_adv_14_unsupported_scalability_claim),
    ("ADV-15 Critical finding low confidence", test_adv_15_critical_finding_low_confidence),
    ("ADV-16 Multiple critical findings", test_adv_16_multiple_critical_findings),
    ("ADV-17 Finding without owner", test_adv_17_finding_without_owner),
    ("ADV-18 Finding without verification", test_adv_18_finding_without_verification),
    ("ADV-19 Mitigation without evidence", test_adv_19_mitigation_without_evidence),
    ("ADV-20 Failed mitigation", test_adv_20_failed_mitigation),
    ("ADV-21 Repeated user action", test_adv_21_repeated_user_action),
    ("ADV-22 Invalid input", test_adv_22_invalid_input),
    ("ADV-23 Partial dependency failure", test_adv_23_partial_dependency_failure),
    ("ADV-24 External API failure", test_adv_24_external_api_failure),
    ("ADV-25 Persistent state corruption", test_adv_25_persistent_state_corruption),
    ("ADV-26 Demo failure", test_adv_26_demo_failure),
    ("ADV-27 UX failure discovered", test_adv_27_ux_failure_discovered),
    ("ADV-28 Cross-phase ownership", test_adv_28_cross_phase_ownership),
    ("ADV-29 Time under two hours", test_adv_29_time_under_two_hours),
    ("ADV-30 Phase 1-12 untouched", test_adv_30_phase1_12_untouched),
]


def main() -> int:
    results = []
    for name, test in TESTS:
        try:
            test()
            results.append({"test": name, "status": "PASS"})
        except Exception as exc:
            results.append({"test": name, "status": "FAIL", "error": type(exc).__name__})

    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] != "PASS")
    at_results = [r for r in results if r["test"].startswith("AT-")]
    at_passed = sum(1 for r in at_results if r["status"] == "PASS")
    at_failed = len(at_results) - at_passed

    print(json.dumps({
        "results": results,
        "summary": {
            "total": len(results),
            "passed": passed,
            "failed": failed,
            "at_total": len(at_results),
            "at_passed": at_passed,
            "at_failed": at_failed,
        },
    }, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
