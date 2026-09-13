@echo off
setlocal
title Parrot
pushd "%~dp0"
if errorlevel 1 exit /b 1
if exist "%~dp0.venv\Scripts\python.exe" (
  "%~dp0.venv\Scripts\python.exe" "%~dp0scripts\start_parrot.py" %*
) else (
  where python.exe >nul 2>nul
  if errorlevel 1 (
    echo Python is missing. Install Python 3.12 and follow docs\RUNNING.md.
    popd
    if /i not "%~1"=="-CheckOnly" pause
    exit /b 2
  )
  python.exe "%~dp0scripts\start_parrot.py" %*
)
set "PARROT_EXIT_CODE=%ERRORLEVEL%"
echo.
rem Shut down from the screens is a clean exit, and the window closes with it. Anything else,
rem a failed start or Ctrl+C, stays open so the reason can be read.
if not "%PARROT_EXIT_CODE%"=="0" if /i not "%~1"=="-CheckOnly" pause
popd
exit /b %PARROT_EXIT_CODE%
