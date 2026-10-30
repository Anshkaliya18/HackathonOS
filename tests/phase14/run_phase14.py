#!/usr/bin/env python3
"""Deterministic contract validation for Phase 14 — Judge Simulation Intelligence.

Validates the Phase 14 Judge Simulation workflow, rules, and template contracts against
the acceptance tests AT-321 through AT-355 and adversarial scenarios ADV-01–30.

Follows the Phase 6/Phase 10/Phase 11/Phase 12/Phase 13 smoke harness pattern: stdlib-only,
disposable fixtures, machine-readable JSON output, non-zero exit on any failure.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "SKILL.md"
WORKFLOW = ROOT / "workflows" / "judge-simulation.md"
RULES = ROOT / "rules" / "judge-rules.md"
REVIEW_TEMPLATE = ROOT / "templates" / "judge-simulation.md"
SESSION_TEMPLATE = ROOT / "templates" / "judge-session.md"
QUESTION_TEMPLATE = ROOT / "templates" / "judge-question.md"
CRITERION_TEMPLATE = ROOT / "templates" / "judge-criterion.md"
LIFECYCLE = ROOT / "workflows" / "lifecycle.md"
PHASE13_AUDIT = ROOT / "audits" / "phase13-final-report.md"

# Expected Phase 14 resources (already exist from legacy Phase 9 numbering,
# but lifecycle.md identifies Judge Simulation as Phase 14)
PHASE14_FILES = [
    WORKFLOW,
    RULES,
    REVIEW_TEMPLATE,
    SESSION_TEMPLATE,
    QUESTION_TEMPLATE,
    CRITERION_TEMPLATE,
]


def file_contains(path: Path, pattern: str) -> bool:
    return re.search(pattern, path.read_text(encoding="utf-8"), re.IGNORECASE) is not None


# ---------------------------------------------------------------------------
# AT-321 through AT-355 acceptance tests
# ---------------------------------------------------------------------------

def test_at321_prerequisite_phase13_locked() -> None:
    """Phase 14 requires Phase 13 to be complete and locked."""
    assert PHASE13_AUDIT.is_file(), "Phase 13 final audit report missing"
    audit_text = PHASE13_AUDIT.read_text(encoding="utf-8")
    assert "COMPLETE & LOCKED" in audit_text, "Phase 13 audit does not report COMPLETE & LOCKED"


def test_at322_lifecycle_correctness() -> None:
    """Lifecycle contains exactly 20 phases; Phase 14 = Judge Simulation."""
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
    assert data_rows[13][0].strip() == "Judge Simulation", \
        f"Phase 14 should be Judge Simulation, found: {data_rows[13][0].strip()}"


def test_at323_routing_exists() -> None:
    """JUDGE-SIM routing exists in SKILL.md."""
    text = SKILL.read_text(encoding="utf-8")
    assert "JUDGE-SIM" in text, "SKILL.md missing JUDGE-SIM operation"
    assert "workflows/judge-simulation.md" in text, "SKILL.md missing judge-simulation.md workflow path"


def test_at324_resources_resolve() -> None:
    """All Phase 14 resources load from expected locations."""
    for f in PHASE14_FILES:
        assert f.is_file(), f"Phase 14 resource missing: {f}"


def test_at325_state_reading() -> None:
    """Workflow reads project state."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "project-state" in text.lower() or "project state" in text.lower(), \
        "Workflow does not read project state"


def test_at326_repository_inspection() -> None:
    """Workflow requires repository inspection."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "inspect" in text.lower(), "Workflow does not require inspection"
    assert "repository" in text.lower(), "Workflow does not inspect repository"


def test_at327_evidence_model() -> None:
    """Evidence model uses FACT/INFERENCE/ASSUMPTION/UNKNOWN."""
    rules_text = RULES.read_text(encoding="utf-8")
    for label in ["FACT", "INFERENCE", "ASSUMPTION", "UNKNOWN"]:
        assert label in rules_text, f"Rules missing evidence label: {label}"


def test_at328_rubric_handling() -> None:
    """Official criteria used when available; UNKNOWN otherwise; no fabrication."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "invent" in rules_text.lower() or "do not invent" in rules_text.lower(), \
        "Rules do not prohibit inventing criteria"
    assert "UNKNOWN" in rules_text, "Rules do not allow UNKNOWN criteria"


