# Configuration

sherpa has agent discovery files and project configuration/state. Project examples live in `templates/configuration/`; runtime behavior is implemented in `core/configuration/manager.py`, `src/config_manager.py`, and `workflows/configuration.md`.

Use `/sherpa config` for a redacted overview and `/sherpa config check` to validate project configuration and secret protections. Keep credentials in ignored environment files, starting from `.env.sherpa.example`. Never commit real tokens or keys.

The repo packages a shared Agent Skill and host-specific manifests for Claude Code, Codex, Gemini CLI, and Qwen Code, plus OpenCode and Kilo project integrations. These files are maintained as format-specific entry points rather than generated from a central schema. The global installer targets Claude Code and OpenCode only. Runtime status is recorded separately; manifest presence does not establish runtime compatibility.

The distribution uses `sherpa_RELEASE_MANIFEST_URL` to override the manifest and shell installers accept `sherpa_VERSION` for pinning. See [INSTALLATION.md](INSTALLATION.md) for supported installer variables and switches.
