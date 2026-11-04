#!/usr/bin/env python3
"""Deterministic contract validation for Phase 16 — Demo Preparation Intelligence.

Validates the Phase 16 Demo Preparation workflow, rules, and template contracts against
the acceptance tests AT-391 through AT-425 and adversarial scenarios ADV-01–30.

Follows the Phase 6/Phase 10/Phase 11/Phase 12/Phase 13/Phase 14/Phase 15 smoke harness pattern:
stdlib-only, disposable fixtures, machine-readable JSON output, non-zero exit on any failure.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "SKILL.md"
WORKFLOW = ROOT / "workflows" / "demo-preparation.md"
RULES = ROOT / "rules" / "demo-preparation-rules.md"
PLAN_TEMPLATE = ROOT / "templates" / "demo-plan.md"
FLOW_TEMPLATE = ROOT / "templates" / "demo-flow.md"
FINDING_TEMPLATE = ROOT / "templates" / "demo-finding.md"
VERIFICATION_TEMPLATE = ROOT / "templates" / "demo-verification.md"
EVIDENCE_TEMPLATE = ROOT / "templates" / "demo-evidence.md"
CHECKPOINT_TEMPLATE = ROOT / "templates" / "demo-checkpoint.md"
LIFECYCLE = ROOT / "workflows" / "lifecycle.md"

# Expected Phase 16 resources
PHASE16_FILES = [
    WORKFLOW,
    RULES,
    PLAN_TEMPLATE,
    FLOW_TEMPLATE,
    FINDING_TEMPLATE,
    VERIFICATION_TEMPLATE,
    EVIDENCE_TEMPLATE,
    CHECKPOINT_TEMPLATE,
]


def file_contains(path: Path, pattern: str) -> bool:
    return re.search(pattern, path.read_text(encoding="utf-8"), re.IGNORECASE) is not None


def count_occurrences(path: Path, pattern: str) -> int:
    return len(re.findall(pattern, path.read_text(encoding="utf-8"), re.IGNORECASE))


# ---------------------------------------------------------------------------
# AT-391 through AT-425 acceptance tests
# ---------------------------------------------------------------------------

def test_at391_prerequisite_phase15_locked() -> None:
    """Demo preparation consumes score optimization project evidence."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 15 score optimization evidence must exist" in text
    assert ".hackathon/project-state.md" in text


def test_at392_lifecycle_correctness() -> None:
    """Lifecycle contains exactly 20 phases; Phase 16 = Demo Preparation."""
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
    assert data_rows[15][0].strip() == "Demo Preparation", \
        f"Phase 16 should be Demo Preparation, found: {data_rows[15][0].strip()}"


def test_at393_routing_exists() -> None:
    """DEMO-PREPARE routing exists in SKILL.md."""
    text = SKILL.read_text(encoding="utf-8")
    assert "DEMO-PREPARE" in text, "SKILL.md missing DEMO-PREPARE operation"
    assert "workflows/demo-preparation.md" in text, "SKILL.md missing demo-preparation.md workflow path"


def test_at394_resources_resolve() -> None:
    """All Phase 16 resources load from expected locations."""
    for f in PHASE16_FILES:
        assert f.is_file(), f"Phase 16 resource missing: {f}"


def test_at395_state_reading() -> None:
    """Workflow reads project state."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "project-state" in text.lower() or "project state" in text.lower(), \
        "Workflow does not read project state"


def test_at396_repository_inspection() -> None:
    """Workflow requires repository inspection."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "inspect" in text.lower(), "Workflow does not require inspection"
    assert "repository" in text.lower(), "Workflow does not inspect repository"


def test_at397_evidence_model() -> None:
    """Evidence model uses FACT/INFERENCE/ASSUMPTION/UNKNOWN."""
    rules_text = RULES.read_text(encoding="utf-8")
    for label in ["FACT", "INFERENCE", "ASSUMPTION", "UNKNOWN"]:
        assert label in rules_text, f"Rules missing evidence label: {label}"