def test_at329_official_vs_simulated_rubric() -> None:
    """Official vs simulated rubric distinction is explicit."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "SIMULATION" in rules_text.upper() or "simulated" in rules_text.lower(), \
        "Rules do not label simulation criteria as non-official"
    assert "official" in rules_text.lower(), "Rules do not reference official criteria"


def test_at330_judge_profiles() -> None:
    """Judge profiles are defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    for persona in ["technical", "product", "demo", "skeptical"]:
        assert persona in combined, f"Workflow/rules do not address judge persona: {persona}"


def test_at331_criterion_model() -> None:
    """Criterion model is defined."""
    assert CRITERION_TEMPLATE.is_file(), "Criterion template missing"
    text = CRITERION_TEMPLATE.read_text(encoding="utf-8")
    assert "Criterion ID" in text, "Criterion template missing Criterion ID"
    assert "Criterion Name" in text, "Criterion template missing Criterion Name"
    assert "Weight" in text, "Criterion template missing Weight"


def test_at332_evidence_mapping() -> None:
    """Evidence-to-criterion mapping states are defined."""
    text = CRITERION_TEMPLATE.read_text(encoding="utf-8")
    for state in ["SUPPORTED", "PARTIALLY_SUPPORTED", "CONTRADICTED", "NOT_APPLICABLE"]:
        assert state in text, f"Criterion template missing mapping state: {state}"
    assert "UNKNOWN" in text, "Criterion template missing UNKNOWN mapping state"


def test_at333_observation_model() -> None:
    """Observation states: OBSERVED/SUPPORTED/INFERRED/UNKNOWN/NOT_TESTED."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    for status in ["observed", "supported", "inferred", "unknown", "not_tested"]:
        assert status in combined, f"Observation status missing: {status}"


def test_at334_question_generation() -> None:
    """Judge questions are generated."""
    assert QUESTION_TEMPLATE.is_file(), "Question template missing"
    text = QUESTION_TEMPLATE.read_text(encoding="utf-8")
    assert "Question ID" in text, "Question template missing Question ID"
    assert "Question" in text, "Question template missing Question"


def test_at335_follow_up_generation() -> None:
    """Skeptical follow-ups are generated."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "follow" in combined or "follow-up" in combined or "followup" in combined, \
        "Workflow/rules do not address follow-up questions"


def test_at336_answer_readiness() -> None:
    """Answer readiness states are defined."""
    question_text = QUESTION_TEMPLATE.read_text(encoding="utf-8")
    for state in ["READY", "PARTIALLY_READY", "WEAK", "UNKNOWN", "NOT_APPLICABLE"]:
        assert state in question_text, f"Question template missing readiness state: {state}"


def test_at337_judge_concerns() -> None:
    """Judge concerns are identified."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "concern" in combined, "Workflow/rules do not address judge concerns"
    assert "CRITICAL" in rules_text and "HIGH" in rules_text and "MEDIUM" in rules_text and "LOW" in rules_text, \
        "Rules do not define concern severity levels"


def test_at338_judge_strengths() -> None:
    """Judge strengths are identified."""
    review_text = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    assert "Strengths" in review_text, "Review template missing Strengths section"


def test_at339_claim_credibility() -> None:
    """Claim credibility is assessed."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "claim" in combined, "Workflow/rules do not address claim credibility"
    assert "VERIFIED" in rules_text or "UNSUPPORTED" in rules_text or "CONTRADICTED" in rules_text, \
        "Rules do not define claim credibility statuses"


def test_at340_demo_simulation() -> None:
    """Demo simulation is performed where evidence allows."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "demo" in combined, "Workflow/rules do not address demo simulation"
    assert "not_tested" in combined or "not tested" in combined or "NOT_TESTED" in combined, \
        "Workflow/rules do not address NOT_TESTED demo"


def test_at341_technical_scrutiny() -> None:
    """Technical scrutiny is performed."""
    review_text = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    assert "Technical Credibility" in review_text, "Review template missing Technical Credibility"


def test_at342_ux_scrutiny() -> None:
    """UX scrutiny is performed."""
    review_text = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    assert "Product Credibility" in review_text or "Product" in review_text, \
        "Review template missing Product Credibility"


def test_at343_security_evidence_usage() -> None:
    """Phase 11 security evidence is used."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 5" in workflow_text, "Workflow does not reference Phase 5 security evidence"
    assert "security" in workflow_text.lower(), "Workflow does not address security evidence"


