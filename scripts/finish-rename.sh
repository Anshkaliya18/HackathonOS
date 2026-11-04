#!/usr/bin/env bash
# Review this file, then uncomment/run the GitHub commands after merging.
# GitHub redirects the former repository URL after a rename, but update all
# installer one-liners and pin them to an actual release tag (for example v2.0.0).

# gh repo rename sherpa
# gh repo edit --description "Globally installed AI agent skill and hackathon mentor for Claude Code." --homepage "https://anshkaliya18.github.io/sherpa/"
# gh api --method PUT repos/Anshkaliya18/sherpa/topics --input - <<'JSON'
# {"names":["sherpa","claude-code","claude-skills","ai-agents","agent-skills","opencode","hackathon","ai-mentor","developer-tools","llm"]}
# JSON

# After the rename and v2.0.0 release, publish only tag-pinned install snippets:
# curl -fsSL https://github.com/Anshkaliya18/sherpa/releases/download/v2.0.0/install.sh | bash
# irm https://github.com/Anshkaliya18/sherpa/releases/download/v2.0.0/install.ps1 | iex

echo "Review and uncomment the gh commands above after merge; this script does not rename or publish anything by default."
