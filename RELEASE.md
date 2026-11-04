# HackathonOS Release Publishing

This document describes how to publish a HackathonOS release so that the
one-command installers can download and verify it.

## Release artifacts

For each version (e.g. `v1.0.0`), publish a GitHub Release containing:

```
hackathonos-1.0.0-linux-amd64.tar.gz
hackathonos-1.0.0-darwin-amd64.tar.gz
hackathonos-1.0.0-darwin-arm64.tar.gz
hackathonos-1.0.0-windows-amd64.zip
hackathonos-cli-1.0.0.zip        # required for default CLI-enabled installs
manifest.json
checksums.txt
```

Each archive must contain the skill tree at its top level (or under a single
`hackathonos/` directory):

```
SKILL.md
commands/manifest.json
commands/*.md
core/commands/router.py
core/configuration/manager.py
core/ideas/engine.py
src/verification.py
src/config_manager.py
scripts/*.py
workflows/*.md
templates/*.md
rules/*.md
adapters/*.md
docs/*
VERSION
```

Do **not** include `.git/`, `.hackathon/`, `.claude/`, `.opencode/`, `.kilo/`,
`node_modules/`, `__pycache__/`, `build/`, or `dist/` — these are development
or per-project state, not part of the distributable skill.

## Generate checksums

From the release artifact directory:

```bash
sha256sum hackathonos-*.tar.gz hackathonos-*.zip > distribution/release/checksums.txt
```

Example `checksums.txt` format:

```
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  hackathonos-1.0.0-linux-amd64.tar.gz
...
```

## Update the manifest

Edit `distribution/release/manifest.json`:

- Set `latest.version` to the new version.
- Fill in each archive's `url` (GitHub Releases download URL), `size`, and
  `checksum` (SHA-256).
- Update the `cli.url` and `cli.checksum`.
- Set `published_at`.
- Include the CLI ZIP and its checksum when using the default installer behavior; CLI installation can be disabled with `--no-cli` / `-NoCli`.

Do **not** fabricate checksums — generate them from the real artifacts.

## Publish

1. Tag the commit: `git tag v1.0.0 && git push origin v1.0.0`
2. Create the GitHub Release from the tag and upload the artifacts.
3. Upload `manifest.json` and `checksums.txt` to the release (or host them at
   the `latest/download` path).
4. Point `DEFAULT_MANIFEST_URL` in `install.sh`/`install.ps1` (or rely on the
   GitHub `latest/download/manifest.json` default).

## Versioning

HackathonOS uses semantic versioning (semver). The `VERSION` file in the
distribution and each skill installation records the installed version. The
`hackathonos update` command compares the installed version against
`manifest.json` `latest.version`.

## Rollback

If an update fails validation, the installer automatically restores the
previous `.bak.<timestamp>` backup. No user project data is ever touched.
