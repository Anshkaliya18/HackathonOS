# HackathonOS — Score Optimization Rules

**Lifecycle Phase:** Phase 10 — Score Optimization Intelligence  
**Purpose:** Authoritative rules for score optimization. Phase 10 reviews and recommends; it does not implement, replace prior phases, or modify locked artifacts.

---

## 1. Purpose and Boundaries

Phase 10 answers: "Given the official judging criteria, actual project evidence, judge simulation results, current implementation state, and remaining time, what changes provide the highest expected increase in judging score?"

Phase 10 optimizes **score**, not feature count.

### Phase 10 MAY:

- Inspect official judging criteria
- Inspect Phase 2 evaluation evidence
- Inspect Phase 3 engineering evidence
- Inspect Phase 4 implementation evidence
- Inspect Phase 5 testing/security evidence
- Inspect Phase 7 UX evidence
- Inspect Phase 8 red-team evidence
- Inspect Phase 9 judge simulation
- Inspect repository/project evidence
- Identify score gaps
- Estimate score impact
- Compare improvement options
- Prioritize improvements
- Identify quick wins
- Identify high-risk improvements
- Identify non-worthwhile work
- Create a score optimization plan
- Create prioritized optimization tasks
- Recommend what to implement next
- Update Phase 10 artifacts and project state

### Phase 10 MUST NOT:

- Redesign the idea
- Re-run idea generation
- Replace architecture
- Own implementation
- Replace testing/security
- Replace UX review
- Replace red-team review
- Replace judge simulation
- Create PPT
- Perform final submission
- Perform postmortem
- Silently modify application code
- Silently modify Phase 1–9 artifacts
- Silently redesign architecture; architecture changes require HUMAN ARCHITECTURE APPROVAL
- Recommend duplicate or unnecessary functionality that adds cost without score impact
- Claim score improvements without evidence
- Invent judging criteria
- Invent judge feedback
- Treat estimated scores as official scores

---

## 2. Evidence Model

Every important optimization claim must identify its evidence status.

Allowed evidence labels:

| Label | Definition |
|-------|------------|
| FACT | Directly observed from repository inspection, verified execution, or external source |
| INFERENCE | Logical conclusion drawn from observed facts |
| ASSUMPTION | Not yet verified; requires confirmation |
| UNKNOWN | No information available; not observed |

Rules:

- Never convert UNKNOWN into a favorable assumption.
- No dimension score or gap classification may be justified by UNKNOWN or ASSUMPTION without explicit flagging.
- Every observation cites reproducible evidence: path/line, route/screen, steps, result, or evidence artifact.
- Generated HackathonOS artifacts are not independent evidence. Evidence must trace back to repository inspection, actual execution, external verification, or explicit human-provided information.
- Do not treat previous AI-generated recommendations as facts.

Example:

GOOD:

> FACT — Official judging criterion gives Technical Implementation 30%.
>
> INFERENCE — Improving reliability may materially improve technical and demo perception.
>
> UNKNOWN — Actual judge score impact cannot be known before judging.

BAD:

> Improving reliability will increase the score by 8 points.

Unless there is actual evidence supporting that numerical claim.

---

## 3. Score Model

Build a transparent score model.

### 3.1 Criterion Weights

If official criterion weights exist (KNOWN from hackathon rules):

Use them. Label as OFFICIAL.

If official weights do not exist (UNKNOWN):

- Mark weights UNKNOWN
- Use a clearly labeled PROVISIONAL equal-weight model only for prioritization
- Never pretend provisional weights are official
- Explicitly state: "Judging criteria unknown; score based on equal-weight provisional assessment"

### 3.2 Score Formula

```
Criterion Score = Evidence-backed performance level (1–10)
Weighted Contribution = Criterion Score × Criterion Weight
Total Estimated Score = Σ(Weighted Contributions) / Σ(Weights)
```

### 3.3 Score Labels

All score estimates must be labeled:

| Label | Meaning |
|-------|---------|
| OFFICIAL | Score comes from official judging rubric or verified judge feedback |
| ESTIMATED | Score is estimated from evidence with clear reasoning |
| PROVISIONAL | Score uses provisional/equal weights because official weights are UNKNOWN |
| UNKNOWN | Insufficient evidence to assign a score |

