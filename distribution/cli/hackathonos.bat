@echo off
:: HackathonOS CLI wrapper for Windows.
:: Locates the Python implementation next to this batch file and forwards all arguments.
setlocal
set "SCRIPT_DIR=%~dp0"
if not exist "%SCRIPT_DIR%hackathonos" (
    echo hackathonos: Python implementation not found next to this wrapper. >&2
    exit /b 1
)
python "%SCRIPT_DIR%hackathonos" %*
