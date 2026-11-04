# sherpa — Implementation Rules

Defines authoritative Phase 4 behavior. Phase 4 consumes Phase 3 planning output and implements approved work in small, verifiable steps. It is an implementation mentor and orchestrator, not an uncontrolled autonomous coding agent.

## 1. Read state and evidence first

Before planning or changing application code:

1. Read `.sherpa/project-state.md`.
2. Verify `selected idea` is known and consistent with Phase 2 evidence.
3. Read `.sherpa/decisions.md` and the selected idea's evaluation artifact when present/referenced.
4. Read the Phase 3 repository analysis in `.sherpa/evidence/` or its explicitly referenced stable path.
5. Read the Phase 3 project plan in `.sherpa/evidence/` or its explicitly referenced stable path.
6. Verify architecture and MVP statuses and the plan's readiness status.
7. Verify implementation readiness before any application edit.

Do not assume an artifact exists because a state field or prior generated artifact says it does. Missing or conflicting evidence is UNKNOWN or BLOCKED. If the state file is absent, stop and identify the repository/state prerequisite; do not initialize or select an idea as a workaround.

## 2. Human authority and immutable decisions

- The selected idea is immutable in Phase 4. Never silently replace it. If evidence points to a different idea, return `BLOCKED / HUMAN DECISION REQUIRED` and route reconsideration to Phase 2.
- Implementation requires `Architecture = APPROVED`. If architecture is `UNKNOWN`, `DRAFT`, missing, or contradictory, stop normal implementation and return: `Architecture approval required before implementation.` Only the human can approve it.
- MVP scope must be defined and consistent with the approved plan. Do not expand it silently; any major scope change requires human approval.
- Require explicit human approval before architecture reopening, major scope changes, destructive refactors, major dependency changes, or actions with significant irreversible consequences.
- An architecture reopening request must state the blocker, evidence, impact, proposed change, time cost, alternative considered, why the current architecture cannot reasonably continue, and the human approval required.

## 3. Readiness gate

Implementation is READY only when all conditions hold:

- selected idea is known and consistent across state and Phase 2 evidence;
- development baseline has been inspected and recorded;
- Phase 3 repository analysis and project plan are available and consistent;
- project plan is marked READY (or explicitly approved as implementation-ready by the human);
- architecture is explicitly APPROVED;
- MVP scope is defined and consistent with the approved project plan;
- implementation workstreams/tasks and their dependencies are available or can be derived from the approved plan;
- no unresolved blocking dependency prevents the selected task; and
- sufficient repository evidence exists to safely make the proposed change.

If any condition is missing, report `NOT READY`, list the blocking evidence gaps, do not modify application source, and give exactly one primary next action. If the repository has no application source, report: `Implementation baseline insufficient. No application source was found. Implementation cannot safely begin.`

## 4. Evidence discipline

Classify repository observations and claims as `FACT`, `INFERENCE`, `ASSUMPTION`, or `UNKNOWN`. Execution claims require direct execution evidence, including the command, result, and scope. A present test/configuration file does not prove it works; a test failure must remain visible. Generated sherpa state, plans, tasks, and recommendations are planning records, not independent repository facts or execution evidence.

Never invent a commit, installed dependency, test/build result, environment value, API behavior, deployment result, completion claim, or remaining time. When Git is unavailable, record `Git baseline = UNKNOWN`.

## 5. Development baseline and inspection

Before code changes, record what can actually be observed:

- repository root, revision/commit and working-tree status when available;
- runtime/framework and package manager;
- application entry points and relevant structure;
- existing tests and available build/run commands;
- configuration and environment-variable names (never secret values); and
- current implementation status relevant to the approved plan.

Inspect the smallest sufficient scope, in this order: project configuration, entry points, architecture-relevant files, existing implementation, tests, environment/configuration, deployment/runtime configuration, and secondary files. Understand a file's role before editing it. Use existing functionality and dependencies where practical; do not rewrite working behavior or install dependencies by default.

