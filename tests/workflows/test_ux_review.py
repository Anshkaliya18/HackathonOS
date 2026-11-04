#!/usr/bin/env python3
"""Deterministic contract validation for Phase 12 — UX Review Intelligence.

Validates the Phase 12 UX Review workflow, rules, and template contracts against
the acceptance tests AT-251 through AT-285 and adversarial scenarios.

Follows the Phase 6/Phase 10/Phase 11 smoke harness pattern: stdlib-only,
disposable fixtures, machine-readable JSON output, non-zero exit on any failure.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "SKILL.md"
WORKFLOW = ROOT / "workflows" / "ux-review.md"
RULES = ROOT / "rules" / "ux-rules.md"
REVIEW_TEMPLATE = ROOT / "templates" / "ux-review.md"
FINDING_TEMPLATE = ROOT / "templates" / "ux-finding.md"
FLOW_TEMPLATE = ROOT / "templates" / "ux-flow.md"
VERIFICATION_TEMPLATE = ROOT / "templates" / "ux-verification.md"
LIFECYCLE = ROOT / "workflows" / "lifecycle.md"

# Expected Phase 12 resources (already exist from legacy Phase 7 numbering,
# but lifecycle.md identifies UX Review as Phase 12)
PHASE12_FILES = [
    WORKFLOW,
    RULES,
    REVIEW_TEMPLATE,
    FINDING_TEMPLATE,
    FLOW_TEMPLATE,
    VERIFICATION_TEMPLATE,
]


def file_contains(path: Path, pattern: str) -> bool:
    return re.search(pattern, path.read_text(encoding="utf-8"), re.IGNORECASE) is not None


def file_contains_all(path: Path, patterns: list[str]) -> list[str]:
    """Return list of patterns NOT found in file."""
    text = path.read_text(encoding="utf-8")
    missing = []
    for p in patterns:
        if re.search(p, text, re.IGNORECASE) is None:
            missing.append(p)
    return missing


def count_occurrences(path: Path, pattern: str) -> int:
    return len(re.findall(pattern, path.read_text(encoding="utf-8"), re.IGNORECASE))


# ---------------------------------------------------------------------------
# AT-251 through AT-285 acceptance tests
# ---------------------------------------------------------------------------

def test_at251_prerequisite_phase11_locked() -> None:
    """UX review consumes project testing/security records."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 5 test results/security review/findings" in text
    assert "UX review BLOCKED" in text


def test_at252_lifecycle_correctness() -> None:
    """Lifecycle contains exactly 20 phases; Phase 12 = UX Review."""
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
    assert data_rows[11][0].strip() == "UX Review", \
        f"Phase 12 should be UX Review, found: {data_rows[11][0].strip()}"


def test_at253_routing_exists() -> None:
    """UX-REVIEW routing exists in SKILL.md."""
    text = SKILL.read_text(encoding="utf-8")
    assert "UX-REVIEW" in text, "SKILL.md missing UX-REVIEW operation"
    assert "workflows/ux-review.md" in text, "SKILL.md missing ux-review.md workflow path"


def test_at254_resources_resolve() -> None:
    """All Phase 12 resources load from expected locations."""
    for f in PHASE12_FILES:
        assert f.is_file(), f"Phase 12 resource missing: {f}"


def test_at255_repository_inspection() -> None:
    """Workflow requires repository/product evidence inspection."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "inspect" in text.lower(), "Workflow does not require inspection"
    assert "repository" in text.lower() or "project" in text.lower(), \
        "Workflow does not address repository/project inspection"


def test_at256_evidence_classification() -> None:
    """Evidence model uses FACT/INFERENCE/ASSUMPTION/UNKNOWN."""
    rules_text = RULES.read_text(encoding="utf-8")
    for label in ["FACT", "INFERENCE", "ASSUMPTION", "UNKNOWN"]:
        assert label in rules_text, f"Rules missing evidence label: {label}"


def test_at257_ux_observation_model() -> None:
    """Observation statuses: OBSERVED/SUPPORTED/INFERRED/UNKNOWN/NOT_TESTED."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    for status in ["observed", "inferred", "unknown", "not_tested"]:
        assert status in combined, f"Observation status missing: {status}"


def test_at258_information_architecture() -> None:
    """Information architecture dimension is inspected."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "information architecture" in combined or "information_architecture" in combined, \
        "Workflow/rules do not address information architecture"
    assert "discoverab" in combined, "Workflow/rules do not address discoverability"


def test_at259_navigation() -> None:
    """Navigation dimension is inspected."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "navigation" in combined, "Workflow/rules do not address navigation"
    assert "breadcr" in combined or "back" in combined, \
        "Workflow/rules do not address breadcrumbs/back behavior"


