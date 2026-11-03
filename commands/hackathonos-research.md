# HackathonOS Research Command

Research candidate ideas against evidence.

## Operation: RESEARCH

**Purpose**: Evaluate research questions against evidence in a deterministic pipeline.

**Prerequisite:** HackathonOS must be initialized (`.hackathon/project-state.md` exists).

## Input

**Read from `.hackathon/project-state.md`:**
- Hackathon name, deadline, time remaining
- Judging criteria and weights (or UNKNOWN)
- Problem statement
- Target users (if known)

**Accept from user:**
- Research question (one sentence)
- Scope (what is in scope, what is out of scope)
- Depth (calibration, standard, deep)

**If no research question provided:**
- Report "No research question provided."
- Ask user to supply a research question before research can run.
- Stop.

## Workflow Steps

### Step 1: Research Plan

Define:
- What needs to be found
- Where to look (repository files, web search, documentation, team input)
- Evidence quality threshold
- Time budget

Record the plan in `.hackathon/evidence/research/<research-query>.md`.

### Step 2: Retrieve

Retrieve candidate evidence from:
- Repository source code, config, tests, docs
- Web search (if available and permitted)
- Team input
- Existing HackathonOS artifacts

Save raw retrieval results to `.hackathon/evidence/research/`.

### Step 3: Verify

For each candidate evidence item:
- Verify the source is real and accessible
- Check the claim against the source text
- Verify numbers, dates, entity names match exactly
- Check polarity/negation
- Check temporal consistency (dates, versions)

### Step 4: Analyze

Classify each claim as FACT, INFERENCE, ASSUMPTION, or UNKNOWN.

### Step 5: Synthesize

Combine evidence into a coherent answer:
- What is known (FACT)
- What is reasonable (INFERENCE)
- What is assumed (ASSUMPTION)
- What is unknown (UNKNOWN)

### Step 6: Decide

Determine what the research means for the project decision:
- Does it support proceeding?
- Does it raise blockers?
- What assumptions must hold?
- What is the recommended next action?

### Step 7: Persist

Save the research record to `.hackathon/evidence/research/<research-query>.md`.
Include all evidence, gates, decisions, and unknowns.

## Evidence Model

| Field | Values |
|-------|--------|
| type | FACT | INFERENCE | ASSUMPTION | UNKNOWN |
| value | The claim |
| source | URL, file path, or "team input" |
| confidence | low | medium | high |

Rules:
- No claim may be tagged FACT unless directly verified from source
- No claim may be tagged INFERENCE without explicit reasoning
- ASSUMPTION must be explicitly marked as provisional
- UNKNOWN means no information available
- Never claim research was performed unless evidence was actually retrieved

## Source Priority

Priority order for evidence:
1. Official documentation / official repository / official specification
2. Repository source code and tests (direct inspection)
3. Team input (explicitly attributed)
4. Secondary sources (blog posts, tutorials, secondary docs)
5. General web search results (lowest confidence)

## Source Consistency

When multiple sources conflict:
- Record each claim separately with its source
- Do not silently reconcile contradictions
- Flag contradictory claims explicitly
- Mark conflicting claims as UNKNOWN until resolved

## Time Awareness

- If remaining time is UNKNOWN, record `TIME STRATEGY = UNKNOWN`
- Do not spend unlimited time on research
- If time is limited, prefer repository evidence over web search
- Record time spent on research if it exceeds a reasonable threshold

## Human Authority

Research recommends; the human decides. Research does not:
- Auto-approve ideas
- Auto-approve architecture
- Auto-approve implementation
- Change the selected idea
- Silently redesign architecture
- Replace Phase 5/7/8 engines

Research findings route to the appropriate phase but do not replace it.

## Output Contract

After each research invocation, return:
- Research question
- Evidence found (with sources and confidence)
- Contradictions found (if any)
- Unknowns
- Decision/recommendation
- Exactly one PRIMARY NEXT ACTION

All research artifacts live in `.hackathon/evidence/research/`.
