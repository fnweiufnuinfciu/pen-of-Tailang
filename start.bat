@echo off
chcp 65001 >nul 2>&1
title 太郎的笔

:: 切换脚本所在目录
pushd "%~dp0"

:: 查找 Python（优先用已知路径）
set PYTHON=
if exist "C:\Users\31908\AppData\Local\Programs\Python\Python312\python.exe" (
    set "PYTHON=C:\Users\31908\AppData\Local\Programs\Python\Python312\python.exe"
) else (
    :: 尝试 PATH 中的 python
    where python >nul 2>&1 && set "PYTHON=python"
)

if "%PYTHON%"=="" (
    echo 错误：未找到 Python。请安装 Python 3.8+ 或修改 start.bat 中的路径。
    pause
    exit /b 1
)

echo ================================
echo   太郎的笔 - AI 小说写作工具
echo ================================
echo.
echo   Python: %PYTHON%
echo   地址:   http://127.0.0.1:8765
echo.
echo   按 Ctrl+C 停止服务器
echo ================================
echo.

:loop
"%PYTHON%" server.py
echo.
echo 服务器已停止。3 秒后自动重启...
timeout /t 3 /nobreak >nul
goto loop
