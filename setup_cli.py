#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AvatarHUD - Universal Autonomous CLI Setup Engine
Automatically configures and links AvatarHUD with Antigravity CLI, OpenAI Codex CLI,
and Anthropic Claude Code CLI on Windows, macOS, and Linux with zero hardcoded paths.
"""

import os
import sys
import argparse
import subprocess
import shutil

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass
    if hasattr(sys.stderr, 'reconfigure'):
        try:
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
CORE_DIR = os.path.join(REPO_ROOT, "core")
sys.path.insert(0, CORE_DIR)

from notify import notify_status, is_server_alive


def print_banner():
    print("=" * 60)
    print("  AvatarHUD - Universal CLI Autonomous Setup Engine")
    print("=" * 60)
    print(f"  [System] OS: {sys.platform} | Python: {sys.version.split()[0]}")
    print(f"  [Repo]   {REPO_ROOT}")
    print("=" * 60)


def check_dependencies():
    """Verify core python dependencies."""
    print("\n[STEP 1] Checking Python dependencies...")
    missing = []
    try:
        import webview
    except ImportError:
        missing.append("pywebview")
    try:
        import bottle
    except ImportError:
        missing.append("bottle")

    if missing:
        print(f"  [WARN] Missing dependencies: {', '.join(missing)}")
        req_file = os.path.join(REPO_ROOT, "requirements.txt")
        if sys.platform == 'darwin':
            mac_req = os.path.join(REPO_ROOT, "macos", "requirements_mac.txt")
            if os.path.exists(mac_req):
                req_file = mac_req

        if os.path.exists(req_file):
            print(f"  [INFO] Installing dependencies from {req_file}...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_file], check=False)
    else:
        print("  [OK] Core dependencies (pywebview, bottle) are verified.")


def setup_antigravity():
    """Configure Antigravity CLI skill in ~/.gemini/config/skills/avatar-hud/SKILL.md."""
    print("\n[STEP 2] Configuring Antigravity CLI integration...")
    home = os.path.expanduser("~")
    target_dir = os.path.join(home, ".gemini", "config", "skills", "avatar-hud")
    os.makedirs(target_dir, exist_ok=True)
    target_file = os.path.join(target_dir, "SKILL.md")

    notify_script = os.path.join(REPO_ROOT, "notify.py").replace("\\", "/")
    py_bin = sys.executable.replace("\\", "/")

    skill_content = f"""---
name: avatar-hud
description: 투명 누끼 스탠딩 데스크톱 펫(AvatarHUD)과 연동하여 작업 착수, 진행 단계, 최종 완료 보고를 실시간 말풍선으로 시각화합니다. 사용자가 작업 현황 시각화, AvatarHUD, 바탕화면 캐릭터 말풍선 알림을 요청하거나 활성화할 때 사용합니다.
---

# AvatarHUD 연동 스킬

바탕화면에 상주하는 AvatarHUD 투명 캐릭터 말풍선에 실시간 작업 상황을 보고합니다.

## 표준 보고 프로토콜

작업을 수행할 때 아래 단계를 따라 터미널 명령을 호출하십시오:

### 1. 작업 착수 시
```bash
"{py_bin}" "{notify_script}" --status working --title "작업 착수" --msg "요청 사항을 분석하고 파일 탐색을 시작합니다..." --step "1/3"
```

### 2. 중간 단계 및 코드 구현 중
```bash
"{py_bin}" "{notify_script}" --status working --title "코드 구현 중" --msg "모듈 변경 및 단위 검증을 수행하고 있습니다..." --step "2/3"
```

### 3. 작업 최종 완료 시
```bash
"{py_bin}" "{notify_script}" --status done --title "작업 완료!" --msg "모든 작업이 성공적으로 마무리되었습니다."
```

