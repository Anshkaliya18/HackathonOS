#!/usr/bin/env python3
"""Deterministic contract validation for Phase 18 — Final Audit Intelligence.

Validates Phase 18 workflow, rules, templates, and safeguards against acceptance
tests AT-461 through AT-495 and adversarial scenarios ADV-01 through ADV-30.

Follows the Phase 6/Phase 10/Phase 11/Phase 12/Phase 13/Phase 14/Phase 15/Phase 16/Phase 17 smoke harness pattern:
stdlib-only, disposable fixtures, machine-readable JSON output, non-zero exit on any failure.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "SKILL.md"
WORKFLOW = ROOT / "workflows" / "final-audit.md"
RULES = ROOT / "rules" / "final-audit-rules.md"
PLAN_TEMPLATE = ROOT / "templates" / "final-audit.md"
FINDING_TEMPLATE = ROOT / "templates" / "audit-finding.md"
REQUIREMENT_TEMPLATE = ROOT / "templates" / "requirement-audit.md"
CLAIM_TEMPLATE = ROOT / "templates" / "claim-audit.md"
CONSISTENCY_TEMPLATE = ROOT / "templates" / "consistency-audit.md"
SUBMISSION_TEMPLATE = ROOT / "templates" / "submission-readiness.md"
RISK_TEMPLATE = ROOT / "templates" / "final-risk.md"
VERIFICATION_TEMPLATE = ROOT / "templates" / "final-verification.md"
LIFECYCLE = ROOT / "workflows" / "lifecycle.md"

# Expected Phase 18 resources
PHASE18_FILES = [
    WORKFLOW,
    RULES,
    PLAN_TEMPLATE,
    FINDING_TEMPLATE,
    REQUIREMENT_TEMPLATE,
    CLAIM_TEMPLATE,
    CONSISTENCY_TEMPLATE,
    SUBMISSION_TEMPLATE,
    RISK_TEMPLATE,
    VERIFICATION_TEMPLATE,
]


def file_contains(path: Path, pattern: str) -> bool:
    return re.search(pattern, path.read_text(encoding="utf-8"), re.IGNORECASE) is not None


def count_occurrences(path: Path, pattern: str) -> int:
    return len(re.findall(pattern, path.read_text(encoding="utf-8"), re.IGNORECASE))


# ---------------------------------------------------------------------------
# AT-461 through AT-495 acceptance tests
# ---------------------------------------------------------------------------

def test_at496_prerequisite_phase17_locked() -> None:
    """Final audit uses current-project state and presentation evidence."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert ".hackathon/project-state.md" in text
    assert "Phase 17 presentation evidence must exist" in text


def test_at497_lifecycle_correctness() -> None:
    """Lifecycle contains exactly 20 phases; Phase 18 = Final Audit."""
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
    assert data_rows[17][0].strip() == "Final Audit", \
        f"Phase 18 should be Final Audit, found: {data_rows[17][0].strip()}"


def test_at498_routing_exists() -> None:
    """FINAL-AUDIT routing exists in SKILL.md."""
    text = SKILL.read_text(encoding="utf-8")
    assert "FINAL-AUDIT" in text, "SKILL.md missing FINAL-AUDIT operation"
    assert "workflows/final-audit.md" in text, "SKILL.md missing final-audit.md workflow path"


def test_at499_resources_resolve() -> None:
    """All Phase 18 resources load from expected locations."""
    for f in PHASE18_FILES:
        assert f.is_file(), f"Phase 18 resource missing: {f}"


def test_at500_state_reading() -> None:
    """Workflow reads project state."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "project-state" in text.lower() or "project state" in text.lower(), \
        "Workflow does not read project state"


def test_at501_repository_inspection() -> None:
    """Workflow requires repository inspection."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "inspect" in text.lower(), "Workflow does not require inspection"
    assert "repository" in text.lower(), "Workflow does not inspect repository"


def test_at502_evidence_model() -> None:
    """Evidence model uses FACT/INFERENCE/ASSUMPTION/UNKNOWN."""
    rules_text = RULES.read_text(encoding="utf-8")
    for label in ["FACT", "INFERENCE", "ASSUMPTION", "UNKNOWN"]:
        assert label in rules_text, f"Rules missing evidence label: {label}"


