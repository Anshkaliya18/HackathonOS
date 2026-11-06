# Implementation Changelog

## 2026-11-06 — Distribution architecture repair

- Added `scripts/build-distributions.py` as a deterministic builder for one shared canonical Sherpa resource tree and Claude Code, OpenCode, Codex, and Kilo client entrypoints.
- Added explicit generated metadata separating Agent Skills from native slash commands; Codex is skills-only, and Kilo command prompts make no undocumented argument-substitution assumption.
- Added `distribution/cli/installer.py` for client detection, global/project/custom config roots, transactional install/rollback, managed uninstall, version downgrade protection, and distinct filesystem verification states.
- Added `install`, `verify-install`, and managed client uninstall options to the distribution CLI; retained `prepare-agent-package.py` as a backwards-compatible build entrypoint.
- Changed npm packaging to include generated client distributions and the installer engine; `prepack` now builds only `distribution/generated/` instead of refreshing portable duplicate trees.
- Updated the release builder to include generated distributions and installer engine in release archives and normalize archive timestamps/ownership.
- Added architecture and installer tests for deterministic build output, manifest/native adapter consistency, resource resolution outside the repository, paths with spaces, idempotent installs, upgrade/uninstall ownership, and missing resources.
- Updated standalone uninstaller wrappers to delegate to the receipt-aware engine when distributed with it, while retaining their legacy one-file fallback.
- Replaced the npm install dry-run's legacy fixed paths with a generated client-aware preview, and corrected installation documentation to distinguish native commands and actual release verification.

### Validation at this stage

- `python -m pytest tests/installer -q`: 65 passed, 1 skipped (Windows Kilo temp-directory handle).
- `python tests/run_all.py`: all five phases passed (23 test files) on final implementation.
- Built release artifacts twice and confirmed all 11 artifact SHA-256 values were identical.
- Windows project-local PowerShell and Git Bash installation checks passed at filesystem/resource level; OpenCode and Kilo skill listing returned Sherpa on the Windows host. Interactive command invocation remains unverified.
- No release was published. Linux and macOS client/runtime integration remain untested.

## 2026-11-07 — 2.0.8 release preparation

- Bumped npm, CLI, Agent Skill/plugin, and release manifest metadata to 2.0.8 after confirming npmjs latest was 2.0.7 and the matching prior Git tag existed.
- Updated README, VitePress installation/compatibility/architecture pages, release instructions, and 2.0.8 changelog entry.
- `npm run docs:check`, `npm run docs:build`, generated distribution checks, and the 2.0.8 installer suite passed. The supported full test runner passed all five phases (23 files).
- Built the 2.0.8 release artifact set twice; all 11 artifact hashes matched.
- Registry authentication was unavailable to npm and GitHub CLI at preparation time; publication is not claimed.
