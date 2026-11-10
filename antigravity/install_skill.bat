@echo off
chcp 65001 > nul
echo [AvatarHUD] Antigravity CLI 스킬을 자동 등록합니다...

python "%~dp0..\setup_cli.py" --antigravity
pause
