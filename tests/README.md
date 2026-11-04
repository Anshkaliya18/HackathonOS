# Test suite map

Tests are grouped by the behavior they cover. Workflow contract suites use descriptive `test_*.py` names; their internal lifecycle references remain where they describe HackathonOS behavior.

| Area | Location | Purpose |
|---|---|---|
| Workflow contracts | `tests/workflows/` | Acceptance and adversarial contract checks for each workflow |
| Workflow smoke | `tests/smoke/` | Cross-workflow state, routing, scoring, and approval-gate smoke checks |
| Commands | `tests/commands/` | Command registry and routing behavior |
| Configuration | `tests/configuration/` | Configuration manager and validation behavior |
| Idea engine | `tests/ideas/` | Idea evaluation checks |
| Installer and CLI | `tests/installer/` | Installer scripts and distribution CLI tests |
| Regression | `tests/regression/` | Semantic verification and benchmark regressions |

Run every self-contained Python test file in an isolated process with:

```powershell
python tests/run_all.py
```

The standalone contract harnesses print machine-readable JSON. For example:

```powershell
python tests/workflows/test_submission.py
python tests/smoke/test_workflow_contracts.py
```

The installer tests use pytest:

```powershell
python -m pytest tests/installer
```

Historical repository audit reports were removed. Project audits created while using HackathonOS still belong under the active project's `.hackathon/` directory.
