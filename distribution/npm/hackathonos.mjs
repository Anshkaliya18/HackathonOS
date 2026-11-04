#!/usr/bin/env node

import { spawnSync } from 'node:child_process'
import { existsSync } from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const packageRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..')
const args = process.argv.slice(2)

function help() {
  console.log(`HackathonOS skill installer

Usage:
  hackathonos install [--dry-run]
  hackathonos install --uninstall
  hackathonos uninstall

Install targets: Claude Code and OpenCode. Use --dry-run to print target paths
without downloading or writing files. Uninstall removes managed global installs.`)
}

function run(script, scriptArgs, env = process.env) {
  const result = spawnSync(script, scriptArgs, { cwd: packageRoot, env, stdio: 'inherit' })
  if (result.error) {
    console.error(`Could not start ${script}: ${result.error.message}`)
    process.exit(1)
  }
  process.exit(result.status ?? 1)
}

if (args.includes('--help') || args.includes('-h') || args.length === 0) {
  help()
  process.exit(0)
}

const command = args[0]
const dryRun = args.includes('--dry-run')
const uninstall = command === 'uninstall' || args.includes('--uninstall')
if (!['install', 'uninstall'].includes(command)) {
  console.error(`Unknown command: ${command}`)
  help()
  process.exit(2)
}
if (dryRun && uninstall) {
  console.error('--dry-run cannot be combined with --uninstall.')
  process.exit(2)
}

const windows = process.platform === 'win32'
const profile = windows ? (process.env.USERPROFILE || os.homedir()) : (process.env.HOME || os.homedir())
const targets = windows
  ? [path.join(profile, '.claude', 'skills', 'hackathonos'), path.join(profile, '.config', 'opencode', 'skills', 'hackathonos')]
  : [path.join(profile, '.claude', 'skills', 'hackathonos'), path.join(profile, '.config', 'opencode', 'skills', 'hackathonos')]

if (dryRun) {
  console.log('Dry run: no files were changed.')
  for (const target of targets) console.log(`  ${target}`)
  process.exit(0)
}

const filename = uninstall
  ? (windows ? 'uninstall.ps1' : 'uninstall.sh')
  : (windows ? 'install.ps1' : 'install.sh')
const installer = path.join(packageRoot, 'distribution', filename)
if (!existsSync(installer)) {
  console.error(`Package is missing ${path.relative(packageRoot, installer)}.`)
  process.exit(1)
}

if (windows) {
  const scriptArgs = ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', installer]
  if (uninstall) scriptArgs.push('-Yes')
  else scriptArgs.push('-Both', '-Yes')
  run(process.env.POWERSHELL_EXE || 'powershell.exe', scriptArgs)
} else {
  const env = { ...process.env }
  if (uninstall) env.HACKATHONOS_YES = '1'
  run('bash', uninstall ? [installer] : [installer, '--both', '--yes'], env)
}
