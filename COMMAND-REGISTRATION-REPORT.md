# Command Registration Report

**Date:** 2026-11-07  
**Canonical command count:** 28 entries in `commands/manifest.json`.

## Capability mapping

The generated manifest distinguishes workflow implementation, agent skill entrypoints, and native command files. A shared Sherpa skill is not represented as a native slash command by implication.

| Client | Generated capability | Native registration target | Argument contract | Runtime result |
|---|---|---|---|---|
| Claude Code | 28 operation skill folders, each with `SKILL.md` | Skill discovery under Claude skill directories | Skill frontmatter/instructions; no assumed OpenCode/Kilo placeholder syntax | Registration files validated; invocation not run. |
| OpenCode | 28 native operation command files plus umbrella command | `commands/*.md` under `.opencode` command root | `$ARGUMENTS` per OpenCode command convention | Skill listing passed; command picker/invocation not run. |
| Kilo Code | 28 native workflow command files plus umbrella command | `.kilo/commands` project or `~/.config/kilo/commands` global | Avoids undocumented interpolation assumption | Skill discovery passed; workflow invocation not run. |
| Codex CLI | 28 operation skills | No native slash-command files generated | Skill instruction contract; CLI-specific slash syntax not claimed | Files validated; invocation not run. |

## Checks performed

- Generated native operation-file counts match the 28 manifest operations for Claude, OpenCode, and Kilo.
- Generated Codex distribution contains no `commands/*.md` native-command claim.
- Every generated skill has valid basic Agent Skill metadata and references resources that exist in the packaged shared skill.
- OpenCode and Kilo CLI skill discovery were attempted independently. This confirms skill discovery only, not command registration.
- `opencode debug config --pure` and `kilo debug config --pure` loaded the generated command definitions from an isolated project. Kilo's process retained a handle on its project directory after exit on Windows.
- Clean npm package test executed the packaged CLI installer and verified its generated Codex skills.

## Known limitations

No interactive command picker or end-to-end command workflow was exercised. OpenCode/Kilo config inspection establishes loaded command definitions, but not picker rendering or workflow execution. Kilo argument substitution remains unspecified. Treat command execution as unverified until client-level acceptance automation covers it.