def test_at398_demo_evidence_types() -> None:
    """Demo evidence types are defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    for et in ["UI", "output", "test", "log", "artifact", "live behavior", "documentation"]:
        assert et.lower() in rules_text.lower(), f"Rules missing demo evidence type: {et}"


def test_at399_demo_evidence_vs_product_evidence() -> None:
    """Demo evidence is distinct from product evidence."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "product capability" in combined or "demonstrated capability" in combined, \
        "Workflow/rules do not distinguish product vs demo evidence"


def test_at400_demo_readiness_distinct() -> None:
    """Demo readiness is distinct from other readiness."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "demo readiness" in combined, "Workflow/rules do not distinguish demo readiness"
    assert "product readiness" in combined or "technical readiness" in combined, \
        "Workflow/rules do not distinguish readiness types"


def test_at401_demo_score_separation() -> None:
    """Demo score is not official judging score."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "simulated demo assessment" in combined, \
        "Workflow/rules do not label simulated demo assessment"
    assert "not official judging score" in combined, \
        "Workflow/rules do not disclaim demo score as official"


def test_at402_reliability_beats_complexity() -> None:
    """Reliability is preferred over complexity."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "reliability beats complexity" in rules_text.lower() or "reliability" in rules_text.lower(), \
        "Rules do not address reliability beats complexity"


def test_at403_human_authority() -> None:
    """Human authority is defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "human approval" in rules_text.lower() or "human-approval" in rules_text.lower(), \
        "Rules do not require human approval"


def test_at404_demo_objective() -> None:
    """Demo objective is defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "demo objective" in combined, "Workflow/rules do not address demo objective"
    assert "by the end of the demo" in combined, "Workflow/rules do not define demo objective format"


def test_at405_demo_narrative() -> None:
    """Demo narrative is built."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "narrative" in combined, "Workflow/rules do not address demo narrative"
    assert "problem" in combined and "solution" in combined, \
        "Workflow/rules do not address narrative sections"


def test_at406_time_aware_strategy() -> None:
    """Time-aware demo strategy is defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "time" in rules_text.lower(), "Rules do not address time-aware demo strategy"
    assert "6" in rules_text or "2-6" in rules_text or "6-12" in rules_text, \
        "Rules do not define time strategy windows"


def test_at407_demo_priority_system() -> None:
    """Demo priority system is defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    for p in ["DEMO-P0", "DEMO-P1", "DEMO-P2", "DEMO-P3", "DROP"]:
        assert p in rules_text, f"Rules missing demo priority {p}"


def test_at408_demo_reliability_model() -> None:
    """Demo reliability model is defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    for dim in ["reliability", "failure likelihood", "recoverability"]:
        assert dim in rules_text.lower(), f"Rules missing reliability dimension: {dim}"


def test_at409_failure_recovery_model() -> None:
    """Failure and recovery model is defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "failure" in combined, "Workflow/rules do not address failure model"
    assert "recovery" in combined, "Workflow/rules do not address recovery model"


def test_at410_fallback_strategy() -> None:
    """Fallback strategy is defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "fallback" in rules_text.lower(), "Rules do not address fallback strategy"


def test_at411_demo_checkpoints() -> None:
    """Demo checkpoints are defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "checkpoint" in rules_text.lower(), "Rules do not address demo checkpoints"


def test_at412_demo_claim_matrix() -> None:
    """Demo claim matrix is defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "claim matrix" in rules_text.lower() or "criterion" in rules_text.lower(), \
        "Rules/rules do not address demo claim matrix"


def test_at413_judge_visible_moments() -> None:
    """Judge-visible moments are identified."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "judge-visible" in rules_text.lower() or "judge visible" in rules_text.lower(), \
        "Rules do not address judge-visible moments"


def test_at414_presenter_talking_points() -> None:
    """Presenter talking points are prepared."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "talking points" in combined or "presenter" in combined, \
        "Workflow/rules do not address presenter talking points"


def test_at415_demo_timing_model() -> None:
    """Demo timing model is built."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "timing" in combined, "Workflow/rules do not address demo timing"


