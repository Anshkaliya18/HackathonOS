# Sherpa project guidance for Kilo Code

- Treat repository-root `SKILL.md` as the canonical product guide. Use `commands/manifest.json` and `core/commands/router.py` to resolve command names and operations; follow the referenced workflow instead of duplicating its logic.
- The Kilo-discoverable skill entry point is `.kilo/skills/sherpa-skill/SKILL.md`; when it applies, read the canonical root `SKILL.md` before acting.
- Use the repository's `.kilo/commands/*.md` files as thin slash-command entry points. Invoke commands by filename, such as `/sherpa` or `/sherpa-status`. Do not assume Kilo forwards trailing arguments unless the active host version demonstrates it.
- Work on the user's active project. Do not treat this framework repository as the consuming project unless the user explicitly asks. Preserve existing `.sherpa/` state and never initialize, overwrite, or synchronize it without the relevant command and authorization.
- Preserve human approval gates, phase locks, evidence labels, `UNKNOWN` values, secret redaction, and documented scope limits. Do not install dependencies, publish, deploy, submit, or change consequential project state without explicit authorization.
- For repository checks, use `python tests/run_all.py --phase <smoke|core|workflows|regression|distribution>` or `python tests/run_all.py` for the full suite. Run only the checks relevant to the requested change unless asked for a full validation.
- Do not claim Kilo runtime compatibility from these files alone. Keep it marked unverified until a command is exercised successfully in the actual Kilo host.
