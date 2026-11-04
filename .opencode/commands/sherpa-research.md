---
description: Route an explicit sherpa operation through the canonical project skill.
---

Read @SKILL.md and `core/commands/router.py` before acting. Resolve the registered command `sherpa-research` and route only to `workflows/research.md`. The requested operation and arguments are forwarded unchanged: `$ARGUMENTS`. The host may supply either only the trailing arguments or the full invocation; in the latter case, remove one leading `/sherpa`, `\sherpa`, or `sherpa` command token before resolving.

Resolve the complete normalized argument string using the canonical router, so `config check` routes to CONFIG CHECK, `config` to CONFIG, and `suggest [focus]` to SUGGEST. Explicit config must never STATUS and must never STATUS as a fallback. With no argument, use its ordinary intent-driven router. Unknown explicit commands are unavailable. Preserve human approval, evidence, and lifecycle boundaries. Do not install dependencies, deploy, submit, or make consequential changes without explicit authorization.
