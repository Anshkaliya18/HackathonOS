# Installation

Before you pack, choose an install method that fits your machine. Sherpa is a globally installed mentor skill for use inside each project; its command-line manager updates the skill files separately from agent workflows.

## Release status

Sherpa v2.0.4 is available from GitHub Releases. From a checkout, the Windows PowerShell installer uses a filtered local source tree. Runtime loading by Claude Code and OpenCode remains **NOT VERIFIED**.

## Windows PowerShell

After release, use the version-pinned installer:

```powershell
irm https://github.com/Anshkaliya18/Sherpa/releases/download/v2.0.4/install.ps1 | iex
```

From a checkout, run `./distribution/install.ps1 -Both`. To install the agent skill without the optional Python CLI, run `./distribution/install.ps1 -Both -NoCli` or set `$env:SHERPA_INSTALL_CLI = '0'`. The CLI requires Python 3; its Windows launcher supports either `python` or the `py` launcher. Install paths are `~/.claude/skills/sherpa/`, `~/.config/opencode/skills/sherpa/`, and `%USERPROFILE%\AppData\Local\Sherpa\bin` for the CLI.

## Linux and macOS

After release:

```bash
curl -fsSL https://github.com/Anshkaliya18/Sherpa/releases/download/v2.0.4/install.sh | bash
```

From a checkout, use `bash distribution/install.sh --both`. Skill directories are `~/.claude/skills/sherpa/` and `~/.config/opencode/skills/sherpa/`; the CLI is installed under `~/.local/bin/`.

## Options and environment

The shell installer accepts `--claude`, `--opencode`, `--both`, `--version VERSION`, `--manifest-url URL`, `--no-cli`, `--no-path`, `--yes`, and `--help`. PowerShell uses `-Claude`, `-OpenCode`, `-Both`, `-Version`, `-ManifestUrl`, `-NoCli`, `-NoPath`, and `-Yes`.

Use uppercase `SHERPA_RELEASE_MANIFEST_URL`, `SHERPA_VERSION`, `SHERPA_INSTALL_CLAUDE`, `SHERPA_INSTALL_OPENCODE`, `SHERPA_INSTALL_CLI`, and `SHERPA_NO_PATH`. Former `sherpa_*` variables are accepted for one release. See [migration notes](/migration).

The `@anshkaliya18/sherpa-skill` package is published through GitHub Packages. Its `sherpa install --dry-run` wrapper previews target paths; run it with `npx --registry=https://npm.pkg.github.com @anshkaliya18/sherpa-skill@2.0.4 install --dry-run`.

## Verify, migrate, update

```text
sherpa --version
sherpa doctor
sherpa audit
sherpa clean --dry-run
```

Use `sherpa update` for a checksummed release update. If a project still has `.hackathon/` but not `.sherpa/`, Sherpa reads the old state with a deprecation notice. Run `sherpa migrate` to copy it without deleting or overwriting existing data.

## Uninstall

Run `sherpa uninstall` and confirm, or use `sherpa uninstall --yes`. The uninstaller removes only recognized Sherpa/sherpa managed skill directories, CLI files, and compatibility shims; it preserves project state.

## Troubleshooting

- **404:** verify that the tagged release, manifest, and archive assets exist.
- **Missing checksum:** installation refuses unverifiable archives; publish only checksums generated from the actual assets.
- **403/429:** retry later or configure a trusted manifest URL.
- **CLI not found:** restart the shell and ensure its CLI directory is on `PATH`.

See the [source installation notes](https://github.com/Anshkaliya18/Sherpa/blob/main/INSTALLATION.md) and [troubleshooting guide](/troubleshooting/).
