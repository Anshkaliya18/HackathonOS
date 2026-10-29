# HackathonOS — Idea Evaluation Workflow

**Operation**: IDEA-EVALUATE  
**Purpose**: Evaluate candidate hackathon ideas in context and recommend SELECT / REVISE / REJECT_ALL. Deterministic pipeline. Same inputs produce identical results.

---

## When to Use

Use IDEA-EVALUATE when:
- You have 1 or more candidate ideas to evaluate
- You want to know which idea gives the strongest realistic chance of performing well in this specific hackathon
- You need a transparent, evidence-based comparison before committing to implementation

**Prerequisite:** HackathonOS must be initialized (`.hackathon/project-state.md` exists). If not, run INIT first.

---

## Pipeline Stages

### Stage 1: Input

**Read from `.hackathon/project-state.md`:**
- Hackathon name, deadline, time remaining
- Judging criteria and weights (or UNKNOWN)
- Problem statement
- Target users (if known)

**Accept from user:**
- List of candidate ideas (1 to N), each with a one-line description

**If no candidate ideas provided:**
- Report "No candidate ideas provided."
- Ask user to supply ideas before evaluation can run.
- Stop.

---

### Stage 2: Research

**For each candidate idea, research:**
- Existing solutions
- Competitors
- Similar hackathon projects
- Open-source alternatives
- Existing products
- Market saturation
- Differentiation opportunities

**Evidence tagging (required for every claim):**

| Type | Definition |
|------|------------|
| FACT | Verifiable with source |
| INFERENCE | Logical conclusion from facts |
| ASSUMPTION | Not yet verified |
| UNKNOWN | No information available |

**Rules:**
- Never claim research was performed unless evidence was actually retrieved.
- Preserve sources (URL, file path, or "team input").
- If no evidence exists for a claim, mark UNKNOWN.
- Save evidence to `.hackathon/evidence/<research-query>.md`.

**If OpenCode has no research/web tool access:**
- Mark all external claims as UNKNOWN.
- Proceed with team input only.

---

### Stage 3: Evaluate

**For each candidate idea, score all 21 dimensions (1–10 scale):**

Use `templates/idea-evaluation.md` as the record format.

**Dimension reference:**
| # | Dimension | Scale |
|---|-----------|-------|
| 1 | Problem importance | 1–10 |
| 2 | Problem clarity | 1–10 |
| 3 | Target-user clarity | 1–10 |
| 4 | User pain | 1–10 |
| 5 | Solution usefulness | 1–10 |
| 6 | Innovation | 1–10 |
| 7 | Differentiation | 1–10 |
| 8 | Technical feasibility (10 = high) | 1–10 |
| 9 | AI/ML necessity (10 = essential) | 1–10 |
| 10 | Implementation complexity (10 = high) | 1–10 |
| 11 | Time required (10 = max time) | 1–10 |
| 12 | Team skill fit (10 = high fit) | 1–10 |
| 13 | Demo potential | 1–10 |
| 14 | Judge appeal | 1–10 |
| 15 | Judging-criteria alignment | 1–10 |
| 16 | Scalability/potential | 1–10 |
| 17 | Real-world impact | 1–10 |
| 18 | Competitive landscape (10 = less competition) | 1–10 |
| 19 | Defensibility | 1–10 |
| 20 | Risk (**10 = highest risk**) | 1–10 |
| 21 | Evidence quality | 1–10 |

**Scoring rules:**
- Each dimension: score + reasoning + evidence type + source + confidence
- No dimension score justified by UNKNOWN or ASSUMPTION without explicit flagging
- Same inputs → same scores (deterministic)

**Save to:** `.hackathon/evaluations/<idea-name>.md`

---

### Stage 4: Red Team

**For each candidate idea, apply red-team kill questions:**

| # | Question |
|---|----------|
| 1 | Why would judges reject this? |
| 2 | Is the problem actually significant, or trivial? |
| 3 | Is this just another CRUD application? |
| 4 | Is the AI actually necessary, or just buzzword? |
| 5 | Is the innovation real, or cosmetic? |
| 6 | Is the differentiation obvious to a judge in 30 seconds? |
| 7 | Can the team build it within the deadline? |
| 8 | Is the demo compelling and reliable? |
| 9 | Is the idea dependent on unavailable APIs or data? |
| 10 | Is the idea technically fragile? |
| 11 | Are competitors already doing this better? |
| 12 | Can the team demonstrate measurable impact? |
| 13 | Is there a simpler solution that scores similarly? |
| 14 | What single question could expose the idea's biggest weakness? |

