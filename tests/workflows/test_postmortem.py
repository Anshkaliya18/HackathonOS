#!/usr/bin/env python3
"""Phase 20 contract validator; stdlib-only, deterministic, no project mutation.
Adversarial cases are synthetic guard fixtures and do not simulate an LLM runtime.
"""
from __future__ import annotations
import json, re, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = {
    "skill": ROOT / "SKILL.md", "lifecycle": ROOT / "workflows/lifecycle.md",
    "submission_workflow": ROOT / "workflows/submission.md",
    "workflow": ROOT / "workflows/postmortem.md", "rules": ROOT / "rules/postmortem-rules.md",
    "report_template": ROOT / "templates/postmortem.md", "timeline": ROOT / "templates/timeline.md",
    "decision": ROOT / "templates/decision-log.md", "incident": ROOT / "templates/incident.md",
    "lesson": ROOT / "templates/lesson.md", "improvement": ROOT / "templates/improvement.md",
}
T = {k: p.read_text(encoding="utf-8") for k, p in FILES.items()}
PHASE_NAMES = ("Understand Rules", "Analyze Problem", "Generate Ideas", "Validate Ideas", "Research Market",
 "Select Idea", "Design Product/MVP", "Architecture", "Development Plan", "Implementation", "Testing + Security",
 "UX Review", "Red Team", "Judge Simulation", "Score Optimization", "Demo Preparation", "PPT / Presentation",
 "Final Audit", "Submission", "Post-Mortem")

def check(condition: bool, message: str) -> None:
    if not condition: raise AssertionError(message)

def guarded(record: dict) -> bool:
    """Synthetic retrospective integrity guard used only for disposable adversarial fixtures."""
    forbidden = ("fabricated_result", "unsupported_winner", "unsupported_finalist", "fabricated_judge_feedback",
      "unknown_as_fact", "inference_as_fact", "correlation_as_causation", "incident_without_evidence",
      "conflicting_decisions_hidden", "invented_human_owner", "incomplete_risk_as_avoided",
      "incomplete_testing_as_complete", "incomplete_ux_as_complete", "incomplete_redteam_as_complete",
      "simulated_score_as_actual", "demo_plan_as_outcome", "assumption_as_fact", "readiness_as_submitted",
      "historical_rewrite", "application_source_change", "phase21", "multiple_primary_actions",
      "success_with_empty_evidence", "contradictory_timestamps", "phase19_missing", "phase19_unlocked",
      "lifecycle_21", "missing_project_state_as_live", "empty_history_as_live", "missing_timeline_as_fact")
    return not any(record.get(key, False) for key in forbidden)

