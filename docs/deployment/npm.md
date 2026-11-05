# Publish the npm package

Sherpa's package is named `@anshkaliya18/sherpa-skill` and is published to GitHub Packages. The package exposes the `sherpa` command and downloads the versioned skill archive from this repository's GitHub Releases.

## Before publishing

Publish the matching GitHub release first. The installer uses the release manifest at `https://github.com/Anshkaliya18/Sherpa/releases/latest/download/manifest.json`; without that manifest and its checksummed archives, installation cannot complete.

From the repository root, inspect exactly what npm will include:

```bash
npm pack --dry-run
```

Check that the package contains the README, npm command wrappers, and platform installers, and excludes tests, caches, and local project data.

## Publish a release

Push a matching `vX.Y.Z` tag after merging the version bump to `main`. GitHub Actions creates the release assets and publishes the package using `GITHUB_TOKEN` with `packages: write` permission. For local installation, authenticate to GitHub Packages and set up `@anshkaliya18:registry=https://npm.pkg.github.com` in `.npmrc`. Then verify the registry entry:

```bash
npm view @anshkaliya18/sherpa-skill --registry=https://npm.pkg.github.com
npm install --global @anshkaliya18/sherpa-skill --registry=https://npm.pkg.github.com
sherpa --help
```
