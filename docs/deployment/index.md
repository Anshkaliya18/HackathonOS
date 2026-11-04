# Documentation deployment

The field guide is built with VitePress and deployed to GitHub Pages by `.github/workflows/docs.yml`.

## Preview locally

```bash
npm ci
npm run docs:dev
```

## Build and check

```bash
npm run docs:commands
npm run docs:check
npm run docs:build
npm run docs:preview
```

`docs:build` refreshes the manifest-backed command reference and writes the static site to `docs/.vitepress/dist/`.

## GitHub Pages

The workflow runs on pushes to `main` and manual dispatch. It builds with the repository base `/sherpa/`, uploads the Pages artifact, and deploys it with `actions/deploy-pages@v4`. Before enabling deployment, merge the branch, rename the repository using the reviewed `scripts/finish-rename.sh` commands, and set the Pages source to **GitHub Actions** in repository settings. GitHub Pages must be enabled for deployment creation to succeed.

The configured site URL is [anshkaliya18.github.io/sherpa](https://anshkaliya18.github.io/sherpa/); this change does not deploy the current branch.

## Search and metadata

VitePress local search indexes the generated pages. The site config supplies per-page canonical links, a sitemap hostname, Open Graph and Twitter metadata, and the custom `mark.svg` favicon. `og.svg` is the source social card. `robots.txt` is public and allows indexing; change it if the site becomes private or staged.