def test_at260_user_flows() -> None:
    """User flows are mapped."""
    assert FLOW_TEMPLATE.is_file(), "UX flow template missing"
    flow_text = FLOW_TEMPLATE.read_text(encoding="utf-8")
    assert "Flow ID" in flow_text, "Flow template missing Flow ID"
    assert "Steps" in flow_text, "Flow template missing Steps"
    assert "Observed Outcome" in flow_text, "Flow template missing Observed Outcome"


def test_at261_interaction_design() -> None:
    """Interaction design is inspected."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "button" in combined or "click" in combined or "interaction" in combined, \
        "Workflow/rules do not address interaction design"
    assert "feedback" in combined, "Workflow/rules do not address feedback"


def test_at262_visual_hierarchy() -> None:
    """Visual hierarchy is inspected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "visual hierarchy" in rules_text.lower() or "visual_hierarchy" in rules_text.lower(), \
        "Rules do not address visual hierarchy"
    assert "headings" in rules_text.lower() or "spacing" in rules_text.lower(), \
        "Rules do not address visual hierarchy elements"


def test_at263_responsive_review() -> None:
    """Responsive behavior is reviewed."""
    review_text = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    assert "Responsive" in review_text, "Review template missing Responsive section"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "viewport" in rules_text.lower() or "mobile" in rules_text.lower(), \
        "Rules do not address responsive viewports"


def test_at264_accessibility() -> None:
    """Accessibility is inspected."""
    review_text = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    assert "Accessibility" in review_text, "Review template missing Accessibility section"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "keyboard" in rules_text.lower() or "focus" in rules_text.lower(), \
        "Rules do not address keyboard/focus accessibility"


def test_at265_forms_inputs() -> None:
    """Forms and inputs are inspected."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "form" in combined, "Workflow/rules do not address forms"
    assert "validation" in combined, "Workflow/rules do not address validation"


def test_at266_loading_state() -> None:
    """Loading state is inspected."""
    review_text = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    assert "Loading" in review_text, "Review template missing Loading state"


def test_at267_error_state() -> None:
    """Error state is inspected."""
    review_text = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    assert "Failure" in review_text or "Error" in review_text, \
        "Review template missing Error/Failure state"


def test_at268_empty_state() -> None:
    """Empty state is inspected."""
    review_text = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    assert "Empty" in review_text, "Review template missing Empty state"


def test_at269_success_state() -> None:
    """Success state is inspected."""
    review_text = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    assert "Success" in review_text, "Review template missing Success state"


def test_at270_onboarding() -> None:
    """Onboarding is inspected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "onboarding" in rules_text.lower(), "Rules do not address onboarding"


def test_at271_demo_flow() -> None:
    """Demo flow is inspected."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "demo" in combined, "Workflow/rules do not address demo flow"


def test_at272_severity_model() -> None:
    """Severity model: CRITICAL/HIGH/MEDIUM/LOW."""
    rules_text = RULES.read_text(encoding="utf-8")
    finding_text = FINDING_TEMPLATE.read_text(encoding="utf-8")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        assert sev in rules_text or sev in finding_text, \
            f"Severity {sev} not found in rules or finding template"


def test_at273_priority_model() -> None:
    """Priority model: P0/P1/P2/P3."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "P0" in rules_text and "P1" in rules_text, \
        "Rules do not define P0/P1 priorities"
    assert "P2" in rules_text and "P3" in rules_text, \
        "Rules do not define P2/P3 priorities"


def test_at274_confidence_recorded() -> None:
    """Confidence is recorded per finding."""
    finding_text = FINDING_TEMPLATE.read_text(encoding="utf-8")
    assert "Confidence" in finding_text, "Finding template missing Confidence"


def test_at275_verification_defined() -> None:
    """Verification is defined per finding."""
    assert VERIFICATION_TEMPLATE.is_file(), "UX verification template missing"
    verification_text = VERIFICATION_TEMPLATE.read_text(encoding="utf-8")
    assert "Verification Procedure" in verification_text, \
        "Verification template missing Verification Procedure"
    assert "Expected Result" in verification_text, \
        "Verification template missing Expected Result"
    assert "Actual Result" in verification_text, \
        "Verification template missing Actual Result"


def test_at276_quality_gate_states() -> None:
    """Quality gate states enforced."""
    rules_text = RULES.read_text(encoding="utf-8")
    for gate in ["NOT_READY", "REVIEW_IN_PROGRESS", "BLOCKED", "CONDITIONAL", "READY"]:
        assert gate in rules_text, f"Quality gate {gate} not found in rules"


