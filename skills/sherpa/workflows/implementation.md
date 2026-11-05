# sherpa — IMPLEMENT Workflow

**Operation:** IMPLEMENT (Phase 4: Implementation / Development Intelligence)  
**Purpose:** Safely execute one approved implementation task at a time, guided by the Phase 3 project plan and real repository evidence.

## Routing

Use for explicit requests to IMPLEMENT, BUILD, DEVELOP, START IMPLEMENTATION, CONTINUE IMPLEMENTATION, or IMPLEMENT NEXT TASK. General “what next?” requests remain owned by `workflows/next.md`. Follow `rules/implementation-rules.md`. Do not start Phase 5.

## Deterministic Workflow

1. **Read project state first.** Read `.sherpa/project-state.md` in the active application repository. If missing, stop; do not initialize state or infer the target repository.
2. **Verify selected idea.** Confirm it is known and consistent with `.sherpa/decisions.md` and the selected idea's evaluation artifact. If missing, UNKNOWN, or conflicting, mark implementation BLOCKED; never change the idea.
3. **Read Phase 3 evidence.** Locate and inspect the repository analysis and project plan in `.sherpa/evidence/` or their explicitly referenced stable paths. If either is absent or conflicting, mark NOT READY.
4. **Verify approvals and scope.** Require `Architecture = APPROVED`, a defined MVP scope consistent with the approved project plan, and a project plan marked READY or explicitly approved for implementation. Do not invent an additional MVP approval status. If architecture is UNKNOWN/DRAFT/missing, stop with `Architecture approval required before implementation.` Do not change approval fields.
5. **Establish readiness.** Verify each condition in `rules/implementation-rules.md` Section 3. Record every missing item as UNKNOWN/BLOCKED; do not modify application source while NOT READY.
6. **Inspect the actual development baseline.** Establish repository root, revision/status when Git is available, runtime/framework, package manager, entry points, relevant structure, tests, commands, configuration, environment-variable names, and current implementation status. If Git is unavailable, record `Git baseline = UNKNOWN`. Seeing a command or test does not mean it passed.
7. **Create or update the implementation plan.** Use `templates/implementation-plan.md` at `.sherpa/implementation-plan.md`. Derive workstreams and tasks only from the approved MVP/project plan and inspected repository. Record unknowns rather than filling gaps by guess.
8. **Order tasks.** Record task dependencies and critical path. Prioritize MUST HAVE, critical path, blockers, dependencies, reliability, security, testing, SHOULD HAVE, then OPTIONAL. Order prerequisites before downstream work when they unblock the critical path. Do not choose optional work while blocking MUST HAVE work exists.
9. **Select exactly one current task.** Use an existing task record or create `.sherpa/implementation/task-NNN.md` from `templates/implementation-task.md`. Verify it is in plan and compatible with approved architecture. If out of plan, return `OUT OF PLAN`; if it conflicts with architecture, return `ARCHITECTURE CONFLICT`; in either case stop for a human decision.
10. **Check approval threshold.** Proceed only for a bounded change within the approved plan and architecture. Obtain explicit human approval before architecture reopening, major scope/dependency changes, destructive refactors, or materially irreversible actions. Never infer approval from a recommendation.
11. **Implement incrementally.** Inspect the task's relevant code, then make the smallest coherent change. Do not mix unrelated work or install dependencies without a documented need and approval when warranted.
12. **Validate the change.** Run relevant checks for the changed component. Record exact commands and observed outcomes. If a check fails, preserve its failure, diagnose before further edits, and rerun after an evidence-supported fix. Unrun checks remain UNKNOWN.
13. **Record evidence and task status.** Update the task record with change summary, commands, results, failures, and source evidence. Mark COMPLETE only when task requirements and required validation have evidence; otherwise use IN_PROGRESS or BLOCKED.
14. **Update compact project state.** Update only the Phase 4 fields allowed in `rules/implementation-rules.md` Section 10. Do not alter idea, Phase 2 scores, Phase 3 decisions, architecture approval, or MVP approval.
15. **Recalculate the queue.** Update dependencies, blockers, workstream status, critical path, and next eligible task. Set overall implementation COMPLETE only when all defined implementation-scope tasks are complete with required validation evidence.
16. **Return exactly one primary next action.** Include readiness, current task/status, changes, validation evidence/results, blockers, and unknowns. If blocked, the single action must address the highest-priority blocker.

## Failure and Stop Conditions

- Missing/unknown selected idea: stop normal implementation; human decision required.
- Missing Phase 3 plan or repository analysis: `NOT READY`.
- Architecture UNKNOWN/DRAFT: `Architecture approval required before implementation.`
- No application source: `Implementation baseline insufficient. No application source was found. Implementation cannot safely begin.`
- Missing tests/dependencies/configuration: mark UNKNOWN/BLOCKED as applicable; do not fabricate or install blindly.
- Failed validation: report failure and affected task; do not claim success.
- New idea, out-of-plan task, or architecture conflict: stop and route for human decision.
- Unknown deadline/time: `TIME STRATEGY = UNKNOWN`; do not estimate remaining time.

## Output Contract

Return exactly one `PRIMARY NEXT ACTION`. Do not return competing next actions or proceed to Phase 5.
