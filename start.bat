@echo off
title 太郎的笔
echo Starting 太郎的笔...
cd /d "%~dp0"

:loop
python server.py
echo.
echo Server crashed or stopped. Restarting in 3 seconds...
timeout /t 3 /nobreak >nul
goto loop
