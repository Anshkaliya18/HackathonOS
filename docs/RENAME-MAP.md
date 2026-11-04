---
title: Internal rename inventory
head:
  - - meta
    - name: robots
      content: noindex, nofollow
---

# HackathonOS → Sherpa rename map

## Inventory snapshot

The case-insensitive search `HackathonOS|hackathonos|hackathon-os|HACKATHONOS|\.hackathon|\.env\.hackathon` was run against tracked files at baseline commit `89b39c0` before the rename work. It found **1,531 matching lines in 233 files**. The case-insensitive token counts overlap: 1,442 product/slug matches, 511 `.hackathon` matches (including the `.env.hackathon` substring), and 16 `.env.hackathon` matches. `hackathon-os` had no separate spelling beyond the requested pattern. The tracked `.hackathon/evidence/gold-benchmark/` fixtures account for 245 matching lines.

At inventory time, an independent set of broad uncommitted rename edits was already present in this worktree. Those edits are preserved and are not included in the baseline count; the baseline was read from Git to keep this inventory reproducible.

| Occurrence category | Baseline locations | Decision |
|---|---|---|
| Product name and public copy | README, skill instructions, root docs, docs pages, metadata, launch drafts, SVG social art | Use **Sherpa** for the product; keep “hackathon” when describing the use case. Update current copy and leave historical name references only in the migration guide, changelog, rename map, migration code, and deprecated CLI shim. |
| Repo/package slug and public URLs | `package.json`, lockfile, badges, GitHub links, Pages config, workflow release URLs, docs edit links | Use repository slug `sherpa`. `npm view sherpa` returned version `0.1.8` (taken); `npm view sherpa-skill` returned npm `E404` (no package found at check time), so use `sherpa-skill` for the package. The `Anshkaliya18/sherpa` repository lookup returned HTTP 404. Do not rename or publish remotely in this branch. |
| Master slash command and registered commands | `commands/manifest.json`, command definitions, `.claude/skills/`, `.opencode/commands/`, `.kilo/commands/`, adapter notes, tests | Rename `/hackathonos` to `/sherpa` and command identifiers/files from the `hackathonos-*` prefix to `sherpa-*`. Keep the command set, workflow mappings, and compatibility evidence unchanged except for the renamed identifiers. |
| CLI name, wrappers, and installer copy | `distribution/cli/`, `distribution/npm/`, installer/uninstaller scripts, docs and tests | Install and expose `sherpa`. Retain `hackathonos` only as a deprecated forwarding shim that prints “HackathonOS is now Sherpa”. |
| User skill install directories | Claude Code and OpenCode paths in the installers, CLI, tests, and docs | Install under `~/.claude/skills/sherpa/` and `~/.config/opencode/skills/sherpa/`. Detect the old HackathonOS directories and remove their command files only after the Sherpa installation has been written and validated. |
| Project state directory | `.hackathon/` references in `SKILL.md`, workflows, templates, Python modules, docs, fixtures, and tests | Make `.sherpa/` the current state path. If only `.hackathon/` exists, offer a copy-only migration; never overwrite `.sherpa/` or delete `.hackathon/`. Read `.hackathon/` as a deprecated fallback for one release and report that deprecation. Rename the repository's tracked benchmark state directory while preserving its contents. |
| Environment example and prefixed environment variables | `.env.hackathon.example`, installer variables beginning `HACKATHONOS_` | Rename the template to `.env.sherpa.example`. Use `SHERPA_` for product-specific variables and accept the former `HACKATHONOS_` variable as a documented fallback for one release. Keep generic hackathon/project variables unchanged. |
| Release assets, version, and workflow | `distribution/release/manifest.json`, checksums, `distribution/VERSION`, `CHANGELOG.md`, `RELEASE.md`, release workflow | Use Sherpa asset and CLI names, update release metadata to the prepared **2.0.0** major version because product identity, command namespace, state path, and package identity change. Generate real archive sizes/checksums only when the first release is built; do not claim v2 assets already exist. |
| Python code, imports, tests, benchmark fixtures | `core/`, `src/`, `distribution/cli/`, `tests/`, `.hackathon/evidence/` | Rename product-specific module/path identifiers and fixtures consistently. Add focused tests for state migration and the deprecated CLI shim. Preserve test intent and benchmark evidence, updating product-specific labels to Sherpa. |
| Documentation site and visual assets | `docs/.vitepress/`, all current docs pages, `docs/public/`, Pages workflow | Rebrand titles, command links, state paths, repo links, Pages base path, and assets to Sherpa while retaining all existing content/pages. Build the “ascent” visual identity and keep reference material technically neutral. |
| Historical compatibility references | `CHANGELOG.md`, `MIGRATION.md`, this map, migration code, deprecated `hackathonos` shim | These are intentional remaining references that explain the old product name and upgrade path. List and review each remaining occurrence in the final search. |
| `Microsoft/Windows/PowerShell/ModuleAnalysisCache` | One tracked 6,072-byte file; no source references | This is a PowerShell module-analysis cache, not an installer path or app source. Preserve its bytes in the repository and exclude it from Sherpa release assets. The corresponding local cache already exists with different contents, so do not replace or merge either cache. |

