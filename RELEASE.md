# Sherpa releases

Sherpa uses semantic versioning. Version `2.0.0` is the first release of the Sherpa package and command namespace. The CLI, installer paths, and project state directory use Sherpa naming.

## Release artifacts

The tagged GitHub Actions workflow runs `scripts/build-release.py` and attaches platform skill archives, a CLI archive, shell and PowerShell install/uninstall scripts, `manifest.json`, and `checksums.txt`. The generated manifest contains the real archive sizes and SHA-256 digests. `distribution/release/manifest.json` is only a template; never use it as a release download manifest. The skill archive includes the shared Agent Skill and host plugin manifests.

The builder excludes `.git/`, host-local settings, `.sherpa/`, caches, and generated output. It includes `.agents/skills/`, `skills/`, and the native plugin and extension manifests. The tracked `Microsoft/Windows/PowerShell/ModuleAnalysisCache` is unrelated to installation and is excluded from release archives.

## Prepare a release

1. Review the branch and run the Python suite, `npm run docs:check`, and `npm run docs:build`.
2. Confirm `distribution/VERSION`, `package.json`, plugin/extension manifests, generated docs, and the new `CHANGELOG.md` entry all use the same version.
3. Merge the reviewed branch, then create and push a matching version tag, for example `git tag v2.0.7 && git push origin v2.0.7`. This triggers the GitHub Release and GitHub Packages workflows.
4. Verify the GitHub Release assets and checksums, then publish the unscoped package to npmjs.org with `npm publish --access public` and confirm `npm view sherpa-skill version --registry=https://registry.npmjs.org` reports the same version.
5. The documentation workflow deploys the updated agent guide from `main`; verify the GitHub Pages build before sharing the release.

Repository metadata changes are maintained separately from this release workflow; see `scripts/finish-rename.sh` for the metadata helper.

## Installation URLs

Pin install commands to the selected release tag. The canonical repository is `Anshkaliya18/Sherpa`.

```bash
curl -fsSL https://github.com/Anshkaliya18/Sherpa/releases/download/v2.0.7/install.sh | bash
```

```powershell
irm https://github.com/Anshkaliya18/Sherpa/releases/download/v2.0.7/install.ps1 | iex
```

Avoid `latest` in public setup snippets when reproducible installs matter.
