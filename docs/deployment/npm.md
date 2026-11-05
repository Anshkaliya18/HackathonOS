# Publish the npm package

Sherpa's public npmjs.org package is `sherpa-skill`; the GitHub Packages mirror is `@anshkaliya18/sherpa-skill`. Both expose the `sherpa` command and download the versioned skill archive from this repository's GitHub Releases.

## Before publishing

Publish the matching GitHub release first. The installer uses the release manifest at `https://github.com/Anshkaliya18/Sherpa/releases/latest/download/manifest.json`; without that manifest and its checksummed archives, installation cannot complete.

From the repository root, inspect exactly what npm will include:

```bash
npm pack --dry-run
```

Check that the package contains the README, npm command wrappers, and platform installers, and excludes tests, caches, and local project data.

## Publish a release

Publish the public npm package after the matching GitHub release is available:

```bash
npm publish --access public
npm view sherpa-skill version --registry=https://registry.npmjs.org
npm install --global sherpa-skill --registry=https://registry.npmjs.org
sherpa --help
```

For the GitHub Packages mirror, push a matching `vX.Y.Z` tag after merging the version bump to `main`. The GitHub Actions workflow applies the repository's GitHub owner scope and publishes using `GITHUB_TOKEN` with `packages: write`. Local consumers need a personal access token with `read:packages` and this user-level npm configuration:

```ini
@anshkaliya18:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=YOUR_GITHUB_TOKEN
```

Then install the mirror with `npm install --global @anshkaliya18/sherpa-skill`.
