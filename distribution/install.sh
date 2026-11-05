#!/usr/bin/env bash
#
# sherpa Installer — Linux / macOS / Git Bash
#
# Installs the sherpa AI Hackathon Mentor skill for Claude Code and
# OpenCode from a versioned GitHub Releases archive, verifies its SHA-256
# checksum, and installs the `sherpa` CLI.
#
# Usage:
#   curl -fsSL https://YOUR-DOMAIN/install.sh | bash
#
# Configuration (environment variables, all optional):
#   SHERPA_RELEASE_MANIFEST_URL   Release manifest JSON URL
#                                      (default: GitHub Releases latest)
#   SHERPA_INSTALL_CLAUDE         Install into Claude Code (1) or skip (0)
#   SHERPA_INSTALL_OPENCODE       Install into OpenCode   (1) or skip (0)
#   SHERPA_INSTALL_CLI            Install the CLI (1) or skip (0)
#   SHERPA_VERSION                Pin a specific version (default: latest)
#   SHERPA_NO_PATH                Do not modify shell profile PATH
#
# The installer never touches user project data or `.sherpa/` directories.

set -euo pipefail

###############################################################################
# Constants
###############################################################################
PROJECT="sherpa"
CLI_NAME="sherpa"
DEFAULT_MANIFEST_URL="https://github.com/Anshkaliya18/sherpa/releases/latest/download/manifest.json"

CLAUDE_SKILL_DIR="${HOME}/.claude/skills/sherpa"
OPENCODE_SKILL_DIR="${HOME}/.config/opencode/skills/sherpa"
CLI_BIN_DIR="${HOME}/.local/bin"

STEP=0
STEP_TOTAL=6
TMP_DIR=""
BACKUP_DIRS=()
SHERPA_INSTALL_CLAUDE="${SHERPA_INSTALL_CLAUDE:-1}"
SHERPA_INSTALL_OPENCODE="${SHERPA_INSTALL_OPENCODE:-1}"
SHERPA_INSTALL_CLI="${SHERPA_INSTALL_CLI:-1}"
SHERPA_NO_PATH="${SHERPA_NO_PATH:-0}"

###############################################################################
# Helpers
###############################################################################
err() { printf '  ✗ %s\n' "$*" >&2; }
ok()  { printf '  ✓ %s\n' "$*"; }
info(){ printf '  > %s\n' "$*"; }
step(){ STEP=$((STEP+1)); printf '\n[%d/%d] %s\n' "$STEP" "$STEP_TOTAL" "$*"; }

die() {
    err "$*"
    cleanup
    exit 1
}

cleanup() {
    if [[ -n "${TMP_DIR:-}" && -d "$TMP_DIR" ]]; then
        rm -rf "$TMP_DIR"
    fi
}
trap cleanup EXIT

# Detect the operating system.
detect_os() {
    local os
    os="$(uname -s | tr '[:upper:]' '[:lower:]')"
    case "$os" in
        linux*)   echo "linux" ;;
        darwin*)  echo "darwin" ;;
        cygwin*|mingw*|msys*) echo "windows" ;;  # Git Bash on Windows
        *)        echo "unknown" ;;
    esac
}

# Detect the CPU architecture.
detect_arch() {
    local arch
    arch="$(uname -m | tr '[:upper:]' '[:lower:]')"
    case "$arch" in
        x86_64|amd64) echo "amd64" ;;
        arm64|aarch64) echo "arm64" ;;
        *) echo "unknown" ;;
    esac
}

# sha256 of a file (portable: sha256sum / shasum / openssl).
sha256_of() {
    local file="$1"
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$file" | awk '{print $1}'
    elif command -v shasum >/dev/null 2>&1; then
        shasum -a 256 "$file" | awk '{print $1}'
    elif command -v openssl >/dev/null 2>&1; then
        openssl dgst -sha256 "$file" | awk '{print $NF}'
    else
        die "no SHA-256 tool available (sha256sum/shasum/openssl)"
    fi
}

