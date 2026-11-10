# Claude Code / Claude CLI Rules for AvatarHUD

You are connected to **AvatarHUD**, a lightweight desktop overlay featuring a transparent standing character that visually communicates status updates via animated speech bubbles.

## Status Reporting Rules

During coding and workflow execution, you MUST notify AvatarHUD using `claude/notify_claude.py` or `core/notify.py`:

1. **When starting a significant workflow**:
   ```bash
   python "C:/2026591001/source/github_pr/avatar_hud/claude/notify_claude.py" --status working --title "Claude 작업 시작" --msg "코드 변경 사항을 파악하고 작업을 시작합니다..." --step "1/3"
   ```

2. **When running multi-step commands (build, lint, test)**:
   ```bash
   python "C:/2026591001/source/github_pr/avatar_hud/claude/notify_claude.py" --status working --title "Claude 테스트 실행" --msg "테스트 코드를 검증하고 있습니다..." --step "2/3"
   ```

3. **When completing the task**:
   ```bash
   python "C:/2026591001/source/github_pr/avatar_hud/claude/notify_claude.py" --status done --title "Claude 작업 완료!" --msg "모든 작업이 성공적으로 마무리되었습니다."
   ```

4. **When an error occurs**:
   ```bash
   python "C:/2026591001/source/github_pr/avatar_hud/claude/notify_claude.py" --status error --title "Claude 오류 발생" --msg "예외가 발생하여 로그를 점검하고 있습니다."
   ```
