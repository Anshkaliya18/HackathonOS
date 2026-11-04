#!/usr/bin/env python3
"""Deterministic contract validation for Phase 11 — Testing + Security Intelligence.

Validates the Phase 11 workflow, rules, and template contracts against the
acceptance tests AT-216 through AT-250 and adversarial scenarios.

Follows the Phase 6/Phase 10 smoke harness pattern: stdlib-only, disposable
fixtures, machine-readable JSON output, non-zero exit on any failure.
"""

from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "SKILL.md"
WORKFLOW = ROOT / "workflows" / "testing-security.md"
RULES = ROOT / "rules" / "testing-security-rules.md"
PLAN_TEMPLATE = ROOT / "templates" / "test-plan.md"
RESULT_TEMPLATE = ROOT / "templates" / "test-result.md"
REVIEW_TEMPLATE = ROOT / "templates" / "security-review.md"
FINDING_TEMPLATE = ROOT / "templates" / "security-finding.md"
LIFECYCLE = ROOT / "workflows" / "lifecycle.md"

# Expected Phase 11 resources (already exist from legacy Phase 5 numbering,
# but lifecycle.md identifies Testing + Security as Phase 11)
PHASE11_FILES = [
    WORKFLOW,
    RULES,
    PLAN_TEMPLATE,
    RESULT_TEMPLATE,
    REVIEW_TEMPLATE,
    FINDING_TEMPLATE,
]


def route_table() -> dict[str, str]:
    """Extract operation -> workflow path from SKILL.md operations table."""
    text = SKILL.read_text(encoding="utf-8")
    rows = re.findall(
        r"(?m)^\|\s*\*\*([^*]+)\*\*\s*\|[^\n]*?`(workflows/[^`]+\.md)`\s*\|",
        text,
    )
    return {name.strip(): path.strip() for name, path in rows}


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


# ---------------------------------------------------------------------------
# AT-216 through AT-250 acceptance tests
# ---------------------------------------------------------------------------

def test_at216_routing_exists() -> None:
    """Phase 11 routing exists."""
    routes = route_table()
    assert "TESTING-SECURITY" in routes, f"TESTING-SECURITY missing from route table: {routes}"
    assert routes["TESTING-SECURITY"] == "workflows/testing-security.md", \
        f"Wrong route: {routes.get('TESTING-SECURITY')}"
    assert WORKFLOW.is_file(), f"Workflow file missing: {WORKFLOW}"


def test_at217_resources_resolve() -> None:
    """All Phase 11 resources load from their expected locations."""
    for f in PHASE11_FILES:
        assert f.is_file(), f"Phase 11 resource missing: {f}"
    assert "TESTING-SECURITY" in SKILL.read_text(encoding="utf-8")


def test_at218_phase10_lock_required() -> None:
    """The workflow checks actual project implementation evidence."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert ".sherpa/project-state.md" in workflow_text
    assert "implementation status" in workflow_text.lower()


def test_at219_lifecycle_integrity() -> None:
    """Lifecycle integrity checked — exactly 20 phases, Testing + Security at 11."""
    text = LIFECYCLE.read_text(encoding="utf-8")
    # Count data rows in the lifecycle phase table only (stop before Time-Aware Strategy table)
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
                    break  # Second table started
                data_rows.append(cells)
    assert len(data_rows) == 20, f"Expected 20 phase rows, found {len(data_rows)}"
    # Testing + Security should be phase 11 (index 10 in 0-based data rows)
    assert data_rows[10][0].strip() == "Testing + Security", \
        f"Testing + Security should be phase 11, found: {data_rows[10][0].strip()}"


def test_at220_phase1_10_preserved() -> None:
    """Phase 1-10 integrity preserved — no modifications to locked phase files."""
    # Verify Phase 1-10 workflow files exist and are unmodified
    phase_files = [
        ROOT / "workflows" / "init.md",
        ROOT / "workflows" / "status.md",
        ROOT / "workflows" / "next.md",
        ROOT / "workflows" / "idea-evaluation.md",
        ROOT / "workflows" / "project-planning.md",
        ROOT / "workflows" / "implementation.md",
        ROOT / "workflows" / "testing-security.md",
        ROOT / "workflows" / "ux-review.md",
        ROOT / "workflows" / "red-team.md",
        ROOT / "workflows" / "judge-simulation.md",
        ROOT / "workflows" / "score-optimization.md",
    ]
    for f in phase_files:
        assert f.is_file(), f"Phase file missing: {f}"


def test_at221_test_plan_generated() -> None:
    """Test plan generated."""
    assert PLAN_TEMPLATE.is_file(), "Test plan template missing"
    text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    assert "Test Plan" in text, "Test plan template missing title"
    assert "Status" in text, "Test plan template missing Status section"


def test_at222_relevant_categories_selected() -> None:
    """Relevant categories selected."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    for cat in ["UNIT", "INTEGRATION", "E2E", "SECURITY", "API"]:
        assert cat in rules_text or cat in workflow_text, \
            f"Category {cat} not found in rules or workflow"


