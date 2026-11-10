---
name: avatar-hud
description: 투명 누끼 스탠딩 데스크톱 펫(AvatarHUD)과 연동하여 작업 착수, 진행 단계, 최종 완료 보고를 실시간 말풍선으로 시각화합니다. 사용자가 작업 현황 시각화, AvatarHUD, 바탕화면 캐릭터 말풍선 알림을 요청하거나 활성화할 때 사용합니다.
---

# AvatarHUD (투명 누끼 스탠딩 데스크톱 HUD) 스킬

이 스킬은 Antigravity 에이전트가 코딩, 리서치, 디버깅 작업을 수행할 때 바탕화면에 상주하는 투명 누끼 스탠딩 캐릭터(AvatarHUD)의 말풍선에 실시간 작업 상태와 최종 결과를 즉각 보고하도록 지시합니다.

---

## 에이전트 작업 수행 원칙

### 1. 작업 착수 시 (Working 상태 전송)
작업을 시작하거나 사용자 요청을 분석하여 도구(Tool)를 실행하기 직전, 아래 명령어로 작업 시작을 알립니다:
```powershell
python "C:\2026591001\source\github_pr\avatar_hud\core\notify.py" --status working --title "작업 착수" --msg "요청 사항을 분석하고 파일 탐색을 시작합니다..." --step "1/3"
```

### 2. 중간 진행 단계 (진행 갱신)
빌드, 테스트, 파일 수정 등 주요 중간 단계에서 작업 현황을 갱신합니다:
```powershell
python "C:\2026591001\source\github_pr\avatar_hud\core\notify.py" --status working --title "코드 구현 중" --msg "새로운 모듈 구현 및 단위 테스트 작성 중..." --step "2/3"
```

### 3. 작업 완료 시 (Done 상태 전송)
모든 변경과 검증이 완료되어 최종 응답을 출력하기 직전, 핵심 요약과 함께 완료 상태를 보냅니다:
```powershell
python "C:\2026591001\source\github_pr\avatar_hud\core\notify.py" --status done --title "작업 완료!" --msg "모든 모듈 구현 및 테스트가 성공적으로 통과되었습니다."
```

### 4. 오류 발생 시 (Error 상태 전송)
치명적인 오류나 예외가 발생하여 사용자 확인이 필요할 때 호출합니다:
```powershell
python "C:\2026591001\source\github_pr\avatar_hud\core\notify.py" --status error --title "오류 발생" --msg "빌드 오류가 발생하여 원인을 조사하고 있습니다."
```
