# Configuration

Sherpa has project configuration, project state, and host integration files. These are related but separate.

## Project files

Configuration examples are under `templates/configuration/`. The configuration workflow supports `/sherpa config` for a redacted overview and `/sherpa config check` for validation and secret-protection checks. The implementation is in `core/configuration/manager.py`, `src/config_manager.py`, and `workflows/configuration.md`.

## Secrets

Before you pack credentials, check which values are project facts and which are secrets. Start from `.env.sherpa.example` or the relevant example under `templates/configuration/`. Put real credentials in ignored environment files and never commit tokens or keys. The configuration check reviews Git protections and scanned secret indicators; it does not make committing secrets safe.

## Agent configuration

The repository has checked-in adapter files for Claude Code, OpenCode, and Kilo Code. They are not generated from one shared configuration schema. The global installer targets Claude Code and OpenCode only. No central per-agent JSON configuration is documented.

## Installer environment variables

`SHERPA_RELEASE_MANIFEST_URL` overrides the release manifest URL. Installers also expose `SHERPA_VERSION`, `SHERPA_INSTALL_CLAUDE`, `SHERPA_INSTALL_OPENCODE`, `SHERPA_INSTALL_CLI`, and `SHERPA_NO_PATH`. Former `sherpa_*` prefixed variables are accepted as fallbacks for one release.

The manifest format does not currently resolve arbitrary historical versions, so version pinning is unsupported. For exact switches, see [installation](/installation/) and [configuration source reference](https://github.com/Anshkaliya18/Sherpa/blob/main/CONFIGURATION.md).

## Precedence and custom paths

The repository documents no layered global/project/agent configuration precedence system. Installer targets are fixed by the scripts; a project-local installer switch is not implemented. Do not infer custom paths or configuration overrides beyond the documented installer environment variables.