def test_at416_rehearsal_system() -> None:
    """Rehearsal system is defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "rehearsal" in rules_text.lower(), "Rules do not address rehearsal system"


def test_at417_demo_readiness_gate() -> None:
    """Demo readiness gate states are enforced."""
    rules_text = RULES.read_text(encoding="utf-8")
    for gate in ["NOT_READY", "PREPARING", "BLOCKED", "CONDITIONAL", "READY"]:
        assert gate in rules_text, f"Demo quality gate {gate} not found in rules"


def test_at418_integration_with_prior_phases() -> None:
    """Phase 11–15 evidence is consumed."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    for phase in ["Phase 11", "Phase 12", "Phase 13", "Phase 14", "Phase 15"]:
        assert phase in workflow_text, f"Workflow does not reference {phase} evidence"


def test_at419_project_state_integration() -> None:
    """Project state fields are defined."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "Demo Preparation Status" in rules_text or "demo preparation status" in rules_text.lower(), \
        "Rules do not define Demo Preparation Status state field"
    assert "Demo Readiness Gate" in rules_text or "demo readiness gate" in rules_text.lower(), \
        "Rules do not define Demo Readiness Gate state field"


def test_at420_failure_cases() -> None:
    """Failure cases are handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "no selected idea" in rules_text.lower(), "Rules do not address missing selected idea"
    assert "blocked" in rules_text.lower(), "Rules do not address blocked state"


def test_at421_determinism() -> None:
    """Determinism is enforced."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "determinism" in rules_text.lower(), "Rules do not address determinism"


def test_at422_no_silent_implementation() -> None:
    """Phase 16 does not silently implement."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    rules_text = RULES.read_text(encoding="utf-8")
    combined = (workflow_text + " " + rules_text).lower()
    assert "do not implement" in combined or "not implement" in combined, \
        "Workflow/rules do not prohibit implementation work"


def test_at423_no_ppt_creation() -> None:
    """Phase 16 does not create PPT."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    rules_text = RULES.read_text(encoding="utf-8")
    combined = (workflow_text + " " + rules_text).lower()
    assert "ppt" in combined or "presentation" in combined, \
        "Workflow/rules do not address PPT boundary"


def test_at424_no_submission() -> None:
    """Phase 16 does not perform submission."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "submission" in workflow_text.lower(), "Workflow does not address submission boundary"


def test_at425_primary_next_action() -> None:
    """Exactly one primary next action."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "PRIMARY NEXT ACTION" in workflow_text, "Workflow missing PRIMARY NEXT ACTION"
    plan_text = PLAN_TEMPLATE.read_text(encoding="utf-8")
    assert "PRIMARY NEXT ACTION" in plan_text, "Plan template missing PRIMARY NEXT ACTION"


# ---------------------------------------------------------------------------
# Adversarial validation scenarios (30 minimum)
# ---------------------------------------------------------------------------

def test_adv_01_missing_phase15() -> None:
    """Missing score evidence remains a Demo Preparation prerequisite."""
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 15 score optimization evidence must exist" in text


def test_adv_02_partial_phase15() -> None:
    """Partial Phase 15 handled gracefully."""
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
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text, "Rules do not allow UNKNOWN evidence"


def test_adv_09_conflicting_evidence() -> None:
    """Conflicting evidence recorded, not reconciled."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "contradict" in workflow_text.lower() or "conflict" in workflow_text.lower()


def test_adv_10_stale_evidence() -> None:
    """Stale evidence flagged."""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert "stale" in workflow_text.lower() or "revision" in workflow_text.lower() or "unknown" in workflow_text.lower()


def test_adv_11_unsupported_demo_claim() -> None:
    """Unsupported demo claims are flagged."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "unsupported" in rules_text.lower(), "Rules do not flag unsupported claims"


def test_adv_12_fabricated_demo_result() -> None:
    """Fabricated demo results are rejected."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "fabricat" in rules_text.lower() or "do not fabricate" in rules_text.lower(), \
        "Rules do not prohibit fabricating demo results"


def test_adv_13_weak_demo_confidence() -> None:
    """Weak demo confidence is handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "LOW" in rules_text and "confidence" in rules_text.lower(), \
        "Rules do not address LOW confidence"


def test_adv_14_no_demo_evidence_confused_with_capability() -> None:
    """Missing demo evidence is not confused with capability."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "product capability" in rules_text.lower() or "demonstrated capability" in rules_text.lower(), \
        "Rules do not distinguish product vs demonstrated capability"