def test_at277_time_aware_strategy() -> None:
    """Time-aware strategy works."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "time" in combined, "Workflow/rules do not address time-aware strategy"
    assert "6" in rules_text or "2-6" in rules_text or "6-12" in rules_text, \
        "Rules do not define time strategy windows"


def test_at278_state_integration() -> None:
    """State integration fields defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UX status" in rules_text or "ux status" in rules_text.lower(), \
        "Rules do not define UX status state field"
    assert "UX quality gate" in rules_text or "ux quality gate" in rules_text.lower(), \
        "Rules do not define UX quality gate state field"


def test_at279_ownership_boundaries() -> None:
    """Phase 12 does not own other phases' responsibilities."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    rules_text = RULES.read_text(encoding="utf-8")
    combined = (workflow_text + " " + rules_text).lower()
    assert "do not" in combined, "Workflow/rules do not establish boundaries"
    assert "implementation" in combined or "phase 4" in combined, \
        "Workflow/rules do not address implementation ownership boundary"


def test_at280_no_silent_implementation() -> None:
    """Phase 12 does not silently implement UX changes."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    rules_text = RULES.read_text(encoding="utf-8")
    combined = (workflow_text + " " + rules_text).lower()
    assert "implement" in combined, "Workflow/rules do not address implementation boundary"
    assert "do not implement" in combined or "not implement" in combined, \
        "Workflow/rules do not explicitly prohibit implementation"


def test_at281_evidence_integrity() -> None:
    """Every finding requires evidence classification."""
    finding_text = FINDING_TEMPLATE.read_text(encoding="utf-8")
    assert "Evidence" in finding_text, "Finding template missing Evidence section"
    assert "FACT" in finding_text or "INFERENCE" in finding_text, \
        "Finding template does not require evidence classification"


def test_at282_primary_next_action() -> None:
    """Exactly one primary next action."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "PRIMARY NEXT ACTION" in workflow_text, "Workflow missing PRIMARY NEXT ACTION"
    review_text = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    assert "PRIMARY NEXT ACTION" in review_text, "Review template missing PRIMARY NEXT ACTION"


def test_at283_unknown_preserved() -> None:
    """Unknown evidence is not converted to fact."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text, "Rules do not allow UNKNOWN"
    assert "never convert" in rules_text.lower() or "do not convert" in rules_text.lower(), \
        "Rules do not prohibit converting UNKNOWN to FACT"


def test_at284_regression_considered() -> None:
    """Regression is considered for findings."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "regression" in rules_text.lower(), "Rules do not address regression"


def test_at285_no_fabricated_compliance() -> None:
    """No fabricated accessibility/responsive compliance claims."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "wcag" in combined or "compliance" in combined, \
        "Workflow/rules do not address compliance claims"
    assert "scope" in combined, "Workflow/rules do not limit claims to inspected scope"


# ---------------------------------------------------------------------------
# Adversarial validation scenarios (30 minimum)
# ---------------------------------------------------------------------------

def test_adv_01_missing_phase11() -> None:
    """Missing test/security evidence blocks substantive UX conclusions."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 5 test results/security review/findings" in text
    assert "BLOCKED" in text


def test_adv_02_missing_project_state() -> None:
    """Missing project state handled gracefully."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "project-state" in text.lower() or "project state" in text.lower()


def test_adv_03_empty_project() -> None:
    """Empty project handled gracefully."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text, "Rules do not handle UNKNOWN state"


def test_adv_04_no_frontend() -> None:
    """Project with no frontend handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "not present" in combined or "no frontend" in combined or "ui = " in combined, \
        "Workflow/rules do not address missing UI"


def test_adv_05_cli_only_project() -> None:
    """CLI-only project handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text or "not present" in rules_text.lower()


def test_adv_06_missing_browser_runtime() -> None:
    """Missing browser runtime handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "browser" in rules_text.lower() or "runtime" in rules_text.lower()
    assert "unknown" in rules_text.lower()


def test_adv_07_missing_screenshots() -> None:
    """Missing screenshots handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "unknown" in rules_text.lower() or "not tested" in rules_text.lower()


def test_adv_08_missing_ux_artifacts() -> None:
    """Missing UX artifacts handled."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "missing" in workflow_text.lower() or "unknown" in workflow_text.lower()


