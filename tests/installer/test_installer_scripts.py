#!/usr/bin/env python3
"""Tests for the installer scripts' safety and structure.

These are static checks (no network) verifying that install.sh and install.ps1
contain the required security and lifecycle constructs.
"""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
INSTALL_SH = REPO / "distribution" / "install.sh"
INSTALL_PS1 = REPO / "distribution" / "install.ps1"
UNINSTALL_SH = REPO / "distribution" / "uninstall.sh"
UNINSTALL_PS1 = REPO / "distribution" / "uninstall.ps1"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_install_sh_is_executable_bash():
    text = read(INSTALL_SH)
    assert text.startswith("#!/usr/bin/env bash"), "install.sh must have a bash shebang"
    assert "set -euo pipefail" in text, "install.sh must use strict error handling"


def test_install_sh_https_only():
    text = read(INSTALL_SH)
    assert "curl -fsSL" in text, "install.sh must download with curl -fsSL"
    # Every curl URL should be https.
    import re
    for m in re.finditer(r"curl[^\"\']*([\"\'])(https?://)\1", text):
        assert m.group(2) == "https://", "all installer downloads must use HTTPS"


def test_install_sh_verifies_sha256():
    text = read(INSTALL_SH)
    assert "sha256_of" in text or "sha256sum" in text or "shasum" in text or "openssl" in text
    assert "SHA-256" in text or "sha256" in text.lower()


def test_install_sh_path_traversal_guard():
    text = read(INSTALL_SH)
    assert "\\.\\./" in text or "path traversal" in text, "install.sh must guard against path traversal"


def test_install_sh_backup_and_rollback():
    text = read(INSTALL_SH)
    assert ".bak." in text, "install.sh must back up previous installations"
    assert "rollback" in text.lower(), "install.sh must support rollback"


def test_install_sh_detects_both_environments():
    text = read(INSTALL_SH)
    assert ".claude/skills/sherpa" in text
    assert ".config/opencode/skills/sherpa" in text


def test_install_sh_never_touches_hackathon_state():
    text = read(INSTALL_SH)
    # The installer must not remove or write to a user .hackathon/ directory.
    # It may mention preservation, but must not rm -rf a .hackathon path.
    import re
    bad = re.findall(r"rm -rf[^\r\n]*\.hackathon", text)
    assert not bad, "install.sh must not remove .hackathon/ project state"


def test_install_preshell_https_only():
    text = read(INSTALL_PS1)
    assert "Invoke-WebRequest" in text
    assert "https://" in text.lower() or "https:" in text


def test_install_preshell_sha256():
    text = read(INSTALL_PS1)
    assert "Get-FileHash" in text or "certutil" in text or "SHA256" in text


def test_install_preshell_extract():
    text = read(INSTALL_PS1)
    assert "Expand-Archive" in text


def test_install_preshell_path_traversal():
    text = read(INSTALL_PS1)
    assert "\\.\\." in text or "path traversal" in text.lower()


def test_windows_installer_uses_live_repo_and_guards_old_release():
    text = read(INSTALL_PS1)
    assert "github.com/Anshkaliya18/HackathonOS/releases/latest/download/manifest.json" in text
    assert "The configured release manifest is for" in text
    assert "Use-LocalCheckout" in text
    assert "Copy-LocalSkillTree" in text
    assert "\.sherpa" in text and "__pycache__" in text


def test_windows_installer_supports_headless_and_pythonless_skill_install():
    text = read(INSTALL_PS1)
    assert "Invoke-WebRequest -UseBasicParsing" in text
    assert "Get-WindowsArchitecture" in text and "'x64'   { return 'amd64' }" in text
    assert "$wmiArchitecture -eq 12" in text
    assert "SHERPA_INSTALL_CLI" in text and "if ($script:INSTALL_CLI)" in text
    assert "Test-Command py" in text
    assert "if ($env:SHERPA_NPM_WRAPPER -eq '1') { exit 1 }" in text
    wrapper = read(REPO / "distribution" / "cli" / "sherpa.bat")
    assert "py -3" in wrapper and "where python" in wrapper


def test_install_preshell_iex_manifest_and_cli_fallback():
    text = read(INSTALL_PS1)
    assert "return & ([scriptblock]::Create($ScriptBlock)) $data" in text
    assert "-ArgumentList $data" not in text
    assert "if (-not [string]::IsNullOrWhiteSpace($PSCommandPath))" in text
    assert "if (-not $cliSource -or -not (Test-Path $cliSource))" in text
    assert 'Write-Err ("Installation failed: {0}" -f $_.Exception.Message)' in text
    assert "Rollback-Installs" in text
    assert 'Read-Host "Installation complete. Press Enter to return to PowerShell"' in text
    assert 'Read-Host "Installation failed. Press Enter to return to PowerShell"' in text
    assert "exit 0" not in text, "installer must not close the caller's PowerShell session"


def test_uninstall_scripts_preserve_hackathon_state():
    for path in (UNINSTALL_SH, UNINSTALL_PS1):
        text = read(path)
        import re
        bad = re.findall(r"(rm -rf|Remove-Item)[^\r\n]*\.hackathon", text)
        assert not bad, f"{path.name} must not remove .hackathon/ project state"


def test_uninstall_asks_confirmation():
    sh_text = read(UNINSTALL_SH)
    ps_text = read(UNINSTALL_PS1)
    assert "Proceed with uninstallation" in sh_text or "read -r -p" in sh_text
    assert "Proceed with uninstallation" in ps_text or "Read-Host" in ps_text


def test_cli_and_wrappers_exist():
    assert (REPO / "distribution" / "cli" / "sherpa").is_file()
    assert (REPO / "distribution" / "cli" / "sherpa.bat").is_file()


def test_release_templates_exist():
    assert (REPO / "distribution" / "release" / "manifest.json").is_file()
    assert (REPO / "distribution" / "release" / "checksums.txt").is_file()
    assert (REPO / "distribution" / "VERSION").is_file()


if __name__ == "__main__":
    import traceback

    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception:
            failed += 1
            print(f"FAIL {test.__name__}")
            traceback.print_exc()
    print(f"\n{passed} passed, {failed} failed")
    raise SystemExit(1 if failed else 0)
