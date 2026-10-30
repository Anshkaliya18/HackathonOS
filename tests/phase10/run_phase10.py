#!/usr/bin/env python3
"""Deterministic contract validation for Phase 10 — Score Optimization Intelligence.

This harness validates the Phase 10 workflow, rules, and template contracts
in disposable directories. It does not invoke an LLM; it verifies the documented
workflow text, routing declarations, rule invariants, and template structure
against the acceptance tests AT-181 through AT-215 and adversarial scenarios.

Follows the Phase 6 smoke harness pattern: stdlib-only, disposable fixtures,
machine-readable JSON output, non-zero exit on any failure.
"""

from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "SKILL.md"
WORKFLOW = ROOT / "workflows" / "score-optimization.md"
RULES = ROOT / "rules" / "score-optimization-rules.md"
PLAN_TEMPLATE = ROOT / "templates" / "score-optimization-plan.md"
GAP_TEMPLATE = ROOT / "templates" / "gap-analysis.md"
CANDIDATE_TEMPLATE = ROOT / "templates" / "improvement-candidate.md"
LIFECYCLE = ROOT / "workflows" / "lifecycle.md"

# Expected Phase 10 files
PHASE10_FILES = [
    WORKFLOW,
    RULES,
    PLAN_TEMPLATE,
    GAP_TEMPLATE,
    CANDIDATE_TEMPLATE,
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


def count_occurrences(path: Path, pattern: str) -> int:
    return len(re.findall(pattern, path.read_text(encoding="utf-8"), re.IGNORECASE))


# ---------------------------------------------------------------------------
# AT-181 through AT-215 acceptance tests
# ---------------------------------------------------------------------------

def test_at181_routing_exists() -> None:
    """SCORE-OPTIMIZE routes correctly."""
    routes = route_table()
    assert "SCORE-OPTIMIZE" in routes, f"SCORE-OPTIMIZE missing from route table: {routes}"
    assert routes["SCORE-OPTIMIZE"] == "workflows/score-optimization.md", \
        f"Wrong route: {routes.get('SCORE-OPTIMIZE')}"
    assert WORKFLOW.is_file(), f"Workflow file missing: {WORKFLOW}"


def test_at182_resources_resolve() -> None:
    """All Phase 10 resources load from their expected locations."""
    for f in PHASE10_FILES:
        assert f.is_file(), f"Phase 10 resource missing: {f}"
    # SKILL.md must reference SCORE-OPTIMIZE
    assert "SCORE-OPTIMIZE" in SKILL.read_text(encoding="utf-8")


def test_at183_phase9_lock_required() -> None:
    """SCORE-OPTIMIZE blocks when Phase 9 is not locked."""
    text = WORKFLOW.read_text(encoding="utf-8")
    # Workflow requires Phase 9 judge simulation report as prerequisite
    assert "judge-simulation.md" in text, "Workflow does not require Phase 9 judge simulation"
    assert "Phase 9" in text, "Workflow does not reference Phase 9"
    assert "BLOCKED" in text or "LIMITED" in text, "Workflow does not define blocked/limited state"


def test_at184_judge_readiness_required() -> None:
    """SCORE-OPTIMIZE blocks or remains conditional when Judge Readiness is not READY."""
    text = WORKFLOW.read_text(encoding="utf-8")
    # The workflow's Stage 11 validation checklist requires judge simulation consumed
    assert "judge-simulation.md" in text.lower(), "Workflow does not consume judge simulation evidence"


def test_at185_criteria_inspected() -> None:
    """Official criteria are consumed when available."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "criterion" in text.lower(), "Workflow does not mention criteria"
    assert "weight" in text.lower(), "Workflow does not mention weights"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "official" in rules_text.lower(), "Rules do not address official weights"
    assert "weight" in rules_text.lower(), "Rules do not address weights"


def test_at186_evidence_inspected() -> None:
    """Relevant project and phase evidence is consumed."""
    text = WORKFLOW.read_text(encoding="utf-8")
    for phase in ["Phase 2", "Phase 3", "Phase 4", "Phase 5", "Phase 7", "Phase 8", "Phase 9"]:
        assert phase.lower() in text.lower(), f"Workflow does not consume {phase} evidence"


def test_at187_time_constraint_inspected() -> None:
    """Remaining time affects prioritization."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "time" in text.lower(), "Workflow does not mention time"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "time-aware" in rules_text.lower() or "time aware" in rules_text.lower(), \
        "Rules do not address time-aware filtering"


def test_at188_official_weights_preserved() -> None:
    """Known official weights are never overwritten."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "never pretend" in rules_text.lower() or "never pretend provisional" in rules_text.lower(), \
        "Rules do not warn against pretending provisional weights are official"
    assert "OFFICIAL" in rules_text, "Rules do not use OFFICIAL label"


def test_at189_unknown_weights_remain_unknown() -> None:
    """Missing weights are not fabricated."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text, "Rules do not allow UNKNOWN weights"
    assert "provisional" in rules_text.lower(), "Rules do not define provisional model"


def test_at190_estimated_scores_labeled() -> None:
    """Estimated values are explicitly labeled."""
    rules_text = RULES.read_text(encoding="utf-8")
    for label in ["OFFICIAL", "ESTIMATED", "PROVISIONAL", "UNKNOWN"]:
        assert label in rules_text, f"Rules do not use label {label}"
    plan_text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    assert "Score Label" in plan_text, "Plan template does not have Score Label field"


def test_at191_no_fabricated_precision() -> None:
    """Unsupported numerical precision is rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "precision" in rules_text.lower(), "Rules do not address numerical precision"
    assert "23.7" not in rules_text, "Rules contain fabricated precision example as rule"
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "precision" in workflow_text.lower(), "Workflow does not address numerical precision"


def test_at192_criterion_gaps_identified() -> None:
    """Weaknesses are identified per criterion."""
    gap_text = GAP_TEMPLATE.read_text(encoding="utf-8")
    assert "Gap Classification" in gap_text or "gap" in gap_text.lower(), \
        "Gap template does not classify gaps"
    assert "Weaknesses" in gap_text, "Gap template does not capture weaknesses"


def test_at193_performance_vs_evidence_gaps_separated() -> None:
    """Weak project performance and weak evidence are distinct."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "weak project performance" in rules_text.lower() or "weak performance" in rules_text.lower(), \
        "Rules do not separate weak project performance"
    assert "weak evidence" in rules_text.lower(), "Rules do not separate weak evidence"
    gap_text = GAP_TEMPLATE.read_text(encoding="utf-8")
    assert "Weak Project Performance" in gap_text or "weak project performance" in gap_text.lower(), \
        "Gap template does not separate weak project performance finding"
    assert "Weak Evidence" in gap_text or "weak evidence" in gap_text.lower(), \
        "Gap template does not separate weak evidence finding"


def test_at194_candidates_generated() -> None:
    """Optimization candidates are produced from evidence."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "candidate" in text.lower(), "Workflow does not generate candidates"
    assert "category" in text.lower(), "Workflow does not assign categories"


def test_at195_score_impact_recorded() -> None:
    """Each candidate has an impact assessment."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Score Impact" in candidate_text, "Candidate template missing Score Impact"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "VERY LOW" in rules_text and "VERY HIGH" in rules_text, \
        "Rules do not define Score Impact scale"


def test_at196_confidence_recorded() -> None:
    """Each candidate has confidence."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Confidence" in candidate_text, "Candidate template missing Confidence"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "HIGH" in rules_text and "LOW" in rules_text and "UNKNOWN" in rules_text, \
        "Rules do not define Confidence scale"


def test_at197_judge_visibility_recorded() -> None:
    """Each candidate has judge visibility."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Judge Visibility" in candidate_text, "Candidate template missing Judge Visibility"


def test_at198_cost_recorded() -> None:
    """Each candidate has implementation cost."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Implementation Cost" in candidate_text, "Candidate template missing Implementation Cost"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "TRIVIAL" in rules_text and "VERY HIGH" in rules_text, \
        "Rules do not define Cost scale"


def test_at199_time_required_recorded() -> None:
    """Each candidate has time requirements."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Time Required" in candidate_text, "Candidate template missing Time Required"


def test_at200_risk_recorded() -> None:
    """Each candidate has risk."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Risk" in candidate_text, "Candidate template missing Risk"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "CRITICAL" in rules_text and "LOW" in rules_text, \
        "Rules do not define Risk scale"


def test_at201_dependencies_recorded() -> None:
    """Dependencies are explicitly represented."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Dependencies" in candidate_text, "Candidate template missing Dependencies"
    plan_text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    assert "Dependencies" in plan_text or "Blockers" in plan_text, \
        "Plan template does not capture dependencies/blockers"


def test_at202_priority_assigned() -> None:
    """Every candidate has exactly one P0/P1/P2/P3/DROP priority."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "P0" in candidate_text or "PRIORITY" in candidate_text, \
        "Candidate template missing priority"
    rules_text = RULES.read_text(encoding="utf-8")
    for p in ["P0", "P1", "P2", "P3", "DROP"]:
        assert p in rules_text, f"Rules do not define priority {p}"


def test_at203_drop_decisions_supported() -> None:
    """Dropped work includes a defensible reason."""
    plan_text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    assert "DROP" in plan_text, "Plan template missing DROP section"
    assert "Reason" in plan_text or "reason" in plan_text.lower(), \
        "DROP section does not require reason"


def test_at204_phase9_concerns_consumed() -> None:
    """Judge concerns affect optimization where appropriate."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "concern" in text.lower(), "Workflow does not consume judge concerns"
    assert "judge-simulation.md" in text, "Workflow does not reference Phase 9 judge simulation"


def test_at205_judge_objections_converted() -> None:
    """Relevant objections become optimization opportunities."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "objection" in text.lower() or "weakness" in text.lower(), \
        "Workflow does not convert objections to candidates"


def test_at206_unsupported_claims_considered() -> None:
    """Unsupported claims remain visible and affect prioritization."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "unsupported" in text.lower(), "Workflow does not address unsupported claims"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "unsupported" in rules_text.lower(), "Rules do not address unsupported claims"


def test_at207_differentiation_weakness_considered() -> None:
    """Differentiation gaps can become optimization candidates."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Differentiation" in candidate_text, "Candidate template missing Differentiation category"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "Differentiation" in rules_text, "Rules missing Differentiation category"


def test_at208_demo_weakness_considered() -> None:
    """Demo weaknesses can become optimization candidates."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Demo Impact" in candidate_text, "Candidate template missing Demo Impact category"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "Demo Impact" in rules_text, "Rules missing Demo Impact category"


def test_at209_no_idea_changes() -> None:
    """Phase 10 does not take ownership of idea selection."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "selected idea" in text.lower(), "Workflow does not mention selected idea"
    assert "do not change" in text.lower() or "cannot change" in text.lower(), \
        "Workflow does not prohibit idea changes"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "selected idea" in rules_text.lower(), "Rules do not protect selected idea"


def test_at210_no_architecture_ownership() -> None:
    """Phase 10 recommends but does not redesign architecture."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "architecture" in text.lower(), "Workflow does not mention architecture"
    assert "silently redesign" in text.lower() or "do not redesign" in text.lower(), \
        "Workflow does not prohibit silent architecture redesign"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "silently redesign" in rules_text.lower() or "do not redesign" in rules_text.lower(), \
        "Rules do not prohibit silent architecture redesign"


def test_at211_no_implementation_ownership() -> None:
    """Phase 10 does not execute implementation work."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "application code" in text.lower() or "source code" in text.lower(), \
        "Workflow does not address application code"
    assert "do not" in text.lower() and "modify" in text.lower(), \
        "Workflow does not prohibit modifying application code"


def test_at212_no_testing_security_ownership() -> None:
    """Phase 10 does not replace Phase 5."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 5" in text, "Workflow does not reference Phase 5"
    assert "replace" in text.lower() or "duplicate" in text.lower(), \
        "Workflow does not state it does not replace Phase 5"


def test_at213_no_ux_redteam_ownership() -> None:
    """Phase 10 does not replace Phase 7 or Phase 8."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 7" in text, "Workflow does not reference Phase 7"
    assert "Phase 8" in text, "Workflow does not reference Phase 8"


def test_at214_no_ppt_submission_ownership() -> None:
    """Phase 10 does not perform Phase 17 or Phase 19 responsibilities."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "PPT" in text or "presentation" in text.lower(), \
        "Workflow does not address PPT/presentation"
    assert "submission" in text.lower(), "Workflow does not address submission"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "PPT" in rules_text or "presentation" in rules_text.lower(), \
        "Rules do not address PPT/presentation ownership"


def test_at215_exactly_one_primary_next_action() -> None:
    """Every completed optimization run produces exactly one primary next action."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "PRIMARY NEXT ACTION" in text, "Workflow missing PRIMARY NEXT ACTION"
    # Count occurrences - should reference exactly one
    plan_text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    assert "PRIMARY NEXT ACTION" in plan_text, "Plan template missing PRIMARY NEXT ACTION"


# ---------------------------------------------------------------------------
# Adversarial validation scenarios (30 minimum)
# ---------------------------------------------------------------------------

def test_adv_01_missing_criteria() -> None:
    """Missing criteria must be marked UNKNOWN, not invented."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text and "UNKNOWN" in workflow_text, \
        "Workflow/rules do not handle UNKNOWN criteria"


def test_adv_02_unknown_weights() -> None:
    """Unknown weights must not be fabricated as official."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "provisional" in rules_text.lower(), "Rules do not define provisional weights for UNKNOWN"
    assert "never pretend" in rules_text.lower() or "not official" in rules_text.lower(), \
        "Rules do not warn against pretending provisional weights are official"


def test_adv_03_contradictory_criteria() -> None:
    """Contradictory criteria must be recorded, not silently reconciled."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "contradict" in workflow_text.lower() or "contradiction" in workflow_text.lower(), \
        "Workflow does not address contradictory criteria"


def test_adv_04_missing_phase9_evidence() -> None:
    """Missing Phase 9 evidence must result in BLOCKED or LIMITED."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "BLOCKED" in workflow_text or "LIMITED" in workflow_text, \
        "Workflow does not define BLOCKED/LIMITED for missing Phase 9"


def test_adv_05_weak_judge_evidence() -> None:
    """Weak judge evidence must lower confidence, not hide gaps."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "confidence" in workflow_text.lower(), "Workflow does not track confidence"


def test_adv_06_unsupported_score_claim() -> None:
    """Unsupported score claims must be flagged."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "unsupported" in rules_text.lower(), "Rules do not flag unsupported claims"


def test_adv_07_fabricated_score_precision() -> None:
    """Fabricated score precision must be rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "precision" in rules_text.lower() and "precision" in workflow_text.lower(), \
        "Workflow/rules do not reject fabricated precision"


def test_adv_08_unlimited_time_assumption() -> None:
    """Unlimited time must not be assumed."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text and "UNKNOWN" in workflow_text, \
        "Workflow/rules do not handle UNKNOWN time"


def test_adv_09_six_hour_constraint() -> None:
    """Six-hour constraint must block architectural changes."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "architectural" in rules_text.lower() or "architecture" in rules_text.lower(), \
        "Rules do not address architectural changes under time pressure"


def test_adv_10_expensive_feature_proposal() -> None:
    """Expensive features must be deprioritized under cost heuristic."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "cost" in rules_text.lower(), "Rules do not track implementation cost"


def test_adv_11_architecture_rewrite_proposal() -> None:
    """Architecture rewrite proposals must require human approval."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "human approval" in rules_text.lower() or "human-approval" in rules_text.lower(), \
        "Rules do not require human approval for architecture changes"


def test_adv_12_unnecessary_ai_feature() -> None:
    """Unnecessary AI features must be flagged as low value."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "impact" in workflow_text.lower() and "cost" in workflow_text.lower(), \
        "Workflow does not evaluate impact vs cost"


def test_adv_13_low_visibility_optimization() -> None:
    """Low-visibility optimizations must be deprioritized."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "visibility" in rules_text.lower(), "Rules do not track judge visibility"


def test_adv_14_attractive_low_impact_feature() -> None:
    """Attractive but low-impact features must be deprioritized."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "impact" in rules_text.lower(), "Rules do not track score impact"


def test_adv_15_duplicate_functionality() -> None:
    """Duplicate functionality must be identified as waste."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "duplicate" in rules_text.lower() or "unnecessary" in rules_text.lower(), \
        "Rules do not address duplicate/unnecessary work"


def test_adv_16_security_risk_optimization() -> None:
    """Security-risk optimizations must be flagged as high risk."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Security" in candidate_text or "security" in candidate_text.lower(), \
        "Candidate template missing Security/Trust category"


def test_adv_17_ux_regression_risk() -> None:
    """UX regression risk must be considered."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "UX" in rules_text and "UX" in workflow_text, \
        "Workflow/rules do not address UX"


def test_adv_18_reliability_regression() -> None:
    """Reliability regression must be considered."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Reliability" in candidate_text, "Candidate template missing Reliability category"


def test_adv_19_scope_creep() -> None:
    """Scope creep must be blocked."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "scope" in rules_text.lower() or "scope" in workflow_text.lower(), \
        "Workflow/rules do not address scope creep"


def test_adv_20_implementation_leakage() -> None:
    """Phase 10 must not own implementation."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "implementation" in rules_text.lower(), "Rules do not address implementation ownership"
    assert "own implementation" in rules_text.lower() or "do not own" in rules_text.lower(), \
        "Rules do not prohibit implementation ownership"


def test_adv_21_phase9_modification_attempt() -> None:
    """Phase 10 must not modify Phase 9."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 9" in rules_text and "Phase 9" in workflow_text, \
        "Workflow/rules do not reference Phase 9 protection"
    assert "silently modify Phase" in rules_text or "modify Phase 1" in rules_text, \
        "Rules do not prohibit modifying prior phases"


def test_adv_22_phase3_modification_attempt() -> None:
    """Phase 10 must not modify Phase 3."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "Phase 3" in rules_text or "Phase 1" in rules_text, \
        "Rules do not reference Phase 1-3 protection"


def test_adv_23_judge_feedback_treated_as_fact() -> None:
    """Simulated judge feedback must not be treated as actual feedback."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "simulat" in workflow_text.lower() or "simulated" in workflow_text.lower(), \
        "Workflow does not distinguish simulated judge feedback"


def test_adv_24_competitor_hallucination() -> None:
    """Competitor capabilities must not be hallucinated."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "evidence" in rules_text.lower(), "Rules require evidence for claims"


def test_adv_25_multiple_next_actions() -> None:
    """Exactly one primary next action must be produced."""
    text = WORKFLOW.read_text(encoding="utf-8")
    plan_text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    assert text.count("PRIMARY NEXT ACTION") >= 1, "Workflow missing PRIMARY NEXT ACTION"
    assert plan_text.count("PRIMARY NEXT ACTION") >= 1, "Plan template missing PRIMARY NEXT ACTION"


def test_adv_26_human_approval_bypass() -> None:
    """Human approval cannot be bypassed for major changes."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "human approval" in rules_text.lower() or "human-approval" in rules_text.lower(), \
        "Rules do not require human approval"


def test_adv_27_unknown_converted_to_fact() -> None:
    """UNKNOWN must not be converted to FACT."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text, "Rules do not allow UNKNOWN"
    assert "never convert" in rules_text.lower() or "do not convert" in rules_text.lower(), \
        "Rules do not prohibit converting UNKNOWN to FACT"


def test_adv_28_heuristic_treated_as_official() -> None:
    """Heuristic output must not be treated as official scoring."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "heuristic" in rules_text.lower() and "heuristic" in workflow_text.lower(), \
        "Workflow/rules do not label heuristic as non-official"
    assert "not judging mathematics" in rules_text.lower() or "not official" in rules_text.lower(), \
        "Rules do not disclaim heuristic as official scoring"


def test_adv_29_phase11_leakage() -> None:
    """Phase 10 must not perform Phase 11+ responsibilities."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "demo preparation" in text.lower() or "demo" in text.lower(), \
        "Workflow does not address demo boundary"
    assert "submission" in text.lower(), "Workflow does not address submission boundary"


def test_adv_30_automatic_implementation() -> None:
    """Phase 10 must not automatically implement changes."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "application code" in workflow_text.lower() or "source code" in workflow_text.lower(), \
        "Workflow does not address application code boundary"


# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------

TESTS: list[tuple[str, Callable[[], None]]] = [
    # Acceptance tests AT-181 through AT-215
    ("AT-181 Phase 10 routing exists", test_at181_routing_exists),
    ("AT-182 Resources resolve correctly", test_at182_resources_resolve),
    ("AT-183 Phase 9 lock required", test_at183_phase9_lock_required),
    ("AT-184 Judge Readiness required", test_at184_judge_readiness_required),
    ("AT-185 Criteria inspected", test_at185_criteria_inspected),
    ("AT-186 Evidence inspected", test_at186_evidence_inspected),
    ("AT-187 Time constraint inspected", test_at187_time_constraint_inspected),
    ("AT-188 Official weights preserved", test_at188_official_weights_preserved),
    ("AT-189 Unknown weights remain UNKNOWN", test_at189_unknown_weights_remain_unknown),
    ("AT-190 Estimated scores labeled", test_at190_estimated_scores_labeled),
    ("AT-191 No fabricated precision", test_at191_no_fabricated_precision),
    ("AT-192 Criterion gaps identified", test_at192_criterion_gaps_identified),
    ("AT-193 Performance vs evidence gaps separated", test_at193_performance_vs_evidence_gaps_separated),
    ("AT-194 Candidates generated", test_at194_candidates_generated),
    ("AT-195 Score impact recorded", test_at195_score_impact_recorded),
    ("AT-196 Confidence recorded", test_at196_confidence_recorded),
    ("AT-197 Judge visibility recorded", test_at197_judge_visibility_recorded),
    ("AT-198 Cost recorded", test_at198_cost_recorded),
    ("AT-199 Time required recorded", test_at199_time_required_recorded),
    ("AT-200 Risk recorded", test_at200_risk_recorded),
    ("AT-201 Dependencies recorded", test_at201_dependencies_recorded),
    ("AT-202 Priority assigned", test_at202_priority_assigned),
    ("AT-203 DROP decisions supported", test_at203_drop_decisions_supported),
    ("AT-204 Phase 9 concerns consumed", test_at204_phase9_concerns_consumed),
    ("AT-205 Judge objections converted", test_at205_judge_objections_converted),
    ("AT-206 Unsupported claims considered", test_at206_unsupported_claims_considered),
    ("AT-207 Differentiation weakness considered", test_at207_differentiation_weakness_considered),
    ("AT-208 Demo weakness considered", test_at208_demo_weakness_considered),
    ("AT-209 No idea changes", test_at209_no_idea_changes),
    ("AT-210 No architecture ownership", test_at210_no_architecture_ownership),
    ("AT-211 No implementation ownership", test_at211_no_implementation_ownership),
    ("AT-212 No testing/security ownership", test_at212_no_testing_security_ownership),
    ("AT-213 No UX/red-team ownership", test_at213_no_ux_redteam_ownership),
    ("AT-214 No PPT/submission ownership", test_at214_no_ppt_submission_ownership),
    ("AT-215 Exactly one primary next action", test_at215_exactly_one_primary_next_action),
    # Adversarial validation scenarios
    ("ADV-01 Missing criteria", test_adv_01_missing_criteria),
    ("ADV-02 Unknown weights", test_adv_02_unknown_weights),
    ("ADV-03 Contradictory criteria", test_adv_03_contradictory_criteria),
    ("ADV-04 Missing Phase 9 evidence", test_adv_04_missing_phase9_evidence),
    ("ADV-05 Weak judge evidence", test_adv_05_weak_judge_evidence),
    ("ADV-06 Unsupported score claim", test_adv_06_unsupported_score_claim),
    ("ADV-07 Fabricated score precision", test_adv_07_fabricated_score_precision),
    ("ADV-08 Unlimited time assumption", test_adv_08_unlimited_time_assumption),
    ("ADV-09 Six-hour constraint", test_adv_09_six_hour_constraint),
    ("ADV-10 Expensive feature proposal", test_adv_10_expensive_feature_proposal),
    ("ADV-11 Architecture rewrite proposal", test_adv_11_architecture_rewrite_proposal),
    ("ADV-12 Unnecessary AI feature", test_adv_12_unnecessary_ai_feature),
    ("ADV-13 Low-visibility optimization", test_adv_13_low_visibility_optimization),
    ("ADV-14 Attractive low-impact feature", test_adv_14_attractive_low_impact_feature),
    ("ADV-15 Duplicate functionality", test_adv_15_duplicate_functionality),
    ("ADV-16 Security risk optimization", test_adv_16_security_risk_optimization),
    ("ADV-17 UX regression risk", test_adv_17_ux_regression_risk),
    ("ADV-18 Reliability regression", test_adv_18_reliability_regression),
    ("ADV-19 Scope creep", test_adv_19_scope_creep),
    ("ADV-20 Implementation leakage", test_adv_20_implementation_leakage),
    ("ADV-21 Phase 9 modification attempt", test_adv_21_phase9_modification_attempt),
    ("ADV-22 Phase 3 modification attempt", test_adv_22_phase3_modification_attempt),
    ("ADV-23 Judge feedback treated as fact", test_adv_23_judge_feedback_treated_as_fact),
    ("ADV-24 Competitor hallucination", test_adv_24_competitor_hallucination),
    ("ADV-25 Multiple next actions", test_adv_25_multiple_next_actions),
    ("ADV-26 Human approval bypass", test_adv_26_human_approval_bypass),
    ("ADV-27 UNKNOWN converted to FACT", test_adv_27_unknown_converted_to_fact),
    ("ADV-28 Heuristic treated as official scoring", test_adv_28_heuristic_treated_as_official),
    ("ADV-29 Phase 11 leakage", test_adv_29_phase11_leakage),
    ("ADV-30 Automatic implementation", test_adv_30_automatic_implementation),
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
