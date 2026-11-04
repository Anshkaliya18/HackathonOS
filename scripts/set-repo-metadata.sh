#!/usr/bin/env bash
set -euo pipefail

repository="Anshkaliya18/HackathonOS"
description="Globally installed AI agent skill and hackathon mentor for Claude Code and OpenCode."
homepage="https://anshkaliya18.github.io/HackathonOS/"

gh auth status
gh repo edit "$repository" --description "$description" --homepage "$homepage"

gh api --method PUT "repos/${repository}/topics" --input - <<'JSON'
{
  "names": [
    "claude-code",
    "claude-skills",
    "ai-agents",
    "agent-skills",
    "opencode",
    "hackathon",
    "ai-mentor",
    "developer-tools",
    "prompt-engineering",
    "llm"
  ]
}
JSON

printf 'Updated repository metadata for %s.\n' "$repository"
