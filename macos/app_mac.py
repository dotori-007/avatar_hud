#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AvatarHUD - macOS Optimized Launcher
Configures Cocoa/WebKit transparent window with macOS-specific behaviors.
"""

import sys
import os
import time
import argparse
import threading

# Add core directory to import paths
DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(DIR)
CORE_DIR = os.path.join(ROOT_DIR, 'core')
sys.path.insert(0, CORE_DIR)

from app import (
    app,
    config,
    load_config,
    run_server,
    open_settings_window
)


def apply_macos_window_tweaks(window):
    """
    Apply native Cocoa NSWindow adjustments for macOS when PyObjC is available.
    Ensures window stays visible across Mission Control spaces and floating layer.
    """
    if sys.platform != 'darwin':
        return

    try:
        from AppKit import (
            NSWindowCollectionBehaviorCanJoinAllSpaces,
            NSFloatingWindowLevel,
            NSColor
        )

        def configure_native():
            time.sleep(0.6)
            try:
                # pywebview Cocoa GUI instance handle
                native_window = getattr(window, 'native', None)
                if native_window:
                    # Keep mascot on all virtual desktops (Spaces)
                    native_window.setCollectionBehavior_(NSWindowCollectionBehaviorCanJoinAllSpaces)
                    native_window.setLevel_(NSFloatingWindowLevel)
                    native_window.setOpaque_(False)
                    native_window.setBackgroundColor_(NSColor.clearColor())
                    native_window.setHasShadow_(False)
                    print("[AvatarHUD macOS] Cocoa native window configured for Mission Control & Spaces.")
            except Exception as ex:
                print(f"[AvatarHUD macOS Note] Native tweak skipped: {ex}")

        t = threading.Thread(target=configure_native, daemon=True)
        t.start()
    except ImportError:
        # PyObjC optional, pywebview handles basic transparency without it
        pass


def main():
    parser = argparse.ArgumentParser(description="AvatarHUD macOS Companion")
    parser.add_argument('--server-only', action='store_true', help="Run server only without opening GUI window")
    parser.add_argument('--settings', action='store_true', help="Open settings window directly")
    parser.add_argument('--port', type=int, default=config.get('port', 8765), help="Server port (default: 8765)")
    parser.add_argument('--host', type=str, default=config.get('host', '127.0.0.1'), help="Server host (default: 127.0.0.1)")
    args = parser.parse_args()

    host = args.host
    port = args.port

    # Start Bottle server in background thread
    server_thread = threading.Thread(target=run_server, args=(host, port), daemon=True)
    server_thread.start()
    time.sleep(0.5)

    if args.server_only:
        print("[AvatarHUD macOS] Running in server-only mode. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[AvatarHUD macOS] Server stopped.")
            sys.exit(0)

    if args.settings:
        print("[AvatarHUD macOS] Opening settings...")
        open_settings_window(host, port)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(0)

    # Launch Transparent pywebview Window
    try:
        import webview
    except ImportError:
        print("[AvatarHUD macOS ERROR] pywebview is not installed.")
        print("[HINT] Run: pip install -r macos/requirements_mac.txt")
        sys.exit(1)

    url = f"http://{host}:{port}"
    width = config.get('window_width', 420)
    height = config.get('window_height', 620)
    on_top = config.get('always_on_top', True)

    print(f"[AvatarHUD macOS] Launching transparent window ({width}x{height}, on_top={on_top})...")
    window = webview.create_window(
        title='AvatarHUD',
        url=url,
        width=width,
        height=height,
        frameless=True,
        transparent=True,
        on_top=on_top,
        easy_drag=True,
        background_color='#00000000'
    )

    apply_macos_window_tweaks(window)
    webview.start(debug=False)


if __name__ == '__main__':
    main()
