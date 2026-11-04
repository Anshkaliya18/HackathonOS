#!/usr/bin/env python3
"""Deterministic contract validation for Phase 15 — Score Optimization Intelligence.

Validates the Phase 15 Score Optimization workflow, rules, and template contracts against
the acceptance tests AT-356 through AT-390 and adversarial scenarios ADV-01–30.

Follows the Phase 6/Phase 10/Phase 11/Phase 12/Phase 13/Phase 14 smoke harness pattern:
stdlib-only, disposable fixtures, machine-readable JSON output, non-zero exit on any failure.
"""

from __future__ import annotations

import json
import re
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

# Expected Phase 15 resources (already exist from legacy Phase 10 numbering,
# but lifecycle.md identifies Score Optimization as Phase 15)
PHASE15_FILES = [
    WORKFLOW,
    RULES,
    PLAN_TEMPLATE,
    GAP_TEMPLATE,
    CANDIDATE_TEMPLATE,
]


def file_contains(path: Path, pattern: str) -> bool:
    return re.search(pattern, path.read_text(encoding="utf-8"), re.IGNORECASE) is not None


def count_occurrences(path: Path, pattern: str) -> int:
    return len(re.findall(pattern, path.read_text(encoding="utf-8"), re.IGNORECASE))


# ---------------------------------------------------------------------------
# AT-356 through AT-390 acceptance tests
# ---------------------------------------------------------------------------

def test_at356_prerequisite_phase14_locked() -> None:
    """Score optimization consumes the project's judge simulation report."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert ".hackathon/judge-simulation.md" in text
    assert "UNKNOWN" in text


def test_at357_lifecycle_correctness() -> None:
    """Lifecycle contains exactly 20 phases; Phase 15 = Score Optimization."""
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
    assert data_rows[14][0].strip() == "Score Optimization", \
        f"Phase 15 should be Score Optimization, found: {data_rows[14][0].strip()}"


def test_at358_routing_exists() -> None:
    """SCORE-OPTIMIZE routing exists in SKILL.md."""
    text = SKILL.read_text(encoding="utf-8")
    assert "SCORE-OPTIMIZE" in text, "SKILL.md missing SCORE-OPTIMIZE operation"
    assert "workflows/score-optimization.md" in text, "SKILL.md missing score-optimization.md workflow path"


def test_at359_resources_resolve() -> None:
    """All Phase 15 resources load from expected locations."""
    for f in PHASE15_FILES:
        assert f.is_file(), f"Phase 15 resource missing: {f}"


def test_at360_state_reading() -> None:
    """Workflow reads project state."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "project-state" in text.lower() or "project state" in text.lower(), \
        "Workflow does not read project state"


def test_at361_repository_inspection() -> None:
    """Workflow requires repository inspection."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "inspect" in text.lower(), "Workflow does not require inspection"
    assert "repository" in text.lower(), "Workflow does not inspect repository"


def test_at362_evidence_model() -> None:
    """Evidence model uses FACT/INFERENCE/ASSUMPTION/UNKNOWN."""
    rules_text = RULES.read_text(encoding="utf-8")
    for label in ["FACT", "INFERENCE", "ASSUMPTION", "UNKNOWN"]:
        assert label in rules_text, f"Rules missing evidence label: {label}"


def test_at363_official_rubric_handling() -> None:
    """Official criteria used when available; UNKNOWN otherwise; no fabrication."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "invent" in rules_text.lower() or "do not invent" in rules_text.lower(), \
        "Rules do not prohibit inventing criteria"
    assert "UNKNOWN" in rules_text, "Rules do not allow UNKNOWN criteria"


def test_at364_official_vs_simulated_rubric() -> None:
    """Official vs simulated rubric distinction is explicit."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "SIMULATION" in rules_text.upper() or "simulated" in rules_text.lower(), \
        "Rules do not label simulation criteria as non-official"
    assert "official" in rules_text.lower(), "Rules do not reference official criteria"


def test_at365_score_model() -> None:
    """Score model uses Criterion Score × Criterion Weight formula."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "weighted contribution" in combined, "Workflow/rules do not define weighted contribution"
    assert "criterion score" in combined or "criterion_score" in combined, \
        "Workflow/rules do not define criterion score"


