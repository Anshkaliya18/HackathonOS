# Sherpa Skill and Command Discovery: Forensic Root Cause Report

**Audit date:** 2026-11-06  
**Scope:** The findings below are the read-only forensic snapshot, completed before implementation changes. The follow-on implementation and test evidence is recorded in `IMPLEMENTATION-CHANGELOG.md`, `ARCHITECTURE-REDESIGN.md`, and the companion compatibility, installation, command, and release reports.

## Executive finding

The confirmed root cause is a **distribution lifecycle split**, not one isolated installer bug. Sherpa has a canonical-looking source (`SKILL.md`, `commands/manifest.json`, and top-level workflow/resource directories), but multiple manually maintained or partially generated adapters and bundles are not consistently built, packaged, installed, or invoked together. The installers validate the presence of generic skill files, not whether a client can discover and invoke the client-native command files. This allows a success message while advertised native commands are absent.

The broad claim of universal/global support is not supported by the implementation. The checked-in project configuration currently has adapters for Claude Code, OpenCode, and Kilo Code; the installers target Claude Code and OpenCode only; the npm package omits the `.claude`, `.opencode`, and `.kilo` native adapter trees; and Codex skill files in `.agents/skills` are not an installer target. The release manifest in this checkout is a template with no archives or CLI asset.

## Distribution trace

| Lifecycle stage | Observed implementation | Finding |
|---|---|---|
| Canonical instructions | Root `SKILL.md`; `commands/manifest.json`; top-level `workflows/`, `rules/`, `templates/`, `core/`, `src/` | The command manifest is a useful registry, but native command files are not generated from it by the packaging script. |
| Portable bundle | `scripts/prepare-agent-package.py` copies root `SKILL.md` and selected directories into `skills/sherpa` and `.agents/skills/sherpa`; it generates per-command skills under those two roots | It does not generate Claude/OpenCode/Kilo native command adapters. It is invoked only as npm `prepack`. |
| Client adapters | `.claude/skills`, `.opencode/commands`, `.kilo/commands`, `.kilo/skills`, `.agents/skills`, plugin manifests | Native adapter files are checked in separately. `.claude` and `.opencode` each have 29 command/skill entrypoints versus 28 implemented manifest entries; Kilo has 30 command files. No generator/consistency check for these trees was found. |
| npm package | `package.json` `files` allowlist includes source skill trees, `.agents` bundles, plugins, and installers | It excludes `.claude/`, `.opencode/`, `.kilo/`, and `adapters/`. The checked-in `sherpa-skill-2.0.1.tgz` is older than package/release version 2.0.7 and includes only 4 product-level entrypoints plus launcher/install scripts. |
| Standalone release | `distribution/release/manifest.json` | It declares version 2.0.7 but has `archives: []` and `cli: null`; its note calls it a template. The installer’s online default expects a published manifest with downloadable release archives. |
| Global installation | Both installers select only Claude and OpenCode and copy an archive’s `SKILL.md`, manifest, router, and workflow tree into `~/.claude/skills/sherpa` and `~/.config/opencode/skills/sherpa` (or Windows equivalents) | No native command registration is installed. Kilo, Codex, Gemini, and Qwen destinations are not supported by these installers. |
| Project-local installation | Both scripts accept a project directory parameter/flag, but the shell script explicitly errors; PowerShell rejects/unimplements the mode | Advertised/accepted interface does not implement project-local installation. Docs disclose this limitation, but callers still encounter a dead option. |
| Client discovery | Official docs specify distinct native paths and conventions | A skill in a skill folder does not itself create a client’s native slash-command adapter. Installer validation only checks files/directories. |
| Runtime execution | Some adapter READMEs record picker observations, blocked attempts, and unverified statuses | The recorded data does not establish a cross-client runtime pass. Existing tests do not launch real clients. |
| Supporting file resolution | Several native prompts instruct the client to read `repository-root SKILL.md`, `commands/manifest.json`, and `core/commands/router.py` | These root-relative paths work in this checkout but do not exist in an ordinary consuming project after global install. No packaged path/config handoff is provided by the native prompts. |
| Uninstallation | Shell and PowerShell remove only Claude/OpenCode global skill folders and the CLI | No managed adapter paths or project-local install records exist to remove. No upgrade manifest/ownership registry is shared with install. |