# Extract a JSON scalar from the manifest using python3 (stdlib json).
manifest_field() {
    local manifest_file="$1"
    local python_expr="$2"
    "$PYTHON3" - "$manifest_file" "$python_expr" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as fh:
    data = json.load(fh)
print(json.dumps(eval(sys.argv[2], {"data": data})))
PY
}

# Check whether a command-line tool exists.
have() { command -v "$1" >/dev/null 2>&1; }

# Locate a real Python 3 interpreter. On Git Bash for Windows, `python3` may
# resolve to the Microsoft Store stub, so probe common install locations too.
find_python3() {
    # If `python3` resolves to a Windows Apps store stub, skip it (it can
    # launch the Store instead of running Python).
    local py3_path
    py3_path="$(command -v python3 2>/dev/null || true)"
    if [[ -n "$py3_path" && "$py3_path" != *"WindowsApps"* ]]; then
        if python3 -c "import json" >/dev/null 2>&1; then
            echo "python3"; return 0
        fi
    fi
    # Standard Windows Python installations (probe one path per line to handle
    # spaces in "Program Files"). Validate with a real stdlib import so broken
    # embedded Pythons (e.g. MySQL Workbench) are rejected.
    local roots=("/c/Program Files" "/c/Program Files (x86)")
    local root dir match
    for root in "${roots[@]}"; do
        while IFS= read -r dir; do
            for match in "$dir/python.exe" "$dir/python3.exe"; do
                if [[ -f "$match" ]] && "$match" -c "import json" >/dev/null 2>&1; then
                    echo "$match"; return 0
                fi
            done
        done < <(find "$root" -maxdepth 3 -type d -name 'Python3*' 2>/dev/null)
    done
    return 1
}

PYTHON3="$(find_python3 || true)"
if [[ -z "${PYTHON3:-}" ]]; then
    die "python3 is required but not installed"
fi

