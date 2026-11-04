# Installation

## One-command installation

Windows PowerShell:

```powershell
$env:sherpa_RELEASE_MANIFEST_URL = 'https://github.com/Anshkaliya18/sherpa/releases/download/v1.0.0/manifest.json'
irm https://raw.githubusercontent.com/Anshkaliya18/sherpa/v1.0.0/distribution/install.ps1 | iex
Remove-Item Env:\sherpa_RELEASE_MANIFEST_URL
```

Linux/macOS:

```bash
curl -fsSL https://raw.githubusercontent.com/Anshkaliya18/sherpa/v1.0.0/distribution/install.sh | sherpa_RELEASE_MANIFEST_URL=https://github.com/Anshkaliya18/sherpa/releases/download/v1.0.0/manifest.json bash
```

These commands pin both the installer script and release manifest to v1.0.0; the manifest selects the archive and checksum. Review the script before running it. To install a later release, update both v1.0.0 references to that release tag. Release assets are listed at [GitHub Releases](https://github.com/Anshkaliya18/sherpa/releases).

## npm installer

The package name is `sherpa-cli`. Once it is published to npm:

```sh
npx sherpa-cli install
npx sherpa-cli install --dry-run
npx sherpa-cli install --uninstall
```

`install` reuses the platform distribution installer and targets both Claude Code and OpenCode. `--dry-run` prints both destination paths and makes no changes. `--uninstall` calls the existing uninstaller and removes managed global skill and CLI files while preserving project data. The npm package is not yet published; the npx commands become available after publication.

## Local/source use

Clone or open this repository in a compatible agent and use the repo-local integration files. This does not install the standalone `sherpa` management CLI globally. For a project-local agent setup, use the checked-in repo files; no dedicated `sherpa install --local` command exists yet.

## Installer scripts from a source checkout

Linux/macOS:

```bash
bash distribution/install.sh --both
```

Windows PowerShell:

```powershell
& .\distribution\install.ps1 -Both
```

The standard targets are Claude Code (`~/.claude/skills/sherpa/`) and OpenCode (`~/.config/opencode/skills/sherpa/`). Use `--claude` / `-Claude` or `--opencode` / `-OpenCode` to select one. The installer checks the downloaded archive and skill structure, backs up prior skill folders, and validates the installed result. CLI locations are `~/.local/bin/` on Unix and `%USERPROFILE%\AppData\Local\sherpa\bin` on Windows.

## Options and environment

Shell installer options: `--claude`, `--opencode`, `--both`, `--version VERSION`, `--manifest-url URL`, `--no-cli`, `--no-path`, `--yes`, `--help`. PowerShell parameters: `-Claude`, `-OpenCode`, `-Both`, `-Version`, `-ManifestUrl`, `-NoCli`, `-NoPath`, `-Yes`. The experimental project-dir switch is not supported and returns an error.

Environment variables include `sherpa_RELEASE_MANIFEST_URL`, `sherpa_VERSION`, `sherpa_INSTALL_CLAUDE`, `sherpa_INSTALL_OPENCODE`, `sherpa_INSTALL_CLI`, and `sherpa_NO_PATH`.

## CLI commands

`sherpa --version`, `update`, `doctor`, `audit`, `clean --dry-run`, and `uninstall`. `clean` reports by default; removal requires `--yes`. It is limited to recognized generated debris inside managed skill folders. Uninstall prompts unless `--yes` is supplied and preserves `.sherpa/` project data.

## Updating and uninstalling

Use `sherpa update` to download a checksummed release and replace installed skill directories with backup/rollback. Use `sherpa uninstall` to remove recognized global skill and CLI files. Uninstallers exist at `distribution/uninstall.sh` and `distribution/uninstall.ps1`; they are local scripts and require a published, trusted hosting URL before remote one-line use.

## Version pinning

The one-line curl and PowerShell commands pin both the installer script and manifest URL to a release tag. When running a checked-out installer directly, its default manifest points to the latest release; pass `--manifest-url` / `-ManifestUrl` to select a version-specific manifest.
