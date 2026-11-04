# Publish the npm package

Sherpa's npm package is named `sherpa-skill`; the shorter `sherpa` name is already owned by another publisher. The package exposes the `sherpa` command and downloads the versioned skill archive from this repository's GitHub Releases.

## Before publishing

Publish the matching GitHub release first. The npm installer uses the release manifest at `https://github.com/Anshkaliya18/HackathonOS/releases/latest/download/manifest.json`; without that manifest and its checksummed archives, npm installation cannot complete. Check package availability with `npm view sherpa-skill`; at the time this guide was written, the registry returned 404 for that name. Recheck before publishing because package names can be claimed at any time.

From the repository root, inspect exactly what npm will include:

```bash
npm pack --dry-run
```

Check that the package contains the README, npm command wrappers, and platform installers, and excludes tests, caches, and local project data.

## Publish interactively

Enable npm two-factor authentication, then log in and verify the account:

```bash
npm login
npm whoami
npm publish --dry-run
npm publish
```

Complete the npm 2FA prompt when requested. This package is unscoped, so it does not need `--access public`. After publishing, verify the registry entry:

```bash
npm view sherpa-skill version
npm install --global sherpa-skill
sherpa --help
```

Version `2.0.0` is the prepared first Sherpa package version. npm does not allow reusing a package version: if `2.0.0` has already been published, increment `version` in `package.json` and `package-lock.json` before publishing again.

For automated releases, configure npm trusted publishing for this GitHub repository and workflow instead of storing a long-lived token. See the [npm trusted publishing guide](https://docs.npmjs.com/trusted-publishers/).