###############################################################################
# Environment detection
###############################################################################
detect_environments() {
    info "Operating system: $(detect_os)"
    info "Architecture: $(detect_arch)"
    info "Python: $("$PYTHON3" --version 2>/dev/null || echo 'not found')"

    local claude=0 opencode=0
    if [[ -f "${CLAUDE_SKILL_DIR}/SKILL.md" ]]; then
        ok "Claude Code skill detected (${CLAUDE_SKILL_DIR})"
        claude=1
    else
        info "Claude Code skill not installed"
    fi
    if [[ -f "${OPENCODE_SKILL_DIR}/SKILL.md" ]]; then
        ok "OpenCode skill detected (${OPENCODE_SKILL_DIR})"
        opencode=1
    else
        info "OpenCode skill not installed"
    fi

    # Decide targets.
    INSTALL_CLAUDE="${SHERPA_INSTALL_CLAUDE:-1}"
    INSTALL_OPENCODE="${SHERPA_INSTALL_OPENCODE:-1}"
    if [[ "$INSTALL_CLAUDE" == "1" ]]; then TARGETS+=("claude"); fi
    if [[ "$INSTALL_OPENCODE" == "1" ]]; then TARGETS+=("opencode"); fi
    if [[ ${#TARGETS[@]} -eq 0 ]]; then
        die "no target environments selected"
    fi
}

###############################################################################
# Fetch manifest
###############################################################################
fetch_manifest() {
    local manifest_url="${SHERPA_RELEASE_MANIFEST_URL:-$DEFAULT_MANIFEST_URL}"
    info "Release manifest: $manifest_url"
    TMP_DIR="$(mktemp -d)"
    local manifest_file="${TMP_DIR}/manifest.json"
    if ! curl -fsSL --retry 2 --retry-all-errors --connect-timeout 20 --max-time 120 -o "$manifest_file" "$manifest_url"; then
        die "failed to download release manifest from $manifest_url"
    fi
    MANIFEST_FILE="$manifest_file"
    ok "manifest downloaded"
}

# Select the archive entry matching OS/arch and optional pinned version.
select_archive() {
    local os arch version
    os="$(detect_os)"
    arch="$(detect_arch)"
    version="${SHERPA_VERSION:-}"

    # Extract latest version from manifest.
    local latest
    latest="$(manifest_field "$MANIFEST_FILE" "data['latest'].get('version','')")"
    if [[ -z "$latest" ]]; then
        die "manifest does not declare a latest version"
    fi
    local project major
    project="$(manifest_field "$MANIFEST_FILE" "data.get('project','')")"
    major="${latest%%.*}"
    if [[ "$project" != "Sherpa" && "$project" != "sherpa" || ! "$major" =~ ^[0-9]+$ || "$major" -lt 2 ]]; then
        die "release manifest is for '$project' version '$latest', not Sherpa 2.0.0 or newer; publish the Sherpa release first"
    fi
    if [[ -n "$version" && "$version" != "$latest" ]]; then
        die "this manifest only describes latest ($latest); version-pinned archives are not available"
    else
        version="$latest"
    fi
    INSTALL_VERSION="$version"

    # Choose archive format by OS.
    local fmt="tar.gz"
    if [[ "$os" == "windows" ]]; then fmt="zip"; fi

    local entry
    entry="$(manifest_field "$MANIFEST_FILE" "\
[e for e in data.get('archives',[]) if e.get('os')=='$os' and e.get('arch')=='$arch' and e.get('format')=='$fmt']\
")"
    if [[ -z "$entry" || "$entry" == "[]" ]]; then
        die "no release archive for ${os}/${arch} (format $fmt)"
    fi

    ARCHIVE_URL="$(printf '%s' "$entry" | "$PYTHON3" -c "import json,sys; print(json.load(sys.stdin)[0]['url'])")"
    ARCHIVE_CHECKSUM="$(printf '%s' "$entry" | "$PYTHON3" -c "import json,sys; print(json.load(sys.stdin)[0].get('checksum',''))")"
    ARCHIVE_NAME="${ARCHIVE_URL##*/}"

    if [[ -z "$ARCHIVE_URL" ]]; then
        die "archive entry missing download URL"
    fi

    info "Version: $INSTALL_VERSION"
    info "Archive: $ARCHIVE_NAME"
}

###############################################################################
# Download + verify
###############################################################################
download_and_verify() {
    info "URL: $ARCHIVE_URL"
    local archive="${TMP_DIR}/${ARCHIVE_NAME}"
    if ! curl -fsSL --retry 2 --retry-all-errors --connect-timeout 20 --max-time 300 -o "$archive" "$ARCHIVE_URL"; then
        die "failed to download $ARCHIVE_NAME"
    fi
    ok "download complete"

    if [[ -z "$ARCHIVE_CHECKSUM" ]]; then
        die "release manifest has no SHA-256 checksum; refusing unverified installation"
    else
        local actual expected
        actual="$(sha256_of "$archive")"
        expected="$ARCHIVE_CHECKSUM"
        if [[ "${actual,,}" != "${expected,,}" ]]; then
            die "SHA-256 mismatch for $ARCHIVE_NAME: expected $expected, got $actual"
        fi
        ok "SHA-256 verified ($actual)"
    fi
    ARCHIVE_FILE="$archive"
}

###############################################################################
# Extract + validate + install
###############################################################################
validate_archive_contents() {
    local archive="$1"
    local extract_dir="${TMP_DIR}/extract"
    mkdir -p "$extract_dir"

    local name
    name="$(basename "$archive")"
    if [[ "$name" == *.tar.gz || "$name" == *.tgz ]]; then
        # Path-traversal guard: reject members with '..' or absolute paths.
        if ! tar -tf "$archive" | grep -qE '^(\./)?[^/]' ; then
            :
        fi
        if tar -tf "$archive" | grep -qE '(\.\./|^/)' ; then
            die "archive contains unsafe paths (path traversal)"
        fi
        tar -xzf "$archive" -C "$extract_dir"
    elif [[ "$name" == *.zip ]]; then
        if unzip -l "$archive" >/dev/null 2>&1 && unzip -l "$archive" | grep -qE '(\.\./|^/)'; then
            die "archive contains unsafe paths (path traversal)"
        fi
        unzip -oq "$archive" -d "$extract_dir" >/dev/null
    else
        die "unsupported archive format: $name"
    fi

    # The archive may wrap content in a single top-level directory.
    local source="$extract_dir"
    local candidates
    candidates="$(find "$extract_dir" -mindepth 1 -maxdepth 1 -type d)"
    local count
    count="$(printf '%s\n' "$candidates" | grep -c . || true)"
    if [[ "$count" -eq 1 ]]; then
        local only
        only="$(printf '%s\n' "$candidates")"
        if [[ -f "${only}/SKILL.md" ]]; then
            source="$only"
        fi
    fi

    # Validate the skill tree.
    local problems=0
    for entry in SKILL.md commands/manifest.json core/commands/router.py; do
        if [[ ! -e "${source}/${entry}" ]]; then
            err "missing in archive: ${entry}"
            problems=$((problems+1))
        fi
    done
    if [[ ! -d "${source}/workflows" ]]; then
        err "missing in archive: workflows/"
        problems=$((problems+1))
    fi
    if [[ "$problems" -gt 0 ]]; then
        die "archive failed validation"
    fi
    ok "archive validated"

    EXTRACT_SOURCE="$source"
}

backup_skill_dir() {
    local target_dir="$1"
    if [[ ! -e "$target_dir" ]]; then return 0; fi
    local stamp
    stamp="$(date +%Y%m%d%H%M%S)"
    local backup="${target_dir}.bak.${stamp}"
    cp -a "$target_dir" "$backup"
    ok "backed up $target_dir -> $backup"
    BACKUP_DIRS+=("$backup:$target_dir")
}

install_skill() {
    local target_name="$1"
    local target_dir
    case "$target_name" in
        claude)   target_dir="$CLAUDE_SKILL_DIR" ;;
        opencode) target_dir="$OPENCODE_SKILL_DIR" ;;
        *)        die "unknown target: $target_name" ;;
    esac

    backup_skill_dir "$target_dir"

    if [[ -e "$target_dir" ]]; then
        rm -rf "$target_dir"
    fi
    mkdir -p "$(dirname "$target_dir")"
    cp -a "$EXTRACT_SOURCE" "$target_dir"

    # Validate after install.
    local problems=0
    for entry in SKILL.md commands/manifest.json core/commands/router.py; do
        if [[ ! -e "${target_dir}/${entry}" ]]; then
            err "missing after install: ${entry}"
            problems=$((problems+1))
        fi
    done
    if [[ ! -d "${target_dir}/workflows" ]]; then
        err "missing after install: workflows/"
        problems=$((problems+1))
    fi
    if [[ "$problems" -gt 0 ]]; then
        rollback_installs
        die "installed skill failed validation; rolled back"
    fi
    ok "${target_name^} skill installed -> $target_dir"
}

