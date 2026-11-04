#!/usr/bin/env node
import { spawnSync } from 'node:child_process'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
const target = path.join(path.dirname(fileURLToPath(import.meta.url)), 'sherpa.mjs')
console.error("HackathonOS is now Sherpa. The 'hackathonos' command is deprecated; use 'sherpa'.")
const result = spawnSync(process.execPath, [target, ...process.argv.slice(2)], { stdio: 'inherit' })
if (result.error) { console.error(result.error.message); process.exit(1) }
process.exit(result.status ?? 1)