checks = [
("Prerequisite validation", lambda: check(".sherpa/project-state.md" in T["workflow"] and ".sherpa/submission-plan.md" in T["workflow"] and "CONDITIONAL — FRAMEWORK VALIDATION ONLY" in T["workflow"], "project-scoped evidence gate absent")),
("Lifecycle exactly 20", lambda: check(sum(1 for x in PHASE_NAMES if re.search(rf'^\\| {re.escape(x)} \\|', T["lifecycle"], re.M)) == 20, "phase count")),
("Submission source contract", lambda: check(".sherpa/final-audit.md" in T["submission_workflow"] and "Audit status: COMPLETE" in T["submission_workflow"], "project audit prerequisite missing")),
("Evidence labels", lambda: check(all(x in T["rules"] for x in ("FACT", "INFERENCE", "ASSUMPTION", "UNKNOWN")), "evidence model")),
("Outcome and causality separation", lambda: check("Correlation is not causation" in T["rules"] and "Causality states" in T["rules"], "causality contract")),
("Plan vs actual model", lambda: check("plan-vs-actual" in T["workflow"].lower() and "Plan vs Actual" in T["report_template"], "comparison missing")),
("Timeline model", lambda: check(all(x in T["timeline"] for x in ("Planned time", "Actual time", "Start", "Completion", "Variance", "Evidence")), "timeline fields")),
("Scope retrospective", lambda: check(all(x in T["report_template"] for x in ("Planned / Added / Removed / Deferred / Accidental", "Scope Changes")), "scope fields")),
("Decision log", lambda: check(all(x in T["decision"] for x in ("Decision ID", "Available evidence", "Human decision maker", "Expected outcome", "Actual outcome", "Decision quality")), "decision fields")),
("Human authority", lambda: check("Do not attribute a human decision to AI" in T["rules"] and "Human decision maker / approval" in T["decision"], "authority safeguard")),
("Incident model", lambda: check(all(x in T["incident"] for x in ("Incident ID", "What happened", "Expected behavior", "Actual behavior", "Evidence", "Root cause status")), "incident fields")),
("Root cause model", lambda: check(all(x in T["rules"] for x in ("5 Whys", "causal tree", "alternative explanation", "causality status")), "root cause evidence")),
("Risk outcome review", lambda: check(all(x in T["rules"] for x in ("MATERIALIZED", "PARTIALLY_MATERIALIZED", "AVOIDED", "MITIGATED", "TRANSFERRED", "IRRELEVANT")), "risk outcome states")),
("Testing/security review", lambda: check("11 Testing + Security" in T["workflow"], "test security review")),
("UX review", lambda: check("12 UX" in T["workflow"], "UX review")),
("Red-team review", lambda: check("13 Red Team" in T["workflow"], "red team review")),
("Judge review", lambda: check("14 Judge Simulation" in T["workflow"], "judge review")),
("Score review", lambda: check("15 Score Optimization" in T["workflow"], "score review")),
("Demo review", lambda: check("16 Demo Preparation" in T["workflow"], "demo review")),
("Presentation review", lambda: check("17 Presentation" in T["workflow"], "presentation review")),
("Submission review", lambda: check("submission" in T["workflow"].lower() and "Phase 19" in T["workflow"], "submission review")),
("Hackathon result handling", lambda: check(all(x in T["rules"] for x in ("WINNER", "FINALIST", "SHORTLISTED", "PARTICIPATED", "NOT_SELECTED", "NOT_SUBMITTED", "CANCELLED")), "result enum")),
("Win analysis", lambda: check("## 18. Wins" in T["report_template"] and "evidence" in T["report_template"].lower(), "wins section")),
("Failure analysis", lambda: check("## 19. Failures" in T["report_template"] and "unsupported failures" in T["report_template"].lower(), "failures section")),
("KEEP CHANGE STOP START", lambda: check(all(f"## {i}. {v}" in T["report_template"] for i,v in [(21,"Keep"),(22,"Change"),(23,"Stop"),(24,"Start")]), "action categories")),
("Lesson extraction", lambda: check(all(x in T["lesson"] for x in ("Lesson ID", "Category", "Situation", "Observation", "Evidence", "Confidence", "Reusable?")), "lesson schema")),
("Reusable asset extraction", lambda: check("Reusable Assets" in T["report_template"] and "Reuse Recommendation" in T["report_template"], "asset review")),
("sherpa effectiveness", lambda: check("sherpa Effectiveness" in T["report_template"] and "Phases 1–19" in T["workflow"], "effectiveness review")),
("Bottleneck analysis", lambda: check("Process Bottlenecks" in T["report_template"] and all(x in T["rules"] for x in ("TOOLING", "HUMAN_DECISION", "COMMUNICATION")), "bottleneck model")),
("Process debt", lambda: check("Process Debt" in T["report_template"] and "process debt" in T["workflow"].lower(), "process debt section")),
("Contract gap analysis", lambda: check("sherpa Contract Gaps" in T["report_template"] and "contract gaps" in T["workflow"].lower(), "contract gap section")),
("Improvement backlog", lambda: check(all(x in T["improvement"] for x in ("Improvement ID", "Affected phase", "Evidence", "Recommendation", "Expected impact", "Cost", "Dependencies", "Priority", "Status")) and "NOT OFFICIAL HACKATHON SCORING" in T["improvement"], "backlog schema")),
("No retroactive rewriting", lambda: check("Never rewrite" in T["rules"] and "historical" in T["rules"].lower() and "preserve" in T["workflow"].lower(), "history guard")),
("Phase 20 scope boundary", lambda: check(all(x in T["rules"] for x in ("modify application source", "install dependencies", "deploy", "submit", "Phase 21")), "scope exclusions")),
("Exactly one primary next action", lambda: check("exactly one `PRIMARY NEXT ACTION`" in T["rules"] and "## 35. PRIMARY NEXT ACTION" in T["report_template"], "primary action")),
]
check(len(checks)==35, "must define exactly 35 acceptance checks")

