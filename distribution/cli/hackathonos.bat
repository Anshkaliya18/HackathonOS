@echo off
:: Deprecated HackathonOS compatibility wrapper. Use sherpa.bat.
setlocal
echo HackathonOS is now Sherpa. The 'hackathonos' command is deprecated; use 'sherpa'. 1>&2
"%~dp0sherpa.bat" %*