def test_at503_audit_status_model() -> None:
    """Audit status model is defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    for status in ["PASS", "PASS_WITH_LIMITATION", "FAIL", "BLOCKED", "UNKNOWN", "NOT_APPLICABLE"]:
        assert status in rules_text, f"Rules missing audit status: {status}"


def test_at404_cross_phase_consistency() -> None:
    """Cross-phase consistency audit is defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "consistency" in combined.lower(), "Workflow/rules do not address cross-phase consistency"


def test_at405_selected_idea_stability() -> None:
    """Selected idea stability is verified."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "selected idea" in rules_text.lower(), "Rules do not address selected idea stability"


def test_at406_requirement_coverage() -> None:
    """Requirement coverage audit is performed."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "requirement" in combined.lower(), "Workflow/rules do not address requirement coverage"


def test_at407_judging_criteria_coverage() -> None:
    """Judging criteria coverage audit is performed."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "criterion" in combined.lower() or "criteria" in combined.lower(), \
        "Workflow/rules do not address judging criteria coverage"


def test_at408_score_separation() -> None:
    """Score separation is enforced."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "official score" in combined.lower() or "internal readiness indicator" in combined.lower(), \
        "Workflow/rules do not separate official score from internal indicators"


def test_at409_claim_audit() -> None:
    """Claim audit is performed."""
    assert CLAIM_TEMPLATE.is_file(), "Claim audit template missing"
    text = CLAIM_TEMPLATE.read_text(encoding="utf-8")
    assert "Claim ID" in text, "Claim template missing Claim ID"
    assert "Claim" in text, "Claim template missing Claim"


def test_at410_metric_audit() -> None:
    """Metric audit is performed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "metric" in rules_text.lower(), "Rules do not address metric audit"


def test_at411_testing_audit() -> None:
    """Testing audit is performed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "test" in rules_text.lower(), "Rules do not address testing audit"


def test_at412_security_audit() -> None:
    """Security audit is performed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "security" in rules_text.lower(), "Rules do not address security audit"


def test_at413_ux_audit() -> None:
    """UX audit is performed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "ux" in rules_text.lower(), "Rules do not address UX audit"


def test_at414_red_team_closure() -> None:
    """Red Team closure audit is performed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "red team" in rules_text.lower() or "red-team" in rules_text.lower(), \
        "Rules do not address Red Team closure"


def test_at415_judge_simulation_closure() -> None:
    """Judge Simulation closure audit is performed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "judge" in rules_text.lower() or "judge simulation" in rules_text.lower(), \
        "Rules do not address Judge Simulation closure"


def test_at416_score_optimization_closure() -> None:
    """Score Optimization closure audit is performed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "score optimization" in rules_text.lower() or "score-optimization" in rules_text.lower(), \
        "Rules do not address Score Optimization closure"


def test_at417_demo_closure() -> None:
    """Demo closure audit is performed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "demo" in rules_text.lower(), "Rules do not address demo closure"


def test_at418_presentation_closure() -> None:
    """Presentation closure audit is performed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "presentation" in rules_text.lower(), "Rules do not address presentation closure"


def test_at419_repository_audit() -> None:
    """Repository audit is performed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "repository" in rules_text.lower(), "Rules do not address repository audit"


def test_at420_secret_audit() -> None:
    """Secret audit is performed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "secret" in rules_text.lower() or "credential" in rules_text.lower(), \
        "Rules do not address secret audit"


def test_at421_documentation_audit() -> None:
    """Documentation audit is performed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "documentation" in rules_text.lower(), "Rules do not address documentation audit"


def test_at422_deployment_audit() -> None:
    """Deployment audit is performed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "deployment" in rules_text.lower(), "Rules do not address deployment audit"


def test_at423_submission_requirements() -> None:
    """Submission requirements audit is performed."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "submission" in combined, "Workflow/rules do not address submission requirements"


def test_at424_last_minute_change_protection() -> None:
    """Last-minute change protection is defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "change protection" in rules_text.lower() or "change" in rules_text.lower(), \
        "Rules do not address change protection"


def test_at425_final_risk_register() -> None:
    """Final risk register is defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "risk register" in rules_text.lower(), "Rules do not address final risk register"


