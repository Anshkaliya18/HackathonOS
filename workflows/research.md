# HackathonOS — Research Workflow

**Operation**: RESEARCH  
**Purpose**: Evaluate research questions against evidence in a deterministic, evidence-based pipeline.  
**Prerequisite:** HackathonOS must be initialized (`.hackathon/project-state.md` exists). If not, run INIT first.

## When to Use

Use RESEARCH when:
- You have a specific research question about the hackathon project
- You need evidence to support or refute a claim
- You want to know what is known, unknown, or assumed about a topic
- You need to research competitors, technologies, rules, or best practices

## Workflow Steps

### Step 1: Define the Research Question

Read from `.hackathon/project-state.md`:
- Hackathon name, deadline, time remaining
- Judging criteria and weights (or UNKNOWN)
- Problem statement
- Target users (if known)

Accept from user:
- Research question (one sentence)
- Scope (what is in scope, what is out of scope)
- Depth (calibration, standard, deep)

If no research question provided:
- Report "No research question provided."
- Ask user to supply a research question before research can run.
- Stop.

### Step 2: Research Plan

Define:
- What evidence is needed
- Where to look (repository files, web search, team input, docs)
- Evidence quality threshold
- Time budget

Record the plan in `.hackathon/evidence/research/<research-query>.md`.

### Step 3: Retrieve

Retrieve candidate evidence from:
- Repository source code, config, tests, docs
- Web search (if available and permitted)
- Team input
- Existing HackathonOS artifacts

Save raw retrieval results to `.hackathon/evidence/research/`.

### Step 4: Verify

For each candidate evidence item:
- Verify the source is real and accessible
- Check the claim against the source text
- Verify numbers, dates, entity names match exactly
- Check polarity/negation
- Check temporal consistency (dates, versions)

### Step 5: Analyze

Classify each claim as FACT, INFERENCE, ASSUMPTION, or UNKNOWN.

### Step 6: Synthesize

Combine evidence into a coherent answer. Address:
- What is known
- What is unknown
- What assumptions must hold
- What the evidence does and does not support

### Step 7: Decide

Determine what the research means for the project decision:
- Does it support proceeding?
- Does it raise blockers?
- What assumptions must hold?
- What is the recommended next action?

### Step 8: Persist

Save the research record to `.hackathon/evidence/research/<research-query>.md`.
Include all evidence, gates, decisions, and unknowns.

## 5. Evidence Model

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

## 6. Source Priority

Priority order for evidence:
1. Official documentation / official repository / official specification
2. Repository source code and tests (direct inspection)
3. Team input (explicitly attributed)
4. Secondary sources (blog posts, tutorials, secondary docs)
5. General web search results (lowest confidence)

## 7. Time Awareness

- If remaining time is UNKNOWN, record TIME STRATEGY = UNKNOWN
- Do not spend unlimited time on research
- If time is limited, prefer repository evidence over web search

## 8. Human Authority

Research recommends; the human decides. Research does not:
- Auto-approve ideas
- Auto-approve architecture
- Auto-approve implementation
- Change the selected idea
- Silently redesign architecture
- Replace Phase 5/7/8 engines

Research findings route to the appropriate phase but do not replace it.

## 9. Output Contract

After each research invocation, return:
- Research question
- Evidence found (with sources and confidence)
- Contradictions found (if any)
- Unknowns
- Decision/recommendation
- Exactly one PRIMARY NEXT ACTION

All research artifacts live in `.hackathon/evidence/research/`.