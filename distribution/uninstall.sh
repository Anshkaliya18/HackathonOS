#!/usr/bin/env bash
#
# HackathonOS Uninstaller — Linux / macOS / Git Bash
#
# Removes only HackathonOS installation files. User project data and
# `.hackathon/` directories are never touched.
#
# Usage:
#   curl -fsSL https://YOUR-DOMAIN/uninstall.sh | bash
#
# Environment variables:
#   HACKATHONOS_NO_PATH      1 = do not modify shell profile PATH
#   HACKATHONOS_YES          1 = skip confirmation prompt

set -euo pipefail

PROJECT="HackathonOS"
CLI_NAME="hackathonos"
CLI_BIN_DIR="${HOME}/.local/bin"

CLAUDE_SKILL_DIR="${HOME}/.claude/skills/hackathonos"
OPENCODE_SKILL_DIR="${HOME}/.config/opencode/skills/hackathonos"

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
if [[ "${HACKATHONOS_YES:-0}" == "1" ]]; then confirm=0; fi

step "HackathonOS uninstaller"
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
echo "User project data (.hackathon/ directories) will NOT be removed."
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
    echo "No HackathonOS installation found."
else
    echo
    echo "Uninstallation completed. Removed ${removed} item(s)."
    echo
    echo "Note: your project .hackathon/ state directories were preserved."
fi