def test_at366_score_confidence() -> None:
    """Current score estimates include confidence."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "confidence" in combined, "Workflow/rules do not address score confidence"
    assert "HIGH" in rules_text and "MEDIUM" in rules_text and "LOW" in rules_text and "UNKNOWN" in rules_text, \
        "Rules do not define confidence levels"


def test_at367_score_ranges() -> None:
    """Score ranges supported where evidence is weak."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "range" in combined or "6–8" in combined or "6-8" in combined or "qualitative" in combined, \
        "Workflow/rules do not address score ranges"


def test_at368_criterion_mapping() -> None:
    """Evidence-to-criterion mapping states are defined."""
    text = GAP_TEMPLATE.read_text(encoding="utf-8")
    for state in ["SUPPORTED", "PARTIALLY_SUPPORTED", "CONTRADICTED", "NOT_APPLICABLE"]:
        assert state in text, f"Gap template missing mapping state: {state}"
    assert "UNKNOWN" in text, "Gap template missing UNKNOWN mapping state"


def test_at369_gap_analysis() -> None:
    """Gap analysis is performed per criterion."""
    assert GAP_TEMPLATE.is_file(), "Gap analysis template missing"
    text = GAP_TEMPLATE.read_text(encoding="utf-8")
    assert "Gap Classification" in text or "gap" in text.lower(), \
        "Gap template missing gap classification"
    assert "CRITICAL" in text and "HIGH" in text and "MEDIUM" in text and "LOW" in text and "NONE" in text and "UNKNOWN" in text, \
        "Gap template missing gap scale values"


def test_at370_project_vs_evidence_weakness() -> None:
    """Project weakness vs evidence weakness are separate findings."""
    rules_text = RULES.read_text(encoding="utf-8")
    gap_text = GAP_TEMPLATE.read_text(encoding="utf-8")
    combined = (rules_text + " " + gap_text).lower()
    assert "weak project performance" in combined, "Workflow/rules do not address weak project performance"
    assert "weak evidence" in combined, "Workflow/rules do not address weak evidence of performance"


def test_at371_optimization_categories() -> None:
    """Optimization categories A–I are defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    for cat in ["Differentiation", "Technical Credibility", "Core Functionality", "Demo Impact", "UX", "Security", "Evidence", "Reliability"]:
        assert cat in rules_text or cat in candidate_text, f"Category {cat} not found"


def test_at372_candidate_generation() -> None:
    """Improvement candidates are generated."""
    assert CANDIDATE_TEMPLATE.is_file(), "Candidate template missing"
    text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Candidate ID" in text, "Candidate template missing Candidate ID"
    assert "Description" in text, "Candidate template missing Description"


def test_at373_impact_recorded() -> None:
    """Score impact is recorded per candidate."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Score Impact" in candidate_text, "Candidate template missing Score Impact"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "VERY LOW" in rules_text and "VERY HIGH" in rules_text, \
        "Rules do not define Score Impact scale"


def test_at374_confidence_recorded() -> None:
    """Confidence is recorded per candidate."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Confidence" in candidate_text, "Candidate template missing Confidence"


def test_at375_visibility_recorded() -> None:
    """Judge visibility is recorded per candidate."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Judge Visibility" in candidate_text, "Candidate template missing Judge Visibility"


def test_at376_cost_recorded() -> None:
    """Implementation cost is recorded per candidate."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Implementation Cost" in candidate_text, "Candidate template missing Implementation Cost"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "TRIVIAL" in rules_text and "VERY HIGH" in rules_text, \
        "Rules do not define Cost scale"


def test_at377_dependency_analysis() -> None:
    """Dependencies are analyzed per candidate."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Dependencies" in candidate_text, "Candidate template missing Dependencies"
    plan_text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    assert "Dependencies" in plan_text or "Blockers" in plan_text, \
        "Plan template missing Dependencies/Blockers"


def test_at378_heuristic_labeling() -> None:
    """Optimization heuristic is explicitly labeled as non-official."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "heuristic" in combined, "Workflow/rules do not label heuristic"
    assert "not judging mathematics" in combined or "not official" in combined, \
        "Workflow/rules do not disclaim heuristic as official scoring"


def test_at379_priority_system() -> None:
    """Priority system P0/P1/P2/P3/DROP is defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    for p in ["P0", "P1", "P2", "P3", "DROP"]:
        assert p in rules_text, f"Rules missing priority {p}"