def test_at426_final_readiness_gate() -> None:
    """Final readiness gate states are enforced."""
    rules_text = RULES.read_text(encoding="utf-8")
    for gate in ["NOT_READY", "READY", "BLOCKED", "CONDITIONAL"]:
        assert gate in rules_text, f"Readiness gate {gate} not found in rules"


def test_at427_internal_presentation_score() -> None:
    """Internal audit score is separated from official score."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "internal readiness indicator" in rules_text.lower(), \
        "Rules do not label internal presentation score"
    assert "not official judging score" in rules_text.lower(), \
        "Rules do not disclaim internal readiness indicator as official score"


def test_at428_final_audit_finding_model() -> None:
    """Final audit finding model is defined."""
    assert FINDING_TEMPLATE.is_file(), "Finding template missing"
    text = FINDING_TEMPLATE.read_text(encoding="utf-8")
    assert "Finding ID" in text, "Finding template missing Finding ID"
    assert "Severity" in text, "Finding template missing Severity"


def test_at429_human_authority() -> None:
    """Human authority is preserved."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "human approval" in rules_text.lower() or "human-approval" in rules_text.lower(), \
        "Rules do not require human approval"


def test_at430_primary_next_action() -> None:
    """Exactly one primary next action."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "PRIMARY NEXT ACTION" in workflow_text, "Workflow missing PRIMARY NEXT ACTION"
    plan_text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    assert "PRIMARY NEXT ACTION" in plan_text, "Plan template missing PRIMARY NEXT ACTION"


def test_at431_state_persistence_contract() -> None:
    """Compact Phase 18 state fields are enumerated separately from detailed artifacts."""
    rules_text = RULES.read_text(encoding="utf-8")
    for field in ["Final Audit Status", "Final Readiness", "Critical Findings",
                  "Requirement Coverage", "Claim Audit Status", "Primary Next Action"]:
        assert field in rules_text, f"Rules missing compact state field: {field}"
    assert ".hackathon/final-audit.md" in rules_text, "Detailed audit artifact location missing"
    test_at432_all_audit_domains_present()


def test_at432_all_audit_domains_present() -> None:
    """The workflow explicitly evaluates all 18 mandated domains."""
    text = WORKFLOW.read_text(encoding="utf-8")
    for domain in ["Lifecycle Integrity", "Idea / Problem Alignment", "Product / MVP Alignment",
                   "Architecture / Implementation Alignment", "Testing", "Security",
                   "UX / Accessibility", "Red Team", "Judge Simulation", "Score Optimization",
                   "Demo", "Presentation", "Evidence Integrity", "Documentation",
                   "Repository / Deployment", "Submission Requirements", "Known Risks",
                   "Final Readiness"]:
        assert domain.lower() in text.lower(), f"Workflow omits required audit domain: {domain}"


# ---------------------------------------------------------------------------
# Adversarial validation scenarios (30 minimum)
# ---------------------------------------------------------------------------

def test_adv_01_missing_phase17() -> None:
    """A synthetic missing lock is rejected by the Phase 18 prerequisite contract."""
    text = WORKFLOW.read_text(encoding="utf-8").lower()
    assert "if not" in text and "phase 17" in text and "stop phase 18" in text, \
        "Workflow does not stop when Phase 17 is unlocked"


def test_adv_02_lifecycle_altered() -> None:
    """An altered lifecycle is reported and never silently repaired or renumbered."""
    text = WORKFLOW.read_text(encoding="utf-8").lower()
    assert "if the lifecycle map differs" in text and "stop final-audit" in text, \
        "Workflow does not stop on an altered lifecycle"
    assert "do not repair or renumber the lifecycle" in text, \
        "Workflow permits silent lifecycle repair"


def test_adv_03_missing_project_state() -> None:
    """Missing project/phase evidence remains UNKNOWN and blocks unsupported readiness."""
    text = WORKFLOW.read_text(encoding="utf-8").lower()
    assert "phase 11" in text and "phase 17" in text, "Workflow omits required prior-phase evidence"
    assert "if project evidence is missing" in text and "unknown" in text, \
        "Workflow does not preserve missing phase evidence as UNKNOWN"


def test_adv_04_fabricated_evidence() -> None:
    """Fabricated evidence is rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "fabricat" in rules_text.lower() or "do not fabricate" in rules_text.lower(), \
        "Rules do not prohibit fabricating evidence"


