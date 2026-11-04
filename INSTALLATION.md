# Installation

## One-command installation

Windows PowerShell:

```powershell
irm https://raw.githubusercontent.com/Anshkaliya18/HackathonOS/main/distribution/install.ps1 | iex
```

Linux/macOS:

```bash
curl -fsSL https://raw.githubusercontent.com/Anshkaliya18/HackathonOS/main/distribution/install.sh | bash
```

The installers download the latest GitHub release and verify checksums before extracting. Release assets are available at `https://github.com/Anshkaliya18/HackathonOS/releases`.

## Local/source use

Clone or open this repository in a compatible agent and use the repo-local integration files. This does not install the standalone `hackathonos` management CLI globally. For a project-local agent setup, use the checked-in repo files; no dedicated `hackathonos install --local` command exists yet.

## Installer scripts from a source checkout

Linux/macOS:

```bash
bash distribution/install.sh --both
```

Windows PowerShell:

```powershell
& .\distribution\install.ps1 -Both
```

The standard targets are Claude Code (`~/.claude/skills/hackathonos/`) and OpenCode (`~/.config/opencode/skills/hackathonos/`). Use `--claude` / `-Claude` or `--opencode` / `-OpenCode` to select one. The installer checks the downloaded archive and skill structure, backs up prior skill folders, and validates the installed result. CLI locations are `~/.local/bin/` on Unix and `%USERPROFILE%\AppData\Local\HackathonOS\bin` on Windows.

## Options and environment

Shell installer options: `--claude`, `--opencode`, `--both`, `--version VERSION`, `--manifest-url URL`, `--no-cli`, `--no-path`, `--yes`, `--help`. PowerShell parameters: `-Claude`, `-OpenCode`, `-Both`, `-Version`, `-ManifestUrl`, `-NoCli`, `-NoPath`, `-Yes`. The experimental project-dir switch is not supported and returns an error.

Environment variables include `HACKATHONOS_RELEASE_MANIFEST_URL`, `HACKATHONOS_VERSION`, `HACKATHONOS_INSTALL_CLAUDE`, `HACKATHONOS_INSTALL_OPENCODE`, `HACKATHONOS_INSTALL_CLI`, and `HACKATHONOS_NO_PATH`.

## CLI commands

`hackathonos --version`, `update`, `doctor`, `audit`, `clean --dry-run`, and `uninstall`. `clean` reports by default; removal requires `--yes`. It is limited to recognized generated debris inside managed skill folders. Uninstall prompts unless `--yes` is supplied and preserves `.hackathon/` project data.

## Updating and uninstalling

Use `hackathonos update` to download a checksummed release and replace installed skill directories with backup/rollback. Use `hackathonos uninstall` to remove recognized global skill and CLI files. Uninstallers exist at `distribution/uninstall.sh` and `distribution/uninstall.ps1`; they are local scripts and require a published, trusted hosting URL before remote one-line use.

## Version pinning

`HACKATHONOS_VERSION` / `--version` is present in the shell installer interface, but the current manifest format does not resolve arbitrary historical versions. Treat pinning as unsupported until version-specific manifests/assets are implemented.