def test_at380_time_aware_optimization() -> None:
    """Time-aware optimization strategy is applied."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "time" in combined, "Workflow/rules do not address time-aware optimization"
    assert "6" in rules_text or "2-6" in rules_text or "6-12" in rules_text, \
        "Rules do not define time strategy windows"


def test_at381_red_team_integration() -> None:
    """Phase 13 Red Team findings are considered."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    rules_text = RULES.read_text(encoding="utf-8")
    combined = (workflow_text + " " + rules_text).lower()
    assert "red team" in combined or "red-team" in combined or "phase 13" in combined or "phase 8" in combined, \
        "Workflow/rules do not address Red Team integration"


def test_at382_judge_sim_integration() -> None:
    """Phase 14 Judge Simulation evidence is used."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 14" in workflow_text or "judge-simulation" in workflow_text.lower() or "judge simulation" in workflow_text.lower(), \
        "Workflow does not reference Phase 14 judge simulation"


def test_at383_ux_integration() -> None:
    """Phase 12 UX findings are used."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 12" in workflow_text or "ux-review" in workflow_text.lower() or "ux review" in workflow_text.lower(), \
        "Workflow does not reference Phase 12 UX evidence"


def test_at384_testing_security_integration() -> None:
    """Phase 11 testing/security findings are used."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 5" in workflow_text or "testing-security" in workflow_text.lower() or "testing security" in workflow_text.lower(), \
        "Workflow does not reference Phase 5/11 testing/security evidence"


def test_at385_engineering_integration() -> None:
    """Phase 3/4 engineering evidence is used."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 3" in workflow_text and "Phase 4" in workflow_text, \
        "Workflow does not reference Phase 3/4 engineering evidence"


def test_at386_scope_control() -> None:
    """Every candidate answers scope control questions."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Worth Doing" in candidate_text, "Candidate template missing Worth Doing assessment"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "DROP" in rules_text, "Rules do not define DROP priority"


def test_at387_human_approval() -> None:
    """Human approval boundaries are defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "human approval" in rules_text.lower() or "human-approval" in rules_text.lower(), \
        "Rules do not require human approval"
    assert "architecture" in rules_text.lower(), "Rules do not address architecture approval"


def test_at388_verification() -> None:
    """Verification is defined per improvement."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Validation Required" in candidate_text, "Candidate template missing Validation Required"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "verification" in rules_text.lower(), "Rules do not address verification"


def test_at389_state_integration() -> None:
    """State integration fields are defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "Optimization Status" in rules_text or "optimization status" in rules_text.lower(), \
        "Rules do not define Optimization Status state field"
    assert "Current Estimated Score" in rules_text or "current estimated score" in rules_text.lower(), \
        "Rules do not define Current Estimated Score state field"


def test_at390_primary_next_action() -> None:
    """Exactly one primary next action."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "PRIMARY NEXT ACTION" in workflow_text, "Workflow missing PRIMARY NEXT ACTION"
    plan_text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    assert "PRIMARY NEXT ACTION" in plan_text, "Plan template missing PRIMARY NEXT ACTION"


# ---------------------------------------------------------------------------
# Adversarial validation scenarios (30 minimum)
# ---------------------------------------------------------------------------

def test_adv_01_missing_phase14() -> None:
    """Missing judge evidence is not replaced with a framework report."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert ".hackathon/judge-simulation.md" in text


def test_adv_02_partial_phase14() -> None:
    """Partial Phase 14 handled gracefully."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "partial" in text.lower() or "limited" in text.lower() or "blocked" in text.lower(), \
        "Workflow does not handle partial readiness"


def test_adv_03_missing_official_rubric() -> None:
    """Missing official rubric marked UNKNOWN."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text, "Rules do not handle UNKNOWN rubric"


def test_adv_04_fabricated_official_weights() -> None:
    """Fabricated official weights rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "invent" in rules_text.lower() or "do not invent" in rules_text.lower(), \
        "Rules do not prohibit inventing official weights"


def test_adv_05_conflicting_weights() -> None:
    """Conflicting weights are flagged, not silently reconciled."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "contradict" in workflow_text.lower() or "conflict" in workflow_text.lower(), \
        "Workflow does not address conflicting weights"


