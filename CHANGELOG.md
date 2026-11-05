# Sherpa Changelog

## [2.0.7] — 2026-11-06

### Added

- A shared Agent Skill entry for `.agents/skills/`, alongside native Codex, Gemini CLI, and Qwen Code plugin/extension manifests.
- Claude Code marketplace metadata and package layouts for Claude, Codex, Gemini CLI, and Qwen Code.
- Agent installation and release documentation that uses the public, unscoped npm package name.

### Changed

- The release archive and npm package now include skill and plugin files with the workflows they reference.
- Runtime status remains explicitly unverified for new and updated agent adapters until each host is tested.

## [2.0.6] — 2026-11-06

### Fixed

- The npm `sherpa` command now forwards management commands to the bundled CLI, including `--version`, `update`, `doctor`, `audit`, `clean`, and `help`.
- Unknown CLI commands now show the management CLI's usage and error instead of the npm installer's limited command list.
- `sherpa doctor` now accepts the release manifest's canonical `Sherpa` project name.

## [2.0.5] — 2026-11-06

### Fixed

- Windows npm uninstall now correctly checks CLI files before reporting or removing them.
- The repository package metadata, lockfile, GitHub Packages mirror, and npmjs.org package are aligned at version 2.0.5.

## [2.0.4] — 2026-11-05

### Added

- GitHub Actions publishing for the scoped npm package to GitHub Packages, tied to matching version tags.

## [2.0.1] — 2026-11-05

### Fixed

- PowerShell architecture detection now handles a null `.NET` architecture value and safely falls back to Windows environment/WMI data.
- PowerShell installation supports the `irm | iex` entry point, passes parsed release metadata correctly, reports the underlying failure, and rolls back partial skill installs.

## [2.0.0] — 2026-11-04

### Changed

- sherpa is now Sherpa: command, CLI, package, installer, state, and documentation identities use the new name.
- Project state now uses `.sherpa/`. Existing `.hackathon/` data is read as a one-release fallback; `sherpa migrate` copies it without deleting or overwriting data.
- The CLI package is named `sherpa-skill` because the `sherpa` npm package name is already taken.
- The project version is 2.0.0 because this is a public product and command namespace rename with a new project-state path.
- New installs verify Sherpa before retiring managed sherpa skill folders. The deprecated `sherpa` launcher remains as a forwarding shim.
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
