# Quickstart

This is the shortest path from an installed agent to a first useful project check.

## 1. Install

Use the [Windows](/installation/#windows) or [Linux and macOS](/installation/#linux-and-macos) installer for a published release. It targets Claude Code and OpenCode by default. Or work from a checkout and use the checked-in agent files. Runtime discovery is not verified; see [compatibility](/agents/).

## 2. Open the project repository

Start your AI coding agent in the repository you plan to use for the hackathon. sherpa reads and writes project state under that repository's `.sherpa/` directory.

## 3. Ask for help and initialize

```text
/sherpa help
/sherpa init
```

If `.sherpa/` is already present, ask for `/sherpa status` first and review the existing files before continuing.

## 4. Give it project context

Provide the challenge brief, judging criteria, time constraints, team skills, and repository context when known. If information is missing, sherpa is intended to mark it `UNKNOWN` rather than invent it.

## 5. Choose a workflow

```text
/sherpa suggest focus on accessible tools for campus communities
/sherpa status
/sherpa next
```

Suggest explores and compares ideas; it does not select one. Once a person selects an idea, `/sherpa plan` can create a project plan. Implementation is a separate workflow and requires an approved plan.

## Understand the result

Read the agent's report and any artifacts it identifies under `.sherpa/`. Follow the named evidence and approval requirements. For a map of decisions and phases, see [the lifecycle](/concepts/lifecycle).

## If something does not work

Run `sherpa doctor` for management CLI diagnostics if installed. Confirm you're in the intended project, then see [troubleshooting](/troubleshooting/).
