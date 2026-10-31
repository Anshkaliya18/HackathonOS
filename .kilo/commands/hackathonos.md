---
description: HackathonOS root command. Interpret supplied text as an explicit operation and route through the repository SKILL.md.
---

Read repository-root `SKILL.md` and `core/commands/router.py` before acting. Treat the text following `/hackathonos` as the requested operation and arguments, and resolve the complete argument string using the canonical router (`config check` before/independently of `config`). If no text follows, use the ordinary intent-driven router. `SKILL.md` is canonical; do not duplicate or override its workflows. Preserve evidence labels, unknowns, human approval gates, and phase locks. If an operation is not implemented, say so. Do not install dependencies, deploy, submit, or change consequential project state without explicit authorization.
