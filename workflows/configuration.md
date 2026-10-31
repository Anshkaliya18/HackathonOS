# HackathonOS — Configuration Workflow

**Operations:** CONFIG, CONFIG CHECK  
**Purpose:** Inspect or validate project configuration without starting another lifecycle phase.

## CONFIG

Run the repository's `core/configuration/manager.py` with the current project root and `config` subcommand. Treat output as a redacted overview. Do not fetch provider metadata, make network calls, or infer runtime capabilities from settings. If files are missing, explain that INIT creates only absent files.

## CONFIG CHECK

Run the same utility with the `check` subcommand. Report its exit status, configuration status, errors, warnings, Git protection, and the bounded secret scan. Never print `.env` values, tokens, matched secret text, or command-line secret overrides. “No known secret patterns detected” applies only to scanned files and patterns; it is not proof that the repository contains no secrets. Do not claim provider connectivity, builds, tests, or deployments from this check.

## INIT integration

When INIT creates a project, run the utility's `init` subcommand from the actual target repository root before collecting facts. It creates missing templates only, records the known project root, and preserves existing files. Collect information through the existing INIT workflow; update only fields that remain `UNKNOWN`, using values explicitly supplied or verified from evidence. Keep unknown facts as `UNKNOWN`. Create `.env` only when needed and only with explicit local action; never copy credential values into configuration JSON or project state. Verify `.env` ignore protection before any secret is added.

## Boundaries

- This workflow does not add a lifecycle phase or change the selected idea.
- It does not write application source, install dependencies, contact an AI provider, or deploy.
- `.hackathon/` and `.env` belong to the consuming project, not the HackathonOS framework repository.
- Preserve all user data; never reset or overwrite existing configuration during INIT.
