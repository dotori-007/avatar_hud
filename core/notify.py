#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AvatarHUD - Universal Notification Utility
Used by Antigravity CLI, Codex CLI, Claude CLI, and custom scripts to update AvatarHUD speech bubbles.
"""

import sys
import os
import json
import time
import argparse
import subprocess
import urllib.request
import urllib.error

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

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8765

def is_server_alive(host=DEFAULT_HOST, port=DEFAULT_PORT):
    """Check whether AvatarHUD HTTP server is responding."""
    try:
        url = f"http://{host}:{port}/api/health"
        with urllib.request.urlopen(url, timeout=0.8) as res:
            return res.status == 200
    except Exception:
        return False

def spawn_server_daemon(host=DEFAULT_HOST, port=DEFAULT_PORT):
    """
    Launch AvatarHUD transparent window in the background if not already running.
    """
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app_script = os.path.join(repo_root, "core", "app.py")
    if sys.platform == 'darwin':
        mac_app = os.path.join(repo_root, "macos", "app_mac.py")
        if os.path.exists(mac_app):
            app_script = mac_app

    if not os.path.exists(app_script):
        return False

    cmd = [sys.executable, app_script]

    try:
        if sys.platform == 'win32':
            # Run detached from terminal process group with DEVNULL streams
            subprocess.Popen(
                cmd,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True,
                cwd=repo_root
            )
        else:
            subprocess.Popen(
                cmd,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setpgrp if hasattr(os, 'setpgrp') else None,
                close_fds=True,
                cwd=repo_root
            )
    except Exception as e:
        return False

    # Wait up to 3.5 seconds for server to be responsive
    start = time.time()
    while time.time() - start < 3.5:
        if is_server_alive(host, port):
            return True
        time.sleep(0.2)
    return is_server_alive(host, port)

def notify_status(status="working", title=None, message="", step="", elapsed=None, host=DEFAULT_HOST, port=DEFAULT_PORT, ensure_server=True):
    """
    Send status update to AvatarHUD REST API. Auto-launches server daemon if down.
    :param status: 'working' | 'done' | 'idle' | 'error'
    :param title: Main bubble title
    :param message: Detailed description
    :param step: Step badge string (e.g. '2/5')
    :param elapsed: Elapsed time in seconds
    :param ensure_server: Auto-launch daemon if server is down
    """
    if ensure_server and not is_server_alive(host, port):
        spawn_server_daemon(host, port)

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
    parser.add_argument('--no-launch', action='store_true', help="Do not auto-launch daemon if server is down")

    args = parser.parse_args()

    success, result = notify_status(
        status=args.status,
        title=args.title,
        message=args.msg,
        step=args.step,
        elapsed=args.elapsed,
        host=args.host,
        port=args.port,
        ensure_server=not args.no_launch
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