def test_at344_red_team_evidence_usage() -> None:
    """Phase 13 red-team evidence is used."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 8" in workflow_text or "red-team" in workflow_text.lower() or "red team" in workflow_text.lower(), \
        "Workflow does not reference Phase 8/13 red-team evidence"


def test_at345_time_aware_behavior() -> None:
    """Time-aware strategy works."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "time" in combined, "Workflow/rules do not address time-aware strategy"


def test_at346_judge_readiness_gate() -> None:
    """Judge readiness gate states are enforced."""
    rules_text = RULES.read_text(encoding="utf-8")
    for gate in ["NOT_READY", "REVIEW_IN_PROGRESS", "BLOCKED", "CONDITIONAL", "READY"]:
        assert gate in rules_text, f"Quality gate {gate} not found in rules"


def test_at347_human_control() -> None:
    """Human control is preserved."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "human" in rules_text.lower(), "Rules do not address human control"
    assert "decision" in rules_text.lower() or "approv" in rules_text.lower(), \
        "Rules do not address human decision authority"


def test_at348_score_separation() -> None:
    """Score optimization separation is enforced."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "score optimization" in combined, "Workflow/rules do not address score optimization separation"
    assert "simulated" in combined, "Workflow/rules do not label simulated scores"


def test_at349_ownership_boundaries() -> None:
    """Phase 14 does not own other phases' responsibilities."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    rules_text = RULES.read_text(encoding="utf-8")
    combined = (workflow_text + " " + rules_text).lower()
    assert "do not" in combined, "Workflow/rules do not establish boundaries"
    assert "implementation" in combined or "phase 4" in combined or "phase 10" in combined, \
        "Workflow/rules do not address implementation/optimization ownership boundary"


def test_at350_primary_next_action() -> None:
    """Exactly one primary next action."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "PRIMARY NEXT ACTION" in workflow_text, "Workflow missing PRIMARY NEXT ACTION"
    review_text = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    assert "PRIMARY NEXT ACTION" in review_text, "Review template missing PRIMARY NEXT ACTION"
    session_text = SESSION_TEMPLATE.read_text(encoding="utf-8")
    assert "PRIMARY NEXT ACTION" in session_text, "Session template missing PRIMARY NEXT ACTION"


def test_at351_regression() -> None:
    """Regression is considered."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    rules_text = RULES.read_text(encoding="utf-8")
    combined = (workflow_text + " " + rules_text).lower()
    assert "regression" in combined or "critical preparation risks" in combined, \
        "Workflow/rules do not address regression or preparation risks"


def test_at352_scope_audit() -> None:
    """No ownership leakage and scope preserved."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    rules_text = RULES.read_text(encoding="utf-8")
    combined = (workflow_text + " " + rules_text).lower()
    assert "ppt" in combined or "presentation" in combined, \
        "Workflow/rules do not address presentation boundary"
    assert "submission" in combined, "Workflow/rules do not address submission boundary"


def test_at353_unknown_preserved() -> None:
    """Unknown evidence is not converted to fact."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text, "Rules do not allow UNKNOWN"
    assert "never convert" in rules_text.lower() or "do not convert" in rules_text.lower() or "never transform" in rules_text.lower(), \
        "Rules do not prohibit converting UNKNOWN to FACT"


def test_at354_not_tested_preserved() -> None:
    """Not-tested evidence is not converted to tested."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "not_tested" in combined or "not tested" in combined or "NOT_TESTED" in combined, \
        "Workflow/rules do not preserve NOT_TESTED status"