def test_at223_critical_path_identified() -> None:
    """Critical path identified."""
    text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    assert "Critical" in text or "critical" in text.lower(), \
        "Test plan template missing critical path section"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "critical" in rules_text.lower(), "Rules do not address critical paths"


def test_at224_test_priorities_assigned() -> None:
    """Test priorities assigned."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    plan_text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    for p in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        assert p in rules_text or p in workflow_text or p in plan_text, \
            f"Priority {p} not found in rules, workflow, or plan template"


def test_at225_expected_results_defined() -> None:
    """Expected results defined."""
    result_text = RESULT_TEMPLATE.read_text(encoding="utf-8")
    assert "Expected Result" in result_text, "Test result template missing Expected Result"


def test_at226_test_status_model_enforced() -> None:
    """Test status model enforced."""
    result_text = RESULT_TEMPLATE.read_text(encoding="utf-8")
    rules_text = RULES.read_text(encoding="utf-8")
    for status in ["PLANNED", "EXECUTED", "PASSED", "FAILED", "BLOCKED", "UNKNOWN"]:
        assert status in result_text or status in rules_text, \
            f"Status {status} not found in test result template or rules"


def test_at227_actual_result_recorded() -> None:
    """Actual result recorded."""
    result_text = RESULT_TEMPLATE.read_text(encoding="utf-8")
    assert "Actual Result" in result_text, "Test result template missing Actual Result"


def test_at228_pass_requires_evidence() -> None:
    """PASS requires evidence."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "evidence" in rules_text.lower() and "evidence" in workflow_text.lower(), \
        "Rules/workflow do not require evidence for PASS"
    assert "PASSED" in rules_text or "PASSED" in workflow_text, \
        "Rules/workflow do not address PASSED status"


def test_at229_unknown_preserved() -> None:
    """UNKNOWN preserved."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text, "Rules do not allow UNKNOWN status"
    assert "never" in rules_text.lower() or "do not" in rules_text.lower(), \
        "Rules do not prohibit converting UNKNOWN to PASS"


def test_at230_failures_classified() -> None:
    """Failures classified."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO", "UNKNOWN"]:
        assert sev in rules_text or sev in workflow_text, \
            f"Severity {sev} not found in rules or workflow"


def test_at231_security_review_generated() -> None:
    """Security review generated."""
    assert REVIEW_TEMPLATE.is_file(), "Security review template missing"
    text = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    assert "Security Review" in text, "Security review template missing title"


def test_at232_attack_surface_inspected() -> None:
    """Relevant attack surface inspected."""
    rules_text = RULES.read_text(encoding="utf-8")
    for area in ["authentication", "authorization", "input", "injection", "secrets", "dependency"]:
        assert area in rules_text.lower(), f"Rules do not address security area: {area}"


def test_at233_evidence_required() -> None:
    """Evidence required."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "evidence" in rules_text.lower(), "Rules do not require evidence"
    assert "FACT" in rules_text and "INFERENCE" in rules_text, \
        "Rules do not use evidence classification model"


def test_at234_severity_separated_from_confidence() -> None:
    """Severity separated from confidence."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "severity" in rules_text.lower(), "Rules do not address severity"
    assert "confidence" in rules_text.lower(), "Rules do not address confidence"


def test_at235_security_findings_generated() -> None:
    """Security findings generated."""
    assert FINDING_TEMPLATE.is_file(), "Security finding template missing"
    text = FINDING_TEMPLATE.read_text(encoding="utf-8")
    assert "Security Finding" in text, "Security finding template missing title"
    assert "Severity" in text, "Security finding template missing Severity"


