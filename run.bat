@echo off
chcp 65001 > nul
title AvatarHUD - Transparent Desktop Companion

echo ===================================================
echo   AvatarHUD (투명 누끼 스탠딩 데스크톱 HUD)
echo ===================================================
echo [1/2] 가상환경 및 파이썬 경로 확인 중...

set PYTHON_BIN=
if exist "%~dp0.venv\Scripts\python.exe" set PYTHON_BIN="%~dp0.venv\Scripts\python.exe"
if not defined PYTHON_BIN where python >nul 2>nul && set PYTHON_BIN=python
if not defined PYTHON_BIN where py >nul 2>nul && set PYTHON_BIN=py
if not defined PYTHON_BIN if exist "C:\2026591001\Python_3.10.11_64\python.exe" set PYTHON_BIN="C:\2026591001\Python_3.10.11_64\python.exe"
if not defined PYTHON_BIN set PYTHON_BIN=python

echo [2/2] 투명 윈도우 및 REST/SSE 서버 기동 중 (:8765)...
%PYTHON_BIN% "%~dp0core\app.py" %*

pause
