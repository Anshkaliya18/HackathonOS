import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

export default withMermaid(defineConfig({
  title: 'HackathonOS',
  description: 'Evidence-led AI hackathon mentorship, from idea to submission readiness.',
  base: '/HackathonOS/',
  cleanUrls: true,
  lastUpdated: true,
  themeConfig: {
    logo: '/mark.svg',
    siteTitle: 'HackathonOS',
    search: { provider: 'local' },
    socialLinks: [{ icon: 'github', link: 'https://github.com/Anshkaliya18/HackathonOS' }],
    nav: [
      { text: 'Guides', link: '/getting-started/' },
      { text: 'Reference', link: '/reference/commands' },
      { text: 'Architecture', link: '/architecture/' }
    ],
    sidebar: [
      { text: 'Start here', items: [
        { text: 'Overview', link: '/' }, { text: 'Introduction', link: '/getting-started/' },
        { text: 'Quickstart', link: '/getting-started/quickstart' }, { text: 'Installation', link: '/installation/' }
      ]},
      { text: 'Use HackathonOS', items: [
        { text: 'Core concepts', link: '/concepts/' }, { text: 'Lifecycle', link: '/concepts/lifecycle' },
        { text: 'Agent compatibility', link: '/agents/' }, { text: 'Configuration', link: '/configuration/' },
        { text: 'Workflows', link: '/workflows/' }, { text: 'Project files & audits', link: '/reference/files' }
      ]},
      { text: 'Reference', items: [
        { text: 'Commands', link: '/reference/commands' }, { text: 'Troubleshooting', link: '/troubleshooting/' },
        { text: 'FAQ', link: '/faq/' }, { text: 'Glossary', link: '/glossary/' }
      ]},
      { text: 'Developers', items: [
        { text: 'Architecture', link: '/architecture/' }, { text: 'Contributing', link: '/contributing/' },
        { text: 'Deployment', link: '/deployment/' }, { text: 'Source documents', link: '/reference/source-docs' }
      ]}
    ],
    outline: { level: [2, 3] },
    editLink: { pattern: 'https://github.com/Anshkaliya18/HackathonOS/edit/main/docs/:path', text: 'Edit this page on GitHub' },
    footer: { message: 'Built for evidence-led hackathon work.', copyright: 'HackathonOS contributors' }
  },
  head: [
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:title', content: 'HackathonOS Documentation' }],
    ['meta', { property: 'og:description', content: 'An evidence-led mentor workflow for hackathon teams.' }],
    ['meta', { name: 'theme-color', content: '#f7f8fa' }],
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/mark.svg' }]
  ],
  markdown: { lineNumbers: true }
}))
