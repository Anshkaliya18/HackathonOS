# Environment Files

Copy `.env.example` to `.env` in the hackathon project only when local overrides or credentials are needed. Keep actual secret values in `.env`; never paste them into chat, Markdown, JSON, tests, logs, or audit reports. `.env` is ignored by Git. Example files contain empty placeholders only.

Supported names include hackathon metadata, project path/repository/deployment, `AGENT_PLATFORM`, `AI_PROVIDER`, `AI_MODEL`, `AI_API_KEY`, capability booleans, bounded loop limits, and `REQUIRE_HUMAN_APPROVAL`.

The standard-library loader supports `KEY=value`, optional `export`, blank lines, comments, and single/double quoted values. Duplicate keys, malformed keys/lines, and unterminated quotes are invalid. Variable expansion is not performed. Existing process environment variables take precedence over `.env`. Output shows only whether secret variables are configured, never their values.
