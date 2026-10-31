---
description: Route an explicit HackathonOS operation through the canonical project skill.
---

Read @SKILL.md and `core/commands/router.py` before acting. The requested operation and arguments are forwarded unchanged: `$ARGUMENTS`. The host may supply either only the trailing arguments or the full invocation; in the latter case, remove one leading `/hackathonos`, `\hackathonos`, or `hackathonos` command token before resolving.

Resolve the complete normalized argument string using the canonical router, so `config check` routes to CONFIG CHECK and `config` routes to CONFIG. An explicit `config` or `config check` request must follow the configuration workflow and must never STATUS; do not fall back to STATUS if explicit routing fails. With no argument, use its ordinary intent-driven router. Do not claim an unimplemented operation exists. Preserve human approval, evidence, and lifecycle boundaries. Do not install dependencies, deploy, submit, or make consequential changes without explicit authorization.
