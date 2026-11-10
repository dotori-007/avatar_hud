@echo off
chcp 65001 > nul
title AvatarHUD Settings

set PYTHON_BIN=C:\2026591001\Python_3.10.11_64\python.exe
if not exist "%PYTHON_BIN%" (
    set PYTHON_BIN=python
)

echo [AvatarHUD] 설정창을 엽니다...
start "" http://127.0.0.1:8765/settings
