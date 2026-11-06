# sherpa Installer - Windows PowerShell (5.1+ / 7+)
#
# Installs the sherpa AI Hackathon Mentor skill for Claude Code and
# OpenCode from a versioned GitHub Releases archive, verifies its SHA-256
# checksum, and installs the `sherpa` CLI.
#
# Usage:
#   irm https://YOUR-DOMAIN/install.ps1 | iex
#
# Configuration (environment variables, all optional):
#   $env:SHERPA_RELEASE_MANIFEST_URL   Release manifest JSON URL
#   $env:SHERPA_VERSION                Pin a specific version (default: latest)
#   $env:SHERPA_INSTALL_CLAUDE         1=install (default), 0=skip
#   $env:SHERPA_INSTALL_OPENCODE       1=install (default), 0=skip
#   $env:SHERPA_INSTALL_CLI            1=install (default), 0=skip
#   $env:SHERPA_NO_PATH                1=do not modify user PATH
#
# The installer never touches user project data or `.sherpa/` directories.

[CmdletBinding()]
param(
    [switch] $Claude,
    [switch] $OpenCode,
    [switch] $Codex,
    [switch] $Kilo,
    [switch] $Both,
    [string] $ProjectDir,
    [string] $Destination,
    [string] $Version,
    [string] $ManifestUrl,
    [switch] $NoCli,
    [switch] $NoPath,
    [switch] $Yes
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

$PROJECT = "sherpa"
$CLI_NAME = "sherpa"
$DEFAULT_MANIFEST_URL = "https://github.com/Anshkaliya18/sherpa/releases/latest/download/manifest.json"

$CLAUDE_SKILL_DIR = Join-Path $env:USERPROFILE ".claude\skills\sherpa"
$OPENCODE_SKILL_DIR = Join-Path $env:USERPROFILE ".config\opencode\skills\sherpa"
$CODEX_SKILL_DIR = Join-Path $env:USERPROFILE ".agents\skills\sherpa"
$KILO_SKILL_DIR = Join-Path $env:USERPROFILE ".agents\skills\sherpa"
$CLI_BIN_DIR = Join-Path $env:USERPROFILE "AppData\Local\sherpa\bin"

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
    if ($env:SHERPA_NPM_WRAPPER -eq '1') { exit 1 }
    if (-not $Yes) { try { Read-Host "Installation failed. Press Enter to return to PowerShell" | Out-Null } catch { } }
    return
}

function Test-Command {
    param([string] $Name)
    return (Get-Command $Name -ErrorAction SilentlyContinue) -ne $null
}

function Get-WindowsArchitecture {
    $runtimeInfoType = 'System.Runtime.InteropServices.RuntimeInformation' -as [type]
    if ($runtimeInfoType) {
        try {
            $runtimeArch = $runtimeInfoType::OSArchitecture
            if ($null -ne $runtimeArch) {
                switch ($runtimeArch.ToString().ToLowerInvariant()) {
                    'x64'   { return 'amd64' }
                    'arm64' { return 'arm64' }
                    'x86'   { return 'x86' }
                }
            }
        } catch {
            # Older Windows PowerShell/.NET combinations may expose the type
            # without a usable OSArchitecture property; use the environment
            # and WMI fallbacks below.
        }
    }

    $environmentArch = $env:PROCESSOR_ARCHITEW6432
    if ([string]::IsNullOrWhiteSpace($environmentArch)) { $environmentArch = $env:PROCESSOR_ARCHITECTURE }
    if (-not [string]::IsNullOrWhiteSpace($environmentArch)) {
        switch ($environmentArch.ToUpperInvariant()) {
            'AMD64' { return 'amd64' }
            'ARM64' { return 'arm64' }
            'X86'   { return 'x86' }
        }
    }

    # Win32_Processor reports 9 for x64 and 12 for ARM64.
    $wmiProcessor = Get-WmiObject Win32_Processor -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($null -ne $wmiProcessor) {
        $wmiArchitecture = $wmiProcessor.Architecture
        if ($wmiArchitecture -eq 12) { return 'arm64' }
    }
    return 'amd64'
}

