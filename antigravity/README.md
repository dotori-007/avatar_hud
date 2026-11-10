# Antigravity CLI 연동 가이드 (AvatarHUD)

Antigravity CLI 에이전트가 작업할 때, 바탕화면 투명 누끼 캐릭터의 말풍선에 진행 상황과 완료 보고를 실시간으로 띄워주는 연동 가이드입니다.

---

## 빠른 시작 (원클릭 설치)

1. `antigravity/install_skill.bat`을 실행합니다.
2. `%USERPROFILE%\.gemini\config\skills\avatar-hud\SKILL.md` 경로로 자동 복사 및 등록됩니다.
3. 이제 Antigravity CLI 대화에서 "AvatarHUD 켜줘" 또는 작업 지시 시 에이전트가 자동으로 바탕화면 캐릭터 말풍선에 실시간 보고를 수행합니다.

---

## 수동 호출 명령어 예시

```powershell
# 1. 작업 시작 알림
python core/notify.py --status working --title "Antigravity 분석 중" --msg "코드베이스 전수 검사 진행 중..." --step "1/3"

# 2. 작업 완료 알림
python core/notify.py --status done --title "Antigravity 작업 완료!" --msg "모든 버그 수정 및 테스트 통과."

# 3. 대기 상태 전환
python core/notify.py --status idle
```
