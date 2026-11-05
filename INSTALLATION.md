# Installation

## One-command installation

Windows PowerShell:

```powershell
irm https://github.com/Anshkaliya18/Sherpa/releases/download/v2.0.6/install.ps1 | iex
```

Linux/macOS:

```bash
curl -fsSL https://github.com/Anshkaliya18/Sherpa/releases/download/v2.0.6/install.sh | bash
```

These pinned commands use the Sherpa v2.0.6 release, which publishes the scripts, checksummed archives, and manifest. Review the scripts before running them. Current release assets are listed at [GitHub Releases](https://github.com/Anshkaliya18/Sherpa/releases).

## npm installer

The public npm package is `sherpa-skill` at version `2.0.6`:

```powershell
npm install --global sherpa-skill@2.0.6
sherpa install --dry-run
npx sherpa-skill@2.0.6 install --dry-run
npx sherpa-skill@2.0.6 install --uninstall
```

If you installed it locally with `npm install sherpa-skill@2.0.6`, run commands with `npx` because a local install does not add `sherpa` to your system `PATH`:

```powershell
npx sherpa-skill@2.0.6 --version
npx sherpa-skill@2.0.6 doctor
npx sherpa-skill@2.0.6 audit
npx sherpa-skill@2.0.6 clean --dry-run
```

The GitHub Packages mirror is `@anshkaliya18/sherpa-skill@2.0.6`. It requires a GitHub personal access token with `read:packages`; configure the `@anshkaliya18` scope to use `https://npm.pkg.github.com` before installing it. `install` reuses the platform installer and targets both Claude Code and OpenCode. `--dry-run` prints both destination paths and makes no changes. `--no-cli` skips the optional Python CLI, and `--uninstall` removes managed global skill and CLI files while preserving project data. See [npm publishing](docs/deployment/npm.md).

## Local/source use

Clone or open this repository in a compatible agent and use the repo-local integration files. This does not install the standalone `sherpa` management CLI globally. For a project-local agent setup, use the checked-in repo files; no dedicated `sherpa install --local` command exists yet.

## Installer scripts from a source checkout

Linux/macOS:

```bash
bash distribution/install.sh --both
```

Windows PowerShell:

```powershell
& .\distribution\install.ps1 -Both -NoCli
```

The checkout installer stages only tracked product directories and skips `.sherpa/`, tests, caches, and generated site output. The standard targets are Claude Code (`~/.claude/skills/sherpa/`) and OpenCode (`~/.config/opencode/skills/sherpa/`). Use `--claude` / `-Claude` or `--opencode` / `-OpenCode` to select one. The installer validates the skill after installation. Install the optional CLI with Python 3; its Windows launcher supports `python` or `py -3`. CLI locations are `~/.local/bin/` on Unix and `%USERPROFILE%\AppData\Local\sherpa\bin` on Windows.

## Options and environment

Shell installer options: `--claude`, `--opencode`, `--both`, `--version VERSION`, `--manifest-url URL`, `--no-cli`, `--no-path`, `--yes`, `--help`. PowerShell parameters: `-Claude`, `-OpenCode`, `-Both`, `-Version`, `-ManifestUrl`, `-NoCli`, `-NoPath`, `-Yes`. The experimental project-dir switch is not supported and returns an error.

Environment variables include `SHERPA_RELEASE_MANIFEST_URL`, `SHERPA_VERSION`, `SHERPA_INSTALL_CLAUDE`, `SHERPA_INSTALL_OPENCODE`, `SHERPA_INSTALL_CLI`, and `SHERPA_NO_PATH`.

## CLI commands

The npm `sherpa` launcher supports `--version`, `update`, `doctor`, `audit`, `clean --dry-run`, and `uninstall`; management commands use the bundled Python CLI and require Python 3. `clean` reports by default; removal requires `--yes`. It is limited to recognized generated debris inside managed skill folders. Uninstall preserves `.sherpa/` project data.

## Updating and uninstalling

Use `sherpa update` to download a checksummed release and replace installed skill directories with backup/rollback. Use `sherpa uninstall` to remove recognized global skill and CLI files. Uninstallers exist at `distribution/uninstall.sh` and `distribution/uninstall.ps1`; they are local scripts and require a published, trusted hosting URL before remote one-line use.

## Version pinning

The one-line curl and PowerShell commands pin the installer script to a release tag. When running an installed online script, the default manifest points to the latest release; pass `--manifest-url` / `-ManifestUrl` to select a custom manifest. Running `distribution/install.ps1` from a full checkout uses the local source tree instead.