## Confirmed defects

### F1 — Native command adapters are not distributed by npm or standalone installer

- **Location:** `package.json:17-52`; `scripts/prepare-agent-package.py` (copies portable skills and generates command-specific skills, but no native adapters); `distribution/install.sh:32-33, 351-353`; `distribution/install.ps1:26-28, 420-422`.
- **Actual:** npm allows `skills/`, `.agents/`, plugin manifests, and install scripts, but omits `.claude/`, `.opencode/`, `.kilo/`, and `adapters/`. Standalone installers copy only a generic skill bundle to Claude/OpenCode skill destinations.
- **Expected:** Each supported client distribution contains its native skill and, where advertised, native command definitions plus all required resources; installer writes these to that client’s documented discovery locations.
- **Reproduction:** Run `npm pack --dry-run` (prepack refreshes portable bundles) and inspect the file list; install the package or run the standalone installer into a clean profile, then inspect client command directories. The npm tarball checked into the repository (`sherpa-skill-2.0.1.tgz`) already demonstrates absence of native adapter directories.
- **Affected clients:** Claude Code native skills/aliases, OpenCode slash commands, Kilo commands; distribution-level impact also affects Codex because installer does not install `.agents` skills. Generic OpenCode skill discovery is an exception: OpenCode supports Agent Skills in the skill directory, but that does not register the missing custom commands.
- **Severity:** Critical for command discovery; high for client coverage.
- **Root cause:** Packaging allowlist and installer source/destination model were designed around a shared portable skill, while native adapters remain parallel checkout-only files.
- **Correction:** Make the manifest the command source, generate each client adapter during a deterministic build, package the generated clients, and have the installer select/install/verify the matching distribution.

### F2 — “Successful installation” validates files, not client discovery or command registration

- **Location:** `distribution/install.sh:318-334, 362-378, 462-481`; `distribution/install.ps1:373, 434, 509-526`; `INSTALLATION.md:59`.
- **Actual:** Validation checks `SKILL.md`, `commands/manifest.json`, `core/commands/router.py`, and `workflows/`. It does not check a client-native command file or invoke a client discovery mechanism. Shell success output says installation completed successfully.
- **Expected:** Report separately whether generic skill files were installed and whether that client’s skill/command discovery was verified; do not claim command installation success when the native command adapter is missing.
- **Reproduction:** Run installer in a clean test profile with selected target; it can pass these structural checks despite not writing `.opencode/commands`/`.kilo/commands` or a Claude alias adapter tree.
- **Affected clients:** Claude Code and OpenCode today; any future clients added to this generic validation path.
- **Severity:** Critical because users receive a false success signal.
- **Root cause:** Structural file checks are treated as client integration tests.
- **Correction:** Add client-specific post-install checks and real CLI smoke tests where possible; label “files installed” separately from “client discovery/runtime verified.”

### F3 — Native adapter prompts resolve resources from the consuming repository root

- **Location:** `.opencode/commands/sherpa-status.md` (body); `.kilo/commands/sherpa-status.md` (body); `.claude/skills/sherpa-status/SKILL.md` (body); compare with bundled layout in `skills/sherpa/` and global destinations in installer constants.
- **Actual:** Adapters say to read `repository-root SKILL.md`, `commands/manifest.json`, and `core/commands/router.py`. In a consumer’s project those framework files are absent; global install stores resources in the client’s skill directory, not the project root. The per-command `.agents/skills/sherpa-status/SKILL.md` uses `../sherpa/...`, which is valid only if the bundle is installed into the expected adjacent structure.
- **Expected:** Adapters use a stable path relative to their installed distribution, an explicit generated embedded prompt, or a documented resolver that finds the installed canonical bundle.
- **Reproduction:** In a clean unrelated project, install/open a checked-in adapter or invoke it with a global skill installation; attempt the exact listed file reads. The repository-root targets are missing.
- **Affected clients:** All native prompt adapters when used outside the Sherpa source repository; especially OpenCode/Kilo command files and Claude command-specific skill aliases.
- **Severity:** Critical for runtime execution after successful command discovery.
- **Root cause:** Adapter prompts were authored against repository layout and are copied/advertised as if they were standalone installed adapters.
- **Correction:** Generate prompts with paths based on the client adapter’s installed bundle layout and verify resource resolution in a clean consumer project.

