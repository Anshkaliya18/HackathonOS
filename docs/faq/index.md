# FAQ

## Is Sherpa a standalone AI model or hosted service?

No. It is a Markdown-first skill that an AI coding agent loads, with a small Python core and a separate distribution CLI.

## Where does it save project information?

In `.sherpa/` inside the hackathon project's repository.

## Does it automatically pick an idea or approve architecture?

No. It may recommend an idea or architecture, but human confirmation is required.

## Does the submission workflow submit my project?

No. It prepares and verifies materials without submitting them.

## Which agents are supported?

Sherpa ships a shared Agent Skill and host manifests for Claude Code, Codex, Gemini CLI, Qwen Code, OpenCode, and Kilo Code. Runtime loading remains `NOT VERIFIED` for the updated adapters. The global installer currently targets Claude Code and OpenCode; other hosts use their shared skill directory or plugin/extension flow described in the [agent guide](/agents/).

## Is `/sherpa audit` the same as `sherpa audit`?

No. The slash command routes to the final-audit agent workflow. The standalone CLI command audits recognized managed skill installation folders.

## Can I install into a project directory with the installer?

The installer project-dir mode is explicitly unsupported. Use the checked-in integration files when working from a source checkout.

## Can I pin any historical version?

Not reliably. A version option exists, but the current manifest format does not resolve arbitrary historical assets.

## Is there a license?

The repository README says no license file is present; do not infer licensing terms.