**Deterministic red-team outcomes:**

| Outcome | Conditions |
|---------|------------|
| **KILL** | (a) Feasibility gate FAIL with no credible revision path within time, OR (b) dimension_20 ≥ 9 AND dimension_8 ≤ 3, OR (c) dimension_9 ≤ 3 AND idea claims "AI-powered" |
| **MAJOR CONCERN** | Any criterion-critical dimension scores 3–5, OR feasibility gate score 6.0–7.0 |
| **MINOR CONCERN** | Any non-critical dimension scores 6–7 |

**Not unnecessarily aggressive:** A single medium score does not trigger KILL.

---

### Stage 5: Score

**For each idea that survives red team (not KILL):**

1. **Map categories to judging criteria** (see scoring-rules.md)
2. **Apply judging criteria weights** (if known; equal weights if UNKNOWN)
3. **Calculate raw_score** = weighted criterion average (0–100)
4. **Calculate feasibility_composite:**
   ```
   feasibility_composite = avg(
       dimension_8,
       (11 - dimension_10),
       (11 - dimension_11),
       dimension_12,
       (11 - dimension_20)
   )
   ```
5. **Apply Feasibility & Risk Gate:**
   - If feasibility_composite ≥ 6.0: PASS
   - If feasibility_composite < 6.0: FAIL → cannot be SELECTed
6. **Calculate final_score:**
   ```
   final_score = raw_score × (feasibility_composite / 10)
   ```

**Confidence:** Based on evidence quality (dimension 21), criteria known status, and dimension completeness.

**No stacked multipliers:** The feasibility_composite factor is the only multiplicative adjustment. team_fit_factor, time_pressure_factor, and risk_penalty are not applied separately — they are already inside feasibility_composite.

---

### Stage 6: Compare & Decide

**Compare all non-killed ideas side-by-side** using `templates/idea-comparison.md`.

**Decision outcome rules:**

| Outcome | When |
|---------|------|
| **SELECT** | At least one idea passes feasibility gate AND has highest final score |
| **REVISE** | Ideas survive but have fixable weaknesses (MAJOR CONCERN without KILL) |
| **REJECT_ALL** | All ideas killed by red team OR all fail feasibility gate |

**Output:**
```
RECOMMENDED OUTCOME: SELECT | REVISE | REJECT_ALL

Recommended idea: <name or "None">

Why: <explanation>

Strongest advantages: <list>

Biggest risks: <list>

Why alternatives were rejected: <list>

What must be true for this idea to succeed: <list>

Minimum viable version: <scope>

Highest-value differentiator: <one thing>

Estimated implementation difficulty: <low | medium | high>

Feasibility gate: PASS | FAIL

PRIMARY NEXT ACTION: <exactly one action>
```

**Human authority:**
- The engine recommends. The human/team decides.
- The engine does NOT auto-set `selected idea` in `.hackathon/project-state.md`.
- Only explicit human confirmation can change `selected idea`.

**Write results:**
- Decision log → `.hackathon/decisions.md` (append-only)
- Per-idea evaluation → `.hackathon/evaluations/<idea-name>.md`
- Evidence → `.hackathon/evidence/<research-query>.md`
- Phase in project-state.md → "Idea Evaluation" (only phase field updated; `selected idea` unchanged without human confirmation)

---

## Validation Checklist

After IDEA-EVALUATE completes:
- [ ] Each of 21 dimensions scored for each idea
- [ ] Each dimension in exactly one category (no double-counting)
- [ ] Judging criteria weights applied (or equal weights + low confidence if UNKNOWN)
- [ ] Feasibility & Risk Gate calculated and reported
- [ ] Red-team outcome (KILL / MAJOR CONCERN / MINOR CONCERN) for each idea
- [ ] Decision outcome (SELECT / REVISE / REJECT_ALL)
- [ ] Exactly ONE primary next action
- [ ] Human confirmation status = pending (not auto-confirmed)
- [ ] All evidence tagged FACT / INFERENCE / ASSUMPTION / UNKNOWN with sources
- [ ] Same inputs would produce identical results (deterministic)
