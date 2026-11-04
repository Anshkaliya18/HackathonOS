# Claude Code Adapter — Stage 1

Native entrypoint: `.claude/skills/sherpa/SKILL.md`.

The `sherpa` skill name is invoked as `/sherpa`; the skill uses the documented `$ARGUMENTS` substitution for forms such as `/sherpa status`. It is user-invocable only; Claude does not select it automatically. Root `SKILL.md` is the canonical router.

Official discovery convention: Claude Code project skills live under `.claude/skills/<name>/SKILL.md`; user invocation uses `/<name>`, and skill arguments may be consumed with `$ARGUMENTS` ([official docs](https://code.claude.com/docs/en/skills)).

Runtime discovery: **NOT VERIFIED**. Installed CLI reports Claude Code 2.1.316. An interactive session displayed the workspace trust prompt; it was declined, so the slash-command picker was not opened and no model prompt was sent.

Hyphenated native aliases are registered as user-invocable skills under `.claude/skills/sherpa-<action>/SKILL.md`. Runtime attempt from an isolated temporary project: `claude --print --permission-mode plan '/sherpa-status'` stopped before dispatch because Claude Code rejected the configured model as unrecognized. Hyphenated command runtime remains **NOT VERIFIED**.

Stage 2 command runtime: **VERIFIED PASS** after synchronizing the current repository skill into the active Claude Code installation. The user manually executed `/sherpa config`, `/sherpa config check`, `/sherpa phase`, and `/sherpa next` and confirmed successful output. Earlier attempts using a stale installation failed under model/provider configuration and are superseded by the successful current-skill verification. See `docs/configuration/runtime-verification.md` for the scope and evidence note.
