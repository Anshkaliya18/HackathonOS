---
layout: home
title: HackathonOS · Evidence-led hackathon mentorship
titleTemplate: false
hero:
  name: HackathonOS
  text: Build the right thing. Prove it works. Show why it matters.
  tagline: An AI hackathon mentor that helps teams make evidence-backed decisions from idea selection through implementation, demo preparation, and submission readiness.
  image:
    src: /mark.svg
    alt: HackathonOS mark
  actions:
    - theme: brand
      text: Get started
      link: /getting-started/
    - theme: alt
      text: Install HackathonOS
      link: /installation/
    - theme: alt
      text: Browse commands
      link: /reference/commands
features:
  - title: Decide with evidence
    details: Compare ideas against constraints and judging criteria. Recommendations do not silently select an idea for you.
    link: /workflows/
  - title: Move through clear phases
    details: Plan, implement, verify, review, and prepare. Each workflow consumes evidence and observes approval gates.
    link: /concepts/lifecycle
  - title: Keep project state with the project
    details: Persistent HackathonOS state lives in the project's .hackathon/ directory, not the skill installation.
    link: /concepts/
  - title: Prepare a credible demo
    details: Turn verified project evidence into a judge-oriented demo and presentation plan.
    link: /workflows/
  - title: Separate mentorship from management
    details: Agent workflows guide project work; the standalone CLI manages installation, diagnostics, and generated-file audits.
    link: /reference/commands
  - title: Know the compatibility limits
    details: See which adapter files exist and where runtime loading has not been verified.
    link: /agents/
---

<div class="home-intro">

HackathonOS is a Markdown-first mentor skill backed by a small Python core. It focuses teams on **judging impact per unit time and risk**, challenges unsupported claims, and leaves consequential choices to people.

</div>

## Start in three steps

1. [Install for Claude Code or OpenCode](/installation/) or open the repository's integration files in your agent.
2. In the project repository, run `/hackathonos help`, then `/hackathonos init`.
3. Check `/hackathonos status` and `/hackathonos next` to understand the current project state and next action.

::: warning Compatibility status
Integration files are present for Claude Code, OpenCode, and Kilo Code, but runtime loading is **NOT VERIFIED** for all three in the command manifest. The global installer targets Claude Code and OpenCode. Codex CLI, Qwen Code, and Gemini CLI do not have verified native adapters.
:::

## How the system fits together

```mermaid
flowchart LR
  Person[Team member] --> Agent[AI coding agent]
  Agent --> Skill[SKILL.md router]
  Skill --> Manifest[Command manifest and router]
  Manifest --> Flow[Workflow plus rules]
  Flow --> Artifacts[Evidence and templates]
  Artifacts --> State[Project .hackathon/ state]
  State --> Flow
```

The management CLI is a separate distribution tool. It installs and updates skill files, reports diagnostics, audits managed folders, and can list recognized generated debris for cleanup.

## Pick your path

- **New to HackathonOS:** [Introduction](/getting-started/) → [Quickstart](/getting-started/quickstart) → [First lifecycle pass](/concepts/lifecycle)
- **Installing for a team:** [Installation options](/installation/) → [Agent compatibility](/agents/) → [Configuration](/configuration/)
- **Contributing:** [Architecture](/architecture/) → [Repository map](/architecture/#repository-map) → [Contribution guide](/contributing/)

## Project links

[GitHub repository](https://github.com/Anshkaliya18/HackathonOS) · [Source documentation index](/reference/source-docs)
