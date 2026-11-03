# HackathonOS Installation

One-command installation of the HackathonOS AI Hackathon Mentor skill for
Claude Code and OpenCode.

## One command

### Linux / macOS

```bash
curl -fsSL https://YOUR-DOMAIN/install.sh | bash
```

### Windows (PowerShell)

```powershell
irm https://YOUR-DOMAIN/install.ps1 | iex
```

## Where the hosting URL must be configured

The scripts are ready to use, but **you must publish a real GitHub Release**
and point the installer at it before downloads succeed.

1. Create a GitHub Release in `Anshkaliya18/HackathonOS` (tag `v1.0.0`).
2. Upload versioned archives (`.tar.gz` for Linux/macOS, `.zip` for Windows)
   plus `manifest.json` and `checksums.txt` to the release.
3. Update `distribution/install.sh` / `distribution/install.ps1`
   `DEFAULT_MANIFEST_URL` (or set `HACKATHONOS_RELEASE_MANIFEST_URL`) to the
   release's `manifest.json`, e.g.:

   ```
   https://github.com/Anshkaliya18/HackathonOS/releases/download/v1.0.0/manifest.json
   ```

No fake release URLs or checksums are hardcoded. The installer verifies every
downloaded archive against its SHA-256 checksum before extracting.

## What gets installed

| Target | Location |
|--------|----------|
| Claude Code skill | `~/.claude/skills/hackathonos/` |
| OpenCode skill | `~/.config/opencode/skills/hackathonos/` |
| `hackathonos` CLI | `~/.local/bin/hackathonos` (Linux/macOS) <br> `%USERPROFILE%\AppData\Local\HackathonOS\bin\` (Windows) |

The skill entry point is `/hackathonos` in your AI coding agent:

```text
/hackathonos status
/hackathonos next
/hackathonos suggest
/hackathonos verify
```

## Customising the install

```bash
# Install only Claude Code
curl -fsSL .../install.sh | bash -s -- --claude

# Install only OpenCode
curl -fsSL .../install.sh | bash -s -- --opencode

# Pin a specific version
curl -fsSL .../install.sh | bash -s -- --version 1.2.3

# Use a custom manifest URL (self-hosted releases)
HACKATHONOS_RELEASE_MANIFEST_URL=https://your.domain/manifest.json \
  curl -fsSL .../install.sh | bash

# Skip CLI install / PATH modification
curl -fsSL .../install.sh | bash -s -- --no-cli --no-path
```

Environment variables:

| Variable | Meaning |
|----------|---------|
| `HACKATHONOS_RELEASE_MANIFEST_URL` | Override the release manifest URL |
| `HACKATHONOS_VERSION` | Pin a specific release version |
| `HACKATHONOS_INSTALL_CLAUDE` | `1` install / `0` skip Claude Code |
| `HACKATHONOS_INSTALL_OPENCODE` | `1` install / `0` skip OpenCode |
| `HACKATHONOS_INSTALL_CLI` | `1` install / `0` skip the CLI |
| `HACKATHONOS_NO_PATH` | `1` = do not modify shell profile PATH |
| `HACKATHONOS_YES` | `1` = skip confirmation (uninstaller) |

## Update

```bash
hackathonos update
```

Fetches the latest release, compares versions, downloads, verifies SHA-256,
backs up the previous installation, installs, and rolls back automatically on
failure. User project data and `.hackathon/` directories are preserved.

## Uninstall

```bash
hackathonos uninstall
```

Or via the remote uninstaller:

```bash
curl -fsSL https://YOUR-DOMAIN/uninstall.sh | bash
```

Prompts for confirmation and removes only HackathonOS installation files —
never user projects or `.hackathon/` state.

## Requirements

- Linux / macOS / Git Bash: `bash`, `curl`, `tar`, `sha256sum`/`shasum`/`openssl`, `python3`
- Windows: PowerShell 5.1+, `python`, `Invoke-WebRequest`, `Expand-Archive`
- Agent environments: Claude Code and/or OpenCode

## Security

- Downloads only over HTTPS.
- Every archive verified against SHA-256 before extraction.
- Path-traversal checks during extraction.
- No administrator privileges required.
- No API keys or personal information collected.
- See `SECURITY.md`.

## Support

Issues: https://github.com/Anshkaliya18/HackathonOS/issues