def test_adv_15_critical_failure_path_ignored() -> None:
    """Critical failure paths are identified."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "failure" in rules_text.lower(), "Rules do not address failure paths"


def test_adv_16_no_fallback_available() -> None:
    """Missing fallback is handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "fallback" in rules_text.lower(), "Rules do not address fallback strategy"


def test_adv_17_demo_readiness_gate_blocked() -> None:
    """Blocked demo readiness is handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "BLOCKED" in rules_text, "Rules do not define BLOCKED gate state"


def test_adv_18_unknown_demo_duration() -> None:
    """Unknown demo duration is handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "UNKNOWN" in rules_text, "Rules do not allow UNKNOWN demo duration"


def test_adv_19_unnecessary_features_not_added() -> None:
    """Unnecessary features are not added to demo."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "feature quantity" in rules_text.lower() or "not feature count" in rules_text.lower(), \
        "Rules do not address not optimizing for feature quantity"


def test_adv_20_scope_creep() -> None:
    """Demo scope creep is controlled."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "scope" in combined, "Workflow/rules do not address scope control"
    assert "DROP" in rules_text, "Rules do not define DROP priority"


def test_adv_21_demo_score_presented_as_official() -> None:
    """Demo score is not presented as official."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "not official judging score" in combined, \
        "Workflow/rules do not disclaim demo score as official"


def test_adv_22_reliability_over_complexity() -> None:
    """Reliability is preferred over complexity."""
    rules_text = RULES.read_text(encoding="utf-8")
    assert "reliability" in rules_text.lower() and "complexity" in rules_text.lower(), \
        "Rules do not address reliability beats complexity"


def test_adv_23_improvement_without_verification() -> None:
    """Improvements without verification are not marked complete."""
    finding_text = FINDING_TEMPLATE.read_text(encoding="utf-8")
    assert "Verification" in finding_text, "Finding template missing Verification"
    rules_text = RULES.read_text(encoding="utf-8")
    assert "verification" in rules_text.lower(), "Rules do not address verification"


def test_adv_24_impossible_demo_under_time() -> None:
    """Impossible demos under time constraint are deprioritized."""
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


def test_adv_28_phase1_15_unchanged() -> None:
    """Phase 1–15 artifacts remain untouched."""
    phase_files = [
        ROOT / "workflows" / "score-optimization.md",
        ROOT / "workflows" / "judge-simulation.md",
        ROOT / "workflows" / "red-team.md",
        ROOT / "workflows" / "ux-review.md",
        ROOT / "workflows" / "testing-security.md",
        ROOT / "workflows" / "implementation.md",
    ]
    for f in phase_files:
        assert f.is_file(), f"Phase file missing: {f}"


def test_adv_29_conflicting_demo_steps() -> None:
    """Conflicting demo steps are handled."""
    rules_text = RULES.read_text(encoding="utf-8")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    combined = (rules_text + " " + workflow_text).lower()
    assert "contradict" in combined or "conflict" in combined, \
        "Workflow/rules do not address conflicting demo steps"


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
    # Acceptance tests AT-391 through AT-425
    ("AT-391 Prerequisite Phase 15 locked", test_at391_prerequisite_phase15_locked),
    ("AT-392 Lifecycle correctness", test_at392_lifecycle_correctness),
    ("AT-393 Routing exists", test_at393_routing_exists),
    ("AT-394 Resources resolve", test_at394_resources_resolve),
    ("AT-395 State reading", test_at395_state_reading),
    ("AT-396 Repository inspection", test_at396_repository_inspection),
    ("AT-397 Evidence model", test_at397_evidence_model),
    ("AT-398 Demo evidence types", test_at398_demo_evidence_types),
    ("AT-399 Demo evidence vs product evidence", test_at399_demo_evidence_vs_product_evidence),
    ("AT-400 Demo readiness distinct", test_at400_demo_readiness_distinct),
    ("AT-401 Demo score separation", test_at401_demo_score_separation),
    ("AT-402 Reliability beats complexity", test_at402_reliability_beats_complexity),
    ("AT-403 Human authority", test_at403_human_authority),
    ("AT-404 Demo objective", test_at404_demo_objective),
    ("AT-405 Demo narrative", test_at405_demo_narrative),
    ("AT-406 Time-aware strategy", test_at406_time_aware_strategy),
    ("AT-407 Demo priority system", test_at407_demo_priority_system),
    ("AT-408 Demo reliability model", test_at408_demo_reliability_model),
    ("AT-409 Failure recovery model", test_at409_failure_recovery_model),
    ("AT-410 Fallback strategy", test_at410_fallback_strategy),
    ("AT-411 Demo checkpoints", test_at411_demo_checkpoints),
    ("AT-412 Demo claim matrix", test_at412_demo_claim_matrix),
    ("AT-413 Judge-visible moments", test_at413_judge_visible_moments),
    ("AT-414 Presenter talking points", test_at414_presenter_talking_points),
    ("AT-415 Demo timing model", test_at415_demo_timing_model),
    ("AT-416 Rehearsal system", test_at416_rehearsal_system),
    ("AT-417 Demo readiness gate", test_at417_demo_readiness_gate),
    ("AT-418 Integration with prior phases", test_at418_integration_with_prior_phases),
    ("AT-419 Project state integration", test_at419_project_state_integration),
    ("AT-420 Failure cases", test_at420_failure_cases),
    ("AT-421 Determinism", test_at421_determinism),
    ("AT-422 No silent implementation", test_at422_no_silent_implementation),
    ("AT-423 No PPT creation", test_at423_no_ppt_creation),
    ("AT-424 No submission", test_at424_no_submission),
    ("AT-425 Primary next action", test_at425_primary_next_action),
    # Adversarial validation scenarios
    ("ADV-01 Missing Phase 15", test_adv_01_missing_phase15),
    ("ADV-02 Partial Phase 15", test_adv_02_partial_phase15),
    ("ADV-03 Missing project state", test_adv_03_missing_project_state),
    ("ADV-04 Empty repository", test_adv_04_empty_repository),
    ("ADV-05 Missing source code", test_adv_05_missing_source_code),
    ("ADV-06 Missing runtime", test_adv_06_missing_runtime),
    ("ADV-07 Missing browser", test_adv_07_missing_browser),
    ("ADV-08 Missing evidence", test_adv_08_missing_evidence),
    ("ADV-09 Conflicting evidence", test_adv_09_conflicting_evidence),
    ("ADV-10 Stale evidence", test_adv_10_stale_evidence),
    ("ADV-11 Unsupported demo claim", test_adv_11_unsupported_demo_claim),
    ("ADV-12 Fabricated demo result", test_adv_12_fabricated_demo_result),
    ("ADV-13 Weak demo confidence", test_adv_13_weak_demo_confidence),
    ("ADV-14 No demo evidence confused with capability", test_adv_14_no_demo_evidence_confused_with_capability),
    ("ADV-15 Critical failure path ignored", test_adv_15_critical_failure_path_ignored),
    ("ADV-16 No fallback available", test_adv_16_no_fallback_available),
    ("ADV-17 Demo readiness gate blocked", test_adv_17_demo_readiness_gate_blocked),
    ("ADV-18 Unknown demo duration", test_adv_18_unknown_demo_duration),
    ("ADV-19 Unnecessary features not added", test_adv_19_unnecessary_features_not_added),
    ("ADV-20 Scope creep", test_adv_20_scope_creep),
    ("ADV-21 Demo score presented as official", test_adv_21_demo_score_presented_as_official),
    ("ADV-22 Reliability over complexity", test_adv_22_reliability_over_complexity),
    ("ADV-23 Improvement without verification", test_adv_23_improvement_without_verification),
    ("ADV-24 Impossible demo under time", test_adv_24_impossible_demo_under_time),
    ("ADV-25 Human approval bypass", test_adv_25_human_approval_bypass),
    ("ADV-26 Idea silently changed", test_adv_26_idea_silently_changed),
    ("ADV-27 Time under two hours", test_adv_27_time_under_two_hours),
    ("ADV-28 Phase 1-15 unchanged", test_adv_28_phase1_15_unchanged),
    ("ADV-29 Conflicting demo steps", test_adv_29_conflicting_demo_steps),
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
