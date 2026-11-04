# Installation

The published installer retrieves a release manifest and checks the archive's SHA-256 checksum before extraction. By default it installs the HackathonOS skill for Claude Code and OpenCode, plus the management CLI.

::: warning Runtime verification
An installer completing does not prove an agent will load the files. The repository manifest currently records Claude, OpenCode, and Kilo runtime status as `NOT VERIFIED`.
:::

## Requirements

- Windows PowerShell, or Bash on Linux/macOS.
- Python available on `PATH` (required by the installer and CLI).
- Network access to the configured release manifest and archive host.
- A compatible AI coding agent for skill workflows.

## Windows

Run in PowerShell:

```powershell
irm https://raw.githubusercontent.com/Anshkaliya18/HackathonOS/main/distribution/install.ps1 | iex
```

To install from a source checkout instead:

```powershell
& .\distribution\install.ps1 -Both
```

The PowerShell installer pauses at the end for Enter. Installation paths include `~/.claude/skills/hackathonos/`, `~/.config/opencode/skills/hackathonos/`, and `%USERPROFILE%\AppData\Local\HackathonOS\bin` for the CLI.

## Linux and macOS

```bash
curl -fsSL https://raw.githubusercontent.com/Anshkaliya18/HackathonOS/main/distribution/install.sh | bash
```

From a checkout, use `bash distribution/install.sh --both`. Skill directories are `~/.claude/skills/hackathonos/` and `~/.config/opencode/skills/hackathonos/`; the CLI is installed under `~/.local/bin/`.

## Choose targets and options

The shell installer accepts `--claude`, `--opencode`, `--both`, `--version VERSION`, `--manifest-url URL`, `--no-cli`, `--no-path`, `--yes`, and `--help`. PowerShell uses `-Claude`, `-OpenCode`, `-Both`, `-Version`, `-ManifestUrl`, `-NoCli`, `-NoPath`, and `-Yes`.

The PowerShell `-ProjectDir` option is explicitly unsupported. The release manifest format does not resolve arbitrary historical versions, so version pinning should be treated as unsupported until version-specific manifests and assets exist.

Environment variables: `HACKATHONOS_RELEASE_MANIFEST_URL`, `HACKATHONOS_VERSION`, `HACKATHONOS_INSTALL_CLAUDE`, `HACKATHONOS_INSTALL_OPENCODE`, `HACKATHONOS_INSTALL_CLI`, and `HACKATHONOS_NO_PATH`.

## Local or project checkout

Opening the repository in an agent that can load its checked-in instruction files is the local/source path. It does not install the standalone CLI globally. There is no dedicated project-local installer command.

## Verify and update

```text
hackathonos --version
hackathonos doctor
hackathonos audit
hackathonos clean --dry-run
```

Use `hackathonos update` to fetch a checksummed release and replace managed skill directories with backup/rollback behavior. Restart the agent if it does not discover new files.

## Uninstall

Run `hackathonos uninstall` and confirm the prompt, or `hackathonos uninstall --yes`. The CLI uninstaller removes recognized managed skill and CLI files, and preserves project `.hackathon/` data. Shell and PowerShell uninstall scripts are also in `distribution/`.

## Troubleshooting installation

- **404:** check the published release tag, manifest, and archive names.
- **Missing checksum:** installation/update refuses unverifiable archives; publish a correct SHA-256 in the manifest.
- **403/429:** retry later or configure a trusted manifest URL.
- **CLI not found:** restart the shell and ensure `~/.local/bin` or the Windows user bin directory is on `PATH`.
- **Installer reports unsupported project mode:** use repository-local agent files instead.

See [full source installation notes](https://github.com/Anshkaliya18/HackathonOS/blob/main/INSTALLATION.md) and [troubleshooting](/troubleshooting/).
