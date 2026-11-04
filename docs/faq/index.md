# FAQ

## Is HackathonOS a standalone AI model or hosted service?

No. It is a Markdown-first skill that an AI coding agent loads, with a small Python core and a separate distribution CLI.

## Where does it save project information?

In `.hackathon/` inside the hackathon project's repository.

## Does it automatically pick an idea or approve architecture?

No. It may recommend an idea or architecture, but human confirmation is required.

## Does the submission workflow submit my project?

No. It prepares and verifies materials without submitting them.

## Which agents are supported?

Integration files exist for Claude Code, OpenCode, and Kilo Code, but runtime loading is marked `NOT VERIFIED`. The global installer targets Claude Code and OpenCode. Codex CLI, Qwen Code, and Gemini CLI have no verified native adapter.

## Is `/hackathonos audit` the same as `hackathonos audit`?

No. The slash command routes to the final-audit agent workflow. The standalone CLI command audits recognized managed skill installation folders.

## Can I install into a project directory with the installer?

The installer project-dir mode is explicitly unsupported. Use the checked-in integration files when working from a source checkout.

## Can I pin any historical version?

Not reliably. A version option exists, but the current manifest format does not resolve arbitrary historical assets.

## Is there a license?

The repository README says no license file is present; do not infer licensing terms.
