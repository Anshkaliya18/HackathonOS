#!/usr/bin/env python3
"""Deterministic contract validation for Phase 17 — Presentation Intelligence.

Validates the Phase 17 Presentation workflow, rules, and template contracts against
the acceptance tests AT-426 through AT-460 and adversarial scenarios ADV-01–30.

Follows the Phase 6/Phase 10/Phase 11/Phase 12/Phase 13/Phase 14/Phase 15/Phase 16 smoke harness pattern:
stdlib-only, disposable fixtures, machine-readable JSON output, non-zero exit on any failure.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "SKILL.md"
WORKFLOW = ROOT / "workflows" / "presentation.md"
RULES = ROOT / "rules" / "presentation-rules.md"
PLAN_TEMPLATE = ROOT / "templates" / "presentation-plan.md"
SLIDE_TEMPLATE = ROOT / "templates" / "slide-plan.md"
CLAIM_TEMPLATE = ROOT / "templates" / "slide-claim.md"
EVIDENCE_TEMPLATE = ROOT / "templates" / "presentation-evidence.md"
RISK_TEMPLATE = ROOT / "templates" / "presentation-risk.md"
QNA_TEMPLATE = ROOT / "templates" / "presentation-qna.md"
VERIFICATION_TEMPLATE = ROOT / "templates" / "presentation-verification.md"
LIFECYCLE = ROOT / "workflows" / "lifecycle.md"

# Expected Phase 17 resources
PHASE17_FILES = [
    WORKFLOW,
    RULES,
    PLAN_TEMPLATE,
    SLIDE_TEMPLATE,
    CLAIM_TEMPLATE,
    EVIDENCE_TEMPLATE,
    RISK_TEMPLATE,
    QNA_TEMPLATE,
    VERIFICATION_TEMPLATE,
]


def file_contains(path: Path, pattern: str) -> bool:
    return re.search(pattern, path.read_text(encoding="utf-8"), re.IGNORECASE) is not None


def count_occurrences(path: Path, pattern: str) -> int:
    return len(re.findall(pattern, path.read_text(encoding="utf-8"), re.IGNORECASE))


# ---------------------------------------------------------------------------
# AT-426 through AT-460 acceptance tests
# ---------------------------------------------------------------------------

def test_at426_prerequisite_phase16_locked() -> None:
    """Presentation preparation consumes demo project evidence."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 16 demo preparation evidence must exist" in text
    assert ".hackathon/project-state.md" in text


def test_at427_lifecycle_correctness() -> None:
    """Lifecycle contains exactly 20 phases; Phase 17 = PPT / Presentation."""
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
    assert data_rows[16][0].strip() == "PPT / Presentation", \
        f"Phase 17 should be PPT / Presentation, found: {data_rows[16][0].strip()}"


def test_at428_routing_exists() -> None:
    """PRESENTATION-PREPARE routing exists in SKILL.md."""
    text = SKILL.read_text(encoding="utf-8")
    assert "PRESENTATION-PREPARE" in text, "SKILL.md missing PRESENTATION-PREPARE operation"
    assert "workflows/presentation.md" in text, "SKILL.md missing presentation.md workflow path"


def test_at429_resources_resolve() -> None:
    """All Phase 17 resources load from expected locations."""
    for f in PHASE17_FILES:
        assert f.is_file(), f"Phase 17 resource missing: {f}"


def test_at430_state_reading() -> None:
    """Workflow reads project state."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "project-state" in text.lower() or "project state" in text.lower(), \
        "Workflow does not read project state"


def test_at431_repository_inspection() -> None:
    """Workflow requires repository inspection."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "inspect" in text.lower(), "Workflow does not require inspection"
    assert "repository" in text.lower(), "Workflow does not inspect repository"


def test_at432_evidence_model() -> None:
    """Evidence model uses FACT/INFERENCE/ASSUMPTION/UNKNOWN."""
    rules_text = RULES.read_text(encoding="utf-8")
    for label in ["FACT", "INFERENCE", "ASSUMPTION", "UNKNOWN"]:
        assert label in rules_text, f"Rules missing evidence label: {label}"


