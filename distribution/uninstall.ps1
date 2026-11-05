# sherpa Uninstaller - Windows PowerShell (5.1+ / 7+)
#
# Removes only sherpa installation files. User project data and
# `.sherpa/` directories are never touched.
#
# Usage:
#   irm https://YOUR-DOMAIN/uninstall.ps1 | iex

[CmdletBinding()]
param(
    [switch] $Yes
)

$ErrorActionPreference = 'Stop'

$PROJECT = "sherpa"
$CLI_NAME = "sherpa"
$CLI_BIN_DIR = Join-Path $env:USERPROFILE "AppData\Local\sherpa\bin"
$CLAUDE_SKILL_DIR = Join-Path $env:USERPROFILE ".claude\skills\sherpa"
$OPENCODE_SKILL_DIR = Join-Path $env:USERPROFILE ".config\opencode\skills\sherpa"

function Write-Ok { param([string] $M) Write-Host ("  + " + $M) -ForegroundColor Green }
function Write-Info { param([string] $M) Write-Host ("  > " + $M) }
function Write-Err { param([string] $M) Write-Host ("  x " + $M) -ForegroundColor Red }

Write-Host "sherpa uninstaller"
Write-Host ""
Write-Host "The following will be removed:"
$removed = 0
if (Test-Path (Join-Path $CLAUDE_SKILL_DIR "SKILL.md")) {
    Write-Host ("  * Claude Code skill: {0}" -f $CLAUDE_SKILL_DIR) -ForegroundColor Green
    $removed++
}
if (Test-Path (Join-Path $OPENCODE_SKILL_DIR "SKILL.md")) {
    Write-Host ("  * OpenCode skill: {0}" -f $OPENCODE_SKILL_DIR) -ForegroundColor Green
    $removed++
}
$cliExe = Join-Path $CLI_BIN_DIR $CLI_NAME
$cliBat = Join-Path $CLI_BIN_DIR "${CLI_NAME}.bat"
$cliExists = (Test-Path $cliExe) -or (Test-Path $cliBat)
if ($cliExists) {
    Write-Host ("  * CLI: {0}" -f $CLI_BIN_DIR) -ForegroundColor Green
    $removed++
}
Write-Host ""
Write-Host "User project data (.sherpa/ directories) will NOT be removed."
Write-Host "This action cannot be undone."
Write-Host ""

if (-not $Yes) {
    $reply = Read-Host "Proceed with uninstallation? [y/N]"
    if ($reply -ne 'y' -and $reply -ne 'Y' -and $reply -ne 'yes' -and $reply -ne 'YES') {
        Write-Host "Uninstallation cancelled."
        exit 0
    }
}

if (Test-Path (Join-Path $CLAUDE_SKILL_DIR "SKILL.md")) {
    Remove-Item -Path $CLAUDE_SKILL_DIR -Recurse -Force
    Write-Ok "Removed Claude Code skill"
}
if (Test-Path (Join-Path $OPENCODE_SKILL_DIR "SKILL.md")) {
    Remove-Item -Path $OPENCODE_SKILL_DIR -Recurse -Force
    Write-Ok "Removed OpenCode skill"
}
if (Test-Path $cliExe) { Remove-Item -Path $cliExe -Force }
if (Test-Path $cliBat) { Remove-Item -Path $cliBat -Force }
if ($cliExists) { Write-Ok "Removed CLI" }

if ($removed -eq 0) {
    Write-Host "No sherpa installation found."
} else {
    Write-Host ""
    Write-Host ("Uninstallation completed. Removed {0} item(s)." -f $removed) -ForegroundColor Green
    Write-Host ""
    Write-Host "Note: your project .sherpa/ state directories were preserved."
}
