# Phase 6 Smoke Harness

Run from the repository root:

```powershell
python tests/phase6/run_smoke.py
```

## Environment

- Python 3.10 or newer
- Python standard library only; no install step or network access
- Windows, macOS, and Linux are supported

The command prints machine-readable JSON results and exits non-zero if any required smoke test fails. Every test creates a disposable temporary directory and removes it on completion. The harness does not inspect or modify the application's source tree.

## Scope

This is a deterministic contract-level smoke harness for the Markdown workflow specifications. It exercises state initialization/reading, deterministic score and gate logic, human-approval constraints, invalid/unknown-state handling, and routing declarations. The repository contains no executable LLM workflow runtime; this harness does not invoke an assistant, validate generated natural-language prose, or prove that every host model will follow the workflow text. Those behaviors remain covered only by the separately recorded manual workflow operations.

Scores and candidate ideas are fixed synthetic test inputs and are not product recommendations or real hackathon evaluation results.
