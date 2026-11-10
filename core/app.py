#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AvatarHUD - Transparent Standing Desktop Work Companion
Main Application: pywebview Transparent Window + Bottle REST/SSE API Server
"""

import sys
import os
import json
import time
import queue
import threading
import argparse
import webbrowser
from bottle import Bottle, request, response, static_file, abort

# Set UTF-8 encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')

# Load Configuration
def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[Warning] Failed to load config.json: {e}")
    return {
        "host": "127.0.0.1",
        "port": 8765,
        "avatar_image": "default_avatar.png",
        "scale": 1.0,
        "window_width": 420,
        "window_height": 620,
        "always_on_top": True,
        "auto_idle_seconds": 30
    }

config = load_config()

# Global State
current_status = {
    "status": "idle",
    "title": "AvatarHUD 대기 중",
    "message": "작업 시작을 기다리고 있습니다. 모든 AI CLI와 실시간 연동됩니다.",
    "step": "",
    "elapsed": None,
    "timestamp": time.time()
}

sse_subscribers = []
sse_lock = threading.Lock()
settings_window = None

# Bottle Application
app = Bottle()

@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With'

@app.route('/', method=['GET', 'OPTIONS'])
def index():
    return static_file('index.html', root=STATIC_DIR)

@app.route('/settings', method=['GET', 'OPTIONS'])
def settings_page():
    return static_file('settings.html', root=STATIC_DIR)

@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=STATIC_DIR)

@app.route('/api/health')
def health():
    return {"status": "ok", "app": "AvatarHUD", "time": time.time()}

@app.route('/api/status', method='GET')
def get_status():
    response.content_type = 'application/json; charset=utf-8'
    return json.dumps(current_status, ensure_ascii=False)

@app.route('/api/status', method=['POST', 'OPTIONS'])
def update_status():
    if request.method == 'OPTIONS':
        return {}
    
    global current_status
    try:
        data = request.json or {}
    except Exception:
        data = {}

    status = data.get('status', 'working')
    title = data.get('title')
    message = data.get('message') or data.get('msg') or ''
    step = data.get('step', '')
    elapsed = data.get('elapsed')

    if not title:
        if status == 'working':
            title = '작업 수행 중...'
        elif status == 'done':
            title = '작업 완료!'
        elif status == 'error':
            title = '오류 발생'
        else:
            title = '대기 중'

    current_status = {
        "status": status,
        "title": title,
        "message": message,
        "step": step,
        "elapsed": elapsed,
        "timestamp": time.time()
    }

    # Broadcast to SSE clients
    payload = json.dumps(current_status, ensure_ascii=False)
    with sse_lock:
        dead = []
        for q in sse_subscribers:
            try:
                q.put_nowait(payload)
            except Exception:
                dead.append(q)
        for q in dead:
            sse_subscribers.remove(q)

    response.content_type = 'application/json; charset=utf-8'
    return json.dumps({"result": "success", "status": current_status}, ensure_ascii=False)

@app.route('/api/stream')
def sse_stream():
    response.content_type = 'text/event-stream; charset=utf-8'
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Connection'] = 'keep-alive'
    response.headers['X-Accel-Buffering'] = 'no'

    client_queue = queue.Queue(maxsize=20)
    with sse_lock:
        sse_subscribers.append(client_queue)

    # Initial status push
    initial_data = json.dumps(current_status, ensure_ascii=False)
    yield f"data: {initial_data}\n\n"

    try:
        while True:
            try:
                msg = client_queue.get(timeout=20)
                yield f"data: {msg}\n\n"
            except queue.Empty:
                yield ": keep-alive\n\n"
    except GeneratorExit:
        pass
    finally:
        with sse_lock:
            if client_queue in sse_subscribers:
                sse_subscribers.remove(client_queue)

@app.route('/api/config', method=['GET', 'POST', 'OPTIONS'])
def handle_config():
    if request.method == 'OPTIONS':
        return {}
    
    global config
    if request.method == 'POST':
        try:
            req_data = request.json or {}
            config.update(req_data)
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            # Broadcast config update to all connected SSE clients (e.g. main HUD window)
            payload = json.dumps({"type": "config", "config": config}, ensure_ascii=False)
            with sse_lock:
                for q in sse_subscribers:
                    try:
                        q.put_nowait(payload)
                    except Exception:
                        pass
        except Exception as e:
            abort(400, f"Failed to save config: {e}")

    response.content_type = 'application/json; charset=utf-8'
    return json.dumps(config, ensure_ascii=False)

@app.route('/api/open_settings', method=['GET', 'POST', 'OPTIONS'])
def open_settings_endpoint():
    if request.method == 'OPTIONS':
        return {}
    
    host = config.get('host', '127.0.0.1')
    port = config.get('port', 8765)
    open_settings_window(host, port)
    return {"result": "success"}


def open_settings_window(host, port):
    global settings_window
    url = f"http://{host}:{port}/settings"
    try:
        import webview
        if settings_window is not None:
            try:
                settings_window.destroy()
            except Exception:
                pass
            settings_window = None

        settings_window = webview.create_window(
            title='AvatarHUD 설정',
            url=url,
            width=520,
            height=680,
            resizable=True
        )
        return True
    except Exception as e:
        print(f"[AvatarHUD] Opening settings in web browser fallback: {e}")
        webbrowser.open(url)
        return True


def run_server(host, port):
    print(f"[AvatarHUD] REST / SSE API Server listening on http://{host}:{port}")
    try:
        app.run(host=host, port=port, quiet=True)
    except Exception as e:
        print(f"[AvatarHUD] Server error: {e}")


def main():
    parser = argparse.ArgumentParser(description="AvatarHUD Transparent Standing Desktop Companion")
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
        print("[AvatarHUD] Running in server-only mode. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[AvatarHUD] Server stopped.")
            sys.exit(0)

    if args.settings:
        print("[AvatarHUD] Opening settings...")
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
        print("[AvatarHUD] Error: pywebview is not installed. Run `pip install pywebview`.")
        sys.exit(1)

    url = f"http://{host}:{port}"
    width = config.get('window_width', 420)
    height = config.get('window_height', 620)
    on_top = config.get('always_on_top', True)

    print(f"[AvatarHUD] Launching transparent window ({width}x{height}, on_top={on_top})...")
    window_kwargs = {
        'title': 'AvatarHUD',
        'url': url,
        'width': width,
        'height': height,
        'frameless': True,
        'transparent': True,
        'on_top': on_top,
        'background_color': '#00000000'
    }
    if sys.platform == 'darwin':
        window_kwargs['easy_drag'] = True

    window = webview.create_window(**window_kwargs)

    webview.start(debug=False)


if __name__ == '__main__':
    main()
