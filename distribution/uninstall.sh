#!/usr/bin/env bash
#
# sherpa Uninstaller — Linux / macOS / Git Bash
#
# Removes only sherpa installation files. User project data and
# `.sherpa/` directories are never touched.
#
# Usage:
#   curl -fsSL https://YOUR-DOMAIN/uninstall.sh | bash
#
# Environment variables:
#   SHERPA_NO_PATH      1 = do not modify shell profile PATH
#   SHERPA_YES          1 = skip confirmation prompt

set -euo pipefail

# Prefer the receipt-aware installer engine when this script is part of a
# checkout or extracted release. The legacy bootstrap fallback below remains
# for older remote one-file invocations that have no adjacent engine.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "${SCRIPT_DIR}/cli/installer.py" && -f "${SCRIPT_DIR}/cli/sherpa" ]]; then
    PYTHON_BIN=""
    for candidate in python3 python; do
        candidate_path="$(command -v "$candidate" || true)"
        if [[ -n "$candidate_path" ]] && "$candidate_path" -c 'import sys; raise SystemExit(0 if sys.version_info.major == 3 else 1)' >/dev/null 2>&1; then
            PYTHON_BIN="$candidate_path"
            break
        fi
    done
    [[ -n "${PYTHON_BIN}" ]] || { echo "Python 3 is required to remove managed Sherpa installs." >&2; exit 1; }
    CLIENT="all"
    SCOPE="global"
    PROJECT_DIR=""
    DESTINATION=""
    YES="${SHERPA_YES:-0}"
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --client) CLIENT="$2"; shift 2 ;;
            --project) SCOPE="project"; PROJECT_DIR="$2"; shift 2 ;;
            --destination) DESTINATION="$2"; shift 2 ;;
            --yes|-y) YES=1; shift ;;
            *) echo "Unknown option: $1" >&2; exit 2 ;;
        esac
    done
    ARGS=(uninstall --client "$CLIENT" --scope "$SCOPE")
    [[ -z "$PROJECT_DIR" ]] || ARGS+=(--project-dir "$PROJECT_DIR")
    [[ -z "$DESTINATION" ]] || ARGS+=(--destination "$DESTINATION")
    [[ "$YES" != "1" ]] || ARGS+=(--yes)
    exec "$PYTHON_BIN" "${SCRIPT_DIR}/cli/sherpa" "${ARGS[@]}"
fi

PROJECT="sherpa"
CLI_NAME="sherpa"
CLI_BIN_DIR="${HOME}/.local/bin"
SHERPA_YES="${SHERPA_YES:-0}"

CLAUDE_SKILL_DIR="${HOME}/.claude/skills/sherpa"
OPENCODE_SKILL_DIR="${HOME}/.config/opencode/skills/sherpa"

step() { printf '\n==> %s\n' "$*"; }
info(){ printf '  > %s\n' "$*"; }
ok()  { printf '  ✓ %s\n' "$*"; }
err() { printf '  ✗ %s\n' "$*" >&2; }
die() { err "$*"; exit 1; }

HAVE_CLAUDE=0
HAVE_OPENCODE=0
[[ -f "${CLAUDE_SKILL_DIR}/SKILL.md" ]] && HAVE_CLAUDE=1
[[ -f "${OPENCODE_SKILL_DIR}/SKILL.md" ]] && HAVE_OPENCODE=1

confirm=1
if [[ "${SHERPA_YES:-0}" == "1" ]]; then confirm=0; fi

step "sherpa uninstaller"
echo
echo "The following will be removed:"
if [[ "$HAVE_CLAUDE" == "1" ]]; then
    echo "  • Claude Code skill: ${CLAUDE_SKILL_DIR}"
fi
if [[ "$HAVE_OPENCODE" == "1" ]]; then
    echo "  • OpenCode skill: ${OPENCODE_SKILL_DIR}"
fi
if [[ -x "${CLI_BIN_DIR}/${CLI_NAME}" || -f "${CLI_BIN_DIR}/${CLI_NAME}" ]]; then
    echo "  • CLI: ${CLI_BIN_DIR}/${CLI_NAME}"
fi
echo
echo "User project data (.sherpa/ directories) will NOT be removed."
echo "This action cannot be undone."
echo

if [[ "$confirm" == "1" ]]; then
    read -r -p "Proceed with uninstallation? [y/N]: " reply || true
    case "$reply" in
        y|Y|yes|YES) ;;
        *) echo "Uninstallation cancelled."; exit 0 ;;
    esac
fi

removed=0
if [[ "$HAVE_CLAUDE" == "1" ]]; then
    rm -rf "${CLAUDE_SKILL_DIR}"
    ok "Removed Claude Code skill"
    removed=$((removed+1))
fi
if [[ "$HAVE_OPENCODE" == "1" ]]; then
    rm -rf "${OPENCODE_SKILL_DIR}"
    ok "Removed OpenCode skill"
    removed=$((removed+1))
fi
if [[ -e "${CLI_BIN_DIR}/${CLI_NAME}" ]]; then
    rm -f "${CLI_BIN_DIR}/${CLI_NAME}"
    ok "Removed CLI"
    removed=$((removed+1))
fi
if [[ "$removed" -eq 0 ]]; then
    echo "No sherpa installation found."
else
    echo
    echo "Uninstallation completed. Removed ${removed} item(s)."
    echo
    echo "Note: your project .sherpa/ state directories were preserved."
fi
