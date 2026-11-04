# Configuration

HackathonOS has agent discovery files and project configuration/state. Project examples live in `templates/configuration/`; runtime behavior is implemented in `core/configuration/manager.py`, `src/config_manager.py`, and `workflows/configuration.md`.

Use `/hackathonos config` for a redacted overview and `/hackathonos config check` to validate project configuration and secret protections. Keep credentials in ignored environment files, starting from `.env.hackathon.example`. Never commit real tokens or keys.

The repo currently ships Claude Code (`.claude/skills/`), OpenCode (`.opencode/commands/` and package metadata), and Kilo (`.kilo/commands/`) integration files. These are not generated from a centralized schema. The global installer targets Claude Code and OpenCode only. Runtime status is NOT VERIFIED in `commands/manifest.json`. No central per-agent JSON config exists.

The distribution uses `HACKATHONOS_RELEASE_MANIFEST_URL` to override the manifest and shell installers accept `HACKATHONOS_VERSION` for pinning. See [INSTALLATION.md](INSTALLATION.md) for supported installer variables and switches.
