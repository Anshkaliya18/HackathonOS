# Installation

Before you pack, choose an install method that fits your machine. Sherpa is a globally installed mentor skill for use inside each project; its command-line manager updates the skill files separately from agent workflows.

## Release status

Sherpa 2.0.8 contains generated client distributions and a managed installer. Release publication runs after the matching version tag is pushed; do not use its pinned URLs until the GitHub Release and npm package are available. Filesystem validation does not prove runtime loading.

## Windows PowerShell

After release, use the version-pinned installer:

```powershell
irm https://github.com/Anshkaliya18/Sherpa/releases/download/v2.0.8/install.ps1 | iex
```

From a checkout, build distributions with `python scripts/build-distributions.py`, then run `./distribution/install.ps1 -Codex -ProjectDir .` or select Claude, OpenCode, or Kilo with the corresponding switch. The CLI requires Python 3. The installer reports filesystem verification separately from client discovery and runtime execution.

## Linux and macOS

After release:

```bash
curl -fsSL https://github.com/Anshkaliya18/Sherpa/releases/download/v2.0.8/install.sh | bash
```

From a checkout, build distributions with `python3 scripts/build-distributions.py`, then use `bash distribution/install.sh --codex --project .` or select a supported client explicitly. The installer reports filesystem verification separately from client discovery and runtime execution.

## Options and environment

The npm installer supports Claude Code, OpenCode, Codex, and Kilo Code with `--client auto|claude|opencode|codex|kilo|all`, `--scope global|project`, `--project-dir PATH`, `--destination PATH`, and `--dry-run`. Checkout shell/PowerShell installers accept client switches and local-project/custom-root options.

Release install scripts use `SHERPA_RELEASE_MANIFEST_URL` and `SHERPA_VERSION`. See [migration notes](/migration).

The release package is `sherpa-skill@2.0.8`. After publication, install it with `npm install --global sherpa-skill@2.0.8`, then preview generated client destinations using `sherpa install --dry-run`. For a local install, run commands with `npx sherpa-skill@2.0.8 doctor`. Public npm uses the unscoped name; the GitHub Packages mirror uses `@anshkaliya18/sherpa-skill`.

## Verify, migrate, update

```text
sherpa --version
sherpa doctor
sherpa audit
sherpa clean --dry-run
```

The npm launcher forwards `sherpa --version`, install, verify-install, uninstall, update, doctor, audit, and clean to its bundled Python CLI; these commands require Python 3. Use `sherpa update` for a checksummed release update. If a project still has `.hackathon/` but not `.sherpa/`, Sherpa reads the old state with a deprecation notice. Run `sherpa migrate` to copy it without deleting or overwriting existing data.

When the package is installed locally rather than globally, prefix these CLI commands with `npx sherpa-skill@2.0.8`.

## Uninstall

Run `sherpa uninstall` and confirm, or use `sherpa uninstall --yes`. The uninstaller removes only recognized Sherpa/sherpa managed skill directories, CLI files, and compatibility shims; it preserves project state.

## Troubleshooting

- **404:** verify that the tagged release, manifest, and archive assets exist.
- **Missing checksum:** installation refuses unverifiable archives; publish only checksums generated from the actual assets.
- **403/429:** retry later or configure a trusted manifest URL.
- **CLI not found:** restart the shell and ensure its CLI directory is on `PATH`.

See the [source installation notes](https://github.com/Anshkaliya18/Sherpa/blob/main/INSTALLATION.md) and [troubleshooting guide](/troubleshooting/).
