# Persistent Settings

`<project>/.sherpa/hackathon.json` stores non-secret hackathon and project metadata. `UNKNOWN` is valid. Deadline datetime and timezone are separate, and source/confidence are retained.

`<project>/.sherpa/settings.json` stores `agent_platform`, provider/model metadata, capability preferences, verification, and safety limits. Keep operational preferences separate from hackathon facts. `.sherpa/project-state.md` remains the phase/progress source of truth.

Precedence: explicit command override → project JSON → process environment → project `.env` → documented setting default → `UNKNOWN`. A literal `UNKNOWN` is retained. Secrets use only process environment or `.env` and are never persisted to JSON.

The config overview is read-only. `config check` reports errors and warnings. INIT creates missing files only and preserves all existing configuration.