### 4. 오류 발생 시
```bash
"{py_bin}" "{notify_script}" --status error --title "오류 발생" --msg "예외가 감지되어 디버깅을 시작합니다."
```
"""

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(skill_content)

    print(f"  [OK] Antigravity skill successfully registered:")
    print(f"       -> {target_file}")


def setup_codex(target_project=None):
    """Configure Codex CLI system instructions (AGENTS.md)."""
    print("\n[STEP 3] Configuring Codex CLI integration...")
    notify_script = os.path.join(REPO_ROOT, "codex", "notify_codex.py").replace("\\", "/")
    py_bin = sys.executable.replace("\\", "/")

    def get_content(cmd_str):
        return f"""# Codex CLI Agent Instructions for AvatarHUD

You are integrated with **AvatarHUD**, a transparent standing desktop companion overlay that visually reports your live status to the user through speech bubbles.

## Mandatory Operating Protocol

Whenever you execute coding, refactoring, building, or debugging tasks:

1. **Before Running Complex Actions / Commands**:
   Call the notification script to display your current step and intent:
   ```bash
   {cmd_str} --status working --title "Codex 작업 착수" --msg "요청 사항을 분석하고 파일 수정을 준비합니다..." --step "1/3"
   ```

2. **During Long Executions or Multi-step Tasks**:
   Update progress:
   ```bash
   {cmd_str} --status working --title "Codex 빌드 및 검증" --msg "코드 수정 후 테스트 스위트를 실행하고 있습니다..." --step "2/3"
   ```

3. **Upon Task Completion**:
   Report the final summary in the speech bubble before outputting your final response:
   ```bash
   {cmd_str} --status done --title "Codex 작업 완료!" --msg "코드 변경 및 검증이 완벽하게 완료되었습니다."
   ```

4. **When Errors Occur**:
   Notify the user with the error context:
   ```bash
   {cmd_str} --status error --title "Codex 오류 발생" --msg "빌드 오류가 감지되어 디버깅을 시작합니다."
   ```
"""

    # 1. Update repository template codex/AGENTS.md with relative command
    repo_agents = os.path.join(REPO_ROOT, "codex", "AGENTS.md")
    with open(repo_agents, "w", encoding="utf-8") as f:
        f.write(get_content('python codex/notify_codex.py'))
    print(f"  [OK] Repository template updated -> {repo_agents}")

    # 2. Deploy to global user directory ~/.codex/AGENTS.md with absolute dynamic command
    home = os.path.expanduser("~")
    global_codex_dir = os.path.join(home, ".codex")
    try:
        os.makedirs(global_codex_dir, exist_ok=True)
        global_file = os.path.join(global_codex_dir, "AGENTS.md")
        with open(global_file, "w", encoding="utf-8") as f:
            f.write(get_content(f'"{py_bin}" "{notify_script}"'))
        print(f"  [OK] Global Codex instructions registered -> {global_file}")
    except Exception as e:
        print(f"  [INFO] Skipping global Codex folder: {e}")

    # 3. Deploy to target project if specified
    if target_project and os.path.isdir(target_project):
        proj_file = os.path.join(target_project, "AGENTS.md")
        with open(proj_file, "w", encoding="utf-8") as f:
            f.write(get_content(f'"{py_bin}" "{notify_script}"'))
        print(f"  [OK] Project AGENTS.md created -> {proj_file}")


def setup_claude(target_project=None):
    """Configure Claude Code CLI rules (CLAUDE.md)."""
    print("\n[STEP 4] Configuring Claude Code CLI integration...")
    notify_script = os.path.join(REPO_ROOT, "claude", "notify_claude.py").replace("\\", "/")
    py_bin = sys.executable.replace("\\", "/")

    def get_content(cmd_str):
        return f"""# Claude Code Guidelines - AvatarHUD Integration

This project is connected with **AvatarHUD**, a transparent cutout standing desktop pet that visualizes your current thinking, status, and task completion directly on the user's screen.

## Automatic Status Reporting Rules

Whenever you begin a non-trivial user task, run intermediate tests/builds, or complete an instruction, invoke the notification adapter:

1. **Task Start / Investigation**:
   ```bash
   {cmd_str} --status working --title "Claude 작업 시작" --msg "코드 변경 사항을 파악하고 작업을 시작합니다..." --step "1/3"
   ```

