# Installation

## One-command installation

Windows PowerShell:

```powershell
irm https://github.com/Anshkaliya18/Sherpa/releases/download/v2.0.8/install.ps1 | iex
```

Linux/macOS:

```bash
curl -fsSL https://github.com/Anshkaliya18/Sherpa/releases/download/v2.0.8/install.sh | bash
```

These commands require an already published release with matching scripts, checksummed archives, and manifest. This repair did not publish or verify the registry/release assets. Check the [GitHub Releases](https://github.com/Anshkaliya18/Sherpa/releases) page and confirm the requested version contains the expected artifacts before using a pinned URL.

## npm installer

The package metadata in this checkout identifies `sherpa-skill` as version `2.0.8`:

```powershell
npm install --global sherpa-skill@2.0.8
sherpa install --dry-run
npx sherpa-skill@2.0.8 install --dry-run
npx sherpa-skill@2.0.8 uninstall --client all
```

If you installed it locally with `npm install sherpa-skill@2.0.8`, run commands with `npx` because a local install does not add `sherpa` to your system `PATH`:

```powershell
npx sherpa-skill@2.0.8 --version
npx sherpa-skill@2.0.8 doctor
npx sherpa-skill@2.0.8 audit
npx sherpa-skill@2.0.8 clean --dry-run
```

The npm launcher supports Claude Code, OpenCode, Codex, and Kilo Code with `--client auto` (default), an explicit client, or `all`. Select one client when using `--destination`. Use `--scope project --project-dir PATH` for project-local installation. `--dry-run` prints generated targets without writing files and does not verify client discovery.

## Local/source use

Clone or open this repository and run `python scripts/build-distributions.py` before using generated project-local adapters.

## Installer scripts from a source checkout

Linux/macOS:

```bash
bash distribution/install.sh --both
```

Windows PowerShell:

```powershell
& .\distribution\install.ps1 -Both -NoCli
```

The checkout installer uses the generated distribution and the standard-library Python engine. Targets include Claude Code, OpenCode, Codex, and Kilo Code. Shell options include `--claude`, `--opencode`, `--codex`, `--kilo`, `--project PATH`, and `--destination PATH`. PowerShell uses `-Claude`, `-OpenCode`, `-Codex`, `-Kilo`, `-ProjectDir`, and `-Destination`. The engine reports file/skill/command/resource validation separately from client discovery and runtime execution.

## Options and environment

Shell installer options: `--claude`, `--opencode`, `--codex`, `--kilo`, `--both`, `--project PATH`, `--destination PATH`, `--version VERSION`, `--manifest-url URL`, `--no-cli`, `--no-path`, `--yes`, `--help`. PowerShell parameters: `-Claude`, `-OpenCode`, `-Codex`, `-Kilo`, `-Both`, `-ProjectDir`, `-Destination`, `-Version`, `-ManifestUrl`, `-NoCli`, `-NoPath`, `-Yes`.

Environment variables include `SHERPA_RELEASE_MANIFEST_URL`, `SHERPA_VERSION`, `SHERPA_INSTALL_CLAUDE`, `SHERPA_INSTALL_OPENCODE`, `SHERPA_INSTALL_CLI`, and `SHERPA_NO_PATH`.

## CLI commands

The npm `sherpa` launcher supports `install`, `verify-install`, `uninstall`, `update`, `doctor`, `audit`, and `clean --dry-run`; the bundled Python CLI requires Python 3. File verification reports `CLIENT_DISCOVERY_VERIFIED` and `RUNTIME_EXECUTION_VERIFIED` as NOT RUN until a real client test establishes those states. Uninstall uses the installation receipt to remove only managed files and preserves project state.

## Updating and uninstalling

Use `sherpa update` to download a checksummed release and replace installed skill directories with backup/rollback. Use `sherpa uninstall --client all` to remove files recorded in managed installation receipts. The standalone uninstaller scripts delegate to the receipt-aware engine when distributed with it; a one-file remote invocation has only legacy cleanup behavior. Remote use requires a published, trusted hosting URL and matching release assets.

## Version pinning

The one-line curl and PowerShell commands pin the installer script to a release tag. When running an installed online script, the default manifest points to the latest release; pass `--manifest-url` / `-ManifestUrl` to select a custom manifest. Running `distribution/install.ps1` from a full checkout uses the local source tree instead.
