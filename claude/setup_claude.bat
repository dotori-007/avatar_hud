@echo off
chcp 65001 > nul
echo [AvatarHUD] Claude Code 연동 설정을 구성합니다...

echo [AvatarHUD] 작업할 프로젝트 루트에 CLAUDE.md를 복사하시면 Claude Code가 자동 인식합니다:
echo copy /Y "%~dp0CLAUDE.md" "<your_target_project_dir>\CLAUDE.md"
pause
