---
description: Show current lifecycle phase and evidence.
---

Read repository-root `SKILL.md`, `commands/manifest.json`, and `core/commands/router.py`. Resolve the registered command `sherpa-phase` through the shared router, then execute only operation `PHASE` using its manifest workflow. Keep all business logic in the existing workflow and engines. Operate on the active consuming project, never this framework repo by assumption; read its state in place and never replace, initialize, sync, or overwrite its `.sherpa/` files unless that operation explicitly requires initialization. Preserve human approval gates, UNKNOWN values, phase locks, secret redaction, and existing scope limits. Do not start Stage 4 merely because an engineering command is registered. Unknown or unmet prerequisites must be reported honestly. User-supplied arguments: `$ARGUMENTS`.