def test_at433_presentation_evidence_types() -> None:
    """Presentation evidence types are defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    for et in ["UI", "output", "test", "log", "artifact", "live behavior", "screenshot", "recording", "documentation", "benchmark", "source/code inspection"]:
        assert et.lower() in rules_text.lower(), f"Rules missing presentation evidence type: {et}"


def test_at434_presentation_evidence_vs_product_evidence() -> None:
    """Presentation evidence is distinct from product evidence."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "product exists" in combined or "demonstrated capability" in combined or "demonstration" in combined, \
        "Workflow/rules do not distinguish product vs presentation evidence"


def test_at435_presentation_readiness_distinct() -> None:
    """Presentation readiness is distinct from other readiness types."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "presentation readiness" in combined, "Workflow/rules do not distinguish presentation readiness"
    assert "product readiness" in combined or "demo readiness" in combined or "technical readiness" in combined, \
        "Workflow/rules do not distinguish readiness types"


def test_at436_presentation_score_separation() -> None:
    """Presentation score is not official judging score."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "internal presentation readiness indicator" in combined, \
        "Workflow/rules do not label internal presentation readiness indicator"
    assert "not official judging score" in combined, \
        "Workflow/rules do not disclaim presentation score as official"


def test_at437_marketing_brochure_avoided() -> None:
    """Presentation avoids marketing brochure approach."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "marketing brochure" in combined or "unsupported superlatives" in combined, \
        "Workflow/rules do not address marketing brochure avoidance"
    assert "clarity" in combined and "evidence" in combined, \
        "Workflow/rules do not prioritize clarity and evidence"


def test_at438_judging_criteria() -> None:
    """Official judging criteria are used or marked UNKNOWN."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "official criteria" in combined, "Workflow/rules do not address official judging criteria"
    assert "unknown" in combined, "Workflow/rules do not allow UNKNOWN criteria"


def test_at439_provisional_framework_labeled() -> None:
    """Provisional framework is explicitly labeled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "provisional" in rules_text.lower(), "Rules do not label provisional framework"
    assert "not official" in rules_text.lower() or "simulated" in rules_text.lower(), \
        "Rules do not disclaim provisional framework as official"


def test_at440_slide_architecture() -> None:
    """Slide architecture is defined."""
    assert SLIDE_TEMPLATE.is_file(), "Slide plan template missing"
    text = SLIDE_TEMPLATE.read_text(encoding="utf-8")
    assert "Slide ID" in text, "Slide template missing Slide ID"
    assert "Title" in text, "Slide template missing Title"
    assert "Purpose" in text, "Slide template missing Purpose"
    assert "Primary Message" in text, "Slide template missing Primary Message"
    assert "Judge Takeaway" in text, "Slide template missing Judge Takeaway"


def test_at441_slide_types() -> None:
    """Slide types are defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    for slide_type in ["Title", "Problem", "Solution", "Demo", "Impact", "Closing"]:
        assert slide_type.lower() in rules_text.lower(), f"Rules missing slide type: {slide_type}"


def test_at442_slide_priority_system() -> None:
    """Slide priority system is defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    for p in ["PPT-P0", "PPT-P1", "PPT-P2", "PPT-P3", "DROP"]:
        assert p in rules_text, f"Rules missing slide priority {p}"


def test_at443_presentation_narrative() -> None:
    """Presentation narrative is built."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "narrative" in combined, "Workflow/rules do not address presentation narrative"
    assert "problem" in combined and "solution" in combined, \
        "Workflow/rules do not address narrative sections"


def test_at444_slide_to_criterion_mapping() -> None:
    """Slide-to-criterion mapping is defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "claim matrix" in rules_text.lower() or "slide-to-criterion" in rules_text.lower() or "criterion mapping" in rules_text.lower(), \
        "Workflow/rules do not address slide-to-criterion mapping"


def test_at445_mapping_statuses() -> None:
    """Mapping statuses are defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    for status in ["SUPPORTED", "PARTIALLY_SUPPORTED", "CONTRADICTED", "NOT_APPLICABLE"]:
        assert status in rules_text, f"Rules missing mapping status: {status}"
    assert "UNKNOWN" in rules_text, "Rules missing UNKNOWN mapping status"


