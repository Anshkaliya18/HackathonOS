# Release Validation Report

**Date:** 2026-11-07  
**Package version:** 2.0.8  
**Publishing:** Not performed.

## Validated

- `package.json` exposes the npm launcher, Python installation engine, installers, generated distributions, and root skill/documentation.
- npm `prepack` deterministically rebuilds the generated distribution from canonical repository sources.
- Prepublish registry check found npmjs latest at 2.0.7, so this release uses the next version, 2.0.8. npmjs and GitHub Packages credentials are unavailable in the current CLI environment.
- A clean `npm pack` and offline install of that tarball succeeded in the installer integration test; the packaged launcher installed a Codex skill and command-specific skill entries.
- Release builder now stages generated client distributions and installer engine; archives use normalized metadata and generated manifest checksums.
- Built the 2.0.8 release artifact set twice into isolated temporary directories; all 11 artifact names and SHA-256 hashes matched exactly.
- `npm run docs:check` passed for 32 Markdown pages and 28 manifest commands; `npm run docs:build` completed successfully.
- `python tests/run_all.py` passed all five phases (23 test files); installer phase passed with one documented Windows Kilo skip.
- Generated outputs are ignored build products and can be checked with `python scripts/build-distributions.py --check`.
- Old manually maintained client trees are excluded from generated release archive staging to avoid shipping a second stale distribution source.

## Not yet validated

- Linux/macOS/Windows release archive extraction and execution were not run as a matrix.
- Existing npm version metadata was queried; full published tarball contents and v2.0.8 tagged release assets cannot be inspected until publication.
- No release was published. Existing repository release manifest and old tarball are historical checkout evidence only.
- No signed provenance, SBOM, or cross-platform binary was generated; the release is source archives plus Python/Node launchers.

## Gate

Do not publish based on this report alone. Before release, build archives twice from the same revision and compare hashes; extract each supported archive; run installer and uninstall tests on Linux, macOS, and Windows; validate npm tarball contents; and verify release metadata/checksums match the exact tag. Native command invocation still needs client-level acceptance tests.
