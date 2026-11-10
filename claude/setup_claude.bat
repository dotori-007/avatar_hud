@echo off
chcp 65001 > nul
echo [AvatarHUD] Claude Code 연동 설정을 자동 구성합니다...

python "%~dp0..\setup_cli.py" --claude
pause
