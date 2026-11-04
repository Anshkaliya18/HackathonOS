# HackathonOS Installer - Windows PowerShell (5.1+ / 7+)
#
# Installs the HackathonOS AI Hackathon Mentor skill for Claude Code and
# OpenCode from a versioned GitHub Releases archive, verifies its SHA-256
# checksum, and installs the `hackathonos` CLI.
#
# Usage:
#   irm https://YOUR-DOMAIN/install.ps1 | iex
#
# Configuration (environment variables, all optional):
#   $env:HACKATHONOS_RELEASE_MANIFEST_URL   Release manifest JSON URL
#   $env:HACKATHONOS_VERSION                Pin a specific version (default: latest)
#   $env:HACKATHONOS_INSTALL_CLAUDE         1=install (default), 0=skip
#   $env:HACKATHONOS_INSTALL_OPENCODE       1=install (default), 0=skip
#   $env:HACKATHONOS_INSTALL_CLI            1=install (default), 0=skip
#   $env:HACKATHONOS_NO_PATH                1=do not modify user PATH
#
# The installer never touches user project data or `.hackathon/` directories.

[CmdletBinding()]
param(
    [switch] $Claude,
    [switch] $OpenCode,
    [switch] $Both,
    [string] $ProjectDir,
    [string] $Version,
    [string] $ManifestUrl,
    [switch] $NoCli,
    [switch] $NoPath,
    [switch] $Yes
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

$PROJECT = "HackathonOS"
$CLI_NAME = "hackathonos"
$DEFAULT_MANIFEST_URL = "https://github.com/Anshkaliya18/HackathonOS/releases/latest/download/manifest.json"

$CLAUDE_SKILL_DIR = Join-Path $env:USERPROFILE ".claude\skills\hackathonos"
$OPENCODE_SKILL_DIR = Join-Path $env:USERPROFILE ".config\opencode\skills\hackathonos"
$CLI_BIN_DIR = Join-Path $env:USERPROFILE "AppData\Local\HackathonOS\bin"

$script:TMP_DIR = $null
$script:BACKUP_DIRS = @()
$script:CREATED_DIRS = @()

###############################################################################
# Helpers
###############################################################################
function Write-Err {
    param([string] $Message)
    Write-Host ("  x " + $Message) -ForegroundColor Red
}
function Write-Ok {
    param([string] $Message)
    Write-Host ("  + " + $Message) -ForegroundColor Green
}
function Write-Info {
    param([string] $Message)
    Write-Host ("  > " + $Message)
}
function Write-Step {
    param([string] $Message)
    $script:STEP++
    Write-Host ""
    Write-Host ("[{0}/{1}] {2}" -f $script:STEP, $script:STEP_TOTAL, $Message) -ForegroundColor Cyan
}

$script:STEP = 0
$script:STEP_TOTAL = 6

function Cleanup {
    if ($script:TMP_DIR -and (Test-Path $script:TMP_DIR)) {
        Remove-Item -Path $script:TMP_DIR -Recurse -Force -ErrorAction SilentlyContinue
    }
}
trap {
    Write-Err ("Installation failed: {0}" -f $_.Exception.Message)
    if ($script:BACKUP_DIRS.Count -gt 0 -or $script:CREATED_DIRS.Count -gt 0) {
        try { Rollback-Installs } catch { Write-Err ("Rollback failed: {0}" -f $_.Exception.Message) }
    }
    Cleanup
    exit 1
}

function Test-Command {
    param([string] $Name)
    return (Get-Command $Name -ErrorAction SilentlyContinue) -ne $null
}

function Invoke-DownloadWithRetry {
    param([string] $Uri, [string] $Destination, [int] $TimeoutSec)
    for ($attempt = 0; $attempt -lt 3; $attempt++) {
        try {
            Invoke-WebRequest -Uri $Uri -OutFile $Destination -TimeoutSec $TimeoutSec -ErrorAction Stop | Out-Null
            return
        } catch {
            if (Test-Path $Destination) { Remove-Item -LiteralPath $Destination -Force -ErrorAction SilentlyContinue }
            if ($attempt -eq 2) { throw "Download failed after 3 attempts ($Uri): $($_.Exception.Message)" }
            Start-Sleep -Seconds ([math]::Pow(2, $attempt))
        }
    }
}

function Get-Sha256 {
    param([string] $Path)
    # Prefer the built-in Get-FileHash (PowerShell 4.0+ / 5.1+).
    try {
        $hash = Get-FileHash -Path $Path -Algorithm SHA256
        return $hash.Hash
    } catch {
        # Fallback to certutil.
        $tmp = Join-Path $env:TEMP "hackathonos-sha256-$([guid]::NewGuid()).txt"
        certutil -hashfile $Path SHA256 > $tmp 2>$null
        $lines = Get-Content $tmp
        Remove-Item $tmp -Force -ErrorAction SilentlyContinue
        foreach ($line in $lines) {
            $line = $line.Trim()
            if ($line -match '^[0-9a-fA-F]{64}$') { return $line }
        }
        throw "No SHA-256 tool available."
    }
}

function Parse-JsonField {
    param([string] $ManifestFile, [string] $ScriptBlock)
    $data = Get-Content -Path $ManifestFile -Raw | ConvertFrom-Json
    return & ([scriptblock]::Create($ScriptBlock)) $data
}

###############################################################################
# Environment detection
###############################################################################
function Detect-Environment {
    Write-Info "Operating system: Windows"
    $arch = (Get-WmiObject Win32_Processor -ErrorAction SilentlyContinue).Architecture
    $archName = switch ($arch) {
        0 { "x86" } 1 { "MIPS" } 2 { "Alpha" } 6 { "ia64" } 9 { "amd64" }
        11 { "arm64" } default { "unknown($arch)" }
    }
    Write-Info "Architecture: $archName"
    if (Test-Command python) {
        Write-Info "Python: $(python --version 2>&1)"
    } elseif (Test-Command python3) {
        Write-Info "Python: $(python3 --version 2>&1)"
    } else {
        Write-Info "Python: not found"
    }

    $claudeInstalled = Test-Path (Join-Path $CLAUDE_SKILL_DIR "SKILL.md")
    $opencodeInstalled = Test-Path (Join-Path $OPENCODE_SKILL_DIR "SKILL.md")

    if ($claudeInstalled) { Write-Ok "Claude Code skill detected ($CLAUDE_SKILL_DIR)" }
    else { Write-Info "Claude Code skill not installed" }
    if ($opencodeInstalled) { Write-Ok "OpenCode skill detected ($OPENCODE_SKILL_DIR)" }
    else { Write-Info "OpenCode skill not installed" }

    $script:INSTALL_CLAUDE = [bool]($env:HACKATHONOS_INSTALL_CLAUDE -ne "0")
    $script:INSTALL_OPENCODE = [bool]($env:HACKATHONOS_INSTALL_OPENCODE -ne "0")
    if ($Claude) { $script:INSTALL_CLAUDE = $true; $script:INSTALL_OPENCODE = $false }
    if ($OpenCode) { $script:INSTALL_OPENCODE = $true; $script:INSTALL_CLAUDE = $false }
    if ($Both) { $script:INSTALL_CLAUDE = $true; $script:INSTALL_OPENCODE = $true }

    $script:TARGETS = New-Object System.Collections.Generic.List[string]
    if ($script:INSTALL_CLAUDE) { $script:TARGETS.Add("claude") }
    if ($script:INSTALL_OPENCODE) { $script:TARGETS.Add("opencode") }
    if ($script:TARGETS.Count -eq 0) {
        throw "No target environments selected."
    }
}

###############################################################################
# Fetch manifest
###############################################################################
function Fetch-Manifest {
    $manifestUrl = $ManifestUrl
    if ([string]::IsNullOrWhiteSpace($manifestUrl)) { $manifestUrl = $env:HACKATHONOS_RELEASE_MANIFEST_URL }
    if ([string]::IsNullOrWhiteSpace($manifestUrl)) { $manifestUrl = $DEFAULT_MANIFEST_URL }
    $script:MANIFEST_URL_DISPLAY = $manifestUrl

    Write-Info "Release manifest: $manifestUrl"
    $script:TMP_DIR = Join-Path $env:TEMP ("hackathonos-install-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $script:TMP_DIR -Force | Out-Null
    $manifestFile = Join-Path $script:TMP_DIR "manifest.json"

    Invoke-DownloadWithRetry -Uri $manifestUrl -Destination $manifestFile -TimeoutSec 120
    $script:MANIFEST_FILE = $manifestFile
    Write-Ok "Manifest downloaded"
}

function Select-Archive {
    $os = "windows"
    $archName = switch ((Get-WmiObject Win32_Processor -ErrorAction SilentlyContinue).Architecture) {
        6 { "amd64" } 9 { "amd64" } 11 { "arm64" } default { "amd64" }
    }
    $format = "zip"

    $latest = Parse-JsonField $script:MANIFEST_FILE 'param($d) $d.latest.version'
    if ([string]::IsNullOrWhiteSpace($latest)) {
        throw "Manifest does not declare a latest version."
    }
    if ([string]::IsNullOrWhiteSpace($Version)) { $Version = $env:HACKATHONOS_VERSION }
    if (-not [string]::IsNullOrWhiteSpace($Version)) {
        $script:INSTALL_VERSION = $Version
        if ($Version -ne $latest) { throw "This manifest only describes latest ($latest); version-pinned archives are not available." }
    } else {
        $script:INSTALL_VERSION = $latest
    }

    $archives = Parse-JsonField $script:MANIFEST_FILE 'param($d) $d.archives'
    $entry = $archives | Where-Object { $_.os -eq $os -and $_.arch -eq $archName -and $_.format -eq $format } | Select-Object -First 1
    if (-not $entry) {
        throw "No release archive for ${os}/${archName} (format $format)."
    }
    $script:ARCHIVE_URL = $entry.url
    $script:ARCHIVE_CHECKSUM = if ($entry.PSObject.Properties.Name -contains 'checksum') { $entry.checksum } else { "" }
    $script:ARCHIVE_NAME = $script:ARCHIVE_URL.Split("/")[-1]

    Write-Info "Version: $script:INSTALL_VERSION"
    Write-Info "Archive: $script:ARCHIVE_NAME"
}

function Assert-SafeZip {
    param([string] $Archive)
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $zip = [System.IO.Compression.ZipFile]::OpenRead($Archive)
    try {
        foreach ($entry in $zip.Entries) {
            $name = $entry.FullName.Replace('\', '/')
            if ($name.StartsWith('/') -or $name -match '^[A-Za-z]:' -or ($name.Split('/') -contains '..')) {
                throw "Archive contains unsafe path: $($entry.FullName)"
            }
            $unixMode = ($entry.ExternalAttributes -shr 16) -band 0xF000
            if ($unixMode -eq 0xA000) { throw "Archive contains unsupported symbolic link: $($entry.FullName)" }
        }
    } finally { $zip.Dispose() }
}

###############################################################################
# Download + verify
###############################################################################
function Download-And-Verify {
    Write-Info "URL: $script:ARCHIVE_URL"
    $archive = Join-Path $script:TMP_DIR $script:ARCHIVE_NAME
    Invoke-DownloadWithRetry -Uri $script:ARCHIVE_URL -Destination $archive -TimeoutSec 300
    Write-Ok "Download complete"

    if ([string]::IsNullOrWhiteSpace($script:ARCHIVE_CHECKSUM)) {
        throw "Release manifest has no SHA-256 checksum; refusing unverified installation."
    } else {
        $actual = Get-Sha256 $archive
        if ($actual -ne $script:ARCHIVE_CHECKSUM) {
            throw "SHA-256 mismatch for $($script:ARCHIVE_NAME): expected $($script:ARCHIVE_CHECKSUM), got $actual"
        }
        Write-Ok ("SHA-256 verified ({0})" -f $actual)
    }
    $script:ARCHIVE_FILE = $archive
}

###############################################################################
# Extract + validate + install
###############################################################################
function Validate-Archive {
    param([string] $Archive)
    $extractDir = Join-Path $script:TMP_DIR "extract"
    New-Item -ItemType Directory -Path $extractDir -Force | Out-Null

    # Inspect every ZIP entry before extraction; post-extraction checks are too late.
    Assert-SafeZip $Archive
    $entries = Expand-Archive -Path $Archive -DestinationPath $extractDir -Force -ErrorAction Stop
    # Expand-Archive extracts; now scan for unsafe paths already on disk.
    $unsafe = Get-ChildItem -Path $extractDir -Recurse -File |
        Where-Object { $_.FullName -match '\\\.\.' -or $_.FullName -match '^/' }
    if ($unsafe) {
        throw "Archive contains unsafe paths (path traversal)."
    }

    # Locate the skill tree root (single top-level wrapper or extract dir itself).
    $children = Get-ChildItem -Path $extractDir -Directory
    $source = $extractDir
    if ($children.Count -eq 1 -and (Test-Path (Join-Path $children[0].FullName "SKILL.md"))) {
        $source = $children[0].FullName
    }

    $required = @("SKILL.md", "commands\manifest.json", "core\commands\router.py")
    $problems = 0
    foreach ($req in $required) {
        if (-not (Test-Path (Join-Path $source $req))) {
            Write-Err "Missing in archive: $req"
            $problems++
        }
    }
    if (-not (Test-Path (Join-Path $source "workflows") -PathType Container)) {
        Write-Err "Missing in archive: workflows/"
        $problems++
    }
    if ($problems -gt 0) { throw "Archive failed validation." }
    Write-Ok "Archive validated"
    $script:EXTRACT_SOURCE = $source
}

function Backup-SkillDir {
    param([string] $TargetDir)
    if (-not (Test-Path $TargetDir)) { return }
    $stamp = Get-Date -Format "yyyyMMddHHmmss"
    $backup = "${TargetDir}.bak.${stamp}"
    Copy-Item -Path $TargetDir -Destination $backup -Recurse -Force
    Write-Ok ("Backed up {0} -> {1}" -f $TargetDir, $backup)
    $script:BACKUP_DIRS += @{ Backup = $backup; Target = $TargetDir }
}

function Rollback-Installs {
    Write-Info "Rolling back..."
    for ($i = $script:CREATED_DIRS.Count - 1; $i -ge 0; $i--) {
        $target = $script:CREATED_DIRS[$i]
        if (Test-Path $target) { Remove-Item -Path $target -Recurse -Force; Write-Ok ("Removed incomplete install {0}" -f $target) }
    }
    for ($i = $script:BACKUP_DIRS.Count - 1; $i -ge 0; $i--) {
        $entry = $script:BACKUP_DIRS[$i]
        $target = $entry.Target
        $backup = $entry.Backup
        if (Test-Path $target) { Remove-Item -Path $target -Recurse -Force }
        if (Test-Path $backup) { Move-Item -Path $backup -Destination $target; Write-Ok ("Restored {0}" -f $target) }
    }
    $script:CREATED_DIRS = @()
    $script:BACKUP_DIRS = @()
}

function Install-Skill {
    param([string] $TargetName)
    switch ($TargetName) {
        "claude"   { $targetDir = $CLAUDE_SKILL_DIR }
        "opencode" { $targetDir = $OPENCODE_SKILL_DIR }
        default    { throw "Unknown target: $TargetName" }
    }

    if (Test-Path $targetDir) {
        Backup-SkillDir $targetDir
    } else {
        $script:CREATED_DIRS += $targetDir
    }
    if (Test-Path $targetDir) { Remove-Item -Path $targetDir -Recurse -Force }
    New-Item -ItemType Directory -Path (Split-Path -Parent $targetDir) -Force | Out-Null
    Copy-Item -Path $script:EXTRACT_SOURCE -Destination $targetDir -Recurse -Force

    $required = @("SKILL.md", "commands\manifest.json", "core\commands\router.py")
    $problems = 0
    foreach ($req in $required) {
        if (-not (Test-Path (Join-Path $targetDir $req))) {
            Write-Err ("Missing after install: {0}" -f $req); $problems++
        }
    }
    if (-not (Test-Path (Join-Path $targetDir "workflows") -PathType Container)) {
        Write-Err "Missing after install: workflows/"; $problems++
    }
    if ($problems -gt 0) { Rollback-Installs; throw "Installed skill failed validation; rolled back." }
    Write-Ok ("{0} skill installed -> {1}" -f (Get-Culture).TextInfo.ToTitleCase($TargetName), $targetDir)
}

function Install-Cli {
    Write-Info ("Installing CLI -> {0}" -f $CLI_BIN_DIR)
    New-Item -ItemType Directory -Path $CLI_BIN_DIR -Force | Out-Null

    # Locate the CLI source next to this installer, or download from manifest.
    $scriptDir = $null
    if (-not [string]::IsNullOrWhiteSpace($PSCommandPath)) { $scriptDir = Split-Path -Parent $PSCommandPath }
    $cliSource = $null
    $cliBatSource = $null
    if ($scriptDir) {
        $cliSource = Join-Path $scriptDir "cli\hackathonos"
        $cliBatSource = Join-Path $scriptDir "cli\hackathonos.bat"
    }
    if (-not $cliSource -or -not (Test-Path $cliSource)) {
        $cliUrl = Parse-JsonField $script:MANIFEST_FILE 'param($d) $d.cli.url'
        $cliChecksum = Parse-JsonField $script:MANIFEST_FILE 'param($d) $d.cli.checksum'
        if ([string]::IsNullOrWhiteSpace($cliUrl) -or [string]::IsNullOrWhiteSpace($cliChecksum)) {
            throw "CLI not available with a URL and SHA-256 in this installer bundle."
        }
        $cliArchive = Join-Path $script:TMP_DIR "hackathonos-cli.zip"
        Invoke-DownloadWithRetry -Uri $cliUrl -Destination $cliArchive -TimeoutSec 120
        if ((Get-Sha256 $cliArchive) -ne $cliChecksum) { throw "CLI archive SHA-256 mismatch." }
        Assert-SafeZip $cliArchive
        $cliExtract = Join-Path $script:TMP_DIR "cli"
        Expand-Archive -Path $cliArchive -DestinationPath $cliExtract -Force -ErrorAction Stop
        $cliSource = Get-ChildItem -Path $cliExtract -Recurse -File | Where-Object { $_.Name -eq "hackathonos" } | Select-Object -First 1 -ExpandProperty FullName
        if (-not $cliSource) { throw "CLI archive is missing the hackathonos executable." }
        $cliBatSource = Get-ChildItem -Path $cliExtract -Recurse -File | Where-Object { $_.Name -eq "hackathonos.bat" } | Select-Object -First 1 -ExpandProperty FullName
    }

    Copy-Item -Path $cliSource -Destination (Join-Path $CLI_BIN_DIR $CLI_NAME) -Force
    if ($cliBatSource -and (Test-Path $cliBatSource)) { Copy-Item -Path $cliBatSource -Destination (Join-Path $CLI_BIN_DIR "$CLI_NAME.bat") -Force }
    Write-Ok "CLI installed"

    Ensure-Path
}

function Ensure-Path {
    if ($NoPath -or [string]::IsNullOrWhiteSpace($env:HACKATHONOS_NO_PATH) -eq $false -and $env:HACKATHONOS_NO_PATH -eq "1") {
        Write-Info "Skipping PATH modification (HACKATHONOS_NO_PATH=1)"
        return
    }
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    $separator = ";"
    $already = ($currentPath -split $separator) | Where-Object { $_ -eq $CLI_BIN_DIR }
    if ($already) {
        Write-Ok "CLI dir already on user PATH"
        return
    }
    $newPath = if ([string]::IsNullOrWhiteSpace($currentPath)) { $CLI_BIN_DIR } else { $currentPath + $separator + $CLI_BIN_DIR }
    try {
        [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
        Write-Ok ("Added {0} to user PATH" -f $CLI_BIN_DIR)
        Write-Info "Restart your shell or run: `$env:PATH = `"$newPath;${env:PATH}`""
    } catch {
        Write-Info "Add $CLI_BIN_DIR to your PATH manually."
    }
}

function Validate-Installation {
    $problems = 0
    foreach ($target in $script:TARGETS) {
        switch ($target) {
            "claude"   { $dir = $CLAUDE_SKILL_DIR }
            "opencode" { $dir = $OPENCODE_SKILL_DIR }
        }
        if (-not (Test-Path (Join-Path $dir "SKILL.md"))) { Write-Err ("SKILL.md missing in {0}" -f $dir); $problems++ }
        if (-not (Test-Path (Join-Path $dir "commands\manifest.json"))) { Write-Err ("Manifest missing in {0}" -f $dir); $problems++ }
        if (-not (Test-Path (Join-Path $dir "workflows") -PathType Container)) { Write-Err ("Workflows missing in {0}" -f $dir); $problems++ }
    }
    if (Test-Command $CLI_NAME) { Write-Ok "CLI available on PATH" }
    else { Write-Info ("CLI not on PATH (use {0}\{1})" -f $CLI_BIN_DIR, $CLI_NAME) }
    if ($problems -gt 0) { throw "Validation failed." }
    Write-Ok "Installation validated"
}

###############################################################################
# Output
###############################################################################
function Print-Banner {
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Cyan
    Write-Host "|          HACKATHONOS                 |" -ForegroundColor Cyan
    Write-Host "|       AI HACKATHON MENTOR             |" -ForegroundColor Cyan
    Write-Host "=========================================" -ForegroundColor Cyan
    Write-Host ""
}
function Print-Success {
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host "|  Installation completed successfully! |" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "HackathonOS is installed:"
    foreach ($target in $script:TARGETS) {
        switch ($target) {
            "claude"   { $dir = $CLAUDE_SKILL_DIR }
            "opencode" { $dir = $OPENCODE_SKILL_DIR }
        }
        Write-Host ("  * {0}: {1}" -f $target, $dir) -ForegroundColor Green
    }
    if (-not $NoCli) {
        Write-Host ("  * CLI: {0}\{1}" -f $CLI_BIN_DIR, $CLI_NAME) -ForegroundColor Green
    }
    Write-Host ""
    Write-Host "Try it in your AI coding agent:"
    Write-Host "  /hackathonos status"
    Write-Host "  /hackathonos next"
    Write-Host "  /hackathonos suggest"
    Write-Host ""
    Write-Host "CLI commands:"
    Write-Host "  hackathonos --version"
    Write-Host "  hackathonos update"
    Write-Host "  hackathonos doctor"
    Write-Host "  hackathonos uninstall"
    Write-Host ""
    Write-Host ("Release manifest: {0}" -f $script:MANIFEST_URL_DISPLAY)
    Write-Host "Docs: INSTALLATION.md README.md SECURITY.md"
    Write-Host ""
}

###############################################################################
# Argument handling
###############################################################################
# $NoCli, $NoPath, $Yes are already params.

###############################################################################
# Main
###############################################################################
Print-Banner

if (-not [string]::IsNullOrWhiteSpace($ProjectDir)) {
    throw "Project-level installer mode is not implemented; use the repository-local agent files."
}

if (-not (Test-Command python)) {
    throw "python is required but not installed."
}

Write-Step "Detecting environment"
Detect-Environment

Write-Step "Fetching latest release"
Fetch-Manifest
Select-Archive

Write-Step "Downloading package"
Download-And-Verify

Write-Step "Verifying integrity"
Validate-Archive $script:ARCHIVE_FILE

Write-Step "Installing skill"
foreach ($target in $script:TARGETS) {
    Install-Skill $target
}

if (-not $NoCli) {
    Install-Cli
}

Write-Step "Validating installation"
Validate-Installation

Print-Success
Cleanup
