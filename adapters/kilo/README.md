# Kilo Code adapter

This repository is configured for project-local Kilo Code workflows.

- `kilo.jsonc` loads `.kilo/rules/sherpa-project.md` as project instructions.
- `.kilo/commands/` contains the slash commands. Kilo derives each command name from its filename, for example `sherpa-status.md` becomes `/sherpa-status`.
- `.kilo/skills/sherpa-skill/SKILL.md` registers Sherpa in Kilo's Skills list and points back to the canonical root `SKILL.md`.
- The command files are thin entry points. `SKILL.md`, `commands/manifest.json`, `core/commands/router.py`, and the referenced workflow remain canonical.
- No Kilo global install is performed; the commands are available when Kilo opens this repository.

Open this repository as the Kilo workspace, start a new session or reload the window after updating, then type `/sherpa-` to filter project workflows in the slash-command picker. Use `/sherpa` or a specific command such as `/sherpa-status`; `/sherpa-cmds` lists the available commands through the help operation. These `.kilo/commands/` files are project-scoped, so they appear only when Kilo has this repository open. Kilo's workflow documentation does not document argument substitution, so the adapters do not depend on trailing-argument substitution. Project state must stay in the consuming project's `.sherpa/` directory, with existing approval gates and safety rules intact.

**Runtime status: NOT VERIFIED.** Configuration and command files do not establish host runtime compatibility. Verify discovery and invocation in the target Kilo Code installation before changing the compatibility status.

See [Kilo workflows](https://kilo.ai/docs/customize/workflows) and [Kilo custom rules](https://kilo.ai/docs/customize/custom-rules).