### F4 — Project-local install is a dead/unsupported installer option

- **Location:** `distribution/install.sh` argument parser `--project`; `distribution/install.ps1` parameter `$ProjectDir` and its validation/selection path; `distribution/npm/sherpa.mjs:16-20`; `INSTALLATION.md:43,63`.
- **Actual:** Shell explicitly exits with “project-level installer mode is not implemented”; PowerShell does not provide a working local install. The npm help lists no project target option, while documentation calls project-local setup experimental/unsupported.
- **Expected:** Either implement a client-aware project-local mode or remove the unusable option from installer interface/help and consistently document manual repo integration.
- **Reproduction:** `bash distribution/install.sh --project <temp-dir>`; PowerShell `distribution/install.ps1 -ProjectDir <temp-dir>`.
- **Affected clients:** All intended project-local use cases.
- **Severity:** High for usability, moderate for runtime safety (fails explicitly rather than corrupting files).
- **Root cause:** Installer parameters and scope were added without implementing per-client project destinations and transaction handling.
- **Correction:** Implement project-local selection as part of a shared install engine, with ownership/rollback metadata, or remove the option until implemented.

### F5 — Platform adapter copies drift and are not generated from one source

- **Location:** `.claude/`, `.opencode/`, `.kilo/`, `skills/`, `.agents/`; `scripts/prepare-agent-package.py`.
- **Actual:** Audit found 28 implemented manifest entries, 29 OpenCode command files, 30 Kilo command files, and 29 Claude skill entrypoints. The checked-in client command sets are not generated by the npm prepack script. `commands/manifest.json` copies at top level and in the two portable bundles are byte-identical, but the wider skill directory contains many independent and stale hashes because skill copies are separate entries; only the three root skill copies (`SKILL.md`, `skills/sherpa/SKILL.md`, `.agents/skills/sherpa/SKILL.md`) were identical at audit time. The `prepack` script refreshes the two portable bundles, so a future package operation mutates generated files in the checkout.
- **Expected:** Canonical authored sources plus deterministic generated outputs; CI fails on stale generated files and every manifest command has a valid adapter mapping.
- **Reproduction:** Compare manifest command names with basenames of `.opencode/commands`, `.kilo/commands`, and Claude skill directories. Run the prepack preparation in a clean worktree then compare generated trees. (The source-level counts are factual; which extra filenames are legacy aliases requires mapping each entry to the manifest before removal.)
- **Affected clients:** All clients with maintained adapter copies; NPM packaging/release repeatability.
- **Severity:** High.
- **Root cause:** Canonical registry and manually maintained adapter trees have no deterministic generation/check gate; prepack performs in-place build work.
- **Correction:** Generate output in a staging directory from canonical skill/command specs; compare every adapter name and resource reference in CI; package staged output without silently mutating source.

### F6 — Release artifact source is not release-ready in this checkout

- **Location:** `distribution/release/manifest.json`; `distribution/VERSION`; root `package.json:3`; checked-in `sherpa-skill-2.0.1.tgz`.
- **Actual:** Package and release template say 2.0.7, but release manifest has no archives and no CLI URL/checksum, while the checked-in npm tarball is 2.0.1. Installer fetches the online manifest and refuses to install when no OS/architecture archive exists. Manifest text says a release build process populates URLs/checksums, so the empty file is plausibly an intentional template, not proof that the published GitHub latest release is empty.
- **Expected:** Release validation tests built artifacts and published manifest for exact version, file completeness, and checksums; stale sample tarballs are absent from deliverables or clearly marked as historical fixtures.
- **Reproduction:** Point either online installer at this checkout’s `distribution/release/manifest.json` using its manifest URL override; archive selection fails because `archives` is empty. Inspect the checked-in tarball metadata; it does not match current version.
- **Affected clients:** All users installing from the local manifest/artifacts; published installation is not established by checkout evidence alone.
- **Severity:** Critical for local release install; high release integrity risk.
- **Root cause:** No release gate ties package version, release manifest, archives, and checksums together, and a stale package artifact remains in the repository.
- **Correction:** Build artifacts from a clean checkout, verify generated manifest and archives, and reject publish if they are missing or version-mismatched.