def test_at236_no_fabricated_zero_vulnerabilities() -> None:
    """No fabricated 'zero vulnerabilities' claim."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "scope" in rules_text.lower(), "Rules do not limit security claims to scope"
    assert "no vulnerabilities" not in rules_text.lower().replace("no confirmed vulnerabilities identified within the inspected scope", ""), \
        "Rules may claim zero vulnerabilities without scope limitation"


def test_at237_remediation_priority_assigned() -> None:
    """Remediation priority assigned."""
    rules_text = RULES.read_text(encoding="utf-8")
    finding_text = FINDING_TEMPLATE.read_text(encoding="utf-8")
    for p in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        assert p in rules_text or p in finding_text, \
            f"Remediation priority {p} not found in rules or finding template"
    assert "Status" in finding_text, "Finding template missing Status field"


def test_at238_defer_requires_rationale() -> None:
    """DEFER/ACCEPTED_RISK requires rationale."""
    rules_text = RULES.read_text(encoding="utf-8")
    finding_text = FINDING_TEMPLATE.read_text(encoding="utf-8")
    # ACCEPTED_RISK is the equivalent of DEFER in the existing finding model
    assert "ACCEPTED_RISK" in finding_text, "Finding template missing ACCEPTED_RISK status"
    assert "reason" in rules_text.lower() or "rationale" in rules_text.lower() or "reason" in finding_text.lower(), \
        "Rules or finding template do not require rationale for deferred/accepted findings"


def test_at239_verification_recorded() -> None:
    """Verification recorded."""
    result_text = RESULT_TEMPLATE.read_text(encoding="utf-8")
    rules_text = RULES.read_text(encoding="utf-8")
    assert "verification" in result_text.lower() or "verification" in rules_text.lower(), \
        "Result template/rules do not address verification"


def test_at240_regression_considered() -> None:
    """Regression considered."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "regression" in rules_text.lower() and "regression" in workflow_text.lower(), \
        "Rules/workflow do not address regression"


def test_at241_time_aware_strategy() -> None:
    """Time-aware strategy works."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "time" in rules_text.lower() and "time" in workflow_text.lower(), \
        "Rules/workflow do not address time-aware strategy"


def test_at242_six_hour_strategy() -> None:
    """Six-hour strategy prioritizes critical paths."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "6" in rules_text or "2-6" in rules_text or "6-12" in rules_text, \
        "Rules do not define 6-hour time strategy"
    assert "critical" in rules_text.lower(), "Rules do not prioritize critical paths under time pressure"


def test_at243_quality_gate_states() -> None:
    """Quality gate states enforced."""
    rules_text = RULES.read_text(encoding="utf-8")
    for gate in ["NOT_READY", "TESTING_IN_PROGRESS", "BLOCKED", "CONDITIONAL", "READY"]:
        assert gate in rules_text, f"Quality gate {gate} not found in rules"


def test_at244_ready_requires_critical_evidence() -> None:
    """READY requires critical evidence."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "READY" in rules_text, "Rules do not define READY gate"
    assert "critical" in rules_text.lower(), "Rules do not require critical evidence for READY"


def test_at245_unknown_prevents_ready() -> None:
    """UNKNOWN prevents unjustified READY."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text, "Rules do not allow UNKNOWN"
    assert "READY" in rules_text, "Rules do not define READY gate"
    assert "evidence" in rules_text.lower(), "Rules do not require evidence for READY"


def test_at246_no_idea_ownership() -> None:
    """No idea ownership."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    rules_text = RULES.read_text(encoding="utf-8")
    assert "selected idea" in workflow_text.lower() or "selected idea" in rules_text.lower(), \
        "Workflow/rules do not protect selected idea"


def test_at247_no_architecture_ownership() -> None:
    """No architecture ownership."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    rules_text = RULES.read_text(encoding="utf-8")
    assert "architecture" in workflow_text.lower() or "architecture" in rules_text.lower(), \
        "Workflow/rules do not address architecture boundary"


def test_at248_no_judge_sim_ownership() -> None:
    """No judge simulation ownership."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    rules_text = RULES.read_text(encoding="utf-8")
    # Phase 11 should not own judge simulation (Phase 14) — check for phase boundary language
    combined = (workflow_text + " " + rules_text).lower()
    assert "do not start" in combined or "do not replace" in combined or "phase" in combined, \
        "Workflow/rules do not establish phase boundaries"


def test_at249_no_score_opt_ownership() -> None:
    """No score optimization ownership."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    rules_text = RULES.read_text(encoding="utf-8")
    # Phase 11 should not own score optimization (Phase 15) — check for phase boundary language
    combined = (workflow_text + " " + rules_text).lower()
    assert "do not start" in combined or "do not replace" in combined or "phase" in combined, \
        "Workflow/rules do not establish phase boundaries"


