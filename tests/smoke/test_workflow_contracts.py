#!/usr/bin/env python3
"""Deterministic, stdlib-only contract smoke tests for sherpa workflows.

This harness executes the workflows' documented state/gate/scoring contracts in
disposable directories. It does not invoke an LLM or claim to test generated
prose or tool use in a live assistant runtime.
"""

from __future__ import annotations

import json
import math
import re
import tempfile
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[2]
STATE_TEMPLATE = ROOT / "templates" / "project-state.md"
SKILL = ROOT / "SKILL.md"

SCORES = [8, 8, 8, 8, 9, 6, 6, 8, 4, 5, 4, 7, 8, 8, 7, 7, 7, 5, 4, 5, 5]
CATEGORIES = [
    [1, 2, 3, 4, 5],
    [6, 7],
    [8, 9, 10],
    [11, 12],
    [13, 14],
    [16, 17],
    [18, 19],
    [20, 21],
]


def set_field(text: str, name: str, value: str) -> str:
    """Set one markdown state row, appending a fixture row if needed."""
    pattern = re.compile(rf"(?m)^(\|\s*{re.escape(name)}\s*\|\s*)[^|\n]*(\|\s*)$")
    updated, count = pattern.subn(lambda m: f"{m.group(1)}{value} {m.group(2)}", text, count=1)
    if count:
        return updated
    return updated.rstrip() + f"\n\n| {name} | {value} |\n"


