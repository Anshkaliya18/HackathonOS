# Documentation deployment

The documentation site is a VitePress static site. This repository does not currently declare a production documentation domain, so the site omits canonical URLs.

## Run locally

```bash
npm install
npm run docs:dev
```

## Build and preview

```bash
npm run docs:commands
npm run docs:check
npm run docs:build
npm run docs:preview
```

The generated site is in `docs/.vitepress/dist/`.

## GitHub Pages

The repository's remote is GitHub, so a Pages workflow is included at `.github/workflows/docs.yml`. It builds the VitePress site with the repository base path and deploys the artifact when pushed to `main`. Enable GitHub Pages in repository settings with **GitHub Actions** as the source. The resulting Pages address depends on repository/account settings and is intentionally not hard-coded here.

## SEO and metadata

Pages inherit site title/description and Open Graph metadata, and use the repository mark as favicon. Configure a canonical URL and sitemap hostname only after the public docs domain is established. `docs/public/robots.txt` allows indexing; adjust it if deployment is private or staged.
