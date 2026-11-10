# AvatarHUD (투명 누끼 스탠딩 데스크톱 HUD)

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)
[![OS Support](https://img.shields.io/badge/OS-Windows%20%7C%20macOS%20%7C%20Linux-blue.svg)](#1-os별-상세-셋업-가이드)
[![CLI Support](https://img.shields.io/badge/CLI-Antigravity%20%7C%20Codex%20%7C%20Claude-blueviolet.svg)](#2-사용하는-ai-cli별-상세-셋업-가이드)

사용자가 지정한 투명 누끼 스탠딩 인물/캐릭터(Transparent Cutout Standing PNG)가 윈도우, 맥북(macOS), 리눅스 바탕화면에 자연스럽게 상시 상주하며, Antigravity CLI, Codex CLI, Claude CLI 에이전트의 실시간 작업 상태와 최종 완료 보고를 시각화해 주는 초경량 데스크톱 HUD 시스템입니다.

---

## 주요 특징 (Key Features)

1. **오로지 투명 누끼 스탠딩 모드 전용 (Transparent Cutout Standing Only)**:
   - 불필요한 사각 박스나 불투명 프레임을 배제하고, 배경이 투명한 인물/캐릭터 스탠딩 일러스트만 바탕화면에 자연스럽게 렌더링됩니다.
2. **크로스 플랫폼 지원 (Windows, macOS MacBook, Linux)**:
   - 윈도우 데스크톱 및 Apple Silicon(M1/M2/M3/M4) / Intel MacBook, Linux 환경 지원.
   - macOS Cocoa WKWebView 기반 투명 프레임 및 Mission Control 가상 데스크톱(Spaces) 상주 지원.
3. **상시 스탠딩 상주 (Persistent Desktop Companion)**:
   - 화면에서 숨거나 사라지지 않고 항상 바탕화면(원하는 위치)에 상주합니다.
   - 캐릭터를 마우스/트랙패드로 자유롭게 드래그하여 원하는 위치로 옮길 수 있으며, 휠 스크롤로 크기를 자유롭게 확대/축소할 수 있습니다.
4. **만화풍 순백색 다이내믹 말풍선 (Clean Pure White Speech Bubble)**:
   - antiy-zunda 시그니처 순백색 카드 UI와 바운스 인 애니메이션 완벽 구현.
   - **작업 중 (Working)**: 블루 소프트 칩 + 단계(Step) 배지 + 부드러운 상태 표시.
   - **작업 완료 (Done)**: 경쾌한 바운스 효과 + 에메랄드 그린 완료 배지 + 소요 시간 태그 및 결과 요약.
   - **오류 발생 (Error)**: 레드 경고 배지 + 예외 상황 요약.
   - **대기 상태 (Idle)**: 화면을 가리지 않는 미니멀 순백색 말풍선.
5. **전용 그래픽 환경설정창 (Settings Window)**:
   - 탐색기 및 Finder에서 투명 누끼 이미지를 끌어다 놓기만 하면 즉시 반영되는 드래그 앤 드롭 업로더.
   - 투명도 확인을 위한 실시간 체커보드 프리뷰.
   - 캐릭터 크기 배율(Scale) 슬라이더 (50% ~ 200%).
   - 말풍선 상태별 실시간 발화 테스트 기능.
6. **3대 메이저 AI CLI 완벽 지원**:
   - Antigravity CLI, Codex CLI, Claude CLI (Claude Code) 전용 연동 디렉토리 및 규칙 파일 완비.
7. **클린 UI 표준**:
   - 프로젝트 전체 소스코드, UI, 문서에서 이모티콘을 배제한 깔끔하고 신뢰도 높은 디자인.

---

## 시스템 아키텍처

```mermaid
flowchart TD
    subgraph Clients["3대 AI CLI 및 외부 트리거"]
        AG["Antigravity CLI 에이전트<br/>(antigravity/)"]
        CX["Codex CLI 에이전트<br/>(codex/)"]
        CL["Claude CLI / Code<br/>(claude/)"]
        CLI["공용 CLI 도구 (notify.py)"]
    end

    subgraph CoreEngine["AvatarHUD 코어 엔진 (:8765)"]
        Server["Bottle REST / SSE 서버<br/>(core/app.py)"]
        State["상태 관리자<br/>(working, done, idle, error)"]
        Stream["실시간 SSE 브로드캐스터"]
    end

    subgraph Platforms["운영체제별 뷰포트"]
        WinView["Windows 투명 오버레이<br/>(DWM Webview2)"]
        MacView["macOS 투명 오버레이<br/>(Cocoa WKWebView)"]
        LinuxView["Linux 투명 오버레이<br/>(WebKitGTK)"]
    end

    subgraph Overlay["투명 데스크톱 뷰"]
        Standing["투명 누끼 스탠딩 캐릭터<br/>(드래그 이동 / 휠 크기 조절)"]
        Bubble["동적 반응형 순백색 말풍선<br/>진행 바, 완료 배지, 상태 칩"]
    end

    AG --> CLI
    CX --> CLI
    CL --> CLI
    CLI -->|POST /api/status| Server
    Server --> State
    State --> Stream
    Stream --> WinView
    Stream --> MacView
    Stream --> LinuxView
    WinView --> Standing
    WinView --> Bubble
    MacView --> Standing
    MacView --> Bubble
    LinuxView --> Standing
    LinuxView --> Bubble
```

---

## 프로젝트 디렉토리 구조

```
avatar_hud/
├── README.md               # 프로젝트 전체 안내서
├── run.bat                 # 윈도우 원클릭 실행 스크립트
├── run.sh                  # macOS / Linux 원클릭 실행 스크립트
├── open_settings.bat       # 환경설정창 원클릭 실행 스크립트
├── requirements.txt        # 기본 파이썬 패키지 목록
├── notify.py               # 루트 단축 알림 래퍼 도구
├── macos/                  # [macOS MacBook 호환 전용 디렉토리]
│   ├── README.md           # 맥북 전용 완벽 가이드
│   ├── run_mac.sh          # 맥북 원클릭 런처 (Cocoa 투명 윈도우)
│   ├── setup_mac.sh        # 맥북 가상환경 및 PyObjC 의존성 자동 설치기
│   ├── open_settings_mac.sh # 맥북 브라우저 설정창 원클릭 호출 스크립트
│   ├── app_mac.py          # macOS 최적화 런처 (Spaces/Mission Control 연동)
│   ├── notify_mac.py       # macOS 터미널/쉘 전용 알림 어댑터
│   └── requirements_mac.txt # macOS 전용 의존성 목록
├── core/                   # [공통 코어 엔진]
│   ├── app.py              # pywebview 투명 윈도우 + 내장 REST/SSE 서버
│   ├── notify.py           # 상태 전송 메인 라이브러리 및 CLI 도구
│   ├── config.json         # HUD 기본 설정 (포트, 이미지, 스케일 등)
│   ├── test_flow.py        # 작업중 -> 갱신 -> 완료 -> 대기 시나리오 자동 검증 스크립트
│   └── static/             # 투명 오버레이 프론트엔드
│       ├── index.html      # 메인 뷰 (스탠딩 캐릭터 + 순백색 말풍선)
│       ├── settings.html   # 드래그 앤 드롭 캐릭터 교체 설정창
│       ├── style.css       # 투명 윈도우 및 말풍선 애니메이션 스타일시트
│       ├── app.js          # SSE 수신, 휠 줌, 실시간 상태 반영 UI 로직
│       └── default_avatar.png # 기본 제공 투명 누끼 일러스트
├── antigravity/            # [Antigravity CLI 전용]
│   ├── README.md           # Antigravity 연동 가이드
│   ├── skills/
│   │   └── avatar-hud/SKILL.md # Antigravity 에이전트 자동 보고 스킬
│   ├── hook.py             # 파이썬 수명주기 훅 래퍼
│   └── install_skill.bat   # 에이전트 스킬 원클릭 등록 배치파일
├── codex/                  # [Codex CLI 전용]
│   ├── README.md           # Codex 연동 가이드
│   ├── AGENTS.md           # Codex 에이전트 시스템 지침
│   ├── notify_codex.py     # Codex 최적화 알림 스크립트
│   └── codex_config.json   # Codex 설정 템플릿
└── claude/                 # [Claude CLI / Code 전용]
    ├── README.md           # Claude 연동 가이드
    ├── CLAUDE.md           # Claude Code 자동 인식 프로젝트 규칙
    ├── notify_claude.py    # Claude 전용 알림 어댑터
    └── setup_claude.bat    # Claude 연동 보조 배치파일
```

---

## 1. OS별 상세 셋업 가이드

### A. Windows 환경 (Windows 10 / 11)

1. **사전 준비**:
   * Python 3.10 이상 설치 및 PATH 등록.
2. **패키지 설치**:
   ```cmd
   pip install -r requirements.txt
   ```
3. **실행**:
   * 프로젝트 루트의 `run.bat`을 더블 클릭하여 실행합니다.
   * 또는 명령 프롬프트 / PowerShell에서 직접 실행:
     ```cmd
     python core\app.py
     ```
4. **설정창 열기**:
   * `open_settings.bat`을 더블 클릭하거나, 바탕화면 캐릭터를 마우스 우클릭합니다.

---

### B. macOS 환경 (MacBook Air / Pro, Mac mini, Mac Studio)

Apple Silicon (M1, M2, M3, M4) 및 Intel 기반 Mac을 모두 지원합니다.

1. **사전 준비**:
   * Homebrew 및 Python 3.9 이상:
     ```bash
     brew install python
     ```
2. **원클릭 환경 구성 및 의존성 설치**:
   ```bash
   # 가상환경 .venv_mac 생성, PyObjC 및 필요 패키지 설치, 스크립트 실행 권한 부여
   ./macos/setup_mac.sh
   ```
3. **실행**:
   * 터미널에서 아래 스크립트를 실행합니다:
     ```bash
     ./macos/run_mac.sh
     # 또는 루트 디렉토리에서
     ./run.sh
     ```
4. **설정창 열기**:
   ```bash
   ./macos/open_settings_mac.sh
   # 또는 브라우저에서 http://127.0.0.1:8765/settings 접속
   ```
5. **macOS 특화 기능**:
   * Mission Control 가상 데스크톱(Spaces)을 넘겨도 캐릭터가 항상 고정 상주합니다.
   * 트랙패드 두 손가락 스크롤로 크기 확대/축소 및 마우스 드래그 이동을 지원합니다.

---

### C. Linux 환경 (Ubuntu, Debian, Fedora)

1. **사전 준비 (WebKitGTK 및 파이썬)**:
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip python3-venv libwebkit2gtk-4.0-dev
   ```
2. **패키지 설치**:
   ```bash
   pip3 install -r requirements.txt
   ```
3. **실행**:
   ```bash
   ./run.sh
   # 또는
   python3 core/app.py
   ```

---

## 2. 사용하는 AI CLI별 상세 셋업 가이드

각 CLI 에이전트가 코딩 및 작업을 진행할 때 스스로 notify 도구를 호출하여 바탕화면 캐릭터 말풍선에 보고하도록 사전에 완벽히 구성되어 있습니다.

---

### A. Antigravity CLI (Google DeepMind)

Antigravity CLI 에이전트가 작업 착수 시점, 중간 단계, 최종 완료 시점에 스스로 말풍선을 업데이트하도록 스킬을 등록합니다.

1. **스킬 등록**:
   * **Windows**:
     `antigravity\install_skill.bat`을 실행합니다. (자동으로 `%USERPROFILE%\.gemini\config\skills\avatar-hud\SKILL.md`로 복사 및 등록)
   * **macOS / Linux**:
     ```bash
     mkdir -p ~/.gemini/config/skills/avatar-hud
     cp antigravity/skills/avatar-hud/SKILL.md ~/.gemini/config/skills/avatar-hud/SKILL.md
     ```
2. **작동 방식**:
   * 사용자가 Antigravity CLI에서 작업 지시 시 에이전트가 자동으로 스킬을 읽고 도구 실행 전후 `core/notify.py`를 호출하여 말풍선에 실시간 보고합니다.
3. **수동 호출 테스트**:
   ```bash
   python core/notify.py --status working --title "Antigravity 분석 중" --msg "코드베이스 전수 검사 진행 중..." --step "1/3"
   python core/notify.py --status done --title "Antigravity 완료!" --msg "모든 작업이 성공적으로 끝났습니다."
   ```

---

### B. Codex CLI (OpenAI Codex)

Codex CLI 에이전트가 코드 작업 시 말풍선에 진행 상황을 보고하도록 시스템 프롬프트 지침을 연동합니다.

1. **지침 파일 연동**:
   * `codex/AGENTS.md` 파일을 작업 대상 프로젝트 루트로 복사합니다:
     ```bash
     # Windows
     copy codex\AGENTS.md <your_project_dir>\AGENTS.md

     # macOS / Linux
     cp codex/AGENTS.md <your_project_dir>/AGENTS.md
     ```
   * 또는 사용자의 글로벌 Codex 프롬프트 지침에 `codex/AGENTS.md` 내용을 추가합니다.
2. **작동 방식**:
   * Codex CLI 에이전트가 작업을 수행하기 전과 후, 오류 발생 시 `codex/notify_codex.py`를 호출합니다.
3. **수동 호출 테스트**:
   ```bash
   python codex/notify_codex.py --status working --title "Codex 분석 중" --msg "코드 구조 분석을 시작합니다." --step "1/2"
   python codex/notify_codex.py --status done --title "Codex 완료" --msg "요청된 코드 구현을 마쳤습니다."
   ```

---

### C. Claude CLI / Claude Code (Anthropic)

Anthropic의 Claude Code CLI 에이전트가 시작, 빌드/테스트, 최종 완료 시점에 스스로 말풍선을 업데이트하도록 프로젝트 규칙을 연동합니다.

1. **프로젝트 규칙(CLAUDE.md) 연동**:
   * `claude/CLAUDE.md` 파일을 작업 대상 프로젝트 루트로 복사합니다:
     ```bash
     # Windows
     copy claude\CLAUDE.md <your_project_dir>\CLAUDE.md

     # macOS / Linux
     cp claude/CLAUDE.md <your_project_dir>/CLAUDE.md
     ```
2. **작동 방식**:
   * Claude Code가 프로젝트 디렉토리를 열 때 `CLAUDE.md`를 자동으로 로드하여, 주요 명령어 실행 전후 `claude/notify_claude.py`를 호출합니다.
3. **수동 호출 테스트**:
   ```bash
   python claude/notify_claude.py --status working --title "Claude 작업 중" --msg "버그 픽스 및 리팩토링 진행 중..." --step "1/3"
   python claude/notify_claude.py --status done --title "Claude 완료!" --msg "코드 리팩토링 및 테스트가 성공했습니다."
   ```

---

## 환경설정창 & 캐릭터 이미지 교체 가이드

사용자가 연예인 사진, 버튜버, 애니메이션 등 원하는 투명 누끼 PNG를 아주 쉽게 넣고 변경할 수 있도록 전용 그래픽 환경설정창을 제공합니다.

### 설정창 여는 방법
1. **바탕화면 캐릭터 우클릭**: 바탕화면에 서 있는 캐릭터를 마우스 오른쪽 클릭하면 즉시 설정창이 열립니다.
2. **호버 툴바의 SET 버튼 클릭**: 캐릭터에 마우스를 올렸을 때 나타나는 SET 버튼 클릭.
3. **원클릭 실행 스크립트**:
   * Windows: `open_settings.bat` 실행
   * macOS: `./macos/open_settings_mac.sh` 실행
   * 브라우저: `http://127.0.0.1:8765/settings` 접속

### 이미지 변경 기능
* **드래그 앤 드롭 (Drag & Drop)**: 탐색기 및 Finder에서 투명 누끼 PNG/WebP 파일을 설정창의 점선 영역으로 끌어다 놓기만 하면 즉시 바탕화면에 실시간 반영됩니다.
* **실시간 체커보드 투명도 미리보기**: 투명 알파 채널이 잘 뚫려 있는지 체커보드 프리뷰로 확인 가능.
* **크기 배율 슬라이더**: 50% ~ 200% 배율을 슬라이더로 조절하여 바탕화면에 딱 맞는 크기로 맞춤.
* **말풍선 실시간 테스트**: 작업 중, 완료, 대기 상태를 설정창에서 즉시 버튼으로 테스트 가능.
* **기본 즌다몬 복구**: 언제든 원클릭으로 기본 즌다몬 스탠딩으로 초기화 가능.

---

## REST API 레퍼런스

HUD는 로컬 `http://127.0.0.1:8765`에서 경량 HTTP 서비스를 제공합니다:

| 엔드포인트 | 메서드 | 설명 | 페이로드 예시 |
|------------|--------|------|---------------|
| `/api/status` | `POST` | 상태 업데이트 및 SSE 브로드캐스트 | `{"status": "working", "title": "...", "message": "...", "step": "1/2"}` |
| `/api/status` | `GET` | 현재 상태 JSON 조회 | - |
| `/api/stream` | `GET` | 실시간 Server-Sent Events (SSE) 스트림 | - |
| `/api/config` | `GET`/`POST` | 이미지 경로, 스케일 등 환경설정 조회/저장 | `{"scale": 1.2}` |
| `/api/open_settings` | `POST` | 환경설정창 열기 | - |
| `/api/health` | `GET` | 서버 헬스체크 | - |

---

## 검증 스크립트 실행

```bash
# 서버 기동 후 자동 흐름 검증 실행
python core/test_flow.py
```
검증 항목: 서버 헬스체크 -> 작업 착수(1/3) -> 진행 갱신(2/3) -> 작업 완료 -> 대기 복귀 4단계 상태 전이 100% 자동 통과.

---

## 라이선스
MIT License (c) 2026 dotori-007
