# Codex CLI 연동 가이드 (AvatarHUD)

Codex CLI 사용 시 바탕화면의 투명 누끼 캐릭터가 작업 단계 및 완료 상태를 실시간으로 브리핑하도록 연동하는 가이드입니다.

---

## 설정 방법

1. **에이전트 지침 파일 (AGENTS.md)**:
   * 본 디렉토리의 AGENTS.md 파일은 Codex CLI가 읽는 시스템 지침입니다.
   * 작업 대상 프로젝트 루트 또는 사용자의 Codex 지침 디렉토리에 복사하여 사용합니다.
2. **알림 도구 실행**:
   ```bash
   # 작업 중 알림
   python codex/notify_codex.py --status working --title "Codex 분석 중" --msg "코드 구조 분석을 시작합니다."

   # 완료 알림
   python codex/notify_codex.py --status done --title "Codex 완료" --msg "요청된 코드 구현을 마쳤습니다."
   ```