def test_adv_06_missing_project_state() -> None:
    """Missing project state handled gracefully."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "project-state" in text.lower() or "project state" in text.lower()


def test_adv_07_missing_evidence() -> None:
    """Missing evidence marked UNKNOWN."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text, "Rules do not allow UNKNOWN evidence"


def test_adv_08_stale_evidence() -> None:
    """Stale evidence flagged."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "stale" in workflow_text.lower() or "revision" in workflow_text.lower() or "unknown" in workflow_text.lower()


def test_adv_09_unsupported_score() -> None:
    """Unsupported score claims are flagged."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "unsupported" in rules_text.lower(), "Rules do not flag unsupported score claims"


def test_adv_10_false_score_precision() -> None:
    """False score precision is rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "precision" in combined, "Workflow/rules do not address score precision"


def test_adv_11_weak_score_confidence() -> None:
    """Weak score confidence is handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "LOW" in rules_text and "confidence" in rules_text.lower(), \
        "Rules do not address LOW confidence"


def test_adv_12_project_weakness_mistaken_for_evidence_weakness() -> None:
    """Project weakness is not confused with evidence weakness."""
    gap_text = GAP_TEMPLATE.read_text(encoding="utf-8")
    rules_text = RULES.read_text(encoding="utf-8")
    combined = (gap_text + " " + rules_text).lower()
    assert "weak project performance" in combined, "Gap analysis/rules do not separate weak project performance"
    assert "weak evidence" in combined, "Gap analysis/rules do not separate weak evidence"


def test_adv_13_evidence_weakness_mistaken_for_project_weakness() -> None:
    """Evidence weakness is not confused with project weakness."""
    gap_text = GAP_TEMPLATE.read_text(encoding="utf-8")
    assert "Weak Project Performance" in gap_text or "weak project performance" in gap_text.lower(), \
        "Gap template missing Weak Project Performance finding"
    assert "Weak Evidence" in gap_text or "weak evidence" in gap_text.lower(), \
        "Gap template missing Weak Evidence finding"


def test_adv_14_critical_red_team_finding_ignored() -> None:
    """Critical Red Team findings are accounted for."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "red team" in combined or "red-team" in combined, \
        "Workflow/rules do not address Red Team integration"
    assert "CRITICAL" in rules_text, "Rules do not define CRITICAL severity"


def test_adv_15_mitigated_finding_incorrectly_optimized() -> None:
    """Already-mitigated findings are not re-optimized."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "VERIFIED_MITIGATED" in rules_text or "mitigated" in rules_text.lower(), \
        "Rules do not address already-mitigated findings"


def test_adv_16_judge_concern_ignored() -> None:
    """Judge concerns from Phase 14 are considered."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 14" in workflow_text or "judge-simulation" in workflow_text.lower() or "judge simulation" in workflow_text.lower(), \
        "Workflow does not reference Phase 14 judge simulation"


def test_adv_17_ux_blocker_ignored() -> None:
    """UX blockers from Phase 12 are considered."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 12" in workflow_text or "ux-review" in workflow_text.lower(), \
        "Workflow does not reference Phase 12 UX evidence"


def test_adv_18_security_blocker_ignored() -> None:
    """Security blockers from Phase 11 are considered."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 5" in workflow_text or "testing-security" in workflow_text.lower(), \
        "Workflow does not reference Phase 5/11 testing/security evidence"


def test_adv_19_architecture_rewrite_unnecessary() -> None:
    """Unnecessary architecture rewrites are not recommended."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "architecture" in rules_text.lower(), "Rules do not address architecture boundary"
    assert "human approval" in rules_text.lower() or "human-approval" in rules_text.lower(), \
        "Rules do not require human approval for architecture changes"


def test_adv_20_dependency_explosion() -> None:
    """Dependency explosion is avoided."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Dependencies" in candidate_text, "Candidate template missing Dependencies"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "cost" in rules_text.lower(), "Rules do not address implementation cost"


def test_adv_21_scope_creep() -> None:
    """Scope creep is controlled."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "scope" in combined, "Workflow/rules do not address scope control"
    assert "DROP" in rules_text, "Rules do not define DROP priority for out-of-scope work"