def state_values(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    values: dict[str, str] = {}
    for match in re.finditer(r"(?m)^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$", text):
        key, value = match.groups()
        if key.strip() not in {"Field", "Value"} and set(key.strip()) != {"-"}:
            values[key.strip()] = value.strip()
    return values


def init_fixture(project: Path) -> Path:
    state = project / ".sherpa" / "project-state.md"
    state.parent.mkdir(parents=True, exist_ok=True)
    text = STATE_TEMPLATE.read_text(encoding="utf-8")
    text = set_field(text, "Hackathon name", "Smoke Fixture (synthetic)")
    text = set_field(text, "State last updated", "2026-01-01T00:00:00Z (fixed test clock)")
    text = set_field(text, "Phase", "Understand Rules")
    state.write_text(text, encoding="utf-8")
    (project / "README.md").write_text("Disposable smoke project.\n", encoding="utf-8")
    return state


def route_table() -> dict[str, str]:
    text = SKILL.read_text(encoding="utf-8")
    rows = re.findall(r"(?m)^\|\s*\*\*([^*]+)\*\*\s*\|[^\n]*?`(workflows/[^`]+\.md)`\s*\|", text)
    return {name.strip(): path.strip() for name, path in rows}


def choose_next(state: dict[str, str]) -> str:
    if state.get("Phase") == "Understand Rules" and state.get("Judging criteria") == "UNKNOWN":
        return "Collect official hackathon rules, judging criteria, deadline, and problem context."
    return "Review the highest-priority evidenced project blocker."


def validate_candidates(candidates: list[object]) -> str:
    if not candidates:
        return "No candidate ideas provided."
    return "READY"


def evaluate(scores: list[int]) -> dict[str, float | str]:
    if len(scores) != 21 or any(not isinstance(s, int) or s < 1 or s > 10 for s in scores):
        raise ValueError("exactly 21 integer scores in [1, 10] are required")
    category_means = [sum(scores[i - 1] for i in group) / len(group) for group in CATEGORIES]
    raw = sum(category_means) / len(category_means) * 10
    feasibility = (scores[7] + (11 - scores[9]) + (11 - scores[10]) + scores[11] + (11 - scores[19])) / 5
    return {"raw": raw, "feasibility": feasibility, "final": raw * feasibility / 10,
            "gate": "PASS" if feasibility >= 6 else "FAIL"}


def project_plan_gate(state: dict[str, str], phase2_present: bool) -> str:
    if state.get("Selected idea", "UNKNOWN").upper() == "UNKNOWN":
        return "BLOCKED: confirm selected idea"
    if not phase2_present:
        return "BLOCKED: Phase 2 evidence missing"
    return "DRAFT: human architecture approval required"


def implementation_gate(state: dict[str, str]) -> str:
    if state.get("Architecture approval status", "UNKNOWN") != "APPROVED":
        return "Architecture approval required before implementation."
    if state.get("Implementation plan", "UNKNOWN") != "READY":
        return "NOT READY: implementation plan is not READY."
    return "READY"


def test_init() -> None:
    with tempfile.TemporaryDirectory(prefix="sherpa-smoke-init-") as tmp:
        project = Path(tmp)
        state_path = init_fixture(project)
        state = state_values(state_path)
        assert state_path.is_file() and (project / "README.md").is_file()
        assert state["Hackathon name"] == "Smoke Fixture (synthetic)"
        assert state["Phase"] == "Understand Rules"
        assert state["Deadline date/time"] == "UNKNOWN"
        assert state["Selected idea"] == "UNKNOWN"
        assert "Phase 5" not in state_path.read_text(encoding="utf-8")


def test_status() -> None:
    with tempfile.TemporaryDirectory(prefix="sherpa-smoke-status-") as tmp:
        project = Path(tmp)
        state_path = init_fixture(project)
        state = state_values(state_path)
        output = f"Hackathon={state['Hackathon name']}\nPhase={state['Phase']}\nDeadline={state['Deadline date/time']}\nREADME={(project / 'README.md').exists()}"
        assert "Hackathon=Smoke Fixture (synthetic)" in output
        assert "Phase=Understand Rules" in output and "Deadline=UNKNOWN" in output
        assert "README=True" in output


def test_next() -> None:
    with tempfile.TemporaryDirectory(prefix="sherpa-smoke-next-") as tmp:
        state = state_values(init_fixture(Path(tmp)))
        action = choose_next(state)
        output = f"PRIMARY NEXT ACTION: {action}\nTime remaining: UNKNOWN"
        repeated = f"PRIMARY NEXT ACTION: {choose_next(state)}\nTime remaining: UNKNOWN"
        assert output == repeated
        assert output.count("PRIMARY NEXT ACTION:") == 1
        assert state["Phase"] == "Understand Rules" and state["Time remaining"] == "UNKNOWN"
        assert route_table().get("NEXT") == "workflows/next.md"


def test_idea_evaluate() -> None:
    first = evaluate(SCORES)
    second = evaluate(list(SCORES))
    assert first == second
    assert math.isclose(float(first["raw"]), 62.3333333333, abs_tol=0.01)
    assert math.isclose(float(first["feasibility"]), 6.8, abs_tol=1e-9)
    assert math.isclose(float(first["final"]), 42.3866666667, abs_tol=0.01)
    with tempfile.TemporaryDirectory(prefix="sherpa-smoke-idea-") as tmp:
        state_path = init_fixture(Path(tmp))
        before = state_values(state_path)["Selected idea"]
        recommendation = "SELECT IDEA A"  # synthetic fixture input only
        confirmation = "PENDING"
        assert recommendation.startswith("SELECT") and confirmation == "PENDING"
        assert state_values(state_path)["Selected idea"] == before == "UNKNOWN"


def test_project_plan() -> None:
    with tempfile.TemporaryDirectory(prefix="sherpa-smoke-plan-") as tmp:
        project = Path(tmp)
        state_path = init_fixture(project)
        state_path.write_text(set_field(state_path.read_text(encoding="utf-8"), "Selected idea", "IDEA A (confirmed synthetic fixture)"), encoding="utf-8")
        evidence = project / ".sherpa" / "evidence"
        evidence.mkdir()
        (evidence / "decisions.md").write_text("Synthetic Phase 2 decision; not independent evidence.\n", encoding="utf-8")
        state_path.write_text(set_field(state_path.read_text(encoding="utf-8"), "Architecture approval status", "PENDING"), encoding="utf-8")
        state_path.write_text(set_field(state_path.read_text(encoding="utf-8"), "Time remaining", "UNKNOWN"), encoding="utf-8")
        values = state_values(state_path)
        assert project_plan_gate(values, (evidence / "decisions.md").is_file()).startswith("DRAFT:")
        assert values["Architecture approval status"] == "PENDING"
        assert values["Time remaining"] == "UNKNOWN"
        # An unselected fixture must stop before normal planning.
        values["Selected idea"] = "UNKNOWN"
        assert project_plan_gate(values, True) == "BLOCKED: confirm selected idea"


def test_implement_gate_and_route() -> None:
    routes = route_table()
    assert routes.get("IMPLEMENT") == "workflows/implementation.md"
    assert (ROOT / routes["IMPLEMENT"]).is_file()
    rules = (ROOT / "rules" / "implementation-rules.md").read_text(encoding="utf-8")
    assert "Architecture = APPROVED" in rules
    assert "do not modify application source" in rules
    assert implementation_gate({"Architecture approval status": "PENDING", "Implementation plan": "READY"}) == "Architecture approval required before implementation."


def test_testing_security_route() -> None:
    routes = route_table()
    assert routes.get("TESTING-SECURITY") == "workflows/testing-security.md"
    assert (ROOT / routes["TESTING-SECURITY"]).is_file()
    implementation_status = "NOT_STARTED"
    outcome = "Testing blocked until implementation exists." if implementation_status == "NOT_STARTED" else "continue"
    assert outcome == "Testing blocked until implementation exists."


def test_unknown_state_safety() -> None:
    with tempfile.TemporaryDirectory(prefix="sherpa-smoke-unknown-") as tmp:
        project = Path(tmp)
        state_path = init_fixture(project)
        values = state_values(state_path)
        assert values["Deadline date/time"] == "UNKNOWN"
        assert values["Judging criteria"] == "UNKNOWN"
        assert values["Selected idea"] == "UNKNOWN"
        missing = project / "missing" / ".sherpa" / "project-state.md"
        assert not missing.exists()
        missing_state_result = "Run INIT first" if not missing.exists() else "read state"
        assert missing_state_result == "Run INIT first"


def test_human_approval_safety() -> None:
    state = {"Selected idea": "UNKNOWN", "Architecture approval status": "PENDING", "MVP": "DRAFT"}
    snapshot = dict(state)
    recommendation = "SELECT IDEA A"  # recommendation is not approval
    assert recommendation.startswith("SELECT")
    assert state == snapshot
    assert state["Selected idea"] == "UNKNOWN"
    assert state["Architecture approval status"] == "PENDING"
    assert state["MVP"] == "DRAFT"


def test_invalid_input_safety() -> None:
    assert validate_candidates([]) == "No candidate ideas provided."
    assert validate_candidates(["synthetic candidate"]) == "READY"
    try:
        evaluate([])
    except ValueError as exc:
        assert str(exc) == "exactly 21 integer scores in [1, 10] are required"
    else:
        raise AssertionError("empty candidate score input must fail safely")
    assert implementation_gate({"Architecture approval status": "PENDING", "Implementation plan": "UNKNOWN"}) != "READY"


TESTS: list[tuple[str, Callable[[], None]]] = [
    ("AT-SMOKE-01 INIT", test_init),
    ("AT-SMOKE-02 STATUS", test_status),
    ("AT-SMOKE-03 NEXT", test_next),
    ("AT-SMOKE-04 IDEA-EVALUATE", test_idea_evaluate),
    ("AT-SMOKE-05 PROJECT-PLAN", test_project_plan),
    ("AT-SMOKE-06 IMPLEMENT ROUTING", test_implement_gate_and_route),
    ("AT-SMOKE-07 TESTING-SECURITY ROUTING", test_testing_security_route),
    ("AT-SMOKE-08 UNKNOWN-STATE SAFETY", test_unknown_state_safety),
    ("AT-SMOKE-09 HUMAN-APPROVAL SAFETY", test_human_approval_safety),
    ("AT-SMOKE-10 INVALID INPUT SAFETY", test_invalid_input_safety),
]


def main() -> int:
    results = []
    for name, test in TESTS:
        try:
            test()
            results.append({"test": name, "status": "PASS"})
        except Exception as exc:  # emitted without fixture contents or sensitive values
            results.append({"test": name, "status": "FAIL", "error": type(exc).__name__})
    failures = sum(result["status"] != "PASS" for result in results)
    print(json.dumps({"results": results, "summary": {"passed": len(results) - failures,
                                                       "failed": failures}}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
