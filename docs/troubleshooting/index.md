# Troubleshooting

Use the symptom to find a likely cause, then verify the result after the fix.

## Installer says Python is missing

**Cause:** Python is not available on `PATH`. **Diagnosis:** run `python --version`. **Fix:** install Python using your operating system's trusted package source and make the executable available on `PATH`. **Verify:** rerun the installer and `hackathonos --version`.

## Release download returns 404

**Cause:** the referenced release, manifest, tag, or archive is unavailable. **Diagnosis:** inspect the release manifest URL and the asset names. **Fix:** use a published manifest and matching assets. **Verify:** retry and confirm checksum validation completes.

## HTTP 403 or 429

**Cause:** the hosting service rejected or rate-limited the request. **Diagnosis:** check the HTTP status and whether the manifest URL is reachable. **Fix:** retry later or point `HACKATHONOS_RELEASE_MANIFEST_URL` to a trusted manifest. **Verify:** run `hackathonos doctor`.

## Checksum missing or mismatched

**Cause:** manifest metadata does not match the downloaded archive. **Diagnosis:** compare the manifest SHA-256 with the final asset bytes. **Fix:** publish correct checksums; do not bypass integrity verification. **Verify:** rerun the install/update and confirm validation passes.

## Agent does not show HackathonOS commands

**Cause:** files are outside the host's discovery path, the host needs a reload, or runtime support is incomplete. **Diagnosis:** confirm files in the documented adapter directory and check [compatibility](/agents/). **Fix:** install to the supported path and reload the host. **Verify:** test `/hackathonos help` in a disposable project. Runtime loading is currently marked `NOT VERIFIED`.

## Workflow reports missing state or evidence

**Cause:** the agent is in the wrong repository, `.hackathon/` is absent, or the required phase artifacts do not exist. **Diagnosis:** check the working directory and project files. **Fix:** run init if appropriate and provide the relevant brief, criteria, or evidence. **Verify:** rerun status or the requested workflow and check which evidence it cites.

## CLI is not found after installation

**Cause:** the user bin directory is not on the current shell's `PATH`. **Diagnosis:** inspect `PATH` and the install path (`~/.local/bin` or `%USERPROFILE%\AppData\Local\HackathonOS\bin`). **Fix:** restart the shell or add the path for the user. **Verify:** run `hackathonos --version`.

## Clean lists files you did not expect

**Cause:** recognized generated debris exists in a managed skill folder. **Diagnosis:** inspect each path from `hackathonos clean --dry-run`. **Fix:** only opt into deletion if the listed items are generated debris you want removed. **Verify:** rerun the dry run and confirm the intended files are gone.

## Windows-specific notes

PowerShell uses `-Both`, `-NoCli`, and similar named parameters. The script requires Python and currently waits for Enter after successful installation. A fresh shell may be required for `PATH` changes to take effect.

## Linux and macOS notes

The Bash installer uses `--both` and related flags. Confirm `~/.local/bin` is on `PATH` for CLI access. On macOS, the release manifest currently lists both amd64 and arm64 archives.

More detail: [source troubleshooting guide](https://github.com/Anshkaliya18/HackathonOS/blob/main/TROUBLESHOOTING.md).