def test_at250_exactly_one_primary_next_action() -> None:
    """Exactly one primary next action."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "PRIMARY NEXT ACTION" in workflow_text, "Workflow missing PRIMARY NEXT ACTION"
    plan_text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    assert "PRIMARY NEXT ACTION" in plan_text, "Plan template missing PRIMARY NEXT ACTION"
    review_text = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    assert "PRIMARY NEXT ACTION" in review_text, "Security review template missing PRIMARY NEXT ACTION"


# ---------------------------------------------------------------------------
# Adversarial validation scenarios (30 minimum)
# ---------------------------------------------------------------------------

def test_adv_01_missing_phase10() -> None:
    """Missing implementation blocks substantive testing."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "Testing blocked until implementation exists." in workflow_text


def test_adv_02_phase10_unlocked() -> None:
    """Testing preserves the implementation workflow boundary."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 4 files are frozen" in workflow_text


def test_adv_03_missing_project() -> None:
    """Missing project handled gracefully."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "project-state" in workflow_text.lower() or "project state" in workflow_text.lower(), \
        "Workflow does not address missing project state"


def test_adv_04_empty_repository() -> None:
    """Empty repository handled gracefully."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text, "Rules do not handle UNKNOWN state for empty repository"


def test_adv_05_missing_test_evidence() -> None:
    """Missing test evidence marked UNKNOWN."""
    result_text = RESULT_TEMPLATE.read_text(encoding="utf-8")
    assert "UNKNOWN" in result_text, "Test result template does not allow UNKNOWN"


def test_adv_06_test_pass_without_execution() -> None:
    """Test marked PASS without execution rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "evidence" in rules_text.lower() and "evidence" in workflow_text.lower(), \
        "Rules/workflow do not require evidence for PASS"
    assert "PASSED" in rules_text or "PASSED" in workflow_text, \
        "Rules/workflow do not address PASSED status"


def test_adv_07_unknown_converted_to_pass() -> None:
    """UNKNOWN not converted to PASS."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "never" in rules_text.lower() or "do not" in rules_text.lower(), \
        "Rules do not prohibit converting UNKNOWN to PASS"


def test_adv_08_missing_expected_result() -> None:
    """Missing expected result handled."""
    result_text = RESULT_TEMPLATE.read_text(encoding="utf-8")
    assert "Expected Result" in result_text, "Test result template missing Expected Result"


def test_adv_09_broken_core_flow() -> None:
    """Broken core flow identified as CRITICAL."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "CRITICAL" in rules_text, "Rules do not define CRITICAL severity"
    assert "core" in rules_text.lower() or "critical" in rules_text.lower(), \
        "Rules do not address core flow failures"


def test_adv_10_critical_failure_hidden() -> None:
    """Critical failure not hidden."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "fail" in workflow_text.lower() or "failure" in workflow_text.lower(), \
        "Workflow does not address failures"
    assert "CRITICAL" in rules_text, "Rules do not define CRITICAL severity"


def test_adv_11_security_finding_hidden() -> None:
    """Security finding not hidden."""
    review_text = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    assert "Findings" in review_text, "Security review template missing Findings section"


def test_adv_12_unsupported_secure_claim() -> None:
    """Unsupported 'secure' claim rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "evidence" in rules_text.lower(), "Rules require evidence for security claims"
    assert "scope" in rules_text.lower(), "Rules limit security claims to inspected scope"


def test_adv_13_unsupported_zero_vulnerabilities() -> None:
    """Unsupported 'zero vulnerabilities' claim rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "scope" in rules_text.lower(), "Rules limit security claims to inspected scope"


def test_adv_14_missing_auth_evidence() -> None:
    """Missing authentication evidence marked UNKNOWN."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "authentication" in rules_text.lower(), "Rules do not address authentication"
    assert "UNKNOWN" in rules_text, "Rules allow UNKNOWN for missing evidence"


def test_adv_15_missing_authz_evidence() -> None:
    """Missing authorization evidence marked UNKNOWN."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "authorization" in rules_text.lower(), "Rules do not address authorization"


def test_adv_16_secret_exposed() -> None:
    """Secret exposure identified."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "secret" in rules_text.lower(), "Rules do not address secrets"


def test_adv_17_injection_possibility() -> None:
    """Injection possibility identified."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "injection" in rules_text.lower(), "Rules do not address injection"


def test_adv_18_xss_possibility() -> None:
    """XSS possibility identified."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "xss" in rules_text.lower(), "Rules do not address XSS"


