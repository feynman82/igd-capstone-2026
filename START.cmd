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
if /i not "%~1"=="-CheckOnly" pause
popd
exit /b %PARROT_EXIT_CODE%