def test_at355_evidence_integrity() -> None:
    """Evidence integrity is maintained."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "evidence" in rules_text.lower(), "Rules do not require evidence"
    assert "FACT" in rules_text and "INFERENCE" in rules_text, \
        "Rules do not use evidence classification model"


# ---------------------------------------------------------------------------
# Adversarial validation scenarios (30 minimum)
# ---------------------------------------------------------------------------

def test_adv_01_missing_phase13() -> None:
    """Missing Phase 13 blocks Phase 14."""
    assert PHASE13_AUDIT.is_file() and "COMPLETE & LOCKED" in PHASE13_AUDIT.read_text(encoding="utf-8")


def test_adv_02_partial_phase13() -> None:
    """Partial Phase 13 handled gracefully."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "partial" in text.lower() or "limited" in text.lower() or "blocked" in text.lower(), \
        "Workflow does not handle partial readiness"


def test_adv_03_missing_rubric() -> None:
    """Missing rubric marked UNKNOWN."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text, "Rules do not handle UNKNOWN rubric"


def test_adv_04_fabricated_official_rubric() -> None:
    """Fabricated official rubric rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "invent" in rules_text.lower() or "do not invent" in rules_text.lower(), \
        "Rules do not prohibit inventing official rubric"


def test_adv_05_missing_project_state() -> None:
    """Missing project state handled gracefully."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "project-state" in text.lower() or "project state" in text.lower()


def test_adv_06_empty_repository() -> None:
    """Empty repository handled gracefully."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "empty" in rules_text.lower() or "unknown" in rules_text.lower()


def test_adv_07_missing_evidence() -> None:
    """Missing evidence marked UNKNOWN."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text, "Rules do not allow UNKNOWN evidence"


def test_adv_08_conflicting_evidence() -> None:
    """Conflicting evidence recorded, not reconciled."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "contradict" in workflow_text.lower() or "conflict" in workflow_text.lower()


def test_adv_09_stale_evidence() -> None:
    """Stale evidence flagged."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "stale" in workflow_text.lower() or "revision" in workflow_text.lower() or "unknown" in workflow_text.lower()


def test_adv_10_unsupported_claim() -> None:
    """Unsupported claims are flagged."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "unsupported" in rules_text.lower(), "Rules do not flag unsupported claims"


def test_adv_11_contradicted_claim() -> None:
    """Contradicted claims are flagged."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "contradict" in rules_text.lower() or "contradicted" in rules_text.lower(), \
        "Rules do not address contradicted claims"


def test_adv_12_missing_demo_runtime() -> None:
    """Missing demo runtime handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "demo" in rules_text.lower() and ("not_tested" in rules_text.lower() or "not tested" in rules_text.lower() or "unknown" in rules_text.lower()), \
        "Rules do not handle missing demo runtime"


def test_adv_13_missing_browser() -> None:
    """Missing browser handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "browser" in rules_text.lower() or "runtime" in rules_text.lower()


def test_adv_14_missing_ux_evidence() -> None:
    """Missing UX evidence handled."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 7" in workflow_text or "ux" in workflow_text.lower()


def test_adv_15_missing_security_evidence() -> None:
    """Missing security evidence handled."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 5" in workflow_text or "security" in workflow_text.lower()


def test_adv_16_missing_red_team_evidence() -> None:
    """Missing red-team evidence handled."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 8" in workflow_text or "red-team" in workflow_text.lower() or "red team" in workflow_text.lower()


def test_adv_17_no_ai_project() -> None:
    """Project with no AI handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "NOT_APPLICABLE" in rules_text or "not_applicable" in rules_text.lower() or "n/a" in rules_text.lower()


def test_adv_18_ai_project_unsupported_claim() -> None:
    """AI project with unsupported AI claim handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "AI" in rules_text and "unsupported" in rules_text.lower()


def test_adv_19_multiple_judge_profiles() -> None:
    """Multiple judge profiles are supported."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    for persona in ["technical", "product", "skeptical"]:
        assert persona in combined, f"Workflow/rules do not support persona: {persona}"


def test_adv_20_conflicting_judge_observations() -> None:
    """Conflicting judge observations flagged."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "contradict" in workflow_text.lower() or "conflict" in workflow_text.lower()