## Installer and migration ordering

1. Install Sherpa files into the new paths.
2. Validate the new skill entry points and manifest.
3. Only after validation, remove old HackathonOS command directories and replace the old CLI with the compatibility shim.
4. Keep `.hackathon/` untouched; migration copies its contents into `.sherpa/` only after explicit user approval and only when `.sherpa/` does not exist.

The Windows `Microsoft/Windows/PowerShell` path is not referenced by the installer. It contains the tracked cache described above; its placement is separate from Sherpa's installation paths.

## Final case-insensitive search

The final search used `rg -ni --hidden` for `HackathonOS|hackathonos|hackathon-os|HACKATHONOS|\.hackathon|\.env\.hackathon`, excluding Git internals, `node_modules`, and generated VitePress output. Every remaining hit is intentional and belongs to one of these reviewed groups:

| Remaining references | Locations and reason |
|---|---|
| Historical product name / migration | `CHANGELOG.md`, `MIGRATION.md`, `docs/migration.md`, `docs/RENAME-MAP.md`, `RELEASE.md`, `docs/first-ascent.md`, and `docs/installation/index.md` describe the rename, compatibility period, or upgrade instructions. |
| Legacy state and environment fallbacks | `core/configuration/manager.py`, `core/ideas/engine.py`, `src/config_manager.py`, `distribution/cli/sherpa`, `SKILL.md`, `workflows/init.md`, `docs/configuration/index.md`, and `docs/installation/index.md` read or explain old state/configuration without deleting or writing to it. |
| Installer cleanup / environment aliases | `distribution/install.sh`, `distribution/install.ps1`, `distribution/uninstall.sh`, and `distribution/uninstall.ps1` recognize only managed old install paths and former variable names; project state remains outside installer cleanup. |
| Deprecated launcher compatibility | `distribution/cli/hackathonos`, `distribution/cli/hackathonos.bat`, `distribution/npm/hackathonos.mjs`, `distribution/cli/sherpa`, `scripts/build-release.py`, `package.json`, and `package-lock.json` provide or package the forwarding command. |
| Safety and migration tests | `tests/configuration/test_configuration.py`, `tests/installer/test_cli.py`, and `tests/installer/test_installer_scripts.py` retain old names only as legacy fixtures/assertions. |
| Preserved benchmark evidence | `.sherpa/evidence/gold-benchmark/dataset.json` and `gold-labels.json` contain historical benchmark claims about a prior repository state. Their evidence text was retained rather than rewritten because that would change benchmark labels and hashes. |

The repository's tracked `Microsoft/Windows/PowerShell/ModuleAnalysisCache` is an opaque cache binary and is not a source reference. It remains unchanged and is not included in the release archives. Generated build files are excluded from this search and from Git.
