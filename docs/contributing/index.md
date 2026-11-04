# Contributing

Contributions should preserve evidence boundaries, human approval gates, and the distinction between installed files and verified runtime behavior.

## Set up the repository

```bash
git clone https://github.com/Anshkaliya18/HackathonOS.git
cd HackathonOS
python --version
```

For documentation work, use Node.js and npm:

```bash
npm install
npm run docs:dev
```

## Understand the change surface

- Update `commands/manifest.json` and `SKILL.md` when changing command routing.
- Update the relevant workflow, shared rules, and templates together when behavior changes.
- Keep agent-specific material in its adapter and record actual runtime evidence.
- Treat installer and CLI changes as distribution/security-sensitive; preserve checksum verification, path validation, backups, and managed path scope.
- Keep project data under `.hackathon/`; installers and CLI must not remove it.

## Coding and writing standards

Keep commands copyable, avoid unsupported feature claims, explain behavior using repository evidence, and document platform coverage actually checked. Do not add real credentials, local caches, or generated output.

## Tests and checks

Focused Python regression scripts are under `tests/`, including command, configuration, installer, idea, and phase checks. Run the checks relevant to your change. Documentation changes can run:

```bash
npm run docs:commands
npm run docs:check
npm run docs:build
```

## Adapter development

Implement only formats the host documents. Check command discovery, argument forwarding, and approval behavior in an isolated project. Update compatibility status only after a successful runtime smoke test and record the evidence in the manifest.

## Pull requests and issue reports

Describe the problem, intended behavior, affected workflows/adapters/platforms, and validation run. For bugs, include minimal reproduction steps and relevant sanitized output. Keep tokens and private project data out of issues and test output.

See the [repository contributor notes](https://github.com/Anshkaliya18/HackathonOS/blob/main/CONTRIBUTING.md), [security guidance](https://github.com/Anshkaliya18/HackathonOS/blob/main/SECURITY.md), and [release process](https://github.com/Anshkaliya18/HackathonOS/blob/main/RELEASE.md).
