@echo off
:: sherpa CLI wrapper for Windows.
:: Locates the Python implementation next to this batch file and forwards all arguments.
setlocal
set "SCRIPT_DIR=%~dp0"
if not exist "%SCRIPT_DIR%sherpa" (
    echo sherpa: Python implementation not found next to this wrapper. >&2
    exit /b 1
)
python "%SCRIPT_DIR%sherpa" %*
