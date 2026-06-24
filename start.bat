@echo off
title TaroPen

:: Switch to script directory
pushd "%~dp0"

:: Find Python
set PYTHON=
if exist "C:\Users\31908\AppData\Local\Programs\Python\Python312\python.exe" (
    set "PYTHON=C:\Users\31908\AppData\Local\Programs\Python\Python312\python.exe"
) else (
    where python >nul 2>&1 && set "PYTHON=python"
)

if "%PYTHON%"=="" (
    echo [ERROR] Python not found.
    echo Please install Python 3.8+ or edit start.bat to set the correct path.
    pause
    exit /b 1
)

echo ================================
echo   TaroPen - Novel Generator
echo ================================
echo.
echo   Python: %PYTHON%
echo   URL:    http://127.0.0.1:8765
echo.
echo   Press Ctrl+C to stop.
echo ================================
echo.

:loop
"%PYTHON%" server.py
echo.
echo Server stopped. Restarting in 3 seconds...
timeout /t 3 /nobreak >nul
goto loop
