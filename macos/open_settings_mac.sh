#!/usr/bin/env bash
# AvatarHUD - macOS Open Settings Script
set -e

echo "[AvatarHUD] Opening settings on macOS..."
if command -v open &> /dev/null; then
    open "http://127.0.0.1:8765/settings"
else
    echo "Visit: http://127.0.0.1:8765/settings in your browser."
fi