rollback_installs() {
    info "Rolling back..."
    local entry target backup
    # Process in reverse order.
    for ((i=${#BACKUP_DIRS[@]}-1; i>=0; i--)); do
        entry="${BACKUP_DIRS[$i]}"
        backup="${entry%%:*}"
        target="${entry##*:}"
        if [[ -e "$target" ]]; then rm -rf "$target"; fi
        if [[ -e "$backup" ]]; then mv "$backup" "$target"; ok "restored $target"; fi
    done
}

install_cli() {
    info "Installing CLI -> $CLI_BIN_DIR"
    mkdir -p "$CLI_BIN_DIR"
    # The CLI ships alongside this installer in the release; copy it.
    local cli_source
    cli_source="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)/cli/sherpa"
    if [[ ! -f "$cli_source" ]]; then
        # Installer was piped via curl: fetch CLI from the manifest cli url.
        local cli_archive="${TMP_DIR}/sherpa-cli.zip"
        local cli_url
        cli_url="$(manifest_field "$MANIFEST_FILE" "data.get('cli',{}).get('url','')")"
        local cli_checksum
        cli_checksum="$(manifest_field "$MANIFEST_FILE" "data.get('cli',{}).get('checksum','')")"
        if [[ -n "$cli_url" && -n "$cli_checksum" ]]; then
            curl -fsSL --retry 2 --retry-all-errors --connect-timeout 20 --max-time 120 -o "$cli_archive" "$cli_url" \
                || die "failed to download CLI"
            [[ "$(sha256_of "$cli_archive")" == "${cli_checksum,,}" ]] || die "CLI archive SHA-256 mismatch"
            local cli_extract="${TMP_DIR}/cli"
            mkdir -p "$cli_extract"
            unzip -oq "$cli_archive" -d "$cli_extract" || die "invalid CLI archive"
            cli_source="$(find "$cli_extract" -type f -name sherpa -print -quit)"
            [[ -n "$cli_source" ]] || die "CLI archive missing sherpa executable"
            local bat_source
            bat_source="$(find "$cli_extract" -type f -name sherpa.bat -print -quit)"
            [[ -z "$bat_source" ]] || cp "$bat_source" "$CLI_BIN_DIR/$CLI_NAME.bat"
        else
            die "CLI not available with a URL and SHA-256 in this installer bundle"
        fi
    fi
    cp -f "$cli_source" "$CLI_BIN_DIR/$CLI_NAME"
    chmod +x "$CLI_BIN_DIR/$CLI_NAME"
    ok "CLI installed"

    ensure_path
}

ensure_path() {
    if [[ "${SHERPA_NO_PATH:-0}" == "1" ]]; then
        info "Skipping PATH modification (SHERPA_NO_PATH=1)"
        return
    fi
    if [[ ":$PATH:" == *":${CLI_BIN_DIR}:"* ]]; then
        ok "CLI dir already on PATH"
        return
    fi
    local profile
    profile=""
    if [[ -n "${ZSH_VERSION:-}" || -f "${HOME}/.zshrc" ]]; then profile="${HOME}/.zshrc"; elif [[ -f "${HOME}/.bashrc" ]]; then profile="${HOME}/.bashrc"; fi
    if [[ -z "$profile" ]]; then
        info "Add $CLI_BIN_DIR to your PATH manually"
        return
    fi
    if ! grep -q "sherpa PATH" "$profile" 2>/dev/null; then
        {
            echo ''
            echo '# sherpa CLI'
            echo "export PATH=\"\${PATH}:${CLI_BIN_DIR}\""
        } >> "$profile"
        ok "Added $CLI_BIN_DIR to PATH in $profile"
    else
        ok "PATH entry already present in $profile"
    fi
    info "Reload your shell or run: export PATH=\"\${PATH}:${CLI_BIN_DIR}\""
}

###############################################################################
# Validation
###############################################################################
validate_installation() {
    local problems=0
    for target in "${TARGETS[@]}"; do
        local dir
        case "$target" in claude) dir="$CLAUDE_SKILL_DIR" ;; opencode) dir="$OPENCODE_SKILL_DIR" ;; esac
        if [[ ! -f "${dir}/SKILL.md" ]]; then err "SKILL.md missing in $dir"; problems=$((problems+1)); fi
        if [[ ! -f "${dir}/commands/manifest.json" ]]; then err "manifest missing in $dir"; problems=$((problems+1)); fi
        if [[ ! -d "${dir}/workflows" ]]; then err "workflows missing in $dir"; problems=$((problems+1)); fi
    done
    if have "$CLI_NAME"; then ok "CLI available on PATH"; else info "CLI not on PATH (use $CLI_BIN_DIR/$CLI_NAME)"; fi
    if [[ "$problems" -gt 0 ]]; then die "validation failed"; fi
    ok "Installation validated"
}

print_banner() {
    printf '\n'
    printf '╔═══════════════════════════════════════╗\n'
    printf '║          sherpa                 ║\n'
    printf '║       AI HACKATHON MENTOR             ║\n'
    printf '╚═══════════════════════════════════════╝\n'
    printf '\n'
}

print_success() {
    printf '\n'
    printf '╔═══════════════════════════════════════╗\n'
    printf '║  Installation completed successfully! ║\n'
    printf '╚═══════════════════════════════════════╝\n'
    printf '\n'
    printf 'sherpa is installed:\n'
    for target in "${TARGETS[@]}"; do
        local dir
        case "$target" in claude) dir="$CLAUDE_SKILL_DIR" ;; opencode) dir="$OPENCODE_SKILL_DIR" ;; esac
        printf '  • %s: %s\n' "$target" "$dir"
    done
    if [[ "${SHERPA_INSTALL_CLI:-1}" == "1" ]]; then
        printf '  • CLI: %s/%s\n' "$CLI_BIN_DIR" "$CLI_NAME"
    fi
    printf '\n'
    printf 'Try it in your AI coding agent:\n'
    printf '  /sherpa status\n'
    printf '  /sherpa next\n'
    printf '  /sherpa suggest\n'
    printf '\n'
    printf 'CLI commands:\n'
    printf '  sherpa --version\n'
    printf '  sherpa update\n'
    printf '  sherpa doctor\n'
    printf '  sherpa uninstall\n'
    printf '\n'
    printf 'Release manifest: %s\n' "$MANIFEST_URL_DISPLAY"
    printf 'Docs: INSTALLATION.md README.md SECURITY.md\n'
    printf '\n'
}

