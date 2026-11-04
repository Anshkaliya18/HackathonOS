# Contributing

1. Preserve command routing and safety gates. Review `commands/manifest.json` and `SKILL.md` before changing workflows.
2. Keep agent integration isolated and document evidence. Do not claim runtime compatibility without a smoke test.
3. Keep installers cross-platform, fail closed on integrity errors, preserve user configuration, and do not touch project `.hackathon/` data.
4. Add or update focused regression coverage and report platforms actually exercised.
5. Exclude generated environments, caches, credentials, and local state from commits. Do not add a license without the owner's licensing decision.

Before proposing a release, follow `RELEASE.md`, build archives from the intended skill content, calculate checksums from final artifacts, and verify manifest URLs against the published release.