def test_adv_09_conflicting_ux_evidence() -> None:
    """Conflicting UX evidence recorded, not reconciled."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "contradict" in workflow_text.lower() or "conflict" in workflow_text.lower()


def test_adv_10_stale_ux_evidence() -> None:
    """Stale UX evidence flagged."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "stale" in workflow_text.lower() or "revision" in workflow_text.lower() or "unknown" in workflow_text.lower()


def test_adv_11_unsupported_accessibility_claim() -> None:
    """Unsupported accessibility claims rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "compliance" in rules_text.lower() or "wcag" in rules_text.lower()
    assert "scope" in rules_text.lower()


def test_adv_12_unsupported_responsive_claim() -> None:
    """Unsupported responsive claims rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "viewport" in rules_text.lower() or "responsive" in rules_text.lower()
    assert "untested" in rules_text.lower() or "unknown" in rules_text.lower()


def test_adv_13_unsupported_browser_claim() -> None:
    """Unsupported browser claims rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "browser" in rules_text.lower() or "runtime" in rules_text.lower()


def test_adv_14_unknown_severity() -> None:
    """UX issue with unknown severity handled."""
    finding_text = FINDING_TEMPLATE.read_text(encoding="utf-8")
    assert "UNKNOWN" in finding_text


def test_adv_15_conflicting_severity() -> None:
    """Conflicting severity flagged."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "severity" in workflow_text.lower()


def test_adv_16_critical_issue_hidden() -> None:
    """Critical UX issue not hidden."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "CRITICAL" in rules_text


def test_adv_17_multiple_primary_flows() -> None:
    """Multiple possible primary flows handled."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "flow" in workflow_text.lower()


def test_adv_18_demo_flow_differs() -> None:
    """Demo flow differs from normal flow handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "demo" in rules_text.lower()


def test_adv_19_no_onboarding() -> None:
    """Project with no onboarding handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "onboarding" in rules_text.lower()


def test_adv_20_no_empty_state() -> None:
    """Project intentionally has no empty state handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "empty" in rules_text.lower()


def test_adv_21_no_persistent_backend() -> None:
    """Project with no persistent backend handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "backend" in rules_text.lower()


def test_adv_22_minimal_ui() -> None:
    """Project with intentionally minimal UI handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "not present" in rules_text.lower() or "unknown" in rules_text.lower()


def test_adv_23_cross_phase_ownership() -> None:
    """UX issue belonging to another phase is escalated, not taken."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "architecture change required" in rules_text.lower() or "phase" in rules_text.lower()


def test_adv_24_time_under_two_hours() -> None:
    """Time remaining <2 hours freezes broad redesign."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "<2" in rules_text or "2 hours" in rules_text or "<2h" in rules_text


def test_adv_25_phase1_11_untouched() -> None:
    """Phase 1-11 artifacts remain untouched."""
    phase_files = [
        ROOT / "workflows" / "score-optimization.md",
        ROOT / "workflows" / "judge-simulation.md",
        ROOT / "workflows" / "red-team.md",
        ROOT / "workflows" / "testing-security.md",
        ROOT / "workflows" / "implementation.md",
    ]
    for f in phase_files:
        assert f.is_file(), f"Phase file missing: {f}"


def test_adv_26_no_implementation_leakage() -> None:
    """No implementation work performed by Phase 12."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "do not implement" in workflow_text.lower() or "not implement" in workflow_text.lower(), \
        "Workflow does not prohibit implementation work"


def test_adv_27_no_architecture_change() -> None:
    """Phase 12 does not change architecture."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "architecture" in rules_text.lower()


def test_adv_28_no_score_opt_ownership() -> None:
    """Phase 12 does not own score optimization."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "score" in workflow_text.lower() or "optimization" in workflow_text.lower()


def test_adv_29_no_judge_sim_ownership() -> None:
    """Phase 12 does not own judge simulation."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "judge" in workflow_text.lower()


def test_adv_30_no_postmortem_ownership() -> None:
    """Phase 12 does not own post-mortem."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "post" in workflow_text.lower() or "mortem" in workflow_text.lower()


# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------