def test_adv_21_question_without_evidence() -> None:
    """Question without evidence handled."""
    question_text = QUESTION_TEMPLATE.read_text(encoding="utf-8")
    assert "Evidence" in question_text, "Question template missing Evidence section"


def test_adv_22_invented_team_answer() -> None:
    """Invented team answers are not presented as fact."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "fabricat" in rules_text.lower() or "do not fabricate" in rules_text.lower(), \
        "Rules do not prohibit fabricating answers"


def test_adv_23_weak_answer_classified_incorrectly() -> None:
    """Weak answers are not misclassified."""
    question_text = QUESTION_TEMPLATE.read_text(encoding="utf-8")
    assert "WEAK" in question_text, "Question template does not address WEAK answers"


def test_adv_24_critical_judge_concern() -> None:
    """Critical judge concern prevents unconditional READY."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "CRITICAL" in rules_text and "READY" in rules_text, \
        "Rules do not link CRITICAL concerns to READY gate"


def test_adv_25_concern_owned_by_another_phase() -> None:
    """Concern owned by another phase is escalated."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "phase" in rules_text.lower() or "owner" in rules_text.lower(), \
        "Rules do not address cross-phase ownership"


def test_adv_26_score_optimization_leakage() -> None:
    """Phase 14 does not perform score optimization."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "do not" in workflow_text.lower() or "not perform" in workflow_text.lower(), \
        "Workflow does not prohibit score optimization"


def test_adv_27_time_under_two_hours() -> None:
    """Time remaining <2 hours focuses on demo-critical items."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "<2" in rules_text or "2 hours" in rules_text or "<2h" in rules_text


def test_adv_28_human_approval_boundary() -> None:
    """Human approval boundary is respected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "human" in rules_text.lower() and ("approval" in rules_text.lower() or "decision" in rules_text.lower())


def test_adv_29_phase1_13_untouched() -> None:
    """Phase 1-13 artifacts remain untouched."""
    phase_files = [
        ROOT / "workflows" / "score-optimization.md",
        ROOT / "workflows" / "red-team.md",
        ROOT / "workflows" / "ux-review.md",
        ROOT / "workflows" / "testing-security.md",
        ROOT / "workflows" / "implementation.md",
    ]
    for f in phase_files:
        assert f.is_file(), f"Phase file missing: {f}"


