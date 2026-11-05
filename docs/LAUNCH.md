---
title: Internal launch drafts
head:
  - - meta
    - name: robots
      content: noindex, nofollow
---

# Launch drafts

The demo GIF is currently a labeled placeholder. Replace it with the real recording described in [`scripts/record-demo.md`](https://github.com/Anshkaliya18/Sherpa/blob/main/scripts/record-demo.md) before posting. Installation into both standard folders was checked using the v1.0.0 Windows installer in an isolated profile; Claude Code and OpenCode runtime loading has not been verified.

Install line used below (Linux/macOS; installer and manifest pinned to v1.0.0):

```bash
curl -fsSL https://raw.githubusercontent.com/Anshkaliya18/Sherpa/v1.0.0/distribution/install.sh | sherpa_RELEASE_MANIFEST_URL=https://github.com/Anshkaliya18/Sherpa/releases/download/v1.0.0/manifest.json bash
```

## Show HN

**Title:** Show HN: sherpa – an evidence-led hackathon mentor skill for Claude Code and OpenCode

> Demo: [sherpa walkthrough](https://github.com/Anshkaliya18/Sherpa/blob/main/docs/public/sherpa.gif) (placeholder until the real recording is added)
>
> Install (Linux/macOS): `curl -fsSL https://raw.githubusercontent.com/Anshkaliya18/Sherpa/v1.0.0/distribution/install.sh | sherpa_RELEASE_MANIFEST_URL=https://github.com/Anshkaliya18/Sherpa/releases/download/v1.0.0/manifest.json bash`
>
> sherpa is a globally installed skill for Claude Code and OpenCode. It helps a team choose a project, plan work against time and judging goals, and prepare a demo using evidence from the project. It keeps unknowns visible and leaves consequential actions to the human.
>
> The v1.0.0 installers placed the skill files in both standard agent directories in an isolated Windows profile. Runtime command loading in either agent is still pending verification. The npx wrapper is in the repository but is not yet published.
>
> The repo includes the skill, installers, workflows, and docs: https://github.com/Anshkaliya18/Sherpa. Feedback on install friction and whether the workflow fits real events is welcome.

## r/ClaudeAI

**Title:** I made a globally installed hackathon mentor skill for Claude Code; looking for install and workflow feedback

> Demo: [sherpa walkthrough](https://github.com/Anshkaliya18/Sherpa/blob/main/docs/public/sherpa.gif) (placeholder until recorded)
>
> Install (Linux/macOS): `curl -fsSL https://raw.githubusercontent.com/Anshkaliya18/Sherpa/v1.0.0/distribution/install.sh | sherpa_RELEASE_MANIFEST_URL=https://github.com/Anshkaliya18/Sherpa/releases/download/v1.0.0/manifest.json bash`
>
> sherpa is a reusable skill that can help with idea selection, next steps, verification, and demo preparation across projects. Its recommendations are meant to cite project evidence and identify unknowns, rather than treating feature count as progress.
>
> I verified that the v1.0.0 installer places a valid skill structure and command manifest in an isolated Claude Code directory. I have not verified command loading inside Claude Code, so I am not claiming runtime compatibility yet. The OpenCode installer path was also checked; its runtime is pending too.
>
> The package includes a preview mode and existing shell/PowerShell installers. The npx package is prepared but not on npm yet. Repo and docs: https://github.com/Anshkaliya18/Sherpa. I’d especially value reports on where installation or the command flow is confusing.

## X / LinkedIn thread

1. **Demo:** [sherpa walkthrough](https://github.com/Anshkaliya18/Sherpa/blob/main/docs/public/sherpa.gif) (placeholder until recorded). **Install (Linux/macOS):** `curl -fsSL https://raw.githubusercontent.com/Anshkaliya18/Sherpa/v1.0.0/distribution/install.sh | sherpa_RELEASE_MANIFEST_URL=https://github.com/Anshkaliya18/Sherpa/releases/download/v1.0.0/manifest.json bash` — a reusable hackathon mentor skill for Claude Code and OpenCode.
2. The workflow starts with the project and its constraints, then helps compare ideas and choose work that fits the time available.
3. Recommendations should connect to files, test results, or other project evidence. Missing proof stays marked unknown; the human keeps approval over consequential steps.
4. I checked the v1.0.0 install paths for both agents in a temporary Windows profile. Runtime loading still needs a real Claude Code and OpenCode session, so that status remains pending.
5. The repository has installers, workflows, docs, and a preview-first npm wrapper that is not published yet. Feedback is welcome: https://github.com/Anshkaliya18/Sherpa
