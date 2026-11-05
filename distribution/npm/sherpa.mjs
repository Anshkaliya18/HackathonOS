#!/usr/bin/env node

import { spawnSync } from 'node:child_process'
import { existsSync } from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const packageRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..')
const args = process.argv.slice(2)

function help() {
  console.log(`sherpa package launcher

Usage:
  sherpa install [--dry-run]
  sherpa install --no-cli
  sherpa install --uninstall
  sherpa uninstall
  sherpa migrate [--project-root PATH] [--yes]
  sherpa --version
  sherpa update | doctor | audit | clean | help

Install targets: Claude Code and OpenCode. Use --dry-run to print target paths
without downloading or writing files. Management commands use the bundled
Python CLI. Uninstall removes managed global installs.`)
}

function run(script, scriptArgs, env = process.env) {
  const result = spawnSync(script, scriptArgs, { cwd: packageRoot, env, stdio: 'inherit' })
  if (result.error) {
    console.error(`Could not start ${script}: ${result.error.message}`)
    process.exit(1)
  }
  process.exit(result.status ?? 1)
}

function runPython(script, scriptArgs) {
  const candidates = process.env.PYTHON
    ? [[process.env.PYTHON, []]]
    : process.platform === 'win32'
      ? [['python', []], ['py', ['-3']]]
      : [['python3', []], ['python', []]]

  for (const [command, prefixArgs] of candidates) {
    const result = spawnSync(command, [...prefixArgs, script, ...scriptArgs], {
      cwd: packageRoot,
      env: process.env,
      stdio: 'inherit',
    })
    if (result.error?.code === 'ENOENT') continue
    if (result.error) {
      console.error(`Could not start ${command}: ${result.error.message}`)
      process.exit(1)
    }
    process.exit(result.status ?? 1)
  }

  console.error('Python 3 was not found. Install Python or set the PYTHON environment variable.')
  process.exit(1)
}

if (args.includes('--help') || args.includes('-h') || args.length === 0) {
  help()
  process.exit(0)
}

const command = args[0]
const managementCommands = new Set(['update', 'doctor', 'audit', 'clean', 'help'])
if (command === '--version' || managementCommands.has(command)) {
  const script = path.join(packageRoot, 'distribution', 'cli', 'sherpa')
  runPython(script, args)
}
if (command === 'migrate') {
  const script = path.join(packageRoot, 'distribution', 'cli', 'sherpa')
  runPython(script, ['migrate', ...args.slice(1)])
}
if (!['install', 'uninstall'].includes(command)) {
  const script = path.join(packageRoot, 'distribution', 'cli', 'sherpa')
  runPython(script, args)
}
const dryRun = args.includes('--dry-run')
const uninstall = command === 'uninstall' || args.includes('--uninstall')
if (dryRun && uninstall) {
  console.error('--dry-run cannot be combined with --uninstall.')
  process.exit(2)
}

const windows = process.platform === 'win32'
const profile = windows ? (process.env.USERPROFILE || os.homedir()) : (process.env.HOME || os.homedir())
const targets = windows
  ? [path.join(profile, '.claude', 'skills', 'sherpa'), path.join(profile, '.config', 'opencode', 'skills', 'sherpa')]
  : [path.join(profile, '.claude', 'skills', 'sherpa'), path.join(profile, '.config', 'opencode', 'skills', 'sherpa')]

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
  const env = { ...process.env }
  env.SHERPA_NPM_WRAPPER = '1'
  if (args.includes('--no-cli')) env.SHERPA_INSTALL_CLI = '0'
  const scriptArgs = ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', installer]
  if (uninstall) scriptArgs.push('-Yes')
  else scriptArgs.push('-Both', '-Yes')
  if (args.includes('--no-cli')) scriptArgs.push('-NoCli')
  run(process.env.POWERSHELL_EXE || 'powershell.exe', scriptArgs, env)
} else {
  const env = { ...process.env }
  if (uninstall) env.SHERPA_YES = '1'
  if (args.includes('--no-cli')) env.SHERPA_INSTALL_CLI = '0'
  run('bash', uninstall ? [installer] : [installer, '--both', '--yes'], env)
}