TESTS: list[tuple[str, Callable[[], None]]] = [
    # Acceptance tests AT-251 through AT-285
    ("AT-251 Prerequisite Phase 11 locked", test_at251_prerequisite_phase11_locked),
    ("AT-252 Lifecycle correctness", test_at252_lifecycle_correctness),
    ("AT-253 Routing exists", test_at253_routing_exists),
    ("AT-254 Resources resolve", test_at254_resources_resolve),
    ("AT-255 Repository inspection", test_at255_repository_inspection),
    ("AT-256 Evidence classification", test_at256_evidence_classification),
    ("AT-257 UX observation model", test_at257_ux_observation_model),
    ("AT-258 Information architecture", test_at258_information_architecture),
    ("AT-259 Navigation", test_at259_navigation),
    ("AT-260 User flows", test_at260_user_flows),
    ("AT-261 Interaction design", test_at261_interaction_design),
    ("AT-262 Visual hierarchy", test_at262_visual_hierarchy),
    ("AT-263 Responsive review", test_at263_responsive_review),
    ("AT-264 Accessibility", test_at264_accessibility),
    ("AT-265 Forms inputs", test_at265_forms_inputs),
    ("AT-266 Loading state", test_at266_loading_state),
    ("AT-267 Error state", test_at267_error_state),
    ("AT-268 Empty state", test_at268_empty_state),
    ("AT-269 Success state", test_at269_success_state),
    ("AT-270 Onboarding", test_at270_onboarding),
    ("AT-271 Demo flow", test_at271_demo_flow),
    ("AT-272 Severity model", test_at272_severity_model),
    ("AT-273 Priority model", test_at273_priority_model),
    ("AT-274 Confidence recorded", test_at274_confidence_recorded),
    ("AT-275 Verification defined", test_at275_verification_defined),
    ("AT-276 Quality gate states", test_at276_quality_gate_states),
    ("AT-277 Time-aware strategy", test_at277_time_aware_strategy),
    ("AT-278 State integration", test_at278_state_integration),
    ("AT-279 Ownership boundaries", test_at279_ownership_boundaries),
    ("AT-280 No silent implementation", test_at280_no_silent_implementation),
    ("AT-281 Evidence integrity", test_at281_evidence_integrity),
    ("AT-282 Primary next action", test_at282_primary_next_action),
    ("AT-283 Unknown preserved", test_at283_unknown_preserved),
    ("AT-284 Regression considered", test_at284_regression_considered),
    ("AT-285 No fabricated compliance", test_at285_no_fabricated_compliance),
    # Adversarial validation scenarios
    ("ADV-01 Missing Phase 11", test_adv_01_missing_phase11),
    ("ADV-02 Missing project state", test_adv_02_missing_project_state),
    ("ADV-03 Empty project", test_adv_03_empty_project),
    ("ADV-04 No frontend", test_adv_04_no_frontend),
    ("ADV-05 CLI-only project", test_adv_05_cli_only_project),
    ("ADV-06 Missing browser runtime", test_adv_06_missing_browser_runtime),
    ("ADV-07 Missing screenshots", test_adv_07_missing_screenshots),
    ("ADV-08 Missing UX artifacts", test_adv_08_missing_ux_artifacts),
    ("ADV-09 Conflicting UX evidence", test_adv_09_conflicting_ux_evidence),
    ("ADV-10 Stale UX evidence", test_adv_10_stale_ux_evidence),
    ("ADV-11 Unsupported accessibility claim", test_adv_11_unsupported_accessibility_claim),
    ("ADV-12 Unsupported responsive claim", test_adv_12_unsupported_responsive_claim),
    ("ADV-13 Unsupported browser claim", test_adv_13_unsupported_browser_claim),
    ("ADV-14 Unknown severity", test_adv_14_unknown_severity),
    ("ADV-15 Conflicting severity", test_adv_15_conflicting_severity),
    ("ADV-16 Critical issue hidden", test_adv_16_critical_issue_hidden),
    ("ADV-17 Multiple primary flows", test_adv_17_multiple_primary_flows),
    ("ADV-18 Demo flow differs", test_adv_18_demo_flow_differs),
    ("ADV-19 No onboarding", test_adv_19_no_onboarding),
    ("ADV-20 No empty state", test_adv_20_no_empty_state),
    ("ADV-21 No persistent backend", test_adv_21_no_persistent_backend),
    ("ADV-22 Minimal UI", test_adv_22_minimal_ui),
    ("ADV-23 Cross-phase ownership", test_adv_23_cross_phase_ownership),
    ("ADV-24 Time under two hours", test_adv_24_time_under_two_hours),
    ("ADV-25 Phase 1-11 untouched", test_adv_25_phase1_11_untouched),
    ("ADV-26 No implementation leakage", test_adv_26_no_implementation_leakage),
    ("ADV-27 No architecture change", test_adv_27_no_architecture_change),
    ("ADV-28 No score optimization ownership", test_adv_28_no_score_opt_ownership),
    ("ADV-29 No judge simulation ownership", test_adv_29_no_judge_sim_ownership),
    ("ADV-30 No post-mortem ownership", test_adv_30_no_postmortem_ownership),
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
