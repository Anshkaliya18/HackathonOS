#!/usr/bin/env bash
set -euo pipefail

repository="Anshkaliya18/sherpa"
description="A portable AI hackathon mentor skill and plugin for multiple coding agents."
homepage="https://anshkaliya18.github.io/sherpa/"

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
