#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AvatarHUD - Universal Notification Utility
Used by Antigravity CLI, Codex CLI, Claude CLI, and custom scripts to update AvatarHUD speech bubbles.
"""

import sys
import json
import argparse
import urllib.request
import urllib.error

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8765

def notify_status(status="working", title=None, message="", step="", elapsed=None, host=DEFAULT_HOST, port=DEFAULT_PORT):
    """
    Send status update to AvatarHUD REST API.
    :param status: 'working' | 'done' | 'idle' | 'error'
    :param title: Main bubble title
    :param message: Detailed description
    :param step: Step badge string (e.g. '2/5')
    :param elapsed: Elapsed time in seconds
    """
    url = f"http://{host}:{port}/api/status"
    payload = {
        "status": status,
        "title": title,
        "message": message,
        "step": step,
        "elapsed": elapsed
    }

    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={'Content-Type': 'application/json; charset=utf-8'},
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=2.0) as res:
            res_data = json.loads(res.read().decode('utf-8'))
            return True, res_data
    except urllib.error.URLError as e:
        return False, f"AvatarHUD is not running on {url}: {e.reason}"
    except Exception as e:
        return False, str(e)


def notify_working(title="작업 수행 중", message="", step=""):
    return notify_status(status="working", title=title, message=message, step=step)

def notify_done(title="작업 완료", message="", elapsed=None):
    return notify_status(status="done", title=title, message=message, elapsed=elapsed)

def notify_error(title="오류 발생", message=""):
    return notify_status(status="error", title=title, message=message)

def notify_idle(message="명령을 기다리고 있습니다."):
    return notify_status(status="idle", title="대기 중", message=message)


def main():
    parser = argparse.ArgumentParser(description="AvatarHUD Notification CLI Tool")
    parser.add_argument('--status', '-s', choices=['working', 'done', 'idle', 'error'], default='working', help="Status type")
    parser.add_argument('--title', '-t', type=str, default=None, help="Bubble title")
    parser.add_argument('--msg', '--message', '-m', type=str, default="", help="Detailed description text")
    parser.add_argument('--step', type=str, default="", help="Step indicator (e.g. 2/5)")
    parser.add_argument('--elapsed', type=int, default=None, help="Elapsed time in seconds")
    parser.add_argument('--port', '-p', type=int, default=DEFAULT_PORT, help="AvatarHUD port (default: 8765)")
    parser.add_argument('--host', type=str, default=DEFAULT_HOST, help="AvatarHUD host (default: 127.0.0.1)")

    args = parser.parse_args()

    success, result = notify_status(
        status=args.status,
        title=args.title,
        message=args.msg,
        step=args.step,
        elapsed=args.elapsed,
        host=args.host,
        port=args.port
    )

    if success:
        print(f"[AvatarHUD] [{args.status.upper()}] Status sent: {args.title or args.status} - {args.msg}")
        sys.exit(0)
    else:
        print(f"[AvatarHUD Warning] {result}")
        # Return 0 so pipeline scripts won't break if HUD is not running
        sys.exit(0)


if __name__ == '__main__':
    main()
