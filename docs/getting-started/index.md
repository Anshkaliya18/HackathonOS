# Introduction

Before you pack, check your route: Sherpa can guide the work, but your team sets the destination and makes the decisions.

Sherpa is a Markdown-first AI hackathon mentor and co-pilot. It guides project teams through decisions and review workflows, with advice grounded in the files and evidence available in the project.

## What it does

Use it to frame an idea, evaluate options, plan an implementation, review evidence, prepare a demo, and check submission readiness. The agent reads `SKILL.md`, routes the request to an implemented workflow, and uses shared rules and templates. Project state is stored in `.sherpa/` in the project repository.

## Why use it

Hackathons reward a clear, working solution under time pressure. sherpa is designed to focus effort on judging impact relative to time and risk. It can recommend and challenge; people still confirm the selected idea, architecture, and other consequential decisions.

## Before you begin

- A project repository (new or existing).
- Claude Code or OpenCode for the global installer path. Kilo Code files exist in the repository, but runtime loading is not verified.
- Python is required by the distribution installer and management CLI.
- Network access for downloading published release files.

See [installation options](/installation/) and [compatibility status](/agents/).

## Your first session

In your project, ask the coding agent to run `/sherpa help`. If this project has not been initialized, run `/sherpa init`. Then use `/sherpa status` to see what state is known.

```text
/sherpa help
/sherpa init
/sherpa status
/sherpa next
```

The first command lists implemented operations. Init creates project-local sherpa state according to its workflow. Status reports evidence; next identifies a high-priority action. Exact artifacts depend on workflow inputs and available project evidence.

::: tip Beginner note
If the agent cannot find sherpa commands, confirm the integration files are installed where that agent discovers skills, then restart or reload the agent. Runtime loading has not yet been verified; consult [agent compatibility](/agents/).
:::

## A useful mental model

Sherpa is an instruction and workflow layer for an AI coding agent. It is not a hosted service, autonomous project tracker, or a replacement for your build and test tools. The standalone `sherpa` CLI manages the skill installation; it does not run project workflows.

## Common first-run mistakes

- Running a workflow outside the hackathon project's repository. State is project-local.
- Treating a suggestion as approval. Idea and architecture decisions require explicit human confirmation.
- Assuming that an integration file proves the host agent loads it. Runtime status is separate and currently unverified.
- Confusing `/sherpa audit` (agent workflow) with `sherpa audit` (managed installation folder report).

Next: [Quickstart](/getting-started/quickstart) · [Core concepts](/concepts/) · [Commands](/reference/commands).
