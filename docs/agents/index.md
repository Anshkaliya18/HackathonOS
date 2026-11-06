# Agent compatibility

Before you set out, check the integration files and the host’s runtime behavior as separate evidence. Files in a repository do not prove the agent discovers or runs them.

| Agent | Generated integration | Installer | Evidence status |
|---|---|---|---|
| Claude Code | Agent Skills; 28 operation entries | Global, project, custom root | Files validated; live invocation NOT RUN |
| Codex CLI / Codex app | Agent Skills; no Sherpa native slash commands | Global, project, custom root | Files validated; live invocation NOT RUN |
| OpenCode | Agent Skills and native `.md` commands using `$ARGUMENTS` | Global, project, custom root | Project skill discovery PASS; command execution NOT RUN |
| Kilo Code | Agent Skills and native workflow command files | Global, project, custom root | Windows skill discovery observed; workflow execution NOT RUN |
| Gemini CLI | Existing extension integration | Manual/repository integration | NOT VERIFIED by universal installer |
| Qwen Code | Existing extension integration | Manual/repository integration | NOT VERIFIED by universal installer |

The npm installer detects Claude Code, OpenCode, Codex, and Kilo CLIs, or accepts an explicit client. Project scope uses each host's documented roots. Codex receives skills only; OpenCode and Kilo receive native command files. Gemini CLI and Qwen Code remain manual integrations and are not targets of the universal installer. See the [detailed compatibility matrix](https://github.com/Anshkaliya18/Sherpa/blob/main/CLIENT-COMPATIBILITY-MATRIX.md).

## Claude Code

Install with `npm install --global sherpa-skill` and run `sherpa install --client claude`. This installs generated Agent Skills. The previous marketplace integration is not part of the generated universal installer. Interactive skill invocation was not tested in this release audit.

## OpenCode

Install with `sherpa install --client opencode`. Sherpa is installed as an Agent Skill and native commands under the OpenCode config roots. Project skill discovery passed on the Windows host; native command execution remains unverified.

## Kilo Code

Install with `sherpa install --client kilo`. The install places the Agent Skill and native workflow command files in Kilo's supported roots. Kilo skill discovery was observed on Windows; command execution and runtime workflow behavior remain unverified.

## Codex, Gemini CLI, and Qwen Code

Codex gets generated skills for each operation and has no Sherpa-native slash commands in this distribution. Install with `sherpa install --client codex`; skill invocation was not tested. Gemini CLI and Qwen Code retain their existing extension manifests but are outside the universal installer and remain unverified.

## Updating a compatibility claim

Record the host and version, install/source method, exact invocation, project context, observed output, and limitations. Add that evidence to the manifest before changing status. See [contributing](/contributing/) and [architecture](/architecture/).