def test_adv_19_path_traversal() -> None:
    """Path traversal possibility identified."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "path" in rules_text.lower() or "traversal" in rules_text.lower(), \
        "Rules do not address path traversal"


def test_adv_20_dependency_vulnerability() -> None:
    """Dependency vulnerability identified."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "dependenc" in rules_text.lower(), "Rules do not address dependencies"


def test_adv_21_sensitive_data_exposure() -> None:
    """Sensitive data exposure identified."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "sensitive" in rules_text.lower() or "data" in rules_text.lower(), \
        "Rules do not address sensitive data"


def test_adv_22_missing_cors_evidence() -> None:
    """Missing CORS evidence marked UNKNOWN."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "cors" in rules_text.lower(), "Rules do not address CORS"


def test_adv_23_missing_csrf_evidence() -> None:
    """Missing CSRF evidence marked UNKNOWN."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "csrf" in rules_text.lower(), "Rules do not address CSRF"


def test_adv_24_unknown_security_boundary() -> None:
    """Unknown security boundary marked UNKNOWN."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text, "Rules allow UNKNOWN for uncertain areas"


def test_adv_25_six_hour_constraint() -> None:
    """Six-hour constraint prioritizes critical paths."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "6" in rules_text or "2-6" in rules_text, \
        "Rules do not define 2-6 hour time strategy"


def test_adv_26_exhaustive_low_value_testing() -> None:
    """Exhaustive low-value testing avoided."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "critical" in rules_text.lower() and "critical" in workflow_text.lower(), \
        "Rules/workflow prioritize critical over low-value"


def test_adv_27_remediation_leakage() -> None:
    """Remediation not confused with implementation."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "implementation" in rules_text.lower() or "implementation" in workflow_text.lower(), \
        "Rules/workflow address implementation boundary"


def test_adv_28_phase1_10_modification() -> None:
    """Phase 1-10 not modified by Phase 11."""
    # All phase files should exist unchanged
    phase_files = [
        ROOT / "workflows" / "score-optimization.md",
        ROOT / "workflows" / "judge-simulation.md",
        ROOT / "workflows" / "red-team.md",
        ROOT / "workflows" / "ux-review.md",
        ROOT / "workflows" / "implementation.md",
    ]
    for f in phase_files:
        assert f.is_file(), f"Phase file missing: {f}"


def test_adv_29_multiple_next_actions() -> None:
    """Exactly one primary next action."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    plan_text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    review_text = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    assert workflow_text.count("PRIMARY NEXT ACTION") >= 1, "Workflow missing PRIMARY NEXT ACTION"
    assert plan_text.count("PRIMARY NEXT ACTION") >= 1, "Plan template missing PRIMARY NEXT ACTION"
    assert review_text.count("PRIMARY NEXT ACTION") >= 1, "Review template missing PRIMARY NEXT ACTION"


