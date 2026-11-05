---
description: sherpa root command. With no arguments, lists available commands. With arguments, routes the operation through SKILL.md and the shared router.
---

Read repository-root `SKILL.md` and `core/commands/router.py` before acting.

If `/sherpa` is invoked with no operation (blank arguments), execute the HELP operation: list the available sherpa commands and their purposes, then stop.

If `/sherpa <operation> [focus]` is invoked with arguments, treat the text following `/sherpa` as the requested operation and arguments. The host may supply only trailing arguments or the full invocation; normalize it through the shared router. `config check` and `config` use the configuration workflow; explicit config must never STATUS and must never STATUS as a fallback. `suggest` with optional focus text uses the idea-intelligence workflow; no separate native suggest alias is needed. Preserve evidence labels, unknowns, human approval gates, and phase locks. Unknown operations are unavailable — say so and list the supported commands instead of guessing. Do not install dependencies, deploy, submit, or change consequential project state without explicit authorization.