###############################################################################
# Argument parsing
###############################################################################
TARGETS=()
MANIFEST_URL_DISPLAY=""
INSTALL_CLI=1

usage() {
    cat <<EOF
Usage: install.sh [options]

Install sherpa (AI Hackathon Mentor) for Claude Code and/or OpenCode.

Options:
  --claude           Install only the Claude Code skill
  --opencode         Install only the OpenCode skill
  --both             Install both Claude Code and OpenCode (default when none detected)
  --project DIR      Project-level install target (experimental)
  --version VER      Pin a specific release version
  --manifest-url URL Override the release manifest URL
  --no-cli           Do not install the sherpa CLI
  --no-path          Do not modify shell profile PATH
  --yes              Non-interactive (accept defaults)
  -h, --help         Show this help

Environment variables:
  SHERPA_RELEASE_MANIFEST_URL  Release manifest JSON URL
  SHERPA_VERSION               Pin a specific release version
  SHERPA_INSTALL_CLAUDE/OPENCODE/CLI  1=install, 0=skip
  SHERPA_NO_PATH               1=skip PATH modification

Examples:
  curl -fsSL https://YOUR-DOMAIN/install.sh | bash
  curl -fsSL https://YOUR-DOMAIN/install.sh | bash -s -- --claude --opencode
EOF
    exit 0
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --claude)   INSTALL_CLAUDE=1; INSTALL_OPENCODE=0; shift ;;
        --opencode) INSTALL_OPENCODE=1; INSTALL_CLAUDE=0; shift ;;
        --both)     INSTALL_CLAUDE=1; INSTALL_OPENCODE=1; shift ;;
        --project)  die "project-level installer mode is not implemented; use the repository-local agent files" ;;
        --version)  SHERPA_VERSION="${2:-}"; shift 2 ;;
        --manifest-url) SHERPA_RELEASE_MANIFEST_URL="${2:-}"; shift 2 ;;
        --no-cli)   INSTALL_CLI=0; shift ;;
        --no-path)  SHERPA_NO_PATH=1; shift ;;
        --yes)      SHERPA_NONINTERACTIVE=1; shift ;;
        -h|--help)  usage ;;
        *)          die "unknown option: $1" ;;
    esac
done

###############################################################################
# Main
###############################################################################
main() {
    print_banner

    # Require python3 (used for manifest parsing and the CLI).
    if ! have python3; then
        die "python3 is required but not installed"
    fi

    step "Detecting environment"
    detect_environments

    step "Fetching latest release"
    fetch_manifest
    MANIFEST_URL_DISPLAY="${SHERPA_RELEASE_MANIFEST_URL:-$DEFAULT_MANIFEST_URL}"
    select_archive

    step "Downloading package"
    download_and_verify

    step "Verifying integrity"
    validate_archive_contents "$ARCHIVE_FILE"

    step "Installing skill"
    for target in "${TARGETS[@]}"; do
        install_skill "$target"
    done

    if [[ "${INSTALL_CLI:-1}" == "1" ]]; then
        install_cli
    fi

    step "Validating installation"
    validate_installation

    print_success
    cleanup
    exit 0
}

main "$@"
