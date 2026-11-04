@echo off
:: sherpa CLI wrapper for Windows.
:: Locates the Python implementation next to this batch file and forwards all arguments.
setlocal
set "SCRIPT_DIR=%~dp0"
if not exist "%SCRIPT_DIR%sherpa" (
    echo sherpa: Python implementation not found next to this wrapper. >&2
    exit /b 1
)
where python >nul 2>&1
if not errorlevel 1 goto use_python
where py >nul 2>&1
if not errorlevel 1 goto use_launcher
echo sherpa: Python 3 was not found. Install Python or add it to PATH. >&2
exit /b 1

:use_python
python "%SCRIPT_DIR%sherpa" %*
exit /b %ERRORLEVEL%

:use_launcher
py -3 "%SCRIPT_DIR%sherpa" %*
exit /b %ERRORLEVEL%
