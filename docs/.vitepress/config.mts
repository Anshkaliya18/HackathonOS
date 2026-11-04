import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

// GitHub Pages project sites are served from /<repository>/. Derive both this
// path and repository links from Actions so the site follows a later repo rename.
const [repositoryOwner, repositoryName] = (process.env.GITHUB_REPOSITORY ?? 'Anshkaliya18/HackathonOS').split('/')
const origin = `https://${repositoryOwner.toLowerCase()}.github.io`
const base = process.env.VITEPRESS_BASE ?? `/${repositoryName}/`
const repositoryUrl = `https://github.com/${repositoryOwner}/${repositoryName}`

export default withMermaid(defineConfig({
  title: 'Sherpa',
  description: 'An AI agent skill that mentors hackathon teams from idea to submission.',
  base,
  cleanUrls: true,
  lastUpdated: true,
  sitemap: { hostname: `${origin}${base}` },
  transformPageData(pageData) {
    const route = pageData.relativePath.replace(/index\.md$/, '').replace(/\.md$/, '')
    const pageUrl = `${origin}${base}${route}`.replace(/\/$/, route ? '' : '/')
    pageData.frontmatter.head ??= []
    pageData.frontmatter.head.push(['link', { rel: 'canonical', href: pageUrl }])
  },
  themeConfig: {
    logo: '/mark.svg',
    siteTitle: 'Sherpa',
    search: { provider: 'local' },
    socialLinks: [{ icon: 'github', link: repositoryUrl }],
    nav: [
      { text: 'Field guide', link: '/getting-started/' },
      { text: 'Commands', link: '/reference/commands' },
      { text: 'Architecture', link: '/architecture/' },
    ],
    sidebar: [
      {
        text: 'Start here', items: [
          { text: 'Overview', link: '/' }, { text: 'Introduction', link: '/getting-started/' },
          { text: 'Your first ascent', link: '/first-ascent' }, { text: 'Quickstart', link: '/getting-started/quickstart' },
          { text: 'Installation', link: '/installation/' }, { text: 'Migration', link: '/migration' },
        ]
      },
      {
        text: 'Use Sherpa', items: [
          { text: 'Core concepts', link: '/concepts/' }, { text: 'Lifecycle', link: '/concepts/lifecycle' },
          { text: 'Agent compatibility', link: '/agents/' }, { text: 'Configuration', link: '/configuration/' },
          { text: 'Workflows', link: '/workflows/' }, { text: 'Project files & audits', link: '/reference/files' },
        ]
      },
      {
        text: 'Reference', items: [
          { text: 'Commands', link: '/reference/commands' }, { text: 'Troubleshooting', link: '/troubleshooting/' },
          { text: 'FAQ', link: '/faq/' }, { text: 'Glossary', link: '/glossary/' },
        ]
      },
      {
        text: 'Developers', items: [
          { text: 'Architecture', link: '/architecture/' }, { text: 'Contributing', link: '/contributing/' },
          { text: 'Deployment', link: '/deployment/' }, { text: 'Publish on npm', link: '/deployment/npm' },
          { text: 'Source documents', link: '/reference/source-docs' },
        ]
      },
    ],
    outline: { level: [2, 3] },
    editLink: { pattern: `${repositoryUrl}/edit/main/docs/:path`, text: 'Edit this page on GitHub' },
    footer: { message: 'Build with evidence. Keep the decisions yours.', copyright: 'Sherpa contributors · MIT License' },
  },
  head: [
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:title', content: 'Sherpa · The ascent from idea to demo' }],
    ['meta', { property: 'og:description', content: 'Build the right thing. Prove it works. Show why it matters.' }],
    ['meta', { property: 'og:image', content: `${origin}${base}og.svg` }],
    ['meta', { name: 'twitter:card', content: 'summary_large_image' }],
    ['meta', { name: 'twitter:title', content: 'Sherpa · Build the right thing' }],
    ['meta', { name: 'twitter:description', content: 'An AI mentor skill for hackathon teams.' }],
    ['meta', { name: 'twitter:image', content: `${origin}${base}og.svg` }],
    ['meta', { name: 'theme-color', content: '#f4f1e8' }],
    ['link', { rel: 'canonical', href: `${origin}${base}` }],
    ['link', { rel: 'icon', type: 'image/svg+xml', href: `${base}mark.svg` }],
  ],
  markdown: { lineNumbers: true },
  mermaid: {
    theme: 'base',
    themeVariables: {
      background: '#f4f1e8', primaryColor: '#dce9e4', primaryTextColor: '#242b2b',
      primaryBorderColor: '#244d47', lineColor: '#9a4f2e', secondaryColor: '#e8e2d5',
      tertiaryColor: '#eeeadf', fontFamily: 'Avenir Next, Avenir, Segoe UI, sans-serif',
    },
  },
}))