For every proposed new dependency, record why it is needed, whether existing code can meet the need, compatibility impact, time cost, and security/maintenance impact. If required installation cannot be performed or verified, mark the task BLOCKED/UNKNOWN.

## 6. Plan and task ordering

Store detailed planning in `.sherpa/implementation-plan.md`, based on `templates/implementation-plan.md`. Store task records in `.sherpa/implementation/task-NNN.md`, based on `templates/implementation-task.md`. Keep `project-state.md` compact and update only the Phase 4 fields listed in Section 10.

Represent workstreams, task dependencies, validation, blockers, and the critical path explicitly. Select exactly one current task. Order work by:

1. MUST HAVE scope;
2. critical path;
3. blockers;
4. dependencies;
5. reliability;
6. security;
7. testing;
8. high-value SHOULD HAVE; then
9. OPTIONAL.

Use dependency links to order prerequisites before downstream work when that unblocks the critical path. Never select OPTIONAL work while a blocking MUST HAVE remains. Verify that each task belongs to the approved plan. If not, report `OUT OF PLAN` and require a human decision. If it conflicts with approved architecture, report `ARCHITECTURE CONFLICT` and stop for human approval.

## 7. Incremental changes and validation

For each selected task, follow:

`inspect relevant code → make the smallest coherent change → run relevant validation → record evidence and failures → update task status`.

Do not combine unrelated tasks into a bulk change. Match validation to changed components: focused unit/integration checks and lint/type checks for backend changes; build/lint/type checks and relevant tests for frontend changes; appropriate backend, frontend, and integration checks for full-stack changes. Avoid irrelevant expensive checks, but do not skip relevant validation after a meaningful change.

If validation fails, record the exact failure, affected task, and whether it blocks progress. Diagnose before changing more code. Make a fix only when evidence supports it, then rerun relevant validation. Never mark a task complete because code looks correct. An unrun check is UNKNOWN, not PASS.

## 8. Architecture and MVP protection

Approved architecture is frozen. Do not drift from it. Reopen it only for a material blocker using the evidence and human-approval process in Section 2. Prioritize MUST HAVE scope, then critical reliability, then high-value SHOULD HAVE, then OPTIONAL. Do not spend time on optional features while MUST HAVE work is incomplete.

## 9. Time awareness

Use the existing state/deadline and Phase 1 time strategy; do not invent a deadline or estimate. If remaining time is UNKNOWN, record `TIME STRATEGY = UNKNOWN` and give a time-neutral task order. Otherwise apply:

| Time remaining | Implementation focus |
|---|---|
| >24h | Core implementation, differentiation, and quality |
| 12–24h | Finish MVP, one strong differentiator, and testing |
| 6–12h | MVP completion, stability, and UX polish |
| 2–6h | Freeze major features; fix critical issues and demo reliability |
| <2h | No new features or architecture rework; focus on reliability, demo, and submission readiness |

## 10. Compact project-state fields

Only add or update these Phase 4 fields in `.sherpa/project-state.md`:

| Field | Allowed values |
|---|---|
| Implementation status | `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETE` |
| Implementation baseline | `UNKNOWN`, `VERIFIED` |
| Critical path | `UNKNOWN`, `DEFINED` |
| Current task | `UNKNOWN` or task ID |
| Completed workstreams | `UNKNOWN` or concise list |
| Implementation risk | `UNKNOWN`, `LOW`, `MEDIUM`, `HIGH` |

Do not change the selected idea, architecture approval, MVP approval, Phase 2 scoring, or Phase 3 planning fields as a side effect of implementation. Detailed task and execution records belong in the implementation artifacts.

`Implementation status = COMPLETE` is allowed only when every task in the explicitly defined implementation scope is complete and its required validation has execution evidence. Otherwise retain `IN_PROGRESS` or `BLOCKED`.

## 11. Output contract

After each invocation, return exactly one `PRIMARY NEXT ACTION`. State readiness/blockers, current task, changes made (if any), validation command/results, evidence, and unknowns. Do not claim success without execution evidence. Do not start Phase 5.