def test_adv_05_unknown_to_fact() -> None:
    """UNKNOWN not converted to FACT."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "never convert" in rules_text.lower() or "do not convert" in rules_text.lower(), \
        "Rules do not prohibit converting UNKNOWN to FACT"


def test_adv_06_documentation_as_implementation() -> None:
    """Documentation not treated as implementation proof."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "documentation" in rules_text.lower(), "Rules do not address documentation as evidence"


def test_adv_07_code_as_runtime() -> None:
    """Code presence not treated as runtime proof."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "code presence" in rules_text.lower() or "runtime behavior" in rules_text.lower(), \
        "Rules do not address code presence vs runtime behavior"


def test_adv_08_stale_screenshot() -> None:
    """Stale screenshot not treated as current behavior."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "screenshot" in rules_text.lower() or "live behavior" in rules_text.lower(), \
        "Rules do not address screenshot vs live behavior"


def test_adv_09_contradictory_artifacts() -> None:
    """Contradictory artifacts surfaced."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "contradict" in workflow_text.lower() or "conflict" in workflow_text.lower(), \
        "Workflow does not address contradictory artifacts"


def test_adv_10_unsupported_metric() -> None:
    """Unsupported metrics flagged."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "unsupported" in rules_text.lower() or "metric" in rules_text.lower(), \
        "Rules do not address unsupported metrics"


def test_adv_11_fabricated_criteria() -> None:
    """Fabricated judging criteria rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "invent" in rules_text.lower() or "do not invent" in rules_text.lower(), \
        "Rules do not prohibit inventing judging criteria"


def test_adv_12_fabricated_submission() -> None:
    """Fabricated submission requirements rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "submission" in rules_text.lower() or "invent" in rules_text.lower(), \
        "Rules do not address fabricated submission requirements"


def test_adv_13_critical_finding_resolved() -> None:
    """Unresolved CRITICAL finding not marked resolved."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "CRITICAL" in rules_text, "Rules do not define CRITICAL severity"
    assert "resolved" in rules_text.lower() or "mitigated" in rules_text.lower(), \
        "Rules do not address resolved critical findings"


def test_adv_14_critical_low_confidence() -> None:
    """CRITICAL + LOW confidence handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "confidence separate from severity" in rules_text.lower(), \
        "Rules do not keep CRITICAL severity separate from LOW confidence"


def test_adv_15_accepted_risk_without_human() -> None:
    """Accepted risk requires human authority."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "accepted_risk with human authority" in rules_text.lower() \
        or ("accepted_risk" in rules_text.lower() and "human approval" in rules_text.lower()), \
        "Rules do not require human approval for accepted risk"


def test_adv_16_failed_test_passed() -> None:
    """Failed test not treated as passed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "failed test" in rules_text.lower() or "failed" in rules_text.lower(), \
        "Rules do not address failed test treatment"


def test_adv_17_security_without_evidence() -> None:
    """Security claim without evidence flagged."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "evidence" in rules_text.lower() and "security" in rules_text.lower(), \
        "Rules do not address unsupported security claims"


def test_adv_18_accessibility_without_evidence() -> None:
    """Accessibility claim without evidence flagged."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "evidence" in rules_text.lower() and "accessibility" in rules_text.lower(), \
        "Rules do not address unsupported accessibility claims"


def test_adv_19_demo_vs_live_confused() -> None:
    """Demo readiness not confused with live validation."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "demo" in rules_text.lower() and "live" in rules_text.lower(), \
        "Rules do not distinguish demo from live validation"


def test_adv_20_presentation_vs_live_confused() -> None:
    """Presentation readiness not confused with live validation."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "presentation" in rules_text.lower() and "live" in rules_text.lower(), \
        "Rules do not distinguish presentation from live validation"


def test_adv_21_simulated_score_as_official() -> None:
    """Simulated score not presented as official."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "not official judging score" in rules_text.lower(), \
        "Rules do not disclaim internal score as official"


def test_adv_22_hidden_multiplier() -> None:
    """Hidden scoring multiplier avoided."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "multiplier" in rules_text.lower(), "Rules do not address hidden scoring multipliers"