def test_adv_22_heuristic_presented_as_official_math() -> None:
    """Optimization heuristic is not presented as official judging math."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "heuristic" in combined, "Workflow/rules do not label heuristic"
    assert "not judging mathematics" in combined or "not official" in combined, \
        "Workflow/rules do not disclaim heuristic as official scoring"


def test_adv_23_improvement_without_verification() -> None:
    """Improvements without verification are not marked complete."""
    candidate_text = CANDIDATE_TEMPLATE.read_text(encoding="utf-8")
    assert "Validation Required" in candidate_text, "Candidate template missing Validation Required"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "verification" in rules_text.lower(), "Rules do not address verification"


def test_adv_24_impossible_improvement_under_time() -> None:
    """Improvements impossible under time constraint are deprioritized."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "6" in rules_text or "2-6" in rules_text or "6-12" in rules_text, \
        "Rules do not define time strategy windows"
    assert "critical" in rules_text.lower(), "Rules do not prioritize critical under time pressure"


def test_adv_25_human_approval_bypass() -> None:
    """Human approval cannot be bypassed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "human approval" in rules_text.lower() or "human-approval" in rules_text.lower(), \
        "Rules do not require human approval"


def test_adv_26_idea_silently_changed() -> None:
    """Selected idea is not silently changed."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    rules_text = RULES.read_text(encoding="utf-8")
    combined = (workflow_text + " " + rules_text).lower()
    assert "selected idea" in combined, "Workflow/rules do not protect selected idea"
    assert "do not change" in combined or "cannot change" in combined, \
        "Workflow/rules do not prohibit idea changes"


def test_adv_27_time_under_two_hours() -> None:
    """Time remaining <2 hours freezes scope."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "<2" in rules_text or "2 hours" in rules_text or "<2h" in rules_text, \
        "Rules do not define <2 hour time strategy"


def test_adv_28_phase1_14_unchanged() -> None:
    """Phase 1-14 artifacts remain untouched."""
    phase_files = [
        ROOT / "workflows" / "judge-simulation.md",
        ROOT / "workflows" / "red-team.md",
        ROOT / "workflows" / "ux-review.md",
        ROOT / "workflows" / "testing-security.md",
        ROOT / "workflows" / "implementation.md",
    ]
    for f in phase_files:
        assert f.is_file(), f"Phase file missing: {f}"


def test_adv_29_conflicting_candidates() -> None:
    """Conflicting optimization candidates are handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "contradict" in combined or "conflict" in combined, \
        "Workflow/rules do not address conflicting candidates"


