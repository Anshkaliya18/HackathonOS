# Sherpa Changelog

## Unreleased

### Fixed

- PowerShell installer now passes the parsed manifest object correctly, handles the empty `$PSCommandPath` produced by `irm | iex`, reports the underlying failure, and rolls back partial skill installs.

## [2.0.0] — 2026-11-04

### Changed

- HackathonOS is now Sherpa: command, CLI, package, installer, state, and documentation identities use the new name.
- Project state now uses `.sherpa/`. Existing `.hackathon/` data is read as a one-release fallback; `sherpa migrate` copies it without deleting or overwriting data.
- The CLI package is named `sherpa-skill` because the `sherpa` npm package name is already taken.
- The project version is 2.0.0 because this is a public product and command namespace rename with a new project-state path.
- New installs verify Sherpa before retiring managed HackathonOS skill folders. The deprecated `hackathonos` launcher remains as a forwarding shim.
- The docs site now follows the ascent field-guide design, with a manifest-backed command explorer and explicit compatibility status.

## [1.0.0] — 2026-11-04

### Fixed

- CLI downloads use partial files and verify declared Content-Length before accepting the completed file.
- CLI manifest fetching retries transient HTTP/network failures and reports GitHub rate-limit responses clearly.
- CLI updates and shell/PowerShell installs now fail closed when a release archive checksum is absent.

### Added

- `sherpa audit` and report-only-by-default `sherpa clean` for generated debris limited to managed skill installations.
- Beginner and maintainer documentation for quickstart, configuration, agent compatibility, commands, workflows, architecture, troubleshooting, and contribution.

### Added

- One-command installers for Linux / macOS / Git Bash (`install.sh`) and
  Windows PowerShell 5.1+ / 7+ (`install.ps1`).
- Automatic detection of operating system, architecture, and installed agent
  environments (Claude Code, OpenCode).
- Installation into the standard skill directories:
  - `~/.claude/skills/sherpa/` (Claude Code)
  - `~/.config/opencode/skills/sherpa/` (OpenCode)
- Support for installing into one, the other, or both environments
  simultaneously.
- Versioned release downloads from GitHub Releases with SHA-256 checksum
  verification before extraction.
- Path-traversal protection during archive extraction.
- `sherpa` CLI (stdlib Python): `--version`, `update`, `uninstall`,
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

- All existing sherpa skill functionality (workflows, rules, templates,
  command manifest, router, configuration manager, idea engine) remains
  intact. No existing files were modified or removed.

### Security

- HTTPS-only downloads; SHA-256 verification; no administrator privileges; no
  secret collection; non-destructive installation.
