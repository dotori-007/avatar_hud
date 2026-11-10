@echo off
chcp 65001 > nul
title AvatarHUD Settings

echo [AvatarHUD] 브라우저 설정창을 호출합니다 (:8765/settings)...
start "" http://127.0.0.1:8765/settings
