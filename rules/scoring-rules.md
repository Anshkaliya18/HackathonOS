# HackathonOS — Scoring Rules

Defines the Idea Intelligence Engine scoring model. All scores are deterministic:
- Same evidence, criteria, weights, team capability, and time → same score and recommendation.
- No randomness. No LLM-generated scores without explicit numeric input.
- No stacked multipliers. One Feasibility & Risk Gate only.

---

## 1. Diagnostic Dimension Categories (21 dimensions, each in exactly one category)

Each dimension appears in exactly one category. Categories contribute to non-overlapping judging criteria.
Category 6 (Criteria Alignment) is a validation layer — it does not add points.

| # | Category | Dimensions | Primary Judging Criteria Mapped |
|---|----------|------------|--------------------------------|
| 1 | Problem & Solution | 1, 2, 3, 4, 5 | Problem significance, User value |
| 2 | Innovation & Differentiation | 6, 7 | Innovation |
| 3 | Technical Feasibility | 8, 9, 10 | Technical implementation |
| 4 | Implementation Reality | 11, 12 | Feasibility, Team capability |
| 5 | Demo & Presentation | 13, 14 | Demo quality, Presentation quality |
| 6 | Criteria Alignment | 15 | All judging criteria (meta-validation) |
| 7 | Impact & Market | 16, 17 | Potential impact, Business value |
| 8 | Competition & Risk | 18, 19 | Differentiation context, Market opportunity |
| 9 | Risk & Evidence | 20, 21 | Risk level, Score reliability |

**Dimension 15 (Judging-criteria alignment)** is placed in Category 6 only. It produces a boolean check: "Do all category scores map to stated criteria?" If criteria are `UNKNOWN`, this check fails and overall confidence is lowered.

---

## 2. Dimension Definitions (1–10 scale unless noted)

| # | Dimension | Scale | Meaning |
|---|-----------|-------|---------|
| 1 | Problem importance | 1–10 | How meaningful is the problem? |
| 2 | Problem clarity | 1–10 | Is the problem well-defined? |
| 3 | Target-user clarity | 1–10 | Who is the user, exactly? |
| 4 | User pain | 1–10 | How painful is the problem for users? |
| 5 | Solution usefulness | 1–10 | Does the solution actually help? |
| 6 | Innovation | 1–10 | Is it novel? |
| 7 | Differentiation | 1–10 | How different from competitors? |
| 8 | Technical feasibility | 1–10 | Can it be built? (10 = high feasibility) |
| 9 | AI/ML necessity | 1–10 | Is AI actually needed? (10 = essential, 1 = superficial) |
| 10 | Implementation complexity | 1–10 | How complex to build? (10 = high complexity) |
| 11 | Time required | 1–10 | How much time needed? (10 = maximum time) |
| 12 | Team skill fit | 1–10 | Does the team have the skills? (10 = high fit) |
| 13 | Demo potential | 1–10 | Is the demo compelling? |
| 14 | Judge appeal | 1–10 | Will judges like it? |
| 15 | Judging-criteria alignment | 1–10 | Do scores map to stated criteria? |
| 16 | Scalability/potential | 1–10 | Growth potential beyond hackathon |
| 17 | Real-world impact | 1–10 | Actual user value |
| 18 | Competitive landscape | 1–10 | Less competition = higher score |
| 19 | Defensibility | 1–10 | Hard to copy? |
| 20 | Risk | 1–10 | **10 = highest risk** (penalty increases with score) |
| 21 | Evidence quality | 1–10 | How well-backed are claims? |

**Risk direction (dimension 20):** 1 = lowest risk, 10 = highest risk. Higher score = higher penalty.

---

## 3. Criterion-to-Category Mapping

| Judging Criterion | Contributing Categories | Dimensions |
|-------------------|------------------------|------------|
| Problem significance | Problem & Solution | 1, 2, 4 |
| User value | Problem & Solution | 3, 5 |
| Innovation | Innovation & Differentiation | 6 |
| Technical implementation | Technical Feasibility | 8, 9, 10 |
| Feasibility / Team | Implementation Reality | 11, 12 |
| Demo quality | Demo & Presentation | 13 |
| Presentation quality | Demo & Presentation | 14 |
| Criteria alignment | Criteria Alignment | 15 (validation only) |
| Impact / potential | Impact & Market | 16, 17 |
| Market opportunity | Competition & Risk | 18, 19 |
| Risk adjustment | Risk & Evidence | 20, 21 |

**No double-counting rule:** Each dimension appears in exactly one category. Each category contributes to non-overlapping judging criteria. Category 6 does not add points — it validates mapping.

---

## 4. Judging Criteria Weighting

### When criteria and weights are known

Use the hackathon's published judging criteria and weights as the primary scoring buckets:

```
raw_score = Σ(criterion_score_i × weight_i) / Σ(weight_i)
```

Where `criterion_score_i` is the weighted average of category scores mapped to that criterion.

### When criteria/weights are UNKNOWN

- Use equal weights across available categories
- Set overall confidence flag = `low`
- Explicitly state: "Judging criteria unknown; score based on equal-weight diagnostic assessment"
- Do NOT present false precision

---

