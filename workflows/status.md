# sherpa — STATUS Workflow

**Operation**: STATUS  
**Purpose**: Accurately report the current project state by reading `.sherpa/project-state.md` and inspecting the repository for evidence.

## When to Use

Use STATUS when:
- You want to know where you are in the hackathon
- You want to know what's complete, what's in progress, what's blocked
- You want to know your biggest risks and what's incomplete
- You need a snapshot before deciding what to do next

## Workflow Steps

### Step 1: Verify State Exists

Check if `.sherpa/project-state.md` exists in the current project repository.

If it does NOT exist:
- Report that sherpa has not been initialized for this project
- Recommend running INIT first
- Stop

### Step 2: Read Project State

Read `.sherpa/project-state.md` and capture:
- Hackathon name, deadline, time remaining
- Phase
- Problem statement, selected idea, MVP scope
- Tech stack, architecture
- Completed work, current work, blocked work
- Risks, known weaknesses, open questions
- Current estimated score, potential score
- Demo status, PPT status, documentation status

### Step 3: Inspect Repository for Evidence

Inspect the repository to verify claims in the state file. Look for:
- `package.json`, `requirements.txt`, `pyproject.toml` (tech stack verification)
- Source code files (implementation evidence)
- README (documentation evidence)
- Test files (testing evidence)
- Deployment configuration (deployment evidence)
- Environment configuration (secrets/config evidence)

Do NOT make claims about the project without evidence when the repository can be inspected.

### Step 4: Compare State to Reality

Identify gaps between what `.sherpa/project-state.md` says and what the repository shows:
- State says "Authentication implemented" but no auth code exists → flag discrepancy
- State says "Tests passing" but no test files exist → flag discrepancy
- State says "Deployed" but no deployment config exists → flag discrepancy

### Step 5: Calculate Time Remaining

If deadline is known, calculate time remaining from current date/time. If deadline is `UNKNOWN`, report time remaining as `UNKNOWN`.

### Step 6: Report Status

Present a structured status report:

```
sherpa Status — [Hackathon Name]

Phase: [phase]
Time remaining: [time or UNKNOWN]

Project State:
  Problem: [problem statement or UNKNOWN]
  Selected idea: [idea or UNKNOWN]
  MVP scope: [MVP or UNKNOWN]
  Tech stack: [stack or UNKNOWN]

Completed: [list or UNKNOWN]
In progress: [list or UNKNOWN]
Blocked: [list or UNKNOWN]

Risks: [list or UNKNOWN]
Known weaknesses: [list or UNKNOWN]
Open questions: [list or UNKNOWN]

Scores:
  Current estimated: [score or UNKNOWN]
  Potential: [score or UNKNOWN]

Deliverables:
  Demo: [status or UNKNOWN]
  PPT: [status or UNKNOWN]
  Documentation: [status or UNKNOWN]

Evidence Gaps (state vs repository):
  [any discrepancies found]

Biggest Current Risk: [single risk or UNKNOWN]
```

## Validation

After STATUS completes:
- [ ] `.sherpa/project-state.md` was read
- [ ] Repository was inspected for evidence
- [ ] No claims made without evidence
- [ ] Discrepancies between state and reality are flagged
- [ ] Time remaining is calculated or marked UNKNOWN
- [ ] Biggest current risk is identified (one risk, not a list)
