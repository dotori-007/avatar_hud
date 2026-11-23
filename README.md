# 🎭 AvatarHUD — Desktop Transparent Standing HUD for AI CLI Tools

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)
[![OS Support](https://img.shields.io/badge/OS-Windows%20%7C%20macOS%20%7C%20Linux-blue.svg)](#-installation--setup)
[![CLI Support](https://img.shields.io/badge/CLI-Antigravity%20%7C%20Codex%20%7C%20Claude-blueviolet.svg)](#-agent-self-setup-protocol)

An ultra-lightweight desktop HUD system where a user-specified transparent cutout standing character illustration permanently resides on your desktop (Windows, macOS, Linux), visualizing task status, execution steps, and completion reports in real time with dynamic comic speech bubbles for **Google Antigravity CLI, OpenAI Codex CLI, and Anthropic Claude Code**.

---

## ✨ Key Features

1. **Transparent Cutout Standing Only**:
   - Eliminates opaque window borders and backgrounds, cleanly rendering only the character illustration directly onto the desktop.
2. **Comprehensive Image Format Support (PNG, WebP, JPG, GIF, BMP, SVG, AVIF, TIFF, ICO)**:
   - Supports all major raster and vector graphic formats.
   - Drag-and-drop or select images via native file picker.
3. **Dynamic Speech Bubble Anchoring**:
   - As you scale the character (0.5x ~ 2.0x) using the mouse wheel or settings slider, speech bubbles dynamically track the top-most boundary of the character head.
   - Prevents awkward gaps during scale-down and avoids overlapping during scale-up while staying within screen bounds.
4. **Cross-Platform Compatibility (Windows, macOS, Linux)**:
   - Native Windows layered window transparency (`pywin32`) and macOS Cocoa `WKWebView` transparent framing with Spaces/Mission Control persistence.
5. **Persistent Desktop Companion**:
   - Freely reposition character anywhere on desktop via drag-and-drop; scale on the fly using mouse wheel scrolling.
6. **Pure White Dynamic Speech Bubble**:
   - Clean comic card UI with smooth bounce-in animations:
     - **Working**: Soft blue chip + Step badge + gentle status indicator.
     - **Done**: Energetic bounce animation + Emerald green success badge + elapsed time tag & summary.
     - **Error**: Crimson alert badge + exception description.
     - **Idle**: Minimal unobtrusive speech bubble.
7. **Dedicated Graphical Settings Window**:
   - Drag-and-drop image uploader with instant live preview.
   - Checkerboard background for testing transparency.
   - Character scaling slider (50% ~ 200%).
   - Live speech bubble testing controls for all states.
8. **Native Integration for Major AI CLI Agents**:
   - Pre-configured skills and instruction templates for Antigravity, OpenAI Codex, and Anthropic Claude Code.
9. **One-Command Autonomous Agent Self-Setup (`setup_cli.py`)**:
   - Autonomous CLI setup script automatically detects the host OS, repository paths, and binds global/local skills with a single command (`python setup_cli.py --auto`).
10. **Auto-Daemon Launcher**:
    - When a CLI agent dispatches a notification via `python notify.py`, the HUD automatically spawns as a background daemon if not already running.

---

## 🤖 Agent Self-Setup Protocol

> [!TIP]
> If you are an AI CLI Agent (Antigravity, Codex, Claude Code), run the following single command to configure rules and start the desktop HUD automatically:
>
> ```bash
> python setup_cli.py --auto
> ```
>
> What this command performs automatically:
> 1. Detects OS (Windows, macOS, Linux) and repository absolute path
> 2. Generates & registers Antigravity skill (`~/.gemini/config/skills/avatar-hud/SKILL.md`)
> 3. Generates & registers OpenAI Codex instructions (`~/.codex/AGENTS.md`)
> 4. Generates & registers Anthropic Claude Code rules (`~/.claude/CLAUDE.md`)
> 5. Verifies server status and auto-launches background daemon
> 6. Reports successful initialization directly through the desktop speech bubble

---

## 🏗️ Architecture

```
avatar_hud/
├── core/                  # Core HUD engine & UI
│   ├── app.py             # Desktop transparent window & HTTP server
│   ├── index.html         # HUD viewport with transparent canvas & bubble UI
│   ├── settings.html      # Graphical settings panel (drag & drop, scale slider)
│   ├── config.json        # Persistent user configurations
│   └── default_avatar.png # Default standing illustration asset
├── notify.py              # CLI notification sender script (HTTP socket client)
├── setup_cli.py           # Multi-agent automated configuration engine
├── run.bat                # Windows launcher script
├── run.sh                 # macOS / Linux launcher script
├── open_settings.bat      # Quick launcher for settings panel
├── antigravity/           # Antigravity CLI skill definitions & templates
├── claude/                # Claude Code CLI instruction templates
├── codex/                 # OpenAI Codex CLI instruction templates
├── macos/                 # macOS native launcher & Cocoa integration helpers
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Windows 10/11, macOS (Intel / Apple Silicon), or Linux

### Quick Install
```bash
# Clone the repository
git clone https://github.com/dotori-007/avatar_hud.git
cd avatar_hud

# Install Python requirements
pip install -r requirements.txt

# Run automated setup for all CLI agents
python setup_cli.py --auto

# Or launch HUD manually
# Windows:
.\run.bat
# macOS / Linux:
./run.sh
```

---

## 💬 Usage & Notification Dispatch

Send real-time visual progress updates from scripts, terminal sessions, or AI workflows:

```bash
# Step 1: Task inception
python notify.py --title "Refactoring" --step "Analyzing codebase" --status working

# Step 2: Intermediate step
python notify.py --title "Refactoring" --step "Applying optimizations" --status working

# Step 3: Completion report
python notify.py --title "Refactoring" --step "All tests passed (3.2s)" --status done

# Error alert
python notify.py --title "Build Failed" --step "Syntax error at line 42" --status error
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).