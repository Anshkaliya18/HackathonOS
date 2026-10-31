---
name: hackathonos
description: Explicit HackathonOS command entrypoint. Routes the provided operation to the repository SKILL.md while preserving human authority and evidence boundaries.
disable-model-invocation: true
argument-hint: [operation and arguments]
---

Read the repository-root `SKILL.md` and follow it as the sole routing source. The user-invoked operation and arguments are: `$ARGUMENTS`.

Forward the argument text unchanged to the canonical router in `core/commands/router.py` and repository `SKILL.md`. The host may supply either only the trailing arguments or the full invocation; in the latter case, remove one leading `/hackathonos`, `\hackathonos`, or `hackathonos` command token before resolving. Resolve the complete normalized argument string, so `config check` reaches CONFIG CHECK, `config` reaches CONFIG, and `suggest` plus optional focus text reaches SUGGEST. Run only the corresponding documented workflow. Explicit configuration operations must never STATUS; unknown commands are unavailable. For an empty argument, use the ordinary intent-driven router. Follow all repository rules, human approval gates, evidence limits, and phase locks. Do not install dependencies, deploy, submit, or make consequential changes unless separately authorized by the user.
