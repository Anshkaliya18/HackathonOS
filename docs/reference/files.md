# Project files and output audits

## Project state

The expected state root is `.hackathon/` in the project repository. Common artifacts include `project-state.md`, `decisions.md`, `risks.md`, implementation plans and tasks, evidence, judge reviews, and audits. The init workflow defines the actual initialization behavior.

```text
.hackathon/
├── project-state.md
├── decisions.md
├── risks.md
├── implementation-plan.md
├── implementation/
├── evidence/
├── judge-reviews/
└── audits/
```

## Managed installation files

The global skill folders are managed under the Claude Code and OpenCode paths. The CLI's `audit` reports debris, duplicate files, empty directories, and file counts within recognized skill install folders.

`hackathonos clean` is a dry run by default. It lists recognized generated debris. `hackathonos clean --yes` enables removal, still scoped to recognized managed skill directories. Do not treat it as a general repository cleaner.

## Cleanup and preservation

Uninstall removes recognized global skill and CLI files, not project `.hackathon/` state. Installer updates back up existing directories and include rollback behavior. For precise inclusion/exclusion rules, consult [`distribution/cli/hackathonos`](https://github.com/Anshkaliya18/HackathonOS/blob/main/distribution/cli/hackathonos) and [`SECURITY.md`](https://github.com/Anshkaliya18/HackathonOS/blob/main/SECURITY.md).

The CLI's diagnostic output varies by installed files. Run `hackathonos audit` or `hackathonos clean --dry-run` to get a report for your own machine; sample output should not be mistaken for a guaranteed transcript.
