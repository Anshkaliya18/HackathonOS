import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import CommandExplorer from './CommandExplorer.vue'
import ReadingProgress from './ReadingProgress.vue'
import Layout from './Layout.vue'
import InstallCopy from './InstallCopy.vue'
import CompatibilityTable from './CompatibilityTable.vue'
import './custom.css'

const theme: Theme = {
  extends: DefaultTheme,
  Layout,
  enhanceApp({ app }) {
    app.component('CommandExplorer', CommandExplorer)
    app.component('ReadingProgress', ReadingProgress)
    app.component('InstallCopy', InstallCopy)
    app.component('CompatibilityTable', CompatibilityTable)
  },
}

export default theme
