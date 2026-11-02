# HackathonOS — Research Rules

Defines authoritative behavior for the Research capability. Research is a reusable capability
that supports multiple lifecycle phases (Understand Rules, Analyze Problem, Generate Ideas,
Validate Ideas, Research Market, Select Idea, Architecture, Data Architecture, Development
Plan, Testing, Security, UX, Judge Simulation, Score Optimization, Demo Preparation,
Presentation, Final Audit, Submission, Post-Mortem). It does not create a new lifecycle phase.

## 1. Purpose

Research provides transparent, evidence-based answers to research questions. It is not
autonomous web browsing; it is a disciplined process of finding, verifying, and organizing
evidence to support hackathon decisions.

Every research claim must carry an evidence tag: FACT, INFERENCE, ASSUMPTION, or UNKNOWN.
Every research output must trace back to repository inspection, actual execution, external
verification, or explicit human-provided information.

## 2. Core Principles

### Evidence Discipline

Classify repository observations and claims as FACT, INFERENCE, ASSUMPTION, or UNKNOWN.
Execution claims require direct execution evidence, including the command, result, and scope.
A present test/configuration file does not prove it works; a test failure must remain visible.
Generated HackathonOS state, plans, tasks, and recommendations are planning records, not
independent repository facts or execution evidence.

Never invent a commit, installed dependency, test/build result, environment value, API behavior,
deployment result, completion claim, or remaining time. When Git is unavailable, record
`Git baseline = UNKNOWN`.

### Human Authority

Research is advisory. The human team decides what to believe and what to do. Research does not
auto-approve ideas, architecture, implementation, or any decision. Research findings route to
the appropriate phase but do not replace that phase's engine.

### Time Awareness

Research should be time-bounded. Do not spend unlimited time searching. If
remaining time is UNKNOWN, record `TIME STRATEGY = UNKNOWN` and give a
time-neutral research order.

## 3. Research Pipeline Stages

### Stage 1: Input

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

### Step 2: Research Plan

Define:
- What needs to be found
- Where to look (repository files, web search, documentation, team input)
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

## 4. Evidence Model

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

## 5. Source Priority

Priority order for evidence:
1. Official documentation / official repository / official specification
2. Repository source code and tests (direct inspection)
3. Team input (explicitly attributed)
4. Secondary sources (blog posts, tutorials, secondary docs)
5. General web search results (lowest confidence)

## 6. Source Consistency

When multiple sources conflict:
- Record each claim separately with its source
- Do not silently reconcile contradictions
- Flag contradictory claims explicitly
- Mark conflicting claims as UNKNOWN until resolved

## 7. Time Awareness

- If remaining time is UNKNOWN, record `TIME STRATEGY = UNKNOWN`
- Do not spend unlimited time on research
- If time is limited, prefer repository evidence over web search
- Record time spent on research if it exceeds a reasonable threshold

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