### 3.4 Numerical Precision

Do not fabricate numerical precision.

GOOD:

```
Technical Implementation:
Current assessment: 7/10
Confidence: MEDIUM
Weight: 30% OFFICIAL
Estimated contribution: 21/30
```

BAD:

```
Technical score = exactly X.Y/30
```

Claiming decimal precision without supporting evidence. Report whole numbers or clearly labeled ranges unless evidence supports finer precision.

---

## 4. Gap Analysis

For every criterion, determine:

| Field | Description |
|-------|-------------|
| Criterion | Official judging criterion name |
| Official Weight | Weight or UNKNOWN |
| Current Evidence | Summary of evidence backing current level |
| Current Performance | 1–10 with confidence |
| Confidence | HIGH / MEDIUM / LOW / UNKNOWN |
| Strengths | What is working well |
| Weaknesses | What is weak |
| Evidence Gap | Weak project performance vs weak evidence of performance (separate findings) |
| Judge Visibility | How observable is this to a judge |
| Improvement Potential | NONE / LOW / MEDIUM / HIGH / CRITICAL / UNKNOWN |
| Risk | Risk of attempting improvement |

Gap classification:

| Classification | Meaning |
|----------------|---------|
| NONE | No meaningful gap |
| LOW | Small gap |
| MEDIUM | Moderate gap |
| HIGH | Large gap |
| CRITICAL | Severe gap threatening scoring |
| UNKNOWN | Insufficient evidence to classify |

### 4.1 Separate Findings

Do not confuse:

**Weak project performance** — The capability itself is weak

with

**Weak evidence of project performance** — The capability may exist but is not demonstrated, documented, or observable by a judge.

These must be separate findings. A project may have strong internal implementation (weak evidence = fixable with documentation/demo) or weak implementation (weak project performance = requires actual code change).

---

## 5. Improvement Categories

Every proposed improvement must belong to one or more categories:

| ID | Category | Description |
|----|----------|-------------|
| A | Differentiation | Improves uniqueness or competitive positioning |
| B | Technical Credibility | Improves architecture quality, engineering quality, reliability, robustness, technical depth |
| C | Core Functionality | Improves the primary user-facing value |
| D | Demo Impact | Makes the core flow clearer, faster, more impressive, or more reliable |
| E | UX | Improves usability, clarity, accessibility, responsive behavior, or interaction quality |
| F | Security / Trust | Improves security, privacy, validation, resilience, or trust |
| G | Evidence | Improves the ability to prove that an existing capability works |
| H | Presentation | Presentation-related score opportunities within current phase scope only. Do not create PPT content; Phase 17 owns presentation. |
| I | Reliability | Improves stability and reduces judge-visible failure risk |

---

## 6. Improvement Value Model

Each candidate improvement must be evaluated using:

| Dimension | Scale |
|-----------|-------|
| Score Impact | VERY LOW / LOW / MEDIUM / HIGH / VERY HIGH |
| Confidence | HIGH / MEDIUM / LOW / UNKNOWN |
| Judge Visibility | LOW / MEDIUM / HIGH / VERY HIGH |
| Implementation Cost | TRIVIAL / LOW / MEDIUM / HIGH / VERY HIGH |
| Risk | LOW / MEDIUM / HIGH / CRITICAL / UNKNOWN |

**OPTIMIZATION HEURISTIC** (prioritization heuristic, NOT judging mathematics):

```
Expected Value = Score Impact × Confidence × Judge Visibility ÷ Implementation Cost
```

Rules:

- Clearly label this as **OPTIMIZATION HEURISTIC**.
- Do not present it as judging mathematics.
- Use qualitative values where numerical precision is unsupported.
- The heuristic ranks candidates for prioritization; it does not produce official scores.

Each candidate must also identify:

- Time required
- Dependencies / blockers
- Whether the improvement is actually worth doing
- What should explicitly NOT be changed (to protect stable, high-scoring areas)

---

## 7. Priority Classification

Every optimization must receive exactly one priority:

