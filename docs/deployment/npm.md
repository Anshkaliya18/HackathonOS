# Publish the npm package

Sherpa's public npmjs.org package is `sherpa-skill`. It exposes the `sherpa` command and ships shared Agent Skill files plus native Claude, Codex, Gemini CLI, and Qwen Code plugin/extension manifests. GitHub Packages also hosts a scoped mirror for users who need that registry.

## Before publishing

Publish the matching GitHub release first. The installer uses the release manifest at `https://github.com/Anshkaliya18/Sherpa/releases/latest/download/manifest.json`; without that manifest and its checksummed archives, installation cannot complete.

From the repository root, inspect exactly what npm will include:

```bash
npm pack --dry-run
```

Check that the package contains the README, CLI wrappers, platform installers, skill files, workflows, and plugin manifests, and excludes tests, caches, and local project data.

## Publish a release

Publish the public npm package after the matching GitHub release is available:

```bash
npm publish --access public
npm view sherpa-skill version --registry=https://registry.npmjs.org
npm install --global sherpa-skill --registry=https://registry.npmjs.org
sherpa --help
```

For the optional GitHub Packages mirror, push a matching `vX.Y.Z` tag after merging the version bump to `main`. GitHub requires scoped names there, so the mirror is `@anshkaliya18/sherpa-skill`; use the unscoped `sherpa-skill` commands above for the public npm registry. Local mirror consumers need `read:packages` and this user-level npm configuration:

```ini
@anshkaliya18:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=YOUR_GITHUB_TOKEN
```

For public installs, continue using the unscoped npmjs.org commands above. GitHub Packages requires the scoped mirror name.