## 5. Feasibility & Risk Gate (single documented adjustment)

The five feasibility/risk dimensions (8, 10, 11, 12, 20) already feed into categories 3, 4, and 9. Instead of applying separate multipliers on top, apply **one documented gate**:

```
feasibility_composite = avg(
    dimension_8,                        // technical feasibility (10 = high feasibility)
    (11 - dimension_10),                // implementation complexity inverted (10 = simple)
    (11 - dimension_11),                // time required inverted (10 = fits in time)
    dimension_12,                        // team skill fit (10 = high fit)
    (11 - dimension_20)                 // risk inverted (10 = low risk)
)
```

**Gate thresholds:**

| Composite Range | Gate Result | Implication |
|-----------------|-------------|-------------|
| ≥ 6.0 | PASS | Idea can be SELECTed |
| < 6.0 | FAIL | Idea cannot be SELECTed; must be REVISE or REJECT_ALL |

**Rationale:** This is a single gate, not stacked multipliers. The five dimensions count once in their categories; the gate is a single feasibility threshold.

---

## 6. Final Score Formula

```
raw_score = weighted criterion average (0–100)
final_score = raw_score × (feasibility_composite / 10)
```

The `(feasibility_composite / 10)` factor is the **only** multiplicative adjustment. No team_fit_factor, no time_pressure_factor, no separate risk_penalty. Those dimensions are already accounted for inside `feasibility_composite`.

---

## 7. Confidence Model

| Factor | High Confidence | Medium Confidence | Low Confidence |
|--------|----------------|-------------------|----------------|
| Evidence quality (dim 21) | ≥ 8 | 5–7 | ≤ 4 |
| Judging criteria known | Yes | Partial | UNKNOWN |
| Dimension scores all filled | Yes | 1–2 missing | 3+ missing |

**Overall confidence:** Lowest confidence across all factors.

---

## 8. Evidence Model

Every research claim carries:

| Field | Values |
|-------|--------|
| `type` | FACT | INFERENCE | ASSUMPTION | UNKNOWN |
| `value` | The claim |
| `source` | URL, file path, or "team input" |
| `confidence` | low | medium | high |

**Rules:**
- No dimension score may be justified by `UNKNOWN` or `ASSUMPTION` without explicit flagging.
- Never claim research was performed unless evidence was actually retrieved.
- Separate FACT from INFERENCE from ASSUMPTION.

---

## 9. Red-Team Outcomes (Deterministic)

| Outcome | Definition | Conditions |
|---------|------------|------------|
| **KILL** | Idea cannot be presented; fundamental flaw | (a) Feasibility gate FAIL with no credible revision path within time, OR (b) dimension_20 ≥ 9 AND dimension_8 ≤ 3, OR (c) dimension_9 ≤ 3 AND idea claims "AI-powered" (superficial AI) |
| **MAJOR CONCERN** | Significant weakness, fixable | Any criterion-critical dimension scores 3–5, OR feasibility gate score 6.0–7.0 |
| **MINOR CONCERN** | Cosmetic weakness | Any non-critical dimension scores 6–7 |

**Not unnecessarily aggressive:** KILL requires either (a) feasibility gate failure with no revision path, or (b) simultaneous high risk + low feasibility, or (c) superficial AI claim. A single medium score does not trigger KILL.

---

## 10. Decision Outcomes

| Outcome | Meaning | Effect on project-state.md |
|---------|---------|---------------------------|
| **SELECT** | One idea recommended | Writes to `.hackathon/decisions.md` only. Does NOT set `selected idea` |
| **REVISE** | Ideas need modification | Writes revision plan to `.hackathon/decisions.md`. No change to `selected idea` |
| **REJECT_ALL** | No candidate ideas viable | Writes rejection rationale to `.hackathon/decisions.md`. No change to `selected idea` |

**Human authority:** Only explicit human confirmation can change `selected idea` in `.hackathon/project-state.md`.

---

## 11. Acceptance Test Definitions

| Test | Expected Result |
|------|----------------|
| Missing dimension detection | Any dimension scored `UNKNOWN` is flagged; score carries low confidence |
| Risk direction correctness | risk_dimension=10 produces higher penalty than risk_dimension=1 |
| No double-counting | Each of 21 dimensions appears in exactly one category |
| Known judging criteria | Score uses published weights; confidence not lowered for criteria |
| Unknown judging criteria | Score uses equal weights; confidence flag = low; explicit note stated |
| Human confirmation requirement | Engine never auto-sets `selected idea`; human must confirm explicitly |
| REVISE loop | REVISE → weaknesses → changes → re-evaluate → new outcome supported |
| Red-team kill conditions | KILL triggers only under defined conditions (gate failure, risk+feasibility, superficial AI) |
| Exactly one primary next action | Output always contains exactly one PRIMARY NEXT ACTION |

---

## 12. Determinism Guarantee

Two runs with identical:
- Evidence (same FACT/INFERENCE/ASSUMPTION/UNKNOWN tags and sources)
- Criteria and weights
- Team capability (dimension 12)
- Time remaining (dimension 11)

…must produce identical scores and recommendations. No randomness. No LLM-generated numeric scores without explicit input.
