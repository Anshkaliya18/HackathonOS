# sherpa — NEXT Workflow

**Operation**: NEXT  
**Purpose**: Identify exactly ONE highest-priority action to take right now, based on project state, time remaining, risks, and judging criteria.

## When to Use

Use NEXT when:
- You need to know what to work on right now
- You want to avoid wasting time on low-impact tasks
- You want a single clear direction instead of a long task list

## Workflow Steps

### Step 1: Verify State Exists

Check if `.sherpa/project-state.md` exists. If not, recommend INIT first and stop.

### Step 2: Read Project State

Read `.sherpa/project-state.md` and capture:
- Phase
- Time remaining (from deadline)
- Completed work, current work, blocked work
- Risks, known weaknesses
- Current estimated score, potential score
- Largest gaps
- Judging criteria and weights

### Step 3: Inspect Repository for Evidence

Inspect the repository to verify the current state of implementation. Look for broken features, missing tests, missing deployment config, etc.

### Step 4: Apply Time-Aware Filtering

Filter candidate actions based on time remaining:

| Time Remaining | Allow | Block |
|----------------|-------|-------|
| > 24 hours | Core product, differentiation, architecture, important features, validation | Low-judging-value features |
| 12–24 hours | Completing MVP, high-impact features, integration, testing | New feature exploration |
| 6–12 hours | Stability, testing, UX, security, demo reliability, presentation | Architectural changes |
| 2–6 hours | Bug fixing, demo flow, critical polish, PPT, documentation, deployment reliability | Any new feature development |
| < 2 hours | Build working, deployment working, demo working, PPT accurate, links working, critical bugs fixed, submission requirements | All feature development |

### Step 5: Apply Red-Team Filtering

For each candidate action, ask:
- Does this address a known weakness or risk?
- Would a judge likely penalize us if this is not done?
- Is this fixing a contradiction between PPT/README/code/demo?
- Is this addressing the biggest current risk?

### Step 6: Score Candidates

For each remaining candidate, estimate:
- Expected judging impact (High/Medium/Low)
- Implementation effort (Small/Medium/Large)
- Time required
- Technical risk
- Demo risk
- Alignment with judging criteria weights

### Step 7: Select ONE Primary Next Action

Choose the candidate with the highest `judging impact / time / risk` ratio. There must be exactly ONE.

Report:

```
PRIMARY NEXT ACTION: [action name]

Why this is the highest priority:
  [explanation based on impact, time, risk, and judging criteria]

What you need to do:
  [specific, actionable steps]

What completion looks like:
  [clear definition of done]

Time remaining: [time or UNKNOWN]
Blocked by: [any blockers or "None"]
```

Secondary actions may be listed optionally, but must be clearly marked as secondary.

## Validation

After NEXT completes:
- [ ] Exactly one primary next action is identified
- [ ] The "why" explains impact, time, risk, and judging criteria alignment
- [ ] "What you need to do" is specific and actionable
- [ ] "What completion looks like" is a clear definition of done
- [ ] Time-aware filtering was applied
- [ ] Secondary actions (if any) are clearly marked as secondary
