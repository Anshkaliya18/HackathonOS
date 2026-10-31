# Claude Code Adapter — Stage 1

Native entrypoint: `.claude/skills/hackathonos/SKILL.md`.

The `hackathonos` skill name is invoked as `/hackathonos`; the skill uses the documented `$ARGUMENTS` substitution for forms such as `/hackathonos status`. It is user-invocable only; Claude does not select it automatically. Root `SKILL.md` is the canonical router.

Official discovery convention: Claude Code project skills live under `.claude/skills/<name>/SKILL.md`; user invocation uses `/<name>`, and skill arguments may be consumed with `$ARGUMENTS` ([official docs](https://code.claude.com/docs/en/skills)).

Runtime discovery: **NOT VERIFIED**. Installed CLI reports Claude Code 2.1.316. An interactive session displayed the workspace trust prompt; it was declined, so the slash-command picker was not opened and no model prompt was sent.

Hyphenated native aliases are registered as user-invocable skills under `.claude/skills/hackathonos-<action>/SKILL.md`. Runtime attempt from an isolated temporary project: `claude --print --permission-mode plan '/hackathonos-status'` stopped before dispatch because Claude Code rejected the configured model as unrecognized. Hyphenated command runtime remains **NOT VERIFIED**.

Stage 2 command runtime: **VERIFIED PASS** after synchronizing the current repository skill into the active Claude Code installation. The user manually executed `/hackathonos config`, `/hackathonos config check`, `/hackathonos phase`, and `/hackathonos next` and confirmed successful output. Earlier attempts using a stale installation failed under model/provider configuration and are superseded by the successful current-skill verification. See `docs/configuration/runtime-verification.md` for the scope and evidence note.
