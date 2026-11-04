# Workflows

The authoritative entry point and routing rules are in `SKILL.md`; `core/commands/router.py` and `commands/manifest.json` define command routing. Workflows are in `workflows/`, shared rules in `rules/`, and output templates in `templates/`.

The lifecycle is intent-driven: initialize state; understand project constraints; evaluate and select an idea; plan and implement; verify and improve; prepare a demo/presentation; audit submission readiness; capture a postmortem. Related workflows include `init`, `status`, `idea-intelligence`, `idea-evaluation`, `project-planning`, `implementation`, `testing-security`, `demo-preparation`, `presentation`, `final-audit`, `submission`, and `postmortem`.

Human approval gates, evidence boundaries, phase locks, and limits on consequential actions are defined by the skill, workflow, and rule documents. Use `/sherpa help` for implemented operations.