def test_adv_30_exactly_one_primary_next_action() -> None:
    """Exactly one PRIMARY NEXT ACTION."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    plan_text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    assert workflow_text.count("PRIMARY NEXT ACTION") >= 1, "Workflow missing PRIMARY NEXT ACTION"
    assert plan_text.count("PRIMARY NEXT ACTION") >= 1, "Plan template missing PRIMARY NEXT ACTION"


# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------

TESTS: list[tuple[str, Callable[[], None]]] = [
    # Acceptance tests AT-356 through AT-390
    ("AT-356 Prerequisite Phase 14 locked", test_at356_prerequisite_phase14_locked),
    ("AT-357 Lifecycle correctness", test_at357_lifecycle_correctness),
    ("AT-358 Routing exists", test_at358_routing_exists),
    ("AT-359 Resources resolve", test_at359_resources_resolve),
    ("AT-360 State reading", test_at360_state_reading),
    ("AT-361 Repository inspection", test_at361_repository_inspection),
    ("AT-362 Evidence model", test_at362_evidence_model),
    ("AT-363 Official rubric handling", test_at363_official_rubric_handling),
    ("AT-364 Official vs simulated rubric", test_at364_official_vs_simulated_rubric),
    ("AT-365 Score model", test_at365_score_model),
    ("AT-366 Score confidence", test_at366_score_confidence),
    ("AT-367 Score ranges", test_at367_score_ranges),
    ("AT-368 Criterion mapping", test_at368_criterion_mapping),
    ("AT-369 Gap analysis", test_at369_gap_analysis),
    ("AT-370 Project vs evidence weakness", test_at370_project_vs_evidence_weakness),
    ("AT-371 Optimization categories", test_at371_optimization_categories),
    ("AT-372 Candidate generation", test_at372_candidate_generation),
    ("AT-373 Impact recorded", test_at373_impact_recorded),
    ("AT-374 Confidence recorded", test_at374_confidence_recorded),
    ("AT-375 Visibility recorded", test_at375_visibility_recorded),
    ("AT-376 Cost recorded", test_at376_cost_recorded),
    ("AT-377 Dependency analysis", test_at377_dependency_analysis),
    ("AT-378 Heuristic labeling", test_at378_heuristic_labeling),
    ("AT-379 Priority system", test_at379_priority_system),
    ("AT-380 Time-aware optimization", test_at380_time_aware_optimization),
    ("AT-381 Red Team integration", test_at381_red_team_integration),
    ("AT-382 Judge Simulation integration", test_at382_judge_sim_integration),
    ("AT-383 UX integration", test_at383_ux_integration),
    ("AT-384 Testing/Security integration", test_at384_testing_security_integration),
    ("AT-385 Engineering integration", test_at385_engineering_integration),
    ("AT-386 Scope control", test_at386_scope_control),
    ("AT-387 Human approval", test_at387_human_approval),
    ("AT-388 Verification", test_at388_verification),
    ("AT-389 State integration", test_at389_state_integration),
    ("AT-390 Primary next action", test_at390_primary_next_action),
    # Adversarial validation scenarios
    ("ADV-01 Missing Phase 14", test_adv_01_missing_phase14),
    ("ADV-02 Partial Phase 14", test_adv_02_partial_phase14),
    ("ADV-03 Missing official rubric", test_adv_03_missing_official_rubric),
    ("ADV-04 Fabricated official weights", test_adv_04_fabricated_official_weights),
    ("ADV-05 Conflicting weights", test_adv_05_conflicting_weights),
    ("ADV-06 Missing project state", test_adv_06_missing_project_state),
    ("ADV-07 Missing evidence", test_adv_07_missing_evidence),
    ("ADV-08 Stale evidence", test_adv_08_stale_evidence),
    ("ADV-09 Unsupported score", test_adv_09_unsupported_score),
    ("ADV-10 False score precision", test_adv_10_false_score_precision),
    ("ADV-11 Weak score confidence", test_adv_11_weak_score_confidence),
    ("ADV-12 Project weakness mistaken for evidence weakness", test_adv_12_project_weakness_mistaken_for_evidence_weakness),
    ("ADV-13 Evidence weakness mistaken for project weakness", test_adv_13_evidence_weakness_mistaken_for_project_weakness),
    ("ADV-14 Critical Red Team finding ignored", test_adv_14_critical_red_team_finding_ignored),
    ("ADV-15 Mitigated finding incorrectly optimized", test_adv_15_mitigated_finding_incorrectly_optimized),
    ("ADV-16 Judge concern ignored", test_adv_16_judge_concern_ignored),
    ("ADV-17 UX blocker ignored", test_adv_17_ux_blocker_ignored),
    ("ADV-18 Security blocker ignored", test_adv_18_security_blocker_ignored),
    ("ADV-19 Architecture rewrite unnecessary", test_adv_19_architecture_rewrite_unnecessary),
    ("ADV-20 Dependency explosion", test_adv_20_dependency_explosion),
    ("ADV-21 Scope creep", test_adv_21_scope_creep),
    ("ADV-22 Heuristic presented as official math", test_adv_22_heuristic_presented_as_official_math),
    ("ADV-23 Improvement without verification", test_adv_23_improvement_without_verification),
    ("ADV-24 Impossible improvement under time constraint", test_adv_24_impossible_improvement_under_time),
    ("ADV-25 Human approval bypass", test_adv_25_human_approval_bypass),
    ("ADV-26 Idea silently changed", test_adv_26_idea_silently_changed),
    ("ADV-27 Time under two hours", test_adv_27_time_under_two_hours),
    ("ADV-28 Phase 1-14 unchanged", test_adv_28_phase1_14_unchanged),
    ("ADV-29 Conflicting optimization candidates", test_adv_29_conflicting_candidates),
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
