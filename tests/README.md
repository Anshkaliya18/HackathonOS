# Test phases

Run checks from fastest and most focused to broader coverage. Each phase maps to the existing topic folders, so tests stay grouped by what they verify while the run order is visible and selectable.

| Phase | Name | Test folders | Checks |
|---:|---|---|---|
| 1 | Smoke | `smoke/` | Cross-workflow state, routing, scoring, and approval gates |
| 2 | Core | `commands/`, `configuration/`, `ideas/` | Command behavior, configuration, and idea evaluation |
| 3 | Workflows | `workflows/` | Workflow acceptance and adversarial contracts |
| 4 | Regression | `regression/` | Release-note, benchmark, and semantic regressions |
| 5 | Distribution | `installer/` | Installer and CLI behavior, run with pytest |

## Run phases

Run the complete suite in phase order:

```powershell
python tests/run_all.py
```

Run one phase while iterating:

```powershell
python tests/run_all.py --phase smoke
python tests/run_all.py --phase core
python tests/run_all.py --phase workflows
python tests/run_all.py --phase regression
python tests/run_all.py --phase distribution
```

The first four phases execute each standalone Python suite in an isolated process. The distribution phase uses pytest so its test functions are actually collected and run.

## Run a single suite

Standalone contract harnesses print machine-readable JSON and exit non-zero on failure:

```powershell
python tests/workflows/test_submission.py
python tests/smoke/test_workflow_contracts.py
```

Run installer checks directly with pytest:

```powershell
python -m pytest tests/installer
```

Project review and audit records created while using Sherpa belong under the active project's `.sherpa/` directory.
