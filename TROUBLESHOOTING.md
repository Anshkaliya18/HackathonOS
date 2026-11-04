# Troubleshooting

## Download returns 404

The checked-in manifest explicitly calls itself a release template. It references v1.0.0 assets, but this checkout has no published archive/checksum assets. Publishing the tagged GitHub release and matching files is required before the default release URL can work.

## Missing or mismatched checksum

The CLI refuses updates if an archive checksum is missing. Compute SHA-256 from the final uploaded bytes and update the manifest. Never use example values.

## HTTP 403 or 429

GitHub may rate-limit API endpoints. Wait and retry, use a direct release manifest URL, or set `HACKATHONOS_RELEASE_MANIFEST_URL` to a trusted host. HTTP 404 means the tag, file, or asset is absent.

## Agent does not load commands

Check the agent's documented skill/command directory and restart it if needed. Runtime compatibility is not verified for current adapters; see [AGENT-COMPATIBILITY.md](AGENT-COMPATIBILITY.md).

## Recovery

Installation validates before replacement and maintains backups for rollback. Restore the newest `.bak.*` directory beside the affected skill directory if manual recovery is needed. Installer paths do not include project `.hackathon/` state. Run `hackathonos doctor` and `hackathonos audit` for diagnostics.