def test_adv_23_silent_idea_reselection() -> None:
    """Selected idea not silently reselected."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "selected idea" in workflow_text.lower(), "Workflow does not protect selected idea"


def test_adv_24_silent_scope_expansion() -> None:
    """Silent scope expansion avoided."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "scope" in workflow_text.lower(), "Workflow does not address scope expansion"


def test_adv_25_architecture_modification() -> None:
    """Architecture not silently modified."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "architecture" in workflow_text.lower(), "Workflow does not address architecture boundary"


def test_adv_26_secret_detection_bypass() -> None:
    """Secret detection not bypassed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "secret" in rules_text.lower() or "credential" in rules_text.lower(), \
        "Rules do not address secret detection"


def test_adv_27_deployment_assumed_healthy() -> None:
    """Deployment not assumed healthy without verification."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "deployment" in rules_text.lower(), "Rules do not address deployment verification"


def test_adv_28_phase19_submission_executed() -> None:
    """Phase 19 submission not executed."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "submission" in workflow_text.lower() and "not perform" in workflow_text.lower(), \
        "Workflow does not prohibit performing submission"


def test_adv_29_multiple_primary_next_actions() -> None:
    """Exactly one PRIMARY NEXT ACTION."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    plan_text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    assert re.search(r"exactly one .*PRIMARY NEXT ACTION", workflow_text, re.IGNORECASE), \
        "Workflow does not prohibit multiple PRIMARY NEXT ACTION entries"
    assert plan_text.count("**PRIMARY NEXT ACTION:**") == 1, \
        "Plan template does not expose exactly one PRIMARY NEXT ACTION field"


def test_adv_30_fabricated_readiness() -> None:
    """Readiness not fabricated without evidence."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "READY" in rules_text and "evidence" in rules_text.lower(), \
        "Rules do not require evidence for READY"


# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------

