# HackathonOS — Score Optimization Workflow

**Operation:** SCORE-OPTIMIZE  
**Lifecycle Phase:** Phase 15 — Score Optimization Intelligence  
**Purpose:** Answer "Given the official judging criteria, actual project evidence, judge simulation results, current implementation state, and remaining time, what changes provide the highest expected increase in judging score?" Produce a prioritized optimization plan. Phase 15 optimizes score, not feature count.

## Prerequisites

- `.hackathon/project-state.md` must exist
- `selected idea` must be known (not UNKNOWN)
- Phase 2 idea evaluation evidence must exist
- Phase 3 project plan evidence must exist
- Phase 4 implementation evidence must exist
- Phase 5 testing/security evidence must exist
- Phase 7 UX evidence must exist
- Phase 8 Red Team evidence must exist
- Phase 9 Judge Simulation report must exist (`.hackathon/judge-simulation.md`)
- Judging criteria and weights must be identified (KNOWN) or explicitly marked UNKNOWN

If any prerequisite is missing, mark it UNKNOWN, report SCORE-OPTIMIZE = BLOCKED or LIMITED, and do not invent criteria, weights, or evidence.

## Pipeline

### Stage 1: Read Project State

Read `.hackathon/project-state.md` and capture:

- Hackathon name, deadline, time remaining
- Phase
- Selected idea
- Judging criteria and weights
- Current estimated score, potential score (if previously recorded)
- Largest gaps (if previously recorded)
- Highest-priority improvement (if previously recorded)
- Time-aware strategy category

### Stage 2: Read Prior-Phase Evidence

Consume (do not duplicate or replace) the following evidence:

| Phase | Source | What to consume |
|-------|--------|-----------------|
| Phase 2 | `.hackathon/decisions.md`, `.hackathon/evaluations/<idea>.md` | Selected idea, evaluation scores, differentiation, MVP scope |
| Phase 3 | `.hackathon/evidence/project-plan-*.md` | Architecture, MVP scope (MUST/SHOULD/OPTIONAL/EXCLUDED), workstreams, dependencies, critical path, technical risks, time strategy |
| Phase 4 | `.hackathon/evidence/` implementation artifacts | Repository baseline, components implemented, tests executed, deployment configuration, known issues |
| Phase 5 | `.hackathon/evidence/` testing/security artifacts | Test results, security findings, blocked tests, regression risks, known failures |
| Phase 7 | `.hackathon/ux-review.md`, `.hackathon/ux/` artifacts | UX baseline, critical flows, findings, quality gate status, limitations |
| Phase 8 | `.hackathon/red-team.md`, `.hackathon/red-team/` artifacts | Red team findings, risks, mitigations, quality gate status, limitations |
| Phase 9 | `.hackathon/judge-simulation.md` | Judge simulation report, criterion-by-criterion observations, judge concerns, judge trust, differentiation perception |

Do not re-run Phase 2–9 engines. Consume their evidence only.

Flag contradictory claims between phases or between documentation and repository:

```text
Documentation says X
Repository does Y
Phase 9 simulation says Z
```

Do not silently reconcile contradictions. Record them as separate findings.

### Stage 3: Inspect Current Repository

Inspect the actual repository:

- Project metadata
- Dependency manifests
- Top-level project structure
- Application entry points
- Frontend/backend/database/AI components
- APIs
- Tests
- Deployment configuration
- Documentation
- Environment configuration

Classify every observation as FACT, INFERENCE, ASSUMPTION, or UNKNOWN. Cite repository path/line or execution result.

Rules:
- Never fabricate repository facts.
- Seeing a file does not mean it works.
- Generated HackathonOS artifacts are not independent evidence.

### Stage 4: Build Score Model

For each official judging criterion:

1. Map criterion to contributing evidence from Phases 2–9 and repository inspection.
2. Assign a current performance level (1–10 scale) with evidence type and confidence.
3. Use official criterion weight if KNOWN. If weights are UNKNOWN, mark UNKNOWN and use a clearly labeled PROVISIONAL equal-weight model only for prioritization. Never pretend provisional weights are official.
4. Calculate weighted contribution = criterion score × criterion weight.
5. Label every score estimate: OFFICIAL, ESTIMATED, PROVISIONAL, or UNKNOWN.
6. Do not fabricate numerical precision (e.g., do not report "exactly 23.7/30" without supporting evidence).

Score model record:

```
Criterion Score = Evidence-backed performance level (1–10)
Weighted Contribution = Criterion Score × Criterion Weight
Total Estimated Score = Σ(Weighted Contributions) / Σ(Weights)
```

### Stage 5: Gap Analysis

For every criterion, complete a gap analysis using `templates/gap-analysis.md`:

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

Classify the gap:
- **NONE** — No meaningful gap
- **LOW** — Small gap
- **MEDIUM** — Moderate gap
- **HIGH** — Large gap
- **CRITICAL** — Severe gap threatening scoring
- **UNKNOWN** — Insufficient evidence to classify

Separate findings:
- **Weak project performance** — The capability itself is weak
- **Weak evidence of project performance** — The capability may exist but is not demonstrated/documented

### Stage 6: Generate Improvement Candidates

For every criterion with a gap (LOW or higher), generate improvement candidates. Each candidate must belong to one or more categories:

