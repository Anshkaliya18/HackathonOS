import { readdir, readFile, stat } from 'node:fs/promises'
import path from 'node:path'

const root = path.resolve('docs')
const files = []
async function walk(dir) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    if (entry.name === '.vitepress' || entry.name === 'node_modules') continue
    const file = path.join(dir, entry.name)
    if (entry.isDirectory()) await walk(file)
    else if (entry.name.endsWith('.md')) files.push(file)
  }
}
await walk(root)
const routes = new Set()
for (const file of files) {
  const rel = path.relative(root, file).replaceAll('\\', '/')
  if (rel === 'index.md') routes.add('/')
  else if (rel.endsWith('/index.md')) routes.add(`/${rel.slice(0, -'index.md'.length)}`)
  else routes.add(`/${rel.slice(0, -3)}`)
}
const failures = []
for (const file of files) {
  const content = await readFile(file, 'utf8')
  for (const [, target] of content.matchAll(/\]\(([^)]+)\)/g)) {
    const clean = target.split('#')[0].split('?')[0]
    if (!clean || /^(?:https?:|mailto:|tel:|\/\/)/i.test(clean)) continue
    if (clean.startsWith('/')) {
      const route = clean.endsWith('/') ? clean : clean.replace(/\.md$/, '')
      if (!routes.has(route) && !routes.has(`${route}/`)) failures.push(`${path.relative(root, file)} -> ${target}`)
      continue
    }
    if (clean.endsWith('.md')) {
      const targetPath = path.resolve(path.dirname(file), clean)
      try { await stat(targetPath) } catch { failures.push(`${path.relative(root, file)} -> ${target}`) }
    }
  }
}
const manifest = JSON.parse(await readFile('commands/manifest.json', 'utf8'))
const commandPage = await readFile(path.join(root, 'reference/commands.md'), 'utf8').catch(() => '')
for (const command of manifest.implemented) {
  if (!commandPage.includes(command.command)) failures.push(`command reference missing ${command.command}; run npm run docs:commands`)
}
if (failures.length) {
  console.error(`Documentation checks failed:\n${failures.map((item) => `- ${item}`).join('\n')}`)
  process.exitCode = 1
} else {
  console.log(`Documentation checks passed: ${files.length} Markdown pages and ${manifest.implemented.length} manifest commands.`)
}
