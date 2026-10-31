# Claude Code Adapter — Stage 1

Native entrypoint: `.claude/skills/hackathonos/SKILL.md`.

The `hackathonos` skill name is invoked as `/hackathonos`; the skill uses the documented `$ARGUMENTS` substitution for forms such as `/hackathonos status`. It is user-invocable only; Claude does not select it automatically. Root `SKILL.md` is the canonical router.

Official discovery convention: Claude Code project skills live under `.claude/skills/<name>/SKILL.md`; user invocation uses `/<name>`, and skill arguments may be consumed with `$ARGUMENTS` ([official docs](https://code.claude.com/docs/en/skills)).

Runtime discovery: **NOT VERIFIED**. Installed CLI reports Claude Code 2.1.316. An interactive session displayed the workspace trust prompt; it was declined, so the slash-command picker was not opened and no model prompt was sent.

Stage 2 command runtime: **RUNTIME BLOCKED**. In a disposable project, `/hackathonos config` returned a configured-model error (`nvidia/nemotron-3-ultra-550b-a55b:free` was unrecognized). A process-only `--model sonnet` retry still routed to `poolside/laguna-s-2.1:free`, which OpenRouter reported unavailable. Neither attempt returned a configuration report; `/hackathonos config check` was not completed. This is a host model/provider configuration blocker, not a HackathonOS router result. No pass is claimed.
