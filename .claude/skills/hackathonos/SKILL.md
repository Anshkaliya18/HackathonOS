---
name: hackathonos
description: Explicit HackathonOS command entrypoint. Routes the provided operation to the repository SKILL.md while preserving human authority and evidence boundaries.
disable-model-invocation: true
argument-hint: [status|next|help|init|phase]
---

Read the repository-root `SKILL.md` and follow it as the sole routing source. The user-invoked operation and arguments are: `$ARGUMENTS`.

For `status`, `next`, `help`, `init`, and `phase`, route to the corresponding existing operation/workflow in `SKILL.md`. For an empty argument, use the ordinary intent-driven router. Do not invent operations or capabilities. If the requested operation has no implemented workflow, say so and identify it as unavailable. Follow all repository rules, human approval gates, evidence limits, and phase locks. Do not install dependencies, deploy, submit, or make consequential changes unless separately authorized by the user.
