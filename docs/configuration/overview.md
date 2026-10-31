# Configuration Overview

HackathonOS project configuration belongs in the hackathon project's repository, not in the installed skill directory.

## Files

- Root `.env.example`: documented variable names and safe, non-secret defaults.
- Project-root `.env`: local overrides and secrets; ignored by Git. Create it only when needed.
- `.hackathon/hackathon.json`: hackathon facts and project identity/repository/deployment metadata.
- `.hackathon/settings.json`: agent preferences, capabilities, verification, and autonomous safety limits.
- `.hackathon/project-state.md`: phase and workflow state; remains the canonical progress record.
- `.hackathon/config/*.env.example`: optional split examples installed by INIT; these contain placeholders only.

The framework repository itself intentionally has no `.hackathon/` state and no `.env` file.

## Commands

- `/hackathonos config` — concise overview, redacting credentials as Configured/Missing.
- `/hackathonos config check` — validates JSON, environment values, paths, Git ignore/tracking, and bounded secret indicators.
- `/hackathonos init` — creates missing project configuration and state files without overwriting existing files or values.

## Statuses

`CONFIGURED`, `PARTIALLY_CONFIGURED`, `MISSING`, `INVALID`, `UNKNOWN`. Unknown optional facts remain `UNKNOWN`; validation never invents them.

## Precedence

For non-secret settings: explicit command override → project configuration → process environment → project `.env` → documented setting default → `UNKNOWN`. For secrets: process environment → project `.env`; secrets are never copied to JSON or rendered in reports. Existing process environment variables take precedence over `.env` values.

## Safety

Human approval is required by default. Disabling it is accepted only as an explicit setting and shown as a prominent warning. Loop limits are bounded (iterations 1–20, fixes 0–50). Configuration values do not enable features that have not been implemented, and configured provider credentials do not prove network/API connectivity.