| Category | Description |
|----------|-------------|
| A. Differentiation | Improves uniqueness or competitive positioning |
| B. Technical Credibility | Improves architecture quality, engineering quality, reliability, robustness, technical depth |
| C. Core Functionality | Improves the primary user-facing value |
| D. Demo Impact | Makes the core flow clearer, faster, more impressive, more reliable |
| E. UX | Improves usability, clarity, accessibility, responsive behavior, interaction quality |
| F. Security / Trust | Improves security, privacy, validation, resilience, trust |
| G. Evidence | Improves the ability to prove an existing capability works |
| H. Presentation | Presentation-related score opportunities within current phase scope only (no PPT creation; Phase 17 owns presentation) |
| I. Reliability | Improves stability and reduces judge-visible failure risk |

For each candidate, identify:
- What specifically would change
- Which criterion it improves
- Evidence label (FACT / INFERENCE / ASSUMPTION / UNKNOWN) for the claim that this change helps
- Dependencies or blockers
- What explicitly should NOT be changed (to protect stable, high-scoring areas)

### Stage 7: Evaluate Each Candidate

For each improvement candidate, use `templates/improvement-candidate.md` and evaluate:

| Dimension | Scale |
|-----------|-------|
| Score Impact | VERY LOW / LOW / MEDIUM / HIGH / VERY HIGH |
| Confidence | HIGH / MEDIUM / LOW / UNKNOWN |
| Judge Visibility | LOW / MEDIUM / HIGH / VERY HIGH |
| Implementation Cost | TRIVIAL / LOW / MEDIUM / HIGH / VERY HIGH |
| Risk | LOW / MEDIUM / HIGH / CRITICAL / UNKNOWN |

**OPTIMIZATION HEURISTIC** (prioritization heuristic only, NOT judging mathematics):

```
Expected Value = Score Impact × Confidence × Judge Visibility ÷ Implementation Cost
```

Label this clearly as **OPTIMIZATION HEURISTIC**. Do not present it as judging mathematics. Use qualitative values where numerical precision is unsupported.

Also identify:
- Time required
- Whether the improvement is worth doing
- Time-aware filtering (apply lifecycle time-aware strategy)

### Stage 8: Classify Priorities

Assign exactly one priority to every candidate:

| Priority | Definition |
|----------|------------|
| **P0 — CRITICAL** | Must address because it threatens judging readiness, core demo, major criterion, reliability, security, or submission viability |
| **P1 — HIGH IMPACT** | Strong score improvement with realistic implementation cost |
| **P2 — MEDIUM IMPACT** | Useful improvement but not essential |
| **P3 — LOW IMPACT** | Minor polish |
| **DROP** | Do not implement |

Every optimization must receive exactly one priority.

### Stage 9: Build Prioritized Optimization Plan

Use `templates/score-optimization-plan.md` to produce the output plan:

1. Current evidence-backed score position (criterion-by-criterion)
2. Strongest scoring dimensions
3. Weakest scoring dimensions
4. Largest score gaps
5. Prioritized improvement list (P0 first, then P1, P2, P3, then DROP)
6. Smallest set of actions likely to produce the largest judging improvement
7. What should explicitly NOT be changed
8. Time-aware filtering applied

### Stage 10: Update Project State

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
- Do not silently redesign architecture; architecture changes require human approval.
- Do not silently modify application code.
- Do not silently modify Phase 1–9 artifacts.
- Human approval required for major scope or architecture changes.

### Stage 11: Return Exactly One Primary Next Action

Output format:

```
PRIMARY NEXT ACTION: <exactly one action>

WHY: <explanation based on impact, time, risk, and judging criteria>

DONE WHEN: <clear definition of done>

Time remaining: <hours or UNKNOWN>

Blocked by: <blocker or "None">
```

Rule: Exactly one primary next action. Do not produce competing alternatives.

## Validation Checklist

After SCORE-OPTIMIZE completes:

- [ ] Project state read and verified
- [ ] Phase 2–4, 11–14 evidence consumed (not duplicated)
- [ ] Repository inspected for evidence
- [ ] Score model built with official or explicitly provisional weights
- [ ] Every score labeled OFFICIAL / ESTIMATED / PROVISIONAL / UNKNOWN
- [ ] No false numerical precision claimed
- [ ] Gap analysis completed for every criterion
- [ ] Weak project performance separated from weak evidence of performance
- [ ] Improvement candidates generated for all gapped criteria
- [ ] Each candidate assigned to one or more categories (A–I)
- [ ] Each candidate evaluated with Score Impact, Confidence, Judge Visibility, Cost, Risk
- [ ] OPTIMIZATION HEURISTIC labeled as heuristic, not judging mathematics
- [ ] Every candidate assigned exactly one priority (P0–P3 or DROP)
- [ ] Prioritized optimization plan produced
- [ ] Smallest set of high-impact actions identified
- [ ] What NOT to change identified
- [ ] Time-aware filtering applied
- [ ] Project state updated with compact fields only
- [ ] No Phase 1–9 artifacts modified
- [ ] No application source code modified
- [ ] No PPT created
- [ ] No final submission performed
- [ ] No postmortem performed
- [ ] Exactly ONE primary next action returned