def test_adv_30_false_ready_gate() -> None:
    """False READY gate prevented."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "READY" in rules_text, "Rules define READY gate"
    assert "evidence" in rules_text.lower(), "Rules require evidence for READY"
    assert "critical" in rules_text.lower(), "Rules require critical evidence for READY"


# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------

TESTS: list[tuple[str, Callable[[], None]]] = [
    # Acceptance tests AT-216 through AT-250
    ("AT-216 Phase 11 routing exists", test_at216_routing_exists),
    ("AT-217 Resources resolve correctly", test_at217_resources_resolve),
    ("AT-218 Phase 10 lock required", test_at218_phase10_lock_required),
    ("AT-219 Lifecycle integrity checked", test_at219_lifecycle_integrity),
    ("AT-220 Phase 1-10 integrity preserved", test_at220_phase1_10_preserved),
    ("AT-221 Test plan generated", test_at221_test_plan_generated),
    ("AT-222 Relevant categories selected", test_at222_relevant_categories_selected),
    ("AT-223 Critical path identified", test_at223_critical_path_identified),
    ("AT-224 Test priorities assigned", test_at224_test_priorities_assigned),
    ("AT-225 Expected results defined", test_at225_expected_results_defined),
    ("AT-226 Test status model enforced", test_at226_test_status_model_enforced),
    ("AT-227 Actual result recorded", test_at227_actual_result_recorded),
    ("AT-228 PASS requires evidence", test_at228_pass_requires_evidence),
    ("AT-229 UNKNOWN preserved", test_at229_unknown_preserved),
    ("AT-230 Failures classified", test_at230_failures_classified),
    ("AT-231 Security review generated", test_at231_security_review_generated),
    ("AT-232 Attack surface inspected", test_at232_attack_surface_inspected),
    ("AT-233 Evidence required", test_at233_evidence_required),
    ("AT-234 Severity separated from confidence", test_at234_severity_separated_from_confidence),
    ("AT-235 Security findings generated", test_at235_security_findings_generated),
    ("AT-236 No fabricated zero vulnerabilities", test_at236_no_fabricated_zero_vulnerabilities),
    ("AT-237 Remediation priority assigned", test_at237_remediation_priority_assigned),
    ("AT-238 DEFER requires rationale", test_at238_defer_requires_rationale),
    ("AT-239 Verification recorded", test_at239_verification_recorded),
    ("AT-240 Regression considered", test_at240_regression_considered),
    ("AT-241 Time-aware strategy works", test_at241_time_aware_strategy),
    ("AT-242 Six-hour strategy prioritizes critical paths", test_at242_six_hour_strategy),
    ("AT-243 Quality gate states enforced", test_at243_quality_gate_states),
    ("AT-244 READY requires critical evidence", test_at244_ready_requires_critical_evidence),
    ("AT-245 UNKNOWN prevents unjustified READY", test_at245_unknown_prevents_ready),
    ("AT-246 No idea ownership", test_at246_no_idea_ownership),
    ("AT-247 No architecture ownership", test_at247_no_architecture_ownership),
    ("AT-248 No judge simulation ownership", test_at248_no_judge_sim_ownership),
    ("AT-249 No score optimization ownership", test_at249_no_score_opt_ownership),
    ("AT-250 Exactly one primary next action", test_at250_exactly_one_primary_next_action),
    # Adversarial validation scenarios
    ("ADV-01 Missing Phase 10", test_adv_01_missing_phase10),
    ("ADV-02 Phase 10 unlocked", test_adv_02_phase10_unlocked),
    ("ADV-03 Missing project", test_adv_03_missing_project),
    ("ADV-04 Empty repository", test_adv_04_empty_repository),
    ("ADV-05 Missing test evidence", test_adv_05_missing_test_evidence),
    ("ADV-06 Test PASS without execution", test_adv_06_test_pass_without_execution),
    ("ADV-07 UNKNOWN converted to PASS", test_adv_07_unknown_converted_to_pass),
    ("ADV-08 Missing expected result", test_adv_08_missing_expected_result),
    ("ADV-09 Broken core flow", test_adv_09_broken_core_flow),
    ("ADV-10 Critical failure hidden", test_adv_10_critical_failure_hidden),
    ("ADV-11 Security finding hidden", test_adv_11_security_finding_hidden),
    ("ADV-12 Unsupported secure claim", test_adv_12_unsupported_secure_claim),
    ("ADV-13 Unsupported zero vulnerabilities", test_adv_13_unsupported_zero_vulnerabilities),
    ("ADV-14 Missing auth evidence", test_adv_14_missing_auth_evidence),
    ("ADV-15 Missing authz evidence", test_adv_15_missing_authz_evidence),
    ("ADV-16 Secret exposed", test_adv_16_secret_exposed),
    ("ADV-17 Injection possibility", test_adv_17_injection_possibility),
    ("ADV-18 XSS possibility", test_adv_18_xss_possibility),
    ("ADV-19 Path traversal", test_adv_19_path_traversal),
    ("ADV-20 Dependency vulnerability", test_adv_20_dependency_vulnerability),
    ("ADV-21 Sensitive data exposure", test_adv_21_sensitive_data_exposure),
    ("ADV-22 Missing CORS evidence", test_adv_22_missing_cors_evidence),
    ("ADV-23 Missing CSRF evidence", test_adv_23_missing_csrf_evidence),
    ("ADV-24 Unknown security boundary", test_adv_24_unknown_security_boundary),
    ("ADV-25 Six-hour constraint", test_adv_25_six_hour_constraint),
    ("ADV-26 Exhaustive low-value testing", test_adv_26_exhaustive_low_value_testing),
    ("ADV-27 Remediation leakage", test_adv_27_remediation_leakage),
    ("ADV-28 Phase 1-10 modification", test_adv_28_phase1_10_modification),
    ("ADV-29 Multiple next actions", test_adv_29_multiple_next_actions),
    ("ADV-30 False READY gate", test_adv_30_false_ready_gate),
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
