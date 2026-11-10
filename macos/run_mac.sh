#!/usr/bin/env bash
# AvatarHUD - macOS Runner Script
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$DIR/.." && pwd)"

echo "==================================================="
echo "  AvatarHUD - Launching on macOS"
echo "==================================================="

# Activate virtual environment if available
if [ -d "$ROOT_DIR/.venv_mac" ]; then
    source "$ROOT_DIR/.venv_mac/bin/activate"
fi

# Run macOS optimized launcher
PYTHON_CMD="python3"
if command -v python &> /dev/null; then
    PYTHON_CMD="python"
fi

"$PYTHON_CMD" "$DIR/app_mac.py" "$@"
