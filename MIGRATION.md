# Migrating from sherpa to Sherpa

sherpa is now Sherpa. The skill remains a hackathon mentor; its product name, slash command, CLI, and project state path have changed.

## Install Sherpa

After the first Sherpa release is published, use the matching tagged installer from [RELEASE.md](RELEASE.md). The installer validates the new skill before removing its exact managed sherpa skill directory. It preserves other files and project data.

The old `sherpa` command remains as a deprecated shim and prints `sherpa is now Sherpa`. Use `sherpa` going forward.

## Project state

Sherpa stores project state in `.sherpa/`. For one release, it reads `.hackathon/` when `.sherpa/` is absent and emits a deprecation notice. To make a non-destructive copy, run this from the project:

```bash
sherpa migrate
```

Review the copy before removing the old folder yourself. Migration refuses to overwrite an existing `.sherpa/` and never deletes `.hackathon/`.

## Environment variables

Use the `SHERPA_*` installer variables. `sherpa_*` names remain accepted as fallbacks for this release. The framework's hackathon-specific variables such as `HACKATHON_NAME` are unchanged because they describe the event, not the product.

The deprecated source config helper reads `.env.hackathon` only when `.env.sherpa` is absent. Copy it manually to `.env.sherpa`; it is never moved or deleted automatically. Keep credentials in `.env`, not either example/state file.

## Agent commands and package

Use `/sherpa <workflow>` in supported agent hosts. The CLI package name is `sherpa-skill` because npm's `sherpa` name is already occupied. Compatibility status remains host-specific; see [AGENT-COMPATIBILITY.md](AGENT-COMPATIBILITY.md).