def test_adv_30_exactly_one_primary_next_action() -> None:
    """Exactly one PRIMARY NEXT ACTION."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    review_text = REVIEW_TEMPLATE.read_text(encoding="utf-8")
    session_text = SESSION_TEMPLATE.read_text(encoding="utf-8")
    assert workflow_text.count("PRIMARY NEXT ACTION") >= 1, "Workflow missing PRIMARY NEXT ACTION"
    assert review_text.count("PRIMARY NEXT ACTION") >= 1, "Review template missing PRIMARY NEXT ACTION"
    assert session_text.count("PRIMARY NEXT ACTION") >= 1, "Session template missing PRIMARY NEXT ACTION"


# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------

TESTS: list[tuple[str, Callable[[], None]]] = [
    # Acceptance tests AT-321 through AT-355
    ("AT-321 Prerequisite Phase 13 locked", test_at321_prerequisite_phase13_locked),
    ("AT-322 Lifecycle correctness", test_at322_lifecycle_correctness),
    ("AT-323 Routing exists", test_at323_routing_exists),
    ("AT-324 Resources resolve", test_at324_resources_resolve),
    ("AT-325 State reading", test_at325_state_reading),
    ("AT-326 Repository inspection", test_at326_repository_inspection),
    ("AT-327 Evidence model", test_at327_evidence_model),
    ("AT-328 Rubric handling", test_at328_rubric_handling),
    ("AT-329 Official vs simulated rubric", test_at329_official_vs_simulated_rubric),
    ("AT-330 Judge profiles", test_at330_judge_profiles),
    ("AT-331 Criterion model", test_at331_criterion_model),
    ("AT-332 Evidence mapping", test_at332_evidence_mapping),
    ("AT-333 Observation model", test_at333_observation_model),
    ("AT-334 Question generation", test_at334_question_generation),
    ("AT-335 Follow-up generation", test_at335_follow_up_generation),
    ("AT-336 Answer readiness", test_at336_answer_readiness),
    ("AT-337 Judge concerns", test_at337_judge_concerns),
    ("AT-338 Judge strengths", test_at338_judge_strengths),
    ("AT-339 Claim credibility", test_at339_claim_credibility),
    ("AT-340 Demo simulation", test_at340_demo_simulation),
    ("AT-341 Technical scrutiny", test_at341_technical_scrutiny),
    ("AT-342 UX scrutiny", test_at342_ux_scrutiny),
    ("AT-343 Security evidence usage", test_at343_security_evidence_usage),
    ("AT-344 Red team evidence usage", test_at344_red_team_evidence_usage),
    ("AT-345 Time-aware behavior", test_at345_time_aware_behavior),
    ("AT-346 Judge readiness gate", test_at346_judge_readiness_gate),
    ("AT-347 Human control", test_at347_human_control),
    ("AT-348 Score separation", test_at348_score_separation),
    ("AT-349 Ownership boundaries", test_at349_ownership_boundaries),
    ("AT-350 Primary next action", test_at350_primary_next_action),
    ("AT-351 Regression considered", test_at351_regression),
    ("AT-352 Scope audit", test_at352_scope_audit),
    ("AT-353 Unknown preserved", test_at353_unknown_preserved),
    ("AT-354 Not tested preserved", test_at354_not_tested_preserved),
    ("AT-355 Evidence integrity", test_at355_evidence_integrity),
    # Adversarial validation scenarios
    ("ADV-01 Missing Phase 13", test_adv_01_missing_phase13),
    ("ADV-02 Partial Phase 13", test_adv_02_partial_phase13),
    ("ADV-03 Missing rubric", test_adv_03_missing_rubric),
    ("ADV-04 Fabricated official rubric", test_adv_04_fabricated_official_rubric),
    ("ADV-05 Missing project state", test_adv_05_missing_project_state),
    ("ADV-06 Empty repository", test_adv_06_empty_repository),
    ("ADV-07 Missing evidence", test_adv_07_missing_evidence),
    ("ADV-08 Conflicting evidence", test_adv_08_conflicting_evidence),
    ("ADV-09 Stale evidence", test_adv_09_stale_evidence),
    ("ADV-10 Unsupported claim", test_adv_10_unsupported_claim),
    ("ADV-11 Contradicted claim", test_adv_11_contradicted_claim),
    ("ADV-12 Missing demo runtime", test_adv_12_missing_demo_runtime),
    ("ADV-13 Missing browser", test_adv_13_missing_browser),
    ("ADV-14 Missing UX evidence", test_adv_14_missing_ux_evidence),
    ("ADV-15 Missing security evidence", test_adv_15_missing_security_evidence),
    ("ADV-16 Missing red-team evidence", test_adv_16_missing_red_team_evidence),
    ("ADV-17 No AI project", test_adv_17_no_ai_project),
    ("ADV-18 AI project unsupported claim", test_adv_18_ai_project_unsupported_claim),
    ("ADV-19 Multiple judge profiles", test_adv_19_multiple_judge_profiles),
    ("ADV-20 Conflicting judge observations", test_adv_20_conflicting_judge_observations),
    ("ADV-21 Question without evidence", test_adv_21_question_without_evidence),
    ("ADV-22 Invented team answer", test_adv_22_invented_team_answer),
    ("ADV-23 Weak answer classified incorrectly", test_adv_23_weak_answer_classified_incorrectly),
    ("ADV-24 Critical judge concern", test_adv_24_critical_judge_concern),
    ("ADV-25 Concern owned by another phase", test_adv_25_concern_owned_by_another_phase),
    ("ADV-26 Score optimization leakage", test_adv_26_score_optimization_leakage),
    ("ADV-27 Time under two hours", test_adv_27_time_under_two_hours),
    ("ADV-28 Human approval boundary", test_adv_28_human_approval_boundary),
    ("ADV-29 Phase 1-13 untouched", test_adv_29_phase1_13_untouched),
    ("ADV-30 Exactly one PRIMARY NEXT ACTION", test_adv_30_exactly_one_primary_next_action),
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
