# Agent compatibility

Before you set out, check the integration files and the host’s runtime behavior as separate evidence. Files in a repository do not prove the agent discovers or runs them.

| Agent | Repository integration files | Global installer | Runtime status |
|---|---|---:|---|
| Claude Code | Claude plugin marketplace and Agent Skill | npm installer | NOT VERIFIED |
| Codex CLI / Codex app | Codex plugin manifest and Agent Skill | shared skill directory | NOT VERIFIED |
| Gemini CLI | Gemini extension and Agent Skill | shared skill directory | NOT VERIFIED |
| Qwen Code | Qwen extension and Agent Skill | shared skill directory | NOT VERIFIED |
| OpenCode | Agent Skill and legacy commands | npm installer | NOT VERIFIED |
| Kilo Code | Agent Skill and project commands | shared skill directory | NOT VERIFIED |
| Generic host | Root `SKILL.md`, only when manually supported | No | Host-dependent |

Sherpa packages a shared Agent Skill in `.agents/skills/sherpa/` plus plugin/extension manifests for Claude Code, Codex, Gemini CLI, and Qwen Code. Current host documentation recognizes these skill or extension formats, which establishes format compatibility only. Runtime loading and slash-command behavior must be verified independently. The global CLI installer currently targets Claude Code and OpenCode.

## Claude Code

Install through the repository marketplace with `/plugin marketplace add Anshkaliya18/Sherpa`, then `/plugin install sherpa@sherpa`. The npm installer is also available with `npm install --global sherpa-skill`; it copies the skill into Claude Code and OpenCode's personal skill folders. Start a new session after plugin installation. The plugin runtime is not yet verified.

## OpenCode

The repository includes the shared Agent Skill and legacy `.opencode/` command files. The npm installer targets `~/.config/opencode/skills/sherpa/`. Runtime loading of the new shared entry remains unverified.

## Kilo Code

Kilo Code can load `.agents/skills/sherpa/` as an Open Agent Skill; the repository's `.kilo/` commands and rules remain available for project use. Runtime loading remains unverified. See the [Kilo adapter notes](https://github.com/Anshkaliya18/Sherpa/blob/main/adapters/kilo/README.md).

## Codex, Gemini CLI, and Qwen Code

All three can use `.agents/skills/sherpa/`. Codex also has `.codex-plugin/plugin.json` and a repository-local marketplace; add the repository with `codex plugin marketplace add Anshkaliya18/Sherpa`, then add the `sherpa@sherpa` plugin from that marketplace. Gemini CLI has `gemini-extension.json`; install it with `gemini extensions install https://github.com/Anshkaliya18/Sherpa`. Qwen Code has `qwen-extension.json`; install with `qwen extensions install https://github.com/Anshkaliya18/Sherpa`. Qwen also supports the Claude marketplace. These registration flows are not yet verified in live host runtimes. See upstream [Codex plugin documentation](https://developers.openai.com/plugins/build/plugins), [Gemini extension documentation](https://geminicli.com/docs/extensions/), and [Qwen extension documentation](https://github.com/QwenLM/qwen-code/blob/main/docs/users/extension/introduction.md).

## Updating a compatibility claim

Record the host and version, install/source method, exact invocation, project context, observed output, and limitations. Add that evidence to the manifest before changing status. See [contributing](/contributing/) and [architecture](/architecture/).
