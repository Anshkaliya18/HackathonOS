# HackathonOS Changelog

## [1.0.0] — 2026-11-04

### Added

- One-command installers for Linux / macOS / Git Bash (`install.sh`) and
  Windows PowerShell 5.1+ / 7+ (`install.ps1`).
- Automatic detection of operating system, architecture, and installed agent
  environments (Claude Code, OpenCode).
- Installation into the standard skill directories:
  - `~/.claude/skills/hackathonos/` (Claude Code)
  - `~/.config/opencode/skills/hackathonos/` (OpenCode)
- Support for installing into one, the other, or both environments
  simultaneously.
- Versioned release downloads from GitHub Releases with SHA-256 checksum
  verification before extraction.
- Path-traversal protection during archive extraction.
- `hackathonos` CLI (stdlib Python): `--version`, `update`, `uninstall`,
  `doctor`, `help`.
- Update system with previous-installation backup and automatic rollback on
  failure; user project data and `.hackathon/` state preserved.
- Safe uninstaller with confirmation prompt; removes only installation files.
- Uninstallers (`uninstall.sh`, `uninstall.ps1`).
- Release distribution architecture (`distribution/release/manifest.json`,
  `distribution/release/checksums.txt`).
- Documentation: `INSTALLATION.md`, `README.md`, `RELEASE.md`, `SECURITY.md`,
  `CHANGELOG.md`.
- Automated installer tests under `tests/installer/` (mocked downloads).

### Preserved

- All existing HackathonOS skill functionality (workflows, rules, templates,
  command manifest, router, configuration manager, idea engine) remains
  intact. No existing files were modified or removed.

### Security

- HTTPS-only downloads; SHA-256 verification; no administrator privileges; no
  secret collection; non-destructive installation.
