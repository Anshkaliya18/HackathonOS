---
description: Show a redacted project configuration overview.
---

Read repository-root `SKILL.md`, `commands/manifest.json`, and `core/commands/router.py`. Resolve the registered command `hackathonos-config` through the shared router, then execute only operation `CONFIG` using its manifest workflow. Keep all business logic in the existing workflow and engines. Operate on the active consuming project, never this framework repo by assumption; read its state in place and never replace, initialize, sync, or overwrite its `.hackathon/` files unless that operation explicitly requires initialization. Preserve human approval gates, UNKNOWN values, phase locks, secret redaction, and existing scope limits. Do not start Stage 4 merely because an engineering command is registered. Unknown or unmet prerequisites must be reported honestly. Kilo argument placeholder support is not assumed; if the host does not expose trailing input, run the command without a focus hint.
