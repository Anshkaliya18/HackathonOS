# Idea Evaluation — <idea-name>

**One-line description:** <one-sentence description>

**Submitted by:** <team member or "team">
**Evaluation date:** <UTC date/time>

---

## 1. Problem & Solution Framing

**Problem statement:** <problem as stated by user>

**Target users:** <who the product is for, or UNKNOWN>

**Proposed solution:** <one-sentence solution description>

---

## 2. Category Scores

Each dimension is scored 1–10 with reasoning, evidence type (FACT / INFERENCE / ASSUMPTION / UNKNOWN), source, and confidence (low / medium / high).

### Category 1: Problem & Solution

| Dimension | Score | Reasoning | Evidence Type | Source | Confidence |
|-----------|-------|-----------|---------------|--------|------------|
| 1. Problem importance | | | | | |
| 2. Problem clarity | | | | | |
| 3. Target-user clarity | | | | | |
| 4. User pain | | | | | |
| 5. Solution usefulness | | | | | |

**Category score:** <weighted average or simple average>

---

### Category 2: Innovation & Differentiation

| Dimension | Score | Reasoning | Evidence Type | Source | Confidence |
|-----------|-------|-----------|---------------|--------|------------|
| 6. Innovation | | | | | |
| 7. Differentiation | | | | | |

**Category score:** <average>

---

### Category 3: Technical Feasibility

| Dimension | Score | Reasoning | Evidence Type | Source | Confidence |
|-----------|-------|-----------|---------------|--------|------------|
| 8. Technical feasibility | | | | | |
| 9. AI/ML necessity | | | | | |
| 10. Implementation complexity | | | | | |

**Category score:** <average>

---

### Category 4: Implementation Reality

| Dimension | Score | Reasoning | Evidence Type | Source | Confidence |
|-----------|-------|-----------|---------------|--------|------------|
| 11. Time required | | | | | |
| 12. Team skill fit | | | | | |

**Category score:** <average>

---

### Category 5: Demo & Presentation

| Dimension | Score | Reasoning | Evidence Type | Source | Confidence |
|-----------|-------|-----------|---------------|--------|------------|
| 13. Demo potential | | | | | |
| 14. Judge appeal | | | | | |

**Category score:** <average>

---

### Category 6: Criteria Alignment (Meta-Validation)

| Dimension | Score | Reasoning | Evidence Type | Source | Confidence |
|-----------|-------|-----------|---------------|--------|------------|
| 15. Judging-criteria alignment | | | | | |

**Alignment check:** <PASS / FAIL — do all category scores map to stated judging criteria?>

**Note:** Category 6 does not add points. It validates that other category scores correctly map to the hackathon's stated criteria.

---

### Category 7: Impact & Market

| Dimension | Score | Reasoning | Evidence Type | Source | Confidence |
|-----------|-------|-----------|---------------|--------|------------|
| 16. Scalability/potential | | | | | |
| 17. Real-world impact | | | | | |

**Category score:** <average>

---

### Category 8: Competition & Risk Context

| Dimension | Score | Reasoning | Evidence Type | Source | Confidence |
|-----------|-------|-----------|---------------|--------|------------|
| 18. Competitive landscape | | | | | |
| 19. Defensibility | | | | | |

**Category score:** <average>

---

### Category 9: Risk & Evidence Quality

| Dimension | Score | Reasoning | Evidence Type | Source | Confidence |
|-----------|-------|-----------|---------------|--------|------------|
| 20. Risk | | | | | |
| 21. Evidence quality | | | | | |

**Category score:** <average>

---

## 3. Research Evidence

List all external research used to support dimension scores. Each entry must be tagged FACT / INFERENCE / ASSUMPTION / UNKNOWN with a source.

| # | Claim | Type | Source | Confidence |
|---|-------|------|--------|------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

**Rule:** Never claim research was performed unless evidence was actually retrieved. If no evidence exists, mark UNKNOWN.

---

## 4. Feasibility & Risk Gate

**Calculation:**

```
feasibility_composite = avg(
    dimension_8,                        // technical feasibility
    (11 - dimension_10),                // implementation complexity inverted
    (11 - dimension_11),                // time required inverted
    dimension_12,                        // team skill fit
    (11 - dimension_20)                 // risk inverted
)
```

| Component | Value |
|-----------|-------|
| Dimension 8 (technical feasibility) | |
| Dimension 10 (implementation complexity) | |
| 11 − dimension_10 (inverted complexity) | |
| Dimension 11 (time required) | |
| 11 − dimension_11 (inverted time) | |
| Dimension 12 (team skill fit) | |
| Dimension 20 (risk) | |
| 11 − dimension_20 (inverted risk) | |
| **feasibility_composite** | **<value> / 10** |

**Gate result:** <PASS (≥ 6.0) | FAIL (< 6.0)>

---

## 5. Red-Team Outcome

**Outcome:** <KILL | MAJOR CONCERN | MINOR CONCERN>

**KILL conditions checked:**
- [ ] Feasibility gate FAIL with no credible revision path within time
- [ ] Dimension 20 (risk) ≥ 9 AND Dimension 8 (feasibility) ≤ 3
- [ ] Dimension 9 (AI necessity) ≤ 3 AND idea claims "AI-powered"

**Weaknesses identified:**
1. <weakness 1>
2. <weakness 2>
3. <weakness 3>

**Kill question that exposes biggest weakness:** <question>

---

## 6. Scoring

**Judging criteria used:** <list criteria and weights, or "UNKNOWN — equal weights applied">

| Criterion | Weight | Score |
|-----------|--------|-------|
| | | |
| | | |
| | | |

**Raw score:** <0–100>

**Feasibility factor:** <feasibility_composite / 10>

**Final score:** <raw_score × feasibility_factor>

**Overall confidence:** <low | medium | high>

**Confidence factors:**
- Evidence quality (dimension 21): <score>
- Criteria known: <yes / partial / UNKNOWN>
- All dimensions filled: <yes / no>

---

## 7. Decision-Relevant Fields

**Recommended outcome:** <SELECT | REVISE | REJECT_ALL>

**Why this outcome:**
<explanation tied to category scores and red-team outcome>

**Strongest advantages:**
<top 3 category strengths with scores>

**Biggest risks:**
<red-team findings that survived but remain concerns>

**What must be true for this idea to succeed:**
<assumptions that must hold>

**Minimum viable version:**
<scope that can be built in remaining time>

**Highest-value differentiator:**
<the one thing that makes this win>

**Estimated implementation difficulty:** <low | medium | high>

**Recommended next action:**
<exactly ONE action>

---

## 8. Human Confirmation

**Human confirmation status:** <pending | confirmed | rejected>

**Confirmed by:** <name or "pending">
**Confirmed at:** <UTC date/time or "pending">

**Rule:** Only explicit human confirmation can set `selected idea` in `.hackathon/project-state.md`. The engine recommends; the human decides.