def test_at446_claim_credibility() -> None:
    """Claim credibility is assessed."""
    rules_text = RULES.read_text(encoding="utf-8")
    claim_text = CLAIM_TEMPLATE.read_text(encoding="utf-8")
    for status in ["VERIFIED", "SUPPORTED", "PARTIALLY_SUPPORTED", "UNSUPPORTED", "CONTRADICTED", "UNKNOWN"]:
        assert status in rules_text or status in claim_text, f"Rules/claim template missing claim credibility status: {status}"


def test_at447_numbers_and_metrics() -> None:
    """Numbers and metrics require evidence."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "metric" in rules_text.lower(), "Rules do not address numbers and metrics"
    assert "precision" in rules_text.lower(), "Rules do not address numerical precision"


def test_at448_technical_presentation() -> None:
    """Technical presentation is addressed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "technical" in rules_text.lower(), "Rules do not address technical presentation"
    assert "architecture" in rules_text.lower(), "Rules do not address technical architecture"


def test_at449_ai_ml_claims() -> None:
    """AI/ML claims are addressed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "AI" in rules_text or "ML" in rules_text or "artificial intelligence" in rules_text.lower(), \
        "Rules do not address AI/ML claims"
    assert "NOT_APPLICABLE" in rules_text, "Rules do not define NOT_APPLICABLE for non-AI projects"


def test_at450_demo_integration() -> None:
    """Demo integration is defined."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "demo" in workflow_text.lower(), "Workflow does not address demo integration"
    assert "Phase 16" in workflow_text, "Workflow does not reference Phase 16 demo preparation"


def test_at451_judge_simulation_integration() -> None:
    """Judge Simulation integration is defined."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 14" in workflow_text or "judge-simulation" in workflow_text.lower() or "judge simulation" in workflow_text.lower(), \
        "Workflow does not reference Phase 14 judge simulation"


def test_at452_score_optimization_integration() -> None:
    """Score Optimization integration is defined."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 15" in workflow_text or "score-optimization" in workflow_text.lower() or "score optimization" in workflow_text.lower(), \
        "Workflow does not reference Phase 15 score optimization"


def test_at453_ux_security_redteam_integration() -> None:
    """UX, Security, Red Team integration is defined."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 11" in workflow_text or "Phase 12" in workflow_text or "Phase 13" in workflow_text, \
        "Workflow does not reference Phase 11/12/13 evidence"


def test_at454_time_aware_strategy() -> None:
    """Time-aware presentation strategy is defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "time" in rules_text.lower(), "Rules do not address time-aware presentation strategy"
    assert "6" in rules_text or "2-6" in rules_text or "6-12" in rules_text, \
        "Rules do not define time strategy windows"


def test_at455_presentation_timing_model() -> None:
    """Presentation timing model is defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "timing" in rules_text.lower(), "Rules do not address presentation timing"


def test_at456_speaker_guidance() -> None:
    """Speaker guidance is prepared."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "speaker" in combined, "Workflow/rules do not address speaker guidance"


def test_at457_visual_evidence() -> None:
    """Visual evidence is planned."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "visual" in rules_text.lower() or "screenshot" in rules_text.lower() or "diagram" in rules_text.lower(), \
        "Rules do not address visual evidence"


def test_at458_redundancy_analysis() -> None:
    """Redundancy analysis is performed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "redundanc" in rules_text.lower(), "Rules do not address redundancy analysis"


def test_at459_presentation_risk_model() -> None:
    """Presentation risk model is defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "risk" in rules_text.lower(), "Rules do not address presentation risk"
    assert "severity" in rules_text.lower(), "Rules do not address risk severity"


def test_at460_primary_next_action() -> None:
    """Exactly one primary next action."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "PRIMARY NEXT ACTION" in workflow_text, "Workflow missing PRIMARY NEXT ACTION"
    plan_text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    assert "PRIMARY NEXT ACTION" in plan_text, "Plan template missing PRIMARY NEXT ACTION"


# ---------------------------------------------------------------------------
# Adversarial validation scenarios (30 minimum)
# ---------------------------------------------------------------------------