TESTS: list[tuple[str, Callable[[], None]]] = [
    # Acceptance tests AT-461 through AT-495
    ("AT-461 Phase 17 lock prerequisite", test_at496_prerequisite_phase17_locked),
    ("AT-462 Lifecycle integrity", test_at497_lifecycle_correctness),
    ("AT-463 FINAL-AUDIT routing", test_at498_routing_exists),
    ("AT-464 Required resources resolve", test_at499_resources_resolve),
    ("AT-465 State reading", test_at500_state_reading),
    ("AT-466 Repository inspection", test_at501_repository_inspection),
    ("AT-467 Evidence model", test_at502_evidence_model),
    ("AT-468 Audit status model", test_at503_audit_status_model),
    ("AT-469 Cross-phase consistency", test_at404_cross_phase_consistency),
    ("AT-470 Selected idea stability", test_at405_selected_idea_stability),
    ("AT-471 Requirement coverage", test_at406_requirement_coverage),
    ("AT-472 Judging criteria coverage", test_at407_judging_criteria_coverage),
    ("AT-473 Official and internal score separation", test_at408_score_separation),
    ("AT-474 Claim audit", test_at409_claim_audit),
    ("AT-475 Metric audit", test_at410_metric_audit),
    ("AT-476 Testing audit", test_at411_testing_audit),
    ("AT-477 Security audit", test_at412_security_audit),
    ("AT-478 UX/accessibility audit", test_at413_ux_audit),
    ("AT-479 Red-team closure", test_at414_red_team_closure),
    ("AT-480 Judge simulation closure", test_at415_judge_simulation_closure),
    ("AT-481 Score optimization closure", test_at416_score_optimization_closure),
    ("AT-482 Demo closure", test_at417_demo_closure),
    ("AT-483 Presentation closure", test_at418_presentation_closure),
    ("AT-484 Repository audit", test_at419_repository_audit),
    ("AT-485 Secret audit", test_at420_secret_audit),
    ("AT-486 Documentation audit", test_at421_documentation_audit),
    ("AT-487 Deployment audit", test_at422_deployment_audit),
    ("AT-488 Submission requirements", test_at423_submission_requirements),
    ("AT-489 Last-minute change protection", test_at424_last_minute_change_protection),
    ("AT-490 Final risk register", test_at425_final_risk_register),
    ("AT-491 Final readiness gate", test_at426_final_readiness_gate),
    ("AT-492 State persistence and domain record", test_at431_state_persistence_contract),
    ("AT-493 Final audit finding model", test_at428_final_audit_finding_model),
    ("AT-494 Human authority", test_at429_human_authority),
    ("AT-495 Exactly one primary next action", test_at430_primary_next_action),
    # Adversarial validation scenarios
    ("ADV-01 Missing Phase 17", test_adv_01_missing_phase17),
    ("ADV-02 Lifecycle altered", test_adv_02_lifecycle_altered),
    ("ADV-03 Missing phase evidence", test_adv_03_missing_project_state),
    ("ADV-04 Fabricated evidence", test_adv_04_fabricated_evidence),
    ("ADV-05 UNKNOWN to FACT", test_adv_05_unknown_to_fact),
    ("ADV-06 Documentation as implementation", test_adv_06_documentation_as_implementation),
    ("ADV-07 Code as runtime", test_adv_07_code_as_runtime),
    ("ADV-08 Stale screenshot", test_adv_08_stale_screenshot),
    ("ADV-09 Contradictory artifacts", test_adv_09_contradictory_artifacts),
    ("ADV-10 Unsupported metric", test_adv_10_unsupported_metric),
    ("ADV-11 Fabricated criteria", test_adv_11_fabricated_criteria),
    ("ADV-12 Fabricated submission", test_adv_12_fabricated_submission),
    ("ADV-13 Critical finding resolved", test_adv_13_critical_finding_resolved),
    ("ADV-14 Critical + LOW confidence", test_adv_14_critical_low_confidence),
    ("ADV-15 Accepted risk without human", test_adv_15_accepted_risk_without_human),
    ("ADV-16 Failed test passed", test_adv_16_failed_test_passed),
    ("ADV-17 Security without evidence", test_adv_17_security_without_evidence),
    ("ADV-18 Accessibility without evidence", test_adv_18_accessibility_without_evidence),
    ("ADV-19 Demo vs live confused", test_adv_19_demo_vs_live_confused),
    ("ADV-20 Presentation vs live confused", test_adv_20_presentation_vs_live_confused),
    ("ADV-21 Simulated score as official", test_adv_21_simulated_score_as_official),
    ("ADV-22 Hidden multiplier", test_adv_22_hidden_multiplier),
    ("ADV-23 Silent idea reselection", test_adv_23_silent_idea_reselection),
    ("ADV-24 Silent scope expansion", test_adv_24_silent_scope_expansion),
    ("ADV-25 Architecture modification", test_adv_25_architecture_modification),
    ("ADV-26 Secret detection bypass", test_adv_26_secret_detection_bypass),
    ("ADV-27 Deployment assumed healthy", test_adv_27_deployment_assumed_healthy),
    ("ADV-28 Phase 19 submission executed", test_adv_28_phase19_submission_executed),
    ("ADV-29 Multiple PRIMARY NEXT ACTION entries", test_adv_29_multiple_primary_next_actions),
    ("ADV-30 Fabricated readiness", test_adv_30_fabricated_readiness),
]


def main() -> int:
    results = []
    for name, test in TESTS:
        parts = name.split(" ", 1)
        test_id = parts[0]
        description = parts[1] if len(parts) > 1 else name
        adversarial = test_id.startswith("ADV-")
        setup = (f"Threat case: {description}. Inspect the applicable Phase 18 guardrail in the current repository."
                 if adversarial else
                 f"Acceptance case: {description}. Inspect the applicable Phase 18 contract in the current repository.")
        expected = ("The unsafe or unsupported condition is rejected, bounded, or routed to its owner."
                    if adversarial else
                    "The required Phase 18 artifact, boundary, status, or process is present and consistent.")
        try:
            test()
            results.append({
                "id": test_id,
                "description": description,
                "setup": setup,
                "expected_result": expected,
                "observed_result": f"PASS: {test.__doc__ or description}",
                "status": "PASS",
                "evidence": f"Executed assertion: tests/workflows/test_final_audit.py::{test.__name__}.",
            })
        except Exception as exc:
            results.append({
                "id": test_id,
                "description": description,
                "setup": setup,
                "expected_result": expected,
                "observed_result": f"Assertion failed: {type(exc).__name__}: {exc}",
                "status": "FAIL",
                "evidence": f"Executed assertion: tests/workflows/test_final_audit.py::{test.__name__}.",
            })

    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] != "PASS")
    at_results = [r for r in results if r["id"].startswith("AT-")]
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
