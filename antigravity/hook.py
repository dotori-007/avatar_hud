#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity CLI - AvatarHUD Hook Wrapper
Integrates Antigravity agent tool lifecycles with AvatarHUD.
"""

import os
import sys

CORE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'core')
sys.path.insert(0, CORE_DIR)

from notify import notify_working, notify_done, notify_error, notify_idle

def on_tool_start(tool_name, description=""):
    title = f"도구 실행: {tool_name}"
    msg = description or f"{tool_name} 실행을 시작합니다..."
    return notify_working(title=title, message=msg)

def on_tool_end(tool_name, summary=""):
    title = f"도구 완료: {tool_name}"
    msg = summary or f"{tool_name} 실행이 완료되었습니다."
    return notify_working(title=title, message=msg)

def on_task_complete(title="작업 완료", summary=""):
    return notify_done(title=title, message=summary)

def on_task_error(error_msg=""):
    return notify_error(title="에러 발생", message=error_msg)

if __name__ == '__main__':
    print("[Antigravity Hook] Ready to receive lifecycle hooks.")
