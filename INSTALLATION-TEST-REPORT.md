# Installation Test Report

**Date:** 2026-11-07  
**Host:** Windows 11, PowerShell, Python 3.11; Git Bash and Node/npm available.

## Results

| Test | Result | Evidence |
|---|---|---|
| Generated distribution determinism/check | PASS | `python scripts/build-distributions.py --check` and suite check. |
| Install to project directory containing spaces | PASS | OpenCode installer engine validated skill, commands, and every referenced resource. |
| Idempotent install and owned uninstall | PASS | Repeat install preserved content; uninstall removed only managed Sherpa files/receipt. |
| Upgrade/downgrade guard | PASS | Refused a simulated downgrade without altering installed skill or receipt. |
| Transaction rollback | PASS | Simulated adapter copy failure restored prior files and install marker. |
| Shared Codex/Kilo Agent Skill ownership | PASS | Removing one client's receipt preserved shared skill until last owner removed. |
| Missing resource validation | PASS | Missing workflow produced a validation failure naming the unresolved file. |
| Clean npm pack/install | PASS | `npm pack` then offline install into a clean prefix; packaged launcher installed generated Codex skill and aliases. |
| Client-aware npm dry-run | PASS | Direct CLI regression test confirmed generated target paths are printed and no destination files are created. |
| OpenCode live skill discovery | PASS | `opencode debug skill --pure` in an isolated project listed Sherpa. |
| Codex live skill discovery | PASS | `codex debug prompt-input` emitted valid JSON containing the installed Sherpa skill in an isolated project. |
| OpenCode command registration | PASS | `opencode debug config --pure` in an isolated project included the generated `sherpa-*` command entries. |
| Kilo skill and command discovery | PASS, teardown issue | `kilo debug skill --pure` listed Sherpa, and `kilo debug config --pure` included the generated `sherpa-*` workflows. Kilo retained a handle on its Windows project directory after process exit. |
| Claude skill invocation | BLOCKED by model endpoint | `claude -p /sherpa-help` reached the configured custom provider, which returned HTTP 400: the selected free model is unavailable. A paid model was suggested; it was not used. |
| PowerShell installer | PASS (filesystem) | Project-local Codex files/resources validated; CLI/runtime labels remained `NOT RUN`. |
| Shell installer syntax and local install | PASS (syntax/filesystem) | `bash -n`; Git Bash project install into path with spaces succeeded. |
| Receipt-aware uninstaller wrappers | PASS | PowerShell and Git Bash each removed a temporary Codex install with a path containing spaces. |
| Linux install/uninstall | NOT RUN | No Linux runtime available. |
| Claude/Codex model invocation; OpenCode/Kilo command execution | NOT VERIFIED | Codex model invocation was not run; Claude is blocked by the configured model endpoint. OpenCode/Kilo command files are registered, but their workflow execution was not tested. |

## Suites

- `python -m pytest tests/installer -q`: **65 passed, 1 skipped** on Sherpa 2.0.8. The skip is the Windows Kilo cleanup case described above.
- `python tests/run_all.py`: **all five phases passed; 23 test files discovered** on the 2.0.8 tree. The distribution phase reported PASS.
- A direct `python -m pytest -q` attempt is not a supported runner for this repository: it imports standalone harnesses that raise `SystemExit` at module scope, producing a collection internal error. The repository-supported `tests/run_all.py` runs those harnesses in separate processes and passed.

Warnings observed: `requests` dependency compatibility warning and pytest-asyncio loop-scope deprecation warning. Neither caused a test failure.

## Boundaries

These are test observations for this host and current executable versions only. No publish was performed. CLI discovery is distinct from command picker visibility, command execution, or workflow correctness.