function Copy-LocalSkillTree {
    param([string] $SourceDir, [string] $DestinationDir, [string] $RepositoryRoot)
    New-Item -ItemType Directory -Path $DestinationDir -Force | Out-Null
    foreach ($item in Get-ChildItem -LiteralPath $SourceDir -Force) {
        $relative = $item.FullName.Substring($RepositoryRoot.Length).TrimStart('\', '/')
        if ($relative -match '(^|[\\/])(\.git|\.sherpa|tests|__pycache__|\.pytest_cache)([\\/]|$)') { continue }
        if ($relative -match '(^|[\\/])\.vitepress[\\/](dist|cache)([\\/]|$)') { continue }
        if ($relative -match '(^|[\\/])(command-data|compatibility-data)\.generated\.json$') { continue }

        $destination = Join-Path $DestinationDir $item.Name
        if ($item.PSIsContainer) {
            Copy-LocalSkillTree $item.FullName $destination $RepositoryRoot
        } else {
            Copy-Item -LiteralPath $item.FullName -Destination $destination -Force
        }
    }
}

function Use-LocalCheckout {
    if ([string]::IsNullOrWhiteSpace($PSCommandPath)) { return $false }
    $distributionDir = Split-Path -Parent $PSCommandPath
    $repositoryRoot = Split-Path -Parent $distributionDir
    foreach ($required in @('SKILL.md', 'commands\manifest.json', 'workflows')) {
        if (-not (Test-Path (Join-Path $repositoryRoot $required))) { return $false }
    }

    $script:TMP_DIR = Join-Path $env:TEMP ("sherpa-install-" + [guid]::NewGuid().ToString("N"))
    $stage = Join-Path $script:TMP_DIR 'local-skill'
    New-Item -ItemType Directory -Path $stage -Force | Out-Null
    foreach ($name in @('SKILL.md', 'README.md', 'LICENSE', '.env.sherpa.example')) {
        $source = Join-Path $repositoryRoot $name
        if (Test-Path -LiteralPath $source -PathType Leaf) { Copy-Item -LiteralPath $source -Destination $stage -Force }
    }
    foreach ($name in @('commands', 'core', 'workflows', 'rules', 'templates', 'src', 'scripts', 'adapters', 'docs')) {
        $source = Join-Path $repositoryRoot $name
        if (Test-Path -LiteralPath $source -PathType Container) {
            Copy-LocalSkillTree $source (Join-Path $stage $name) $repositoryRoot
        }
    }
    $generated = Join-Path $repositoryRoot 'distribution\generated'
    if (Test-Path $generated) { Copy-LocalSkillTree $generated (Join-Path $stage 'distribution\generated') $repositoryRoot }
    $cliSource = Join-Path $repositoryRoot 'distribution\cli'
    if (Test-Path $cliSource) {
        $cliDest = Join-Path $stage 'distribution\cli'
        New-Item -ItemType Directory -Path $cliDest -Force | Out-Null
        foreach ($file in @('sherpa', 'installer.py')) {
            $source = Join-Path $cliSource $file
            if (Test-Path $source) { Copy-Item -LiteralPath $source -Destination $cliDest -Force }
        }
    }
    $script:EXTRACT_SOURCE = $stage
    $script:INSTALL_VERSION = (Get-Content -LiteralPath (Join-Path $distributionDir 'VERSION') -Raw).Trim()
    $script:MANIFEST_URL_DISPLAY = "local checkout ($script:INSTALL_VERSION)"
    return $true
}

function Invoke-DownloadWithRetry {
    param([string] $Uri, [string] $Destination, [int] $TimeoutSec)
    for ($attempt = 0; $attempt -lt 3; $attempt++) {
        try {
            # Use basic parsing so Windows PowerShell 5.1 works on headless
            # machines without an initialized Internet Explorer engine.
            Invoke-WebRequest -UseBasicParsing -Uri $Uri -OutFile $Destination -TimeoutSec $TimeoutSec -ErrorAction Stop | Out-Null
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
        $tmp = Join-Path $env:TEMP "sherpa-sha256-$([guid]::NewGuid()).txt"
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
    $archName = Get-WindowsArchitecture
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

    $script:INSTALL_CLAUDE = [bool]($env:SHERPA_INSTALL_CLAUDE -ne "0")
    $script:INSTALL_OPENCODE = [bool]($env:SHERPA_INSTALL_OPENCODE -ne "0")
    $script:INSTALL_CODEX = [bool]($env:SHERPA_INSTALL_CODEX -eq "1")
    $script:INSTALL_KILO = [bool]($env:SHERPA_INSTALL_KILO -eq "1")
    $script:INSTALL_CLI = [bool]($env:SHERPA_INSTALL_CLI -ne "0")
    if ($NoCli) { $script:INSTALL_CLI = $false }
    if ($Claude) { $script:INSTALL_CLAUDE = $true; $script:INSTALL_OPENCODE = $false }
    if ($OpenCode) { $script:INSTALL_OPENCODE = $true; $script:INSTALL_CLAUDE = $false }
    if ($Codex -or $Kilo) { $script:INSTALL_CLAUDE = $false; $script:INSTALL_OPENCODE = $false }
    if ($Both) { $script:INSTALL_CLAUDE = $true; $script:INSTALL_OPENCODE = $true }
    if ($Codex) { $script:INSTALL_CODEX = $true }
    if ($Kilo) { $script:INSTALL_KILO = $true }

    $script:TARGETS = New-Object System.Collections.Generic.List[string]
    if ($script:INSTALL_CLAUDE) { $script:TARGETS.Add("claude") }
    if ($script:INSTALL_OPENCODE) { $script:TARGETS.Add("opencode") }
    if ($script:INSTALL_CODEX) { $script:TARGETS.Add("codex") }
    if ($script:INSTALL_KILO) { $script:TARGETS.Add("kilo") }
    if ($script:TARGETS.Count -eq 0) {
        throw "No target environments selected."
    }
}

###############################################################################
# Fetch manifest
###############################################################################
function Fetch-Manifest {
    $manifestUrl = $ManifestUrl
    if ([string]::IsNullOrWhiteSpace($manifestUrl)) { $manifestUrl = $env:SHERPA_RELEASE_MANIFEST_URL }
    if ([string]::IsNullOrWhiteSpace($manifestUrl)) { $manifestUrl = $DEFAULT_MANIFEST_URL }
    $script:MANIFEST_URL_DISPLAY = $manifestUrl

    Write-Info "Release manifest: $manifestUrl"
    $script:TMP_DIR = Join-Path $env:TEMP ("sherpa-install-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $script:TMP_DIR -Force | Out-Null
    $manifestFile = Join-Path $script:TMP_DIR "manifest.json"

    Invoke-DownloadWithRetry -Uri $manifestUrl -Destination $manifestFile -TimeoutSec 120
    $script:MANIFEST_FILE = $manifestFile
    Write-Ok "Manifest downloaded"
}

function Select-Archive {
    $os = "windows"
    $archName = Get-WindowsArchitecture
    $format = "zip"

    $latest = Parse-JsonField $script:MANIFEST_FILE 'param($d) $d.latest.version'
    if ([string]::IsNullOrWhiteSpace($latest)) {
        throw "Manifest does not declare a latest version."
    }
    $project = Parse-JsonField $script:MANIFEST_FILE 'param($d) $d.project'
    if ($project -ne 'Sherpa' -or [version]$latest -lt [version]'2.0.0') {
        throw "The configured release manifest is for '$project' version '$latest', not Sherpa 2.0.0 or newer. Publish the Sherpa release before using the online installer, or run distribution\install.ps1 from a Sherpa checkout."
    }
    if ([string]::IsNullOrWhiteSpace($Version)) { $Version = $env:SHERPA_VERSION }
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
    $engine = Join-Path $script:EXTRACT_SOURCE 'distribution\cli\sherpa'
    if (Test-Path $engine) {
        $python = if (Test-Command python) { 'python' } elseif (Test-Command py) { 'py' } else { throw 'Python 3 is required by the transactional installer.' }
        $pythonPrefix = if ($python -eq 'py') { @('-3') } else { @() }
        $scope = if ([string]::IsNullOrWhiteSpace($ProjectDir)) { 'global' } else { 'project' }
        $installArgs = @($engine, 'install', '--client', $TargetName, '--scope', $scope, '--yes')
        if ($scope -eq 'project') { $installArgs += @('--project-dir', $ProjectDir) }
        if (-not [string]::IsNullOrWhiteSpace($Destination)) { $installArgs += @('--destination', $Destination) }
        & $python @pythonPrefix @installArgs
        if ($LASTEXITCODE -ne 0) { throw ("{0} client installation failed with exit code {1}." -f $TargetName, $LASTEXITCODE) }
        return
    }
    switch ($TargetName) {
        "claude"   { $targetDir = $CLAUDE_SKILL_DIR }
        "opencode" { $targetDir = $OPENCODE_SKILL_DIR }
        "codex"    { $targetDir = $CODEX_SKILL_DIR }
        "kilo"     { $targetDir = $KILO_SKILL_DIR }
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
        $cliSource = Join-Path $scriptDir "cli\sherpa"
        $cliBatSource = Join-Path $scriptDir "cli\sherpa.bat"
    }
    if (-not $cliSource -or -not (Test-Path $cliSource)) {
        $cliUrl = Parse-JsonField $script:MANIFEST_FILE 'param($d) $d.cli.url'
        $cliChecksum = Parse-JsonField $script:MANIFEST_FILE 'param($d) $d.cli.checksum'
        if ([string]::IsNullOrWhiteSpace($cliUrl) -or [string]::IsNullOrWhiteSpace($cliChecksum)) {
            throw "CLI not available with a URL and SHA-256 in this installer bundle."
        }
        $cliArchive = Join-Path $script:TMP_DIR "sherpa-cli.zip"
        Invoke-DownloadWithRetry -Uri $cliUrl -Destination $cliArchive -TimeoutSec 120
        if ((Get-Sha256 $cliArchive) -ne $cliChecksum) { throw "CLI archive SHA-256 mismatch." }
        Assert-SafeZip $cliArchive
        $cliExtract = Join-Path $script:TMP_DIR "cli"
        Expand-Archive -Path $cliArchive -DestinationPath $cliExtract -Force -ErrorAction Stop
        $cliSource = Get-ChildItem -Path $cliExtract -Recurse -File | Where-Object { $_.Name -eq "sherpa" } | Select-Object -First 1 -ExpandProperty FullName
        if (-not $cliSource) { throw "CLI archive is missing the sherpa executable." }
        $cliBatSource = Get-ChildItem -Path $cliExtract -Recurse -File | Where-Object { $_.Name -eq "sherpa.bat" } | Select-Object -First 1 -ExpandProperty FullName
    }

    Copy-Item -Path $cliSource -Destination (Join-Path $CLI_BIN_DIR $CLI_NAME) -Force
    if ($cliBatSource -and (Test-Path $cliBatSource)) { Copy-Item -Path $cliBatSource -Destination (Join-Path $CLI_BIN_DIR "$CLI_NAME.bat") -Force }
    Write-Ok "CLI installed"

    Ensure-Path
}

function Ensure-Path {
    if ($NoPath -or [string]::IsNullOrWhiteSpace($env:SHERPA_NO_PATH) -eq $false -and $env:SHERPA_NO_PATH -eq "1") {
        Write-Info "Skipping PATH modification (SHERPA_NO_PATH=1)"
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
    $engine = Join-Path $script:EXTRACT_SOURCE 'distribution\cli\sherpa'
    if (Test-Path $engine) {
        $python = if (Test-Command python) { 'python' } elseif (Test-Command py) { 'py' } else { throw 'Python 3 is required for installation verification.' }
        $prefix = if ($python -eq 'py') { @('-3') } else { @() }
        $scope = if ([string]::IsNullOrWhiteSpace($ProjectDir)) { 'global' } else { 'project' }
        foreach ($target in $script:TARGETS) {
            $verifyArgs = @($engine, 'verify-install', '--client', $target, '--scope', $scope)
            if ($scope -eq 'project') { $verifyArgs += @('--project-dir', $ProjectDir) }
            if (-not [string]::IsNullOrWhiteSpace($Destination)) { $verifyArgs += @('--destination', $Destination) }
            & $python @prefix @verifyArgs
            if ($LASTEXITCODE -ne 0) { throw ("{0} post-install verification failed." -f $target) }
        }
        return
    }
    $problems = 0
    foreach ($target in $script:TARGETS) {
        switch ($target) {
            "claude"   { $dir = $CLAUDE_SKILL_DIR }
            "opencode" { $dir = $OPENCODE_SKILL_DIR }
            "codex"    { $dir = $CODEX_SKILL_DIR }
            "kilo"     { $dir = $KILO_SKILL_DIR }
        }
        if (-not [string]::IsNullOrWhiteSpace($Destination)) { $dir = Join-Path $Destination 'skills\sherpa' }
        if (-not [string]::IsNullOrWhiteSpace($ProjectDir) -and [string]::IsNullOrWhiteSpace($Destination)) {
            $folder = switch ($target) { 'claude' { '.claude' } 'opencode' { '.opencode' } default { '.agents' } }
            $dir = Join-Path $ProjectDir (Join-Path $folder 'skills\sherpa')
        }
        if (-not (Test-Path (Join-Path $dir "SKILL.md"))) { Write-Err ("SKILL.md missing in {0}" -f $dir); $problems++ }
        if (-not (Test-Path (Join-Path $dir "commands\manifest.json"))) { Write-Err ("Manifest missing in {0}" -f $dir); $problems++ }
        if (-not (Test-Path (Join-Path $dir "workflows") -PathType Container)) { Write-Err ("Workflows missing in {0}" -f $dir); $problems++ }
    }
    if ($script:INSTALL_CLI) {
        if (Test-Command $CLI_NAME) { Write-Ok "CLI available on PATH" }
        else { Write-Info ("CLI not on PATH (use {0}\{1})" -f $CLI_BIN_DIR, $CLI_NAME) }
    } else {
        Write-Info "Optional Python CLI installation was skipped."
    }
    if ($problems -gt 0) { throw "Validation failed." }
    Write-Ok "Installation validated"
}

###############################################################################
# Output
###############################################################################
function Print-Banner {
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Cyan
    Write-Host "|          sherpa                 |" -ForegroundColor Cyan
    Write-Host "|       AI HACKATHON MENTOR             |" -ForegroundColor Cyan
    Write-Host "=========================================" -ForegroundColor Cyan
    Write-Host ""
}
function Print-Success {
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host "|  Installation files validated          |" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "sherpa is installed:"
    foreach ($target in $script:TARGETS) {
        switch ($target) {
            "claude"   { $dir = $CLAUDE_SKILL_DIR }
            "opencode" { $dir = $OPENCODE_SKILL_DIR }
            "codex"    { $dir = $CODEX_SKILL_DIR }
            "kilo"     { $dir = $KILO_SKILL_DIR }
        }
        if (-not [string]::IsNullOrWhiteSpace($Destination)) { $dir = Join-Path $Destination 'skills\sherpa' }
        if (-not [string]::IsNullOrWhiteSpace($ProjectDir) -and [string]::IsNullOrWhiteSpace($Destination)) {
            $folder = switch ($target) { 'claude' { '.claude' } 'opencode' { '.opencode' } default { '.agents' } }
            $dir = Join-Path $ProjectDir (Join-Path $folder 'skills\sherpa')
        }
        Write-Host ("  * {0}: {1}" -f $target, $dir) -ForegroundColor Green
    }
    if ($script:INSTALL_CLI) {
        Write-Host ("  * CLI: {0}\{1}" -f $CLI_BIN_DIR, $CLI_NAME) -ForegroundColor Green
    }
    Write-Host ""
    Write-Host "Client discovery and runtime execution are NOT VERIFIED by file installation."
    Write-Host "Try the skill in your AI coding agent after restarting or reloading it:"
    Write-Host "  Invoke the installed Sherpa skill by name and include the desired operation."
    Write-Host ""
    if ($script:INSTALL_CLI) {
        Write-Host "CLI commands:"
        Write-Host "  sherpa --version"
        Write-Host "  sherpa update"
        Write-Host "  sherpa doctor"
        Write-Host "  sherpa uninstall"
        Write-Host ""
    }
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
    if (-not (Test-Path -LiteralPath $ProjectDir -PathType Container)) { throw "Project directory does not exist: $ProjectDir" }
}
if (-not [string]::IsNullOrWhiteSpace($Destination) -and $script:TARGETS.Count -ne 1) { throw "-Destination requires exactly one selected client." }

$usingLocalCheckout = Use-LocalCheckout
if ($usingLocalCheckout) { $script:STEP_TOTAL = 4 }

Write-Step "Detecting environment"
Detect-Environment

if ($script:INSTALL_CLI -and -not (Test-Command python) -and -not (Test-Command py)) {
    throw "Python 3 is required for the optional sherpa CLI. Install Python 3 or set SHERPA_INSTALL_CLI=0 to install the agent skill only."
}

if ($usingLocalCheckout) {
    Write-Step "Preparing local Sherpa checkout"
    Write-Ok "Using validated source files from the current checkout"
} else {
    Write-Step "Fetching latest Sherpa release"
    Fetch-Manifest
    Select-Archive

    Write-Step "Downloading package"
    Download-And-Verify

    Write-Step "Verifying integrity"
    Validate-Archive $script:ARCHIVE_FILE
}

Write-Step "Installing skill"
foreach ($target in $script:TARGETS) {
    Install-Skill $target
}

if ($script:INSTALL_CLI) {
    Install-Cli
}

Write-Step "Validating installation"
Validate-Installation

Print-Success
Cleanup
if (-not $Yes) { Read-Host "Installation complete. Press Enter to return to PowerShell" | Out-Null }
