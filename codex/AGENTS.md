# Codex CLI Agent Instructions for AvatarHUD

You are integrated with **AvatarHUD**, a transparent standing desktop companion overlay that visually reports your live status to the user through speech bubbles.

## Mandatory Operating Protocol

Whenever you execute coding, refactoring, building, or debugging tasks:

1. **Before Running Complex Actions / Commands**:
   Call the notification script to display your current step and intent:
   ```bash
   python codex/notify_codex.py --status working --title "Codex 작업 착수" --msg "요청 사항을 분석하고 파일 수정을 준비합니다..." --step "1/3"
   ```

2. **During Long Executions or Multi-step Tasks**:
   Update progress:
   ```bash
   python codex/notify_codex.py --status working --title "Codex 빌드 및 검증" --msg "코드 수정 후 테스트 스위트를 실행하고 있습니다..." --step "2/3"
   ```

3. **Upon Task Completion**:
   Report the final summary in the speech bubble before outputting your final response:
   ```bash
   python codex/notify_codex.py --status done --title "Codex 작업 완료!" --msg "코드 변경 및 검증이 완벽하게 완료되었습니다."
   ```

4. **When Errors Occur**:
   Notify the user with the error context:
   ```bash
   python codex/notify_codex.py --status error --title "Codex 오류 발생" --msg "빌드 오류가 감지되어 디버깅을 시작합니다."
   ```
