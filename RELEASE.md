# Sherpa releases

Sherpa uses semantic versioning. Version `2.0.0` is the first release of the Sherpa package and command namespace. The CLI, installer paths, and project state directory use Sherpa naming.

## Release artifacts

The tagged GitHub Actions workflow runs `scripts/build-release.py` and attaches platform skill archives, a CLI archive, shell and PowerShell install/uninstall scripts, `manifest.json`, and `checksums.txt`. The generated manifest contains the real archive sizes and SHA-256 digests. `distribution/release/manifest.json` is only a template; never use it as a release download manifest.

The builder excludes `.git/`, `.claude/`, `.opencode/`, `.kilo/`, `.sherpa/`, caches, and generated output. The tracked `Microsoft/Windows/PowerShell/ModuleAnalysisCache` is unrelated to installation and is excluded from release archives.

## Prepare a release

1. Review the branch and run the documented Python test suite and `npm run docs:build`.
2. Confirm `distribution/VERSION`, `package.json`, and `CHANGELOG.md` agree on the version.
3. Merge the reviewed branch, then create and push a version tag, for example `git tag v2.0.0 && git push origin v2.0.0`.
4. The release workflow builds and uploads the archives and manifest. Verify the attached checksums and release page before sharing the installer.

Repository metadata changes are maintained separately from this release workflow; see `scripts/finish-rename.sh` for the metadata helper.

## Installation URLs

After the v2.0.0 release exists, pin install commands to the selected release tag. The canonical repository is `Anshkaliya18/Sherpa`.

```bash
curl -fsSL https://github.com/Anshkaliya18/Sherpa/releases/download/v2.0.0/install.sh | bash
```

```powershell
irm https://github.com/Anshkaliya18/Sherpa/releases/download/v2.0.0/install.ps1 | iex
```

Avoid `latest` in public setup snippets when reproducible installs matter.