| Priority | Definition | Action |
|----------|------------|--------|
| **P0 — CRITICAL** | Must address because it threatens judging readiness, core demo, major criterion, reliability, security, or submission viability | Implement first; human approval if architecture/scope change |
| **P1 — HIGH IMPACT** | Strong score improvement with realistic implementation cost | Implement after P0 items |
| **P2 — MEDIUM IMPACT** | Useful improvement but not essential | Implement if time permits after P0/P1 |
| **P3 — LOW IMPACT** | Minor polish | Implement only if all higher priorities complete and time remains |
| **DROP** | Do not implement | Explicitly rejected; document reason |

Every candidate must receive exactly one priority. No candidate may be unclassified.

---

## 8. Time-Aware Filtering

Apply the lifecycle time-aware strategy:

| Time Remaining | Allow | Block |
|----------------|-------|-------|
| > 24 hours | Core product, differentiation, architecture, important features, validation | Low-judging-value features |
| 12–24 hours | Completing MVP, high-impact features, integration, testing | New feature exploration |
| 6–12 hours | Stability, testing, UX, security, demo reliability, presentation | Architectural changes |
| 2–6 hours | Bug fixing, demo flow, critical polish, PPT, documentation, deployment reliability | Any new feature development |
| < 2 hours | Build working, deployment working, demo working, PPT accurate, links working, critical bugs fixed, submission requirements satisfied | All feature development |

If time remaining is UNKNOWN:

- Mark it UNKNOWN
- Produce a time-neutral plan
- Recommend establishing the deadline if necessary

---

## 9. Project State Fields

Update ONLY these compact fields in `.hackathon/project-state.md`:

| Field | Allowed Values |
|-------|---------------|
| Score Optimization Status | NOT_STARTED | IN_PROGRESS | BLOCKED | COMPLETE |
| Current Estimated Score | <score or UNKNOWN> |
| Potential Score | <score or UNKNOWN> |
| Largest Gaps | <concise list or UNKNOWN> |
| Highest-Priority Improvement | <concise or UNKNOWN> |

Rules:

- Do NOT put detailed optimization analysis inside project-state.md.
- Detailed material goes to `.hackathon/score-optimization.md` and `.hackathon/score-optimization/`.
- Do not change `selected idea`.
- Do not silently change architecture.
- Do not silently modify application code.
- Do not silently modify Phase 1–9 artifacts.
- Human approval required for major scope or architecture changes.

---

## 10. Failure Cases

| Case | Behavior |
|------|----------|
| No selected idea | Stop and request confirmation |
| Missing Phase 9 judge simulation | Report SCORE-OPTIMIZE = LIMITED; proceed with available evidence, mark gaps UNKNOWN |
| Missing judging criteria | Mark UNKNOWN; use provisional equal-weight model; state explicitly |
| Missing repository evidence | Lower confidence; mark unknowns explicitly; do not fabricate |
| Unsupported score claim | Flag as unsupported; do not treat as verified |
| Contradictory claims | Record contradiction; do not silently reconcile |
| Architecture change required | Record ARCHITECTURE CHANGE REQUIRED; route to HUMAN ARCHITECTURE APPROVAL; stop that remediation |
| Idea change attempt | Blocked; route back to Phase 2 / human |
| Unknown deadline | Do not assume one; mark TIME STRATEGY = UNKNOWN |

Phase 10 MUST NOT:

- Write application code
- Modify application source files
- Modify frontend/backend implementation
- Install dependencies
- Deploy the application
- Change the selected idea
- Silently redesign architecture
- Replace Phase 5 testing/security
- Replace Phase 7 UX review
- Replace Phase 8 Red Team
- Replace Phase 9 Judge Simulation
- Perform final presentation generation
- Perform final submission
- Perform post-mortem
- Fabricate judge opinions
- Claim judge reactions without evidence
- Claim score improvements without evidence
- Silently override Phase 8 or Phase 9 decisions

---

## 11. Determinism

Same evidence, criteria, weights, and time remaining → same optimization plan and priority classifications every time. No randomness. No LLM-generated numeric scores without explicit numeric input.