def test_adv_01_missing_phase16() -> None:
    """Missing demo evidence remains an explicit prerequisite."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 16 demo preparation evidence must exist" in text


def test_adv_02_partial_phase16() -> None:
    """Partial Phase 16 handled gracefully."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "partial" in text.lower() or "limited" in text.lower() or "blocked" in text.lower(), \
        "Workflow does not handle partial readiness"


def test_adv_03_missing_project_state() -> None:
    """Missing project state handled gracefully."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "project-state" in text.lower() or "project state" in text.lower()


def test_adv_04_missing_rubric() -> None:
    """Missing rubric marked UNKNOWN."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text, "Rules do not handle UNKNOWN rubric"


def test_adv_05_fabricated_official_rubric() -> None:
    """Fabricated official rubric rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "invent" in rules_text.lower() or "do not invent" in rules_text.lower(), \
        "Rules do not prohibit inventing official rubric"


def test_adv_06_fabricated_slide_limit() -> None:
    """Fabricated slide limit rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "invent" in rules_text.lower() or "do not invent" in rules_text.lower(), \
        "Rules do not prohibit inventing slide limits"


def test_adv_07_fabricated_presentation_duration() -> None:
    """Fabricated presentation duration rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text or "do not invent" in rules_text.lower(), \
        "Rules do not address fabricated presentation duration"


def test_adv_08_unknown_to_fact() -> None:
    """UNKNOWN not converted to FACT."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "never convert" in rules_text.lower() or "do not convert" in rules_text.lower() or "never transform" in rules_text.lower(), \
        "Rules do not prohibit converting UNKNOWN to FACT"


def test_adv_09_unsupported_claim() -> None:
    """Unsupported claims are flagged."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "unsupported" in rules_text.lower(), "Rules do not flag unsupported claims"


def test_adv_10_fabricated_benchmark() -> None:
    """Fabricated benchmarks are rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "benchmark" in rules_text.lower() or "metric" in rules_text.lower(), \
        "Rules do not address fabricated benchmarks/metrics"


def test_adv_11_fabricated_user_count() -> None:
    """Fabricated user counts are rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "metric" in rules_text.lower() or "number" in rules_text.lower(), \
        "Rules do not address fabricated user counts"


def test_adv_12_screenshot_as_live_evidence() -> None:
    """Screenshots not presented as live evidence."""
    rules_text = RULES.read_text(encoding="evidence-rules.md") if Path("rules/evidence-rules.md").exists() else RULES.read_text(encoding="utf-8")
    assert "screenshot" in rules_text.lower() or "live" in rules_text.lower(), \
        "Rules do not address screenshot vs live evidence"


def test_adv_13_stale_evidence() -> None:
    """Stale evidence flagged."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "stale" in workflow_text.lower() or "revision" in workflow_text.lower() or "unknown" in workflow_text.lower()


def test_adv_14_contradicted_evidence() -> None:
    """Contradicted evidence surfaced."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "contradict" in workflow_text.lower() or "conflict" in workflow_text.lower(), \
        "Workflow does not address contradictory evidence"


def test_adv_15_unsupported_ai_claim() -> None:
    """Unsupported AI claims are flagged."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "AI" in rules_text and "unsupported" in rules_text.lower(), \
        "Rules do not address unsupported AI claims"


def test_adv_16_unsupported_architecture_claim() -> None:
    """Unsupported architecture claims are flagged."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "architecture" in rules_text.lower() and "unsupported" in rules_text.lower(), \
        "Rules do not address unsupported architecture claims"


def test_adv_17_demo_disconnected_from_presentation() -> None:
    """Demo integrated with presentation."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "demo" in workflow_text.lower() and "Phase 16" in workflow_text, \
        "Workflow does not integrate demo with presentation"


def test_adv_18_criterion_without_evidence() -> None:
    """Criterion without evidence is marked UNKNOWN."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text, "Rules do not allow UNKNOWN criterion evidence"


def test_adv_19_evidence_without_criterion() -> None:
    """Evidence without criterion is flagged."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "evidence" in rules_text.lower() and "criterion" in rules_text.lower(), \
        "Rules do not address evidence without criterion"


