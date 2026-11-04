# Your first ascent

Five minutes to set a direction, capture a few project facts, and choose a useful next step. Sherpa works inside your project through your coding agent; the exact response depends on the host and project context.

## Before you pack

Install Sherpa for [Claude Code or OpenCode](/installation/), open your hackathon project, and confirm the host has loaded the skill. Runtime loading is currently **NOT VERIFIED**; see [agent compatibility](/agents/).

## 1. Find your bearings

```text
/sherpa help
```

Illustrative response:

```text
Available workflows: init, suggest, status, next, plan, build, verify, demo, submission…
Use /sherpa <workflow> for a focused action.
```

The host may present these instructions differently. The list above is an example, not captured runtime output.

## 2. Set up project notes

```text
/sherpa init
```

Sherpa may create a `.sherpa/` folder with project configuration and a state note. Existing files are preserved. If an older `.hackathon/` folder exists, Sherpa reads it for this compatibility period; `sherpa migrate` offers an explicit copy that never deletes the original.

## 3. Compare a few directions

```text
/sherpa suggest
```

Give the agent the time limit, team size, and judging criteria that matter. Treat the resulting shortlist as material for your discussion, not as an automatic decision.

## 4. Check the state and choose a next action

```text
/sherpa status
/sherpa next
```

Use status to review recorded progress. Next can help identify an action that fits your remaining time and evidence. Keep the decision with your team.

::: checkpoint
Before implementation, make sure the problem, target user, smallest useful demo, and evaluation plan are understandable to everyone on the team.
:::

::: summit-tip
Keep a short record of what you verified and how. A clear demo gets stronger when each claim points to something a judge can see.
:::

## Continue the route

See the [lifecycle map](/concepts/lifecycle), [workflow guides](/workflows/), and [command reference](/reference/commands).