2. **Testing / Implementation**:
   ```bash
   {cmd_str} --status working --title "Claude 테스트 실행" --msg "테스트 코드를 검증하고 있습니다..." --step "2/3"
   ```

3. **Task Completed**:
   ```bash
   {cmd_str} --status done --title "Claude 작업 완료!" --msg "모든 작업이 성공적으로 마무리되었습니다."
   ```

4. **Error Encountered**:
   ```bash
   {cmd_str} --status error --title "Claude 오류 발생" --msg "예외가 발생하여 로그를 점검하고 있습니다."
   ```
"""

    # 1. Update repository template claude/CLAUDE.md with relative command
    repo_claude = os.path.join(REPO_ROOT, "claude", "CLAUDE.md")
    with open(repo_claude, "w", encoding="utf-8") as f:
        f.write(get_content('python claude/notify_claude.py'))
    print(f"  [OK] Repository template updated -> {repo_claude}")

    # 2. Deploy to global user directory ~/.claude/CLAUDE.md with absolute dynamic command
    home = os.path.expanduser("~")
    global_claude_dir = os.path.join(home, ".claude")
    try:
        os.makedirs(global_claude_dir, exist_ok=True)
        global_file = os.path.join(global_claude_dir, "CLAUDE.md")
        with open(global_file, "w", encoding="utf-8") as f:
            f.write(get_content(f'"{py_bin}" "{notify_script}"'))
        print(f"  [OK] Global Claude rules registered -> {global_file}")
    except Exception as e:
        print(f"  [INFO] Skipping global Claude folder: {e}")

    # 3. Deploy to target project if specified
    if target_project and os.path.isdir(target_project):
        proj_file = os.path.join(target_project, "CLAUDE.md")
        with open(proj_file, "w", encoding="utf-8") as f:
            f.write(get_content(f'"{py_bin}" "{notify_script}"'))
        print(f"  [OK] Project CLAUDE.md created -> {proj_file}")


def verify_and_test():
    """Verify live communication with AvatarHUD."""
    print("\n[STEP 5] Verifying live AvatarHUD connection...")
    success, res = notify_status(
        status="working",
        title="AvatarHUD 셋업 완료",
        message="3대 AI CLI(Antigravity, Codex, Claude) 자율 연동이 구성되었습니다.",
        step="3/3",
        ensure_server=True
    )
    if success:
        print("  [PASS] Successfully communicated with AvatarHUD overlay!")
        print("         The speech bubble is now visible on your desktop.")
    else:
        print(f"  [WARN] Server connection note: {res}")


def main():
    parser = argparse.ArgumentParser(description="AvatarHUD Autonomous CLI Setup Engine")
    parser.add_argument('--auto', '--all', action='store_true', help="Automatically configure all 3 AI CLIs")
    parser.add_argument('--antigravity', action='store_true', help="Configure Antigravity CLI skill")
    parser.add_argument('--codex', action='store_true', help="Configure Codex CLI instructions")
    parser.add_argument('--claude', action='store_true', help="Configure Claude Code CLI rules")
    parser.add_argument('--target-project', type=str, default=None, help="Target project directory for local AGENTS.md / CLAUDE.md")
    parser.add_argument('--check', action='store_true', help="Run verification check only")

    args = parser.parse_args()

    print_banner()

    if args.check:
        verify_and_test()
        sys.exit(0)

    # If no specific CLI is flagged or --auto is passed, configure all
    run_all = args.auto or (not args.antigravity and not args.codex and not args.claude)

    check_dependencies()

    if run_all or args.antigravity:
        setup_antigravity()

    if run_all or args.codex:
        setup_codex(target_project=args.target_project)

    if run_all or args.claude:
        setup_claude(target_project=args.target_project)

    verify_and_test()

    print("\n" + "=" * 60)
    print("  [SUCCESS] All AI CLI setups completed autonomously!")
    print("  You can now issue commands to Antigravity, Codex, or Claude")
    print("  and watch your transparent desktop companion report live.")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
