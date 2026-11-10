# Claude Code Guidelines - AvatarHUD Integration

This project is connected with **AvatarHUD**, a transparent cutout standing desktop pet that visualizes your current thinking, status, and task completion directly on the user's screen.

## Automatic Status Reporting Rules

Whenever you begin a non-trivial user task, run intermediate tests/builds, or complete an instruction, invoke the notification adapter:

1. **Task Start / Investigation**:
   ```bash
   python claude/notify_claude.py --status working --title "Claude 작업 시작" --msg "코드 변경 사항을 파악하고 작업을 시작합니다..." --step "1/3"
   ```

2. **Testing / Implementation**:
   ```bash
   python claude/notify_claude.py --status working --title "Claude 테스트 실행" --msg "테스트 코드를 검증하고 있습니다..." --step "2/3"
   ```

3. **Task Completed**:
   ```bash
   python claude/notify_claude.py --status done --title "Claude 작업 완료!" --msg "모든 작업이 성공적으로 마무리되었습니다."
   ```

4. **Error Encountered**:
   ```bash
   python claude/notify_claude.py --status error --title "Claude 오류 발생" --msg "예외가 발생하여 로그를 점검하고 있습니다."
   ```