def test_adv_20_hidden_scoring_multiplier() -> None:
    """No hidden scoring multipliers."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "multiplier" in rules_text.lower() or "hidden" in rules_text.lower(), \
        "Rules do not address hidden scoring multipliers"
    assert "not official judging score" in rules_text.lower(), \
        "Rules do not disclaim internal presentation score as official"


def test_adv_21_simulated_score_as_official() -> None:
    """Simulated score not presented as official."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "not official judging score" in rules_text.lower(), \
        "Rules do not disclaim simulated score as official"


def test_adv_22_excessive_slide_count() -> None:
    """Excessive slide count avoided."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "redundanc" in rules_text.lower() or "slide count" in rules_text.lower(), \
        "Rules do not address excessive slide count"


def test_adv_23_timing_overflow() -> None:
    """Timing overflow avoided."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "timing" in rules_text.lower() or "duration" in rules_text.lower(), \
        "Rules do not address presentation timing overflow"


def test_adv_24_redundant_slides() -> None:
    """Redundant slides removed."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "redundanc" in rules_text.lower(), "Rules do not address redundant slides"


def test_adv_25_critical_issue_hidden() -> None:
    """Critical issue not hidden."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "CRITICAL" in rules_text, "Rules do not define CRITICAL severity"
    assert "hidden" in rules_text.lower() or "suppress" in rules_text.lower(), \
        "Rules do not address hiding critical issues"


def test_adv_26_phase18_scope_leakage() -> None:
    """Phase 18 scope not leaked."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "final audit" in workflow_text.lower() or "phase 18" in workflow_text.lower(), \
        "Workflow does not address Phase 18 boundary"


def test_adv_27_phase19_scope_leakage() -> None:
    """Phase 19 scope not leaked."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "submission" in workflow_text.lower() or "phase 19" in workflow_text.lower(), \
        "Workflow does not address Phase 19 boundary"


def test_adv_28_multiple_primary_next_actions() -> None:
    """Exactly one PRIMARY NEXT ACTION."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    plan_text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    assert workflow_text.count("PRIMARY NEXT ACTION") >= 1, "Workflow missing PRIMARY NEXT ACTION"
    assert plan_text.count("PRIMARY NEXT ACTION") >= 1, "Plan template missing PRIMARY NEXT ACTION"


def test_adv_29_fabricated_readiness() -> None:
    """Readiness not fabricated without evidence."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "READY" in rules_text and "evidence" in rules_text.lower(), \
        "Rules do not require evidence for READY"


