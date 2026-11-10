# Claude Code / Claude CLI 연동 가이드 (AvatarHUD)

Anthropic의 Claude Code CLI 에이전트가 코딩 작업을 진행할 때, 바탕화면 투명 누끼 캐릭터가 실시간 작업 현황과 완료 요약을 시각적으로 안내하도록 연동하는 가이드입니다.

---

## 📌 설정 및 사용법

1. **`CLAUDE.md` 규칙 파일 연동**:
   * 본 디렉토리에 포함된 `CLAUDE.md`는 Claude Code가 실행 시 자동으로 읽어들이는 시스템 규칙 파일입니다.
   * 작업하고자 하는 프로젝트 루트에 `CLAUDE.md`를 위치시키면 Claude Code가 스스로 AvatarHUD 알림을 전송합니다.
2. **도구 수동 호출 예시**:
   ```bash
   # 작업 중 알림
   python claude/notify_claude.py --status working --title "Claude 작업 중" --msg "버그 픽스 및 리팩토링 진행 중..."

   # 완료 알림
   python claude/notify_claude.py --status done --title "Claude 완료!" --msg "코드 리팩토링 및 테스트가 성공했습니다."
   ```