### F7 — Installer/uninstaller management covers only two clients and no adapter registration

- **Location:** `distribution/install.sh:32-33,160-179,350-354`; `distribution/install.ps1:26-28` and `420-422`; `distribution/uninstall.sh:22-23,31-34,64-78`; `distribution/uninstall.ps1:19-20,58-68`.
- **Actual:** Only Claude and OpenCode global skill directories are installed/removed. Kilo’s repo files state that no global install is performed; Codex `.agents` distribution and native adapters have no corresponding uninstall logic. Command files installed globally/project-locally have no lifecycle because installers never manage them.
- **Expected:** A client adapter registry drives detection, install, validation, upgrade, rollback, and uninstall from one list, with installation ownership recorded so unrelated files are preserved.
- **Reproduction:** Run install/uninstall with only a Kilo or Codex environment available; neither script recognizes or manages its native directories. OpenCode command definitions are not installed by either script.
- **Affected clients:** Kilo, Codex, Gemini, Qwen; and OpenCode/Claude native commands.
- **Severity:** High for supported-client claims and cleanup correctness.
- **Root cause:** Install/uninstall target lists are duplicated constants rather than data from a client adapter registry.
- **Correction:** Centralize client capabilities/paths and lifecycle actions; test installer/uninstaller symmetry for each managed path.

### F8 — Advertised slash-command coverage exceeds verifiable native command coverage

- **Location:** `commands/manifest.json`; `COMMANDS.md`; `commands/README.md`; `.claude/`, `.opencode/`, `.kilo/`; `adapters/*/README.md`.
- **Actual:** The manifest marks 28 commands implemented across `claude`, `opencode`, and `kilo`; only 28 root manifest entries exist, while native command files include extra files and no generator proves one-to-one valid mappings. Root command documentation includes syntax such as `/sherpa <operation>`, which is a skill invocation/argument route for some clients, but native slash commands differ by host. Adapter READMEs correctly mark much runtime state unverified or blocked; however, the presence of command files and manifest `implemented` status can be mistaken for runtime registration.
- **Expected:** Capability-specific command specs: native command registration only where supported and generated; skill invocation documented separately; each command reference/resource resolves; runtime verification status is separate from implementation status.
- **Reproduction:** For each manifest entry, verify adapter file existence, client picker visibility, then invocation/resource loading in each target CLI. The current static trees alone cannot complete those steps.
- **Affected clients:** Claude Code, OpenCode, Kilo Code; other advertised agents where “command” wording is used.
- **Severity:** High.
- **Root cause:** The single command manifest conflates workflow implementation, aliases, adapters, and host-runtime verification.
- **Correction:** Split canonical workflow capability specs from generated client-specific command registrations and publish an evidence-backed per-version compatibility matrix.

## Client discovery evidence and runtime boundary

Official documentation reviewed during this audit:

