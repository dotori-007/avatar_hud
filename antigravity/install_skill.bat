@echo off
chcp 65001 > nul
echo [AvatarHUD] Antigravity CLI 스킬 설치를 시작합니다...

set TARGET_DIR=%USERPROFILE%\.gemini\config\skills\avatar-hud
if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"

copy /Y "%~dp0skills\avatar-hud\SKILL.md" "%TARGET_DIR%\SKILL.md" > nul

echo [AvatarHUD] 스킬이 성공적으로 등록되었습니다: %TARGET_DIR%\SKILL.md
echo [AvatarHUD] 이제 Antigravity CLI 세션에서 AvatarHUD가 자동 활성화됩니다!
pause
