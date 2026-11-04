# sherpa Security

Security model and guarantees for the sherpa distribution installer.

## Guarantees

| Requirement | Implementation |
|-------------|----------------|
| HTTPS only | All downloads use `https://` via `curl` / `Invoke-WebRequest`. |
| Verify before execute | Every downloaded archive is hashed and compared to the SHA-256 checksum from the release manifest **before** any extraction. |
| Path traversal prevention | Archive members are scanned for `..` segments and absolute paths before extraction; unsafe archives are rejected. |
| No admin privileges | Installs to user-writable directories only (`~/.claude`, `~/.config/opencode`, `~/.local/bin`, `%USERPROFILE%\AppData\Local`). |
| No secrets collected | The installer never requests, stores, or transmits API keys, tokens, or personal information. |
| No secrets in logs | Checksums of downloaded archives are logged; no provider credentials or secrets appear in output. |
| Non-destructive | User project files and `.sherpa/` state directories are never modified, moved, or deleted. |
| Rollback on failure | Updates back up the previous installation and restore it automatically if validation fails. |

## What the installer does NOT do

- Does not clone the development repository.
- Does not run `npm`, `pip`, or any package manager.
- Does not execute downloaded content before verification.
- Does not modify `.env`, credentials, or provider configuration.
- Does not collect telemetry or phone home except to fetch the release manifest and archives you explicitly request.

## Verifying the installer itself

Because the installer is delivered over HTTPS, verify the hosting domain and,
for high-security environments, pin `sherpa_RELEASE_MANIFEST_URL` to a
self-hosted manifest you control and inspect `checksums.txt` before running.

## Vulnerability reporting

Report security issues to the repository maintainers via GitHub. Do not
disclose secrets or tokens in issue reports.