- [Claude Code skills](https://code.claude.com/docs/en/skills): defines native skill locations, skill names/command names, argument substitutions, and supporting files.
- [OpenCode Agent Skills](https://opencode.ai/docs/skills/): supports project/global `.opencode/skills`, Claude-compatible `.claude/skills`, and agent-compatible `.agents/skills` skill locations.
- [OpenCode commands](https://opencode.ai/docs/commands/): custom slash commands are separate Markdown files in `commands/` directories such as `.opencode/commands/`.
- [Kilo workflows](https://kilo.ai/docs/customize/workflows): workflow slash commands are Markdown files under project `.kilo/commands/` or global `~/.config/kilo/commands/`.
- [Codex skills](https://developers.openai.com/codex/skills): skills are folder-based `SKILL.md` resources; this does not make them native slash-command registrations.

These conventions confirm the architectural distinction between skill discovery and native command registration. Client runtime integration is **not established** by this audit. The adapter READMEs record some discovery observations and several blocked/unverified invocations. Installed executables were found for `claude`, `opencode`, `kilo`, and `codex`, but this audit did not run new interactive client tests because host/model/auth and confirmation state can affect results. No pass/fail runtime result is inferred from file existence.

## Existing test evidence

Ran the repository’s existing installer tests before any implementation changes:

```text
python -m pytest tests/installer -q
54 passed in 3.43s
```

Warnings: requests dependency version warning and pytest-asyncio default-loop-scope deprecation warning. The installer tests include static structure checks and npm launcher behavior. They do not perform clean npm package installation, extract and install actual generated distributions, launch each client to inspect discovery, invoke commands, or verify supporting-resource resolution. Therefore the passing result does not rebut findings F1–F8.

## Hypotheses requiring follow-up evidence

1. **Published release state:** The checked-in release manifest is empty by design; it does not prove that the latest published GitHub release is missing archives. Verify against the tagged release before labeling a production outage.
2. **Installed client runtime:** Claude, OpenCode, Kilo, and Codex executables are available on this machine, but current versions/configuration/auth and isolated runtime behavior were not audited in this phase. Existing adapter README records are the only runtime evidence consulted.
3. **Extra adapter files:** The count mismatch confirms inconsistency, but some extra adapter files may be deliberate legacy aliases or command utilities. Map each against the manifest and docs before removing or renaming anything.
4. **All 59 skill content hashes:** Different hashes mostly reflect different named skill entrypoints and bundled root-vs-command-specific artifacts, not necessarily stale duplicates. Compare only same logical skill/path when deciding whether a copy is stale.
5. **Published NPM package:** The local 2.0.1 tarball demonstrates staleness in the checkout; current npm registry contents were not queried. Validate the registry package separately before claiming user-facing current npm breakage.

## Prioritized repair plan (proposed; implementation not started)

1. **P0 — Define canonical capabilities and evidence model.** Keep `SKILL.md`/workflow/rule/template resources as authored sources; make command specs encode operation, argument contract, supported client capabilities, workflow/resource refs, and verification state separately. Remove claims that a skill implies native slash-command registration.
2. **P0 — Build native adapter generators.** Generate Claude skill aliases, OpenCode commands, Kilo workflows, and Codex/Agent Skills outputs from the canonical specs. Resolve resource references relative to the installed bundle; preserve existing Sherpa workflows, rules, templates, safety gates, and command behavior.
3. **P0 — Make distributions complete and deterministic.** Build client-specific staged bundles. Include them in NPM/release artifacts. Stop mutating tracked source during `prepack`; produce byte-reproducible bundles with exact version/checksum metadata.
4. **P1 — Replace split installer target logic with a client adapter registry.** Add explicit global/project/manual targets, detection, idempotent version-aware upgrade, backups/rollback, uninstall ownership tracking, and post-install verification. Report unsupported or unverified discovery honestly.
5. **P1 — Add command and resource validators.** Check every implemented command has valid metadata, supported argument handling, native entrypoint where claimed, executable workflow, complete resources, and no repository-root-only file assumptions. Produce command-registration and client-compatibility reports from this data.
6. **P1 — Validate each installed client independently.** Use clean profiles/projects and real CLI applications. Test skill list/discovery, explicit skill invocation, slash picker registration, execution, and resource loading; mark blocked tests with precise reason and never infer success from filesystem checks.
7. **P2 — Release acceptance and documentation.** Build/inspect a clean npm package and release archives, compare versions and checksums, remove stale artifacts only after confirming their role, and update installation docs/matrix to match tested client/version/scope combinations.

**Audit gate:** The confirmed root cause was the disconnected source → generated adapter → package → install → discovery → execution chain. Repairs have since been implemented; see the companion reports for what is verified and what remains unverified. The discovery and runtime claims remain intentionally bounded by actual test evidence.
