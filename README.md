# HackathonOS Distribution

Production-ready distribution packaging for HackathonOS — the AI Hackathon
Mentor/Co-Pilot skill for Claude Code and OpenCode.

This directory contains the one-command installers, the `hackathonos` CLI,
release metadata, and uninstallers. Users install with a single terminal
command; no repository clone is required.

## Install once, use everywhere

```bash
# Linux / macOS
curl -fsSL https://YOUR-DOMAIN/install.sh | bash

# Windows PowerShell
irm https://YOUR-DOMAIN/install.ps1 | iex
```

## Layout

```
distribution/
├── install.sh                  # Linux / macOS / Git Bash installer
├── install.ps1                 # Windows PowerShell installer
├── uninstall.sh                # Linux / macOS / Git Bash uninstaller
├── uninstall.ps1               # Windows PowerShell uninstaller
├── VERSION                     # Distribution version (1.0.0)
├── cli/
│   ├── hackathonos             # stdlib CLI (--version / update / uninstall / doctor / help)
│   └── hackathonos.bat         # Windows CLI wrapper
└── release/
    ├── manifest.json           # release manifest template
    └── checksums.txt           # SHA-256 checksums template
```

## Supported agent environments

- **Claude Code** — `~/.claude/skills/hackathonos/`
- **OpenCode** — `~/.config/opencode/skills/hackathonos/`

Both can be installed simultaneously. The existing HackathonOS functionality
(workflows, rules, templates, command router) is preserved intact.

## CLI

```bash
hackathonos --version   # show version
hackathonos update      # update to latest release (with backup + rollback)
hackathonos uninstall   # remove safely (preserves user data)
hackathonos doctor      # diagnose environment
hackathonos help        # show help
```

## Documentation

- `INSTALLATION.md` — installation instructions, customisation, update/uninstall
- `RELEASE.md` — how to publish a release
- `SECURITY.md` — security model and guarantees
- `CHANGELOG.md` — version history

## Intellectual property

The installer is kept separate from the skill engine. Skill files are ordinary
Markdown/Python; no claim is made that local files are proprietary or
protected. The architecture is modular so a private hosted API can be
introduced in a future version without changing the installer.

## Repository

https://github.com/Anshkaliya18/HackathonOS
