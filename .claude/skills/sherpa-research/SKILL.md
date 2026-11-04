---
name: sherpa-research
description: Research competitors, markets, technologies, and evidence with verifiable sources.
disable-model-invocation: true
argument-hint: [focus or arguments]
---

Read repository-root `SKILL.md`, `commands/manifest.json`, and `core/commands/router.py`. Resolve the registered command `sherpa-research` through the shared router, then execute only operation `RESEARCH` using `workflows/research.md`. Keep all behavior in the documented workflow and preserve its evidence, source quality, and scope limits. Operate on the active consuming project and its `.sherpa/` state; do not assume this framework repository is the project. User-supplied arguments: `$ARGUMENTS`.
