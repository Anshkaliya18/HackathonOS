# OpenCode Adapter — Stage 1

Native project command: `.opencode/commands/hackathonos.md`, invoked as `/hackathonos`. The documented `$ARGUMENTS` placeholder passes forms such as `/hackathonos status` to the canonical router in root `SKILL.md`.

Official discovery convention: project command Markdown files live under `.opencode/commands/`; the filename defines the command name and `$ARGUMENTS` receives trailing user input ([official docs](https://opencode.ai/docs/commands)).

Runtime discovery: **VERIFIED** in OpenCode 1.19.4. The interactive slash picker displayed `/hackathonos` and its command description. This establishes picker visibility only.

Hyphenated native aliases are registered as `.opencode/commands/hackathonos-<action>.md`; the documented `$ARGUMENTS` variable is supported. Runtime attempt from an isolated temporary project: `opencode run --pure --log-level DEBUG --command hackathonos-status` produced no output after 15 seconds and was interrupted; the earlier project-root attempt also waited without workflow output. The alias is **NOT VERIFIED** at runtime. `--pure` was used to prevent external plugin loading.

Stage 2 command runtime: **RUNTIME BLOCKED**. An isolated-project invocation of the canonical command with `config` arguments did not return output before it was stopped. During that OpenCode process, the host created `.opencode/.gitignore`, `.opencode/package.json`, a lockfile, and `node_modules/` containing its own `@opencode-ai/plugin` SDK at version 1.19.4. No HackathonOS workflow or manager code invokes a package manager. OpenCode documents automatic plugin-package installation at startup, and upstream reports document generated project-local plugin packages ([plugin docs](https://opencode.ai/docs/plugins/), [upstream issue #27676](https://github.com/anomalyco/opencode/issues/27676)). This is an OpenCode host bootstrap side effect, not an application dependency, but it still violates this run's no-install condition. The `config check` command was not attempted afterward. No command-runtime pass is claimed.
