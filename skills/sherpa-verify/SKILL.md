---
name: sherpa-verify
description: Verify implementation through the existing testing and security workflow. Use this skill when the user invokes sherpa-verify or asks for this Sherpa operation.
---

This is a command-specific entry point for the Sherpa skill.

1. Read `../sherpa/SKILL.md` and follow its shared mentor, safety, and project-state rules.
2. Read `../sherpa/commands/manifest.json` and resolve `sherpa-verify`. Confirm it is implemented and use only its registered operation and workflow.
3. Read the referenced workflow under `../sherpa/` and execute it for the active consuming project. Keep state in that project's `.sherpa/` directory.
4. Preserve all approval gates, phase locks, evidence requirements, and scope limits in the canonical skill and workflow. Do not infer missing evidence.
