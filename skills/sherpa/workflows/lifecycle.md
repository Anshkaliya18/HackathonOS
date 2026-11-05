# sherpa Lifecycle

Defines the hackathon lifecycle phases and how the skill transitions between them. The lifecycle is time-aware: strategy changes based on time remaining until the deadline.

## Lifecycle Phases

| Phase | When | Primary Focus |
|-------|------|---------------|
| Understand Rules | Start | Read hackathon rules, judging criteria, submission requirements |
| Analyze Problem | Start | Understand the problem statement, target users, constraints |
| Generate Ideas | Early | Brainstorm and capture candidate ideas |
| Validate Ideas | Early | Evaluate ideas against judging criteria, feasibility, differentiation |
| Research Market | Early | Research existing solutions and competitors |
| Select Idea | Early-Mid | Choose the strongest idea to build |
| Design Product/MVP | Mid | Define product scope, MVP, user flows |
| Architecture | Mid | Decide technical architecture, tech stack |
| Development Plan | Mid | Create implementation plan with time estimates |
| Implementation | Mid-Late | Build the MVP |
| Testing + Security | Late | Test the project, secure the application |
| UX Review | Late | Review and improve UI/UX |
| Red Team | Late | Actively find reasons the project could lose |
| Judge Simulation | Late | Simulate multiple judge types |
| Score Optimization | Late | Optimize based on judging criteria gaps |
| Demo Preparation | Final | Prepare the demo |
| PPT / Presentation | Final | Prepare the presentation |
| Final Audit | Final | Final consistency and claim verification |
| Submission | Final | Submit the project |
| Post-Mortem | After | Analyze what worked and what didn't |

## Time-Aware Strategy

The skill adjusts its recommendations based on time remaining:

| Time Remaining | Strategy | What to STOP |
|----------------|----------|--------------|
| > 24 hours | Core product, differentiation, architecture, important features, validation | Low-judging-value features |
| 12–24 hours | Completing MVP, high-impact features, integration, testing | New feature exploration |
| 6–12 hours | Stability, testing, UX, security, demo reliability, presentation | Architectural changes |
| 2–6 hours | Bug fixing, demo flow, critical polish, PPT, documentation, deployment reliability | Any new feature development |
| < 2 hours | Build working, deployment working, demo working, PPT accurate, links working, critical bugs fixed, submission requirements satisfied | All feature development |

## How the Router Determines Phase

1. Read `.sherpa/project-state.md`.
2. Check the `Phase` field (if `UNKNOWN`, default to "Understand Rules").
3. Check `Time remaining` against the deadline.
4. The phase + time remaining determine which workflow guidance applies.

## Persistence

The lifecycle phase and time remaining are stored in `.sherpa/project-state.md` and updated on every skill invocation.