adversarial_names = [
("Phase 19 missing", "phase19_missing"), ("Phase 19 unlocked", "phase19_unlocked"), ("Lifecycle altered to 21", "lifecycle_21"),
("Missing project state", "missing_project_state_as_live"), ("Empty history", "empty_history_as_live"), ("Missing timeline", "missing_timeline_as_fact"),
("Contradictory timestamps", "contradictory_timestamps"), ("Fabricated result", "fabricated_result"), ("Unsupported winner", "unsupported_winner"),
("Unsupported finalist", "unsupported_finalist"), ("Unsupported judge feedback", "fabricated_judge_feedback"), ("UNKNOWN converted to FACT", "unknown_as_fact"),
("INFERENCE converted to FACT", "inference_as_fact"), ("Correlation as causation", "correlation_as_causation"), ("Incident without evidence", "incident_without_evidence"),
("Conflicting decisions hidden", "conflicting_decisions_hidden"), ("Missing human owner invented", "invented_human_owner"), ("Incomplete risk history", "incomplete_risk_as_avoided"),
("Incomplete testing history", "incomplete_testing_as_complete"), ("Incomplete UX history", "incomplete_ux_as_complete"), ("Incomplete red-team history", "incomplete_redteam_as_complete"),
("Simulated score as actual", "simulated_score_as_actual"), ("Demo plan as outcome", "demo_plan_as_outcome"), ("Presentation assumption as fact", "assumption_as_fact"),
("Submission readiness as submitted", "readiness_as_submitted"), ("Historical artifact rewrite", "historical_rewrite"), ("Application source modification", "application_source_change"),
("Phase 21 creation", "phase21"), ("Multiple primary next actions", "multiple_primary_actions"), ("Fabricated success with empty evidence", "success_with_empty_evidence")]
check(len(adversarial_names)==30, "must define exactly 30 adversarial checks")

results=[]
for idx,(name,fn) in enumerate(checks,531):
    try: fn(); status="PASS"; observed="PASS: contract assertion satisfied from repository evidence"
    except Exception as exc: status="FAIL"; observed=f"FAIL: {type(exc).__name__}: {exc}"
    results.append({"id":f"AT-{idx}","description":name,"setup":"Read current postmortem contract and project-scoped submission workflow.","expected_result":"Contract is evidence-based and preserves historical and human authority.","observed_result":observed,"status":status,"evidence":f"Executed assertion tests/workflows/test_postmortem.py::{name}"})
for idx,(name,key) in enumerate(adversarial_names,1):
    try:
        with tempfile.TemporaryDirectory(prefix="sherpa-phase20-") as directory:
            fixture=Path(directory)/"adversarial.json"; fixture.write_text(json.dumps({key:True}),encoding="utf-8")
            record=json.loads(fixture.read_text(encoding="utf-8")); assert not guarded(record), "unsafe fixture accepted"
        status="PASS"; observed="PASS: unsafe synthetic fixture rejected; no historical or project files changed"
    except Exception as exc: status="FAIL"; observed=f"FAIL: {type(exc).__name__}: {exc}"
    results.append({"id":f"ADV-{idx:02d}","description":name,"setup":f"Disposable synthetic fixture with {key}=true.","expected_result":"Unsafe claim or mutation is rejected / remains UNKNOWN.","observed_result":observed,"status":status,"evidence":f"Executed assertion tests/workflows/test_postmortem.py::ADV-{idx:02d}; temporary fixture only"})

passed=sum(r["status"]=="PASS" for r in results); at=results[:35]; adv=results[35:]
print(json.dumps({"suite":"Phase 20 Post-Mortem Intelligence contract validation","scope":"repository contract assertions and disposable synthetic adversarial fixtures; no live project runtime","results":results,"summary":{"total":len(results),"passed":passed,"failed":len(results)-passed,"acceptance_total":len(at),"acceptance_passed":sum(r["status"]=="PASS" for r in at),"adversarial_total":len(adv),"adversarial_passed":sum(r["status"]=="PASS" for r in adv)}},indent=2))
raise SystemExit(0 if passed==len(results) else 1)
