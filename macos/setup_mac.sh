#!/usr/bin/env bash
# AvatarHUD - macOS Environment Setup Script
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$DIR/.." && pwd)"

echo "==================================================="
echo "  AvatarHUD macOS Setup (Apple Silicon & Intel Mac)"
echo "==================================================="

# 1. Check Python3
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 is not installed."
    echo "[HINT] Install python via Homebrew: brew install python"
    exit 1
fi

PYTHON_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "[INFO] Found Python version: $PYTHON_VER"

# 2. Setup Virtual Environment
VENV_DIR="$ROOT_DIR/.venv_mac"
if [ ! -d "$VENV_DIR" ]; then
    echo "[INFO] Creating virtual environment at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

echo "[INFO] Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# 3. Upgrade pip and install dependencies
echo "[INFO] Installing macOS dependencies (PyObjC, pywebview, Bottle, Pillow)..."
pip install --upgrade pip setuptools wheel
pip install -r "$DIR/requirements_mac.txt"

# 4. Make scripts executable
chmod +x "$DIR/run_mac.sh"
chmod +x "$DIR/open_settings_mac.sh"
if [ -f "$ROOT_DIR/run.sh" ]; then
    chmod +x "$ROOT_DIR/run.sh"
fi

echo "==================================================="
echo "[SUCCESS] macOS setup completed successfully!"
echo "Run './macos/run_mac.sh' or './run.sh' to launch."
echo "==================================================="