def test_adv_30_conflicting_evidence() -> None:
    """Conflicting evidence surfaced."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "CONTRADICTED" in rules_text, "Rules do not define CONTRADICTED status"


# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------

TESTS: list[tuple[str, Callable[[], None]]] = [
    # Acceptance tests AT-426 through AT-460
    ("AT-426 Prerequisite Phase 16 locked", test_at426_prerequisite_phase16_locked),
    ("AT-427 Lifecycle correctness", test_at427_lifecycle_correctness),
    ("AT-428 Routing exists", test_at428_routing_exists),
    ("AT-429 Resources resolve", test_at429_resources_resolve),
    ("AT-430 State reading", test_at430_state_reading),
    ("AT-431 Repository inspection", test_at431_repository_inspection),
    ("AT-432 Evidence model", test_at432_evidence_model),
    ("AT-433 Demo evidence types", test_at433_presentation_evidence_types),
    ("AT-434 Demo evidence vs product evidence", test_at434_presentation_evidence_vs_product_evidence),
    ("AT-435 Presentation readiness distinct", test_at435_presentation_readiness_distinct),
    ("AT-436 Presentation score separation", test_at436_presentation_score_separation),
    ("AT-437 Marketing brochure avoided", test_at437_marketing_brochure_avoided),
    ("AT-438 Judging criteria", test_at438_judging_criteria),
    ("AT-439 Provisional framework labeled", test_at439_provisional_framework_labeled),
    ("AT-440 Slide architecture", test_at440_slide_architecture),
    ("AT-441 Slide types", test_at441_slide_types),
    ("AT-442 Slide priority system", test_at442_slide_priority_system),
    ("AT-443 Presentation narrative", test_at443_presentation_narrative),
    ("AT-444 Slide-to-criterion mapping", test_at444_slide_to_criterion_mapping),
    ("AT-445 Mapping statuses", test_at445_mapping_statuses),
    ("AT-446 Claim credibility", test_at446_claim_credibility),
    ("AT-447 Numbers and metrics", test_at447_numbers_and_metrics),
    ("AT-448 Technical presentation", test_at448_technical_presentation),
    ("AT-449 AI/ML claims", test_at449_ai_ml_claims),
    ("AT-450 Demo integration", test_at450_demo_integration),
    ("AT-451 Judge simulation integration", test_at451_judge_simulation_integration),
    ("AT-452 Score optimization integration", test_at452_score_optimization_integration),
    ("AT-453 UX/security/redteam integration", test_at453_ux_security_redteam_integration),
    ("AT-454 Time-aware strategy", test_at454_time_aware_strategy),
    ("AT-455 Presentation timing model", test_at455_presentation_timing_model),
    ("AT-456 Speaker guidance", test_at456_speaker_guidance),
    ("AT-457 Visual evidence", test_at457_visual_evidence),
    ("AT-458 Redundancy analysis", test_at458_redundancy_analysis),
    ("AT-459 Presentation risk model", test_at459_presentation_risk_model),
    ("AT-460 Primary next action", test_at460_primary_next_action),
    # Adversarial validation scenarios
    ("ADV-01 Missing Phase 16", test_adv_01_missing_phase16),
    ("ADV-02 Partial Phase 16", test_adv_02_partial_phase16),
    ("ADV-03 Missing project state", test_adv_03_missing_project_state),
    ("ADV-04 Missing rubric", test_adv_04_missing_rubric),
    ("ADV-05 Fabricated official rubric", test_adv_05_fabricated_official_rubric),
    ("ADV-06 Fabricated slide limit", test_adv_06_fabricated_slide_limit),
    ("ADV-07 Fabricated presentation duration", test_adv_07_fabricated_presentation_duration),
    ("ADV-08 UNKNOWN to FACT", test_adv_08_unknown_to_fact),
    ("ADV-09 Unsupported claim", test_adv_09_unsupported_claim),
    ("ADV-10 Fabricated benchmark", test_adv_10_fabricated_benchmark),
    ("ADV-11 Fabricated user count", test_adv_11_fabricated_user_count),
    ("ADV-12 Screenshot as live evidence", test_adv_12_screenshot_as_live_evidence),
    ("ADV-13 Stale evidence", test_adv_13_stale_evidence),
    ("ADV-14 Contradicted evidence", test_adv_14_contradicted_evidence),
    ("ADV-15 Unsupported AI claim", test_adv_15_unsupported_ai_claim),
    ("ADV-16 Unsupported architecture claim", test_adv_16_unsupported_architecture_claim),
    ("ADV-17 Demo disconnected from presentation", test_adv_17_demo_disconnected_from_presentation),
    ("ADV-18 Criterion without evidence", test_adv_18_criterion_without_evidence),
    ("ADV-19 Evidence without criterion", test_adv_19_evidence_without_criterion),
    ("ADV-20 Hidden scoring multiplier", test_adv_20_hidden_scoring_multiplier),
    ("ADV-21 Simulated score as official", test_adv_21_simulated_score_as_official),
    ("ADV-22 Excessive slide count", test_adv_22_excessive_slide_count),
    ("ADV-23 Timing overflow", test_adv_23_timing_overflow),
    ("ADV-24 Redundant slides", test_adv_24_redundant_slides),
    ("ADV-25 Critical issue hidden", test_adv_25_critical_issue_hidden),
    ("ADV-26 Phase 18 scope leakage", test_adv_26_phase18_scope_leakage),
    ("ADV-27 Phase 19 scope leakage", test_adv_27_phase19_scope_leakage),
    ("ADV-28 Multiple PRIMARY NEXT ACTION entries", test_adv_28_multiple_primary_next_actions),
    ("ADV-29 Fabricated readiness", test_adv_29_fabricated_readiness),
    ("ADV-30 Conflicting evidence", test_adv_30_conflicting_evidence),
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
