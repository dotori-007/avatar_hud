#!/usr/bin/env bash
# AvatarHUD - Root Universal POSIX / macOS Runner Script
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "$(uname)" = "Darwin" ]; then
    # On macOS, delegate to macos/run_mac.sh
    exec "$DIR/macos/run_mac.sh" "$@"
else
    # On Linux/other POSIX, run core/app.py
    PYTHON_CMD="python3"
    if ! command -v python3 &> /dev/null; then
        PYTHON_CMD="python"
    fi
    exec "$PYTHON_CMD" "$DIR/core/app.py" "$@"
fi
