# Troubleshooting

## Download returns 404

Check that the release asset URL and tag are available and that the requested platform has an archive in the manifest. A 404 means the tag, manifest, or asset is absent or the release is not yet published.

## Missing or mismatched checksum

The CLI refuses updates if an archive checksum is missing. Compute SHA-256 from the final uploaded bytes and update the manifest. Never use example values.

## HTTP 403 or 429

GitHub may rate-limit API endpoints. Wait and retry, use a direct release manifest URL, or set `sherpa_RELEASE_MANIFEST_URL` to a trusted host. HTTP 404 means the tag, file, or asset is absent.

## Agent does not load commands

Check the agent's documented skill/command directory and restart it if needed. Runtime compatibility is not verified for current adapters; see [AGENT-COMPATIBILITY.md](AGENT-COMPATIBILITY.md).

## Recovery

Installation validates before replacement and maintains backups for rollback. Restore the newest `.bak.*` directory beside the affected skill directory if manual recovery is needed. Installer paths do not include project `.sherpa/` state. Run `sherpa doctor` and `sherpa audit` for diagnostics.
