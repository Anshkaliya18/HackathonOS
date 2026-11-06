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
| Kilo live skill discovery | PASS, teardown issue | CLI exited successfully and output contained Sherpa. On Windows the test's temporary project remained locked after process exit. Automated test now skips this OS-specific case; no claim of Windows Kilo workflow execution. |
| Claude live invocation | NOT VERIFIED | `claude -p /sherpa-status` in an isolated project did not return within 60 seconds; no success inferred. |
| PowerShell installer | PASS (filesystem) | Project-local Codex files/resources validated; CLI/runtime labels remained `NOT RUN`. |
| Shell installer syntax and local install | PASS (syntax/filesystem) | `bash -n`; Git Bash project install into path with spaces succeeded. |
| Receipt-aware uninstaller wrappers | PASS | PowerShell and Git Bash each removed a temporary Codex install with a path containing spaces. |
| Linux install/uninstall | NOT RUN | No Linux runtime available. |
| Claude/Codex live invocation; OpenCode/Kilo command execution | NOT RUN | Requires interactive host behavior; discovery tests are not invocation tests. |

## Suites

- `python -m pytest tests/installer -q`: **65 passed, 1 skipped** on Sherpa 2.0.8. The skip is the Windows Kilo cleanup case described above.
- `python tests/run_all.py`: **all five phases passed; 23 test files discovered** on the 2.0.8 tree. The distribution phase reported PASS.
- A direct `python -m pytest -q` attempt is not a supported runner for this repository: it imports standalone harnesses that raise `SystemExit` at module scope, producing a collection internal error. The repository-supported `tests/run_all.py` runs those harnesses in separate processes and passed.

Warnings observed: `requests` dependency compatibility warning and pytest-asyncio loop-scope deprecation warning. Neither caused a test failure.

## Boundaries

These are test observations for this host and current executable versions only. No publish was performed. CLI discovery is distinct from command picker visibility, command execution, or workflow correctness.
