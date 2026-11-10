# 💬 AvatarHUD (투명 누끼 스탠딩 데스크톱 HUD)

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)
[![CLI Support](https://img.shields.io/badge/CLI-Antigravity%20%7C%20Codex%20%7C%20Claude-blueviolet.svg)](#-3대-cli-지원-안내)

사용자가 지정한 **투명 누끼 스탠딩 인물/캐릭터(Transparent Cutout Standing PNG)**가 윈도우 바탕화면에 자연스럽게 상시 상주하며, **Antigravity CLI**, **Codex CLI**, **Claude CLI** 에이전트의 실시간 작업 상태와 최종 완료 보고를 시각화해 주는 초경량 데스크톱 HUD 시스템입니다.

---

## 🎯 핵심 특징 (Key Highlights)

1. **오로지 투명 누끼 스탠딩 모드 전용 (Transparent Cutout Only)**:
   - 불필요한 사각 박스나 불투명 프레임을 일절 배제하고, 배경이 투명한 인물/캐릭터 스탠딩 일러스트만 바탕화면에 자연스럽게 렌더링됩니다.
2. **상시 스탠딩 상주 (Persistent Desktop Companion)**:
   - 화면에서 숨거나 사라지지 않고 항상 바탕화면(원하는 위치)에 상주합니다.
   - 캐릭터를 마우스로 자유롭게 드래그하여 원하는 위치로 옮길 수 있으며, 마우스 휠로 크기를 자유롭게 확대/축소할 수 있습니다.
3. **만화풍 & 모던 다이내믹 말풍선 (Dynamic Speech Bubble UX)**:
   - 🔄 **작업 중 (Working)**: 블루/시안 네온 펄스 인디케이터 + 실시간 단계(Step) 표시 + 부드러운 타이핑 애니메이션.
   - ✅ **작업 완료 (Done)**: 경쾌한 바운스 효과 + 에메랄드 그린 완료 배지 + 소요 시간 및 1~3줄 핵심 요약 보고.
   - ⚠️ **오류 발생 (Error)**: 로즈 레드 경고 배지 + 예외 상황 요약.
   - 💤 **대기 상태 (Idle)**: 화면을 가리지 않는 미니멀 반투명 말풍선.
4. **3대 메이저 AI CLI 완벽 지원**:
   - **Antigravity CLI**, **Codex CLI**, **Claude CLI (Claude Code)** 전용 연동 디렉토리와 규칙 파일 완비.

---

## 🏗️ 시스템 아키텍처

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
        State["상태 관리자<br/>(working ↔ done ↔ idle ↔ error)"]
        Stream["실시간 SSE 브로드캐스터"]
    end

    subgraph Overlay["투명 데스크톱 뷰 (pywebview)"]
        Standing["투명 누끼 스탠딩 캐릭터<br/>(드래그 이동 / 휠 크기 조절)"]
        Bubble["동적 반응형 말풍선<br/>• 타이핑 효과 • 진행 바 • 완료 배지"]
    end

    AG --> CLI
    CX --> CLI
    CL --> CLI
    CLI -->|POST /api/status| Server
    Server --> State
    State --> Stream
    Stream -->|실시간 이벤트 스트림| Overlay
    Overlay --> Standing
    Overlay --> Bubble
```

---

## 📂 프로젝트 디렉토리 구조

```
avatar_hud/
├── README.md               # 프로젝트 전체 안내서
├── run.bat                 # 투명 HUD 원클릭 실행 스크립트
├── requirements.txt        # 필요 파이썬 패키지 목록
├── notify.py               # 루트 단축 알림 래퍼 도구
├── core/                   # [공통 코어 엔진]
│   ├── app.py              # pywebview 투명 윈도우 + 내장 REST/SSE 서버
│   ├── notify.py           # 상태 전송 메인 라이브러리/CLI
│   ├── config.json         # HUD 기본 설정 (포트, 이미지, 스케일 등)
│   ├── test_flow.py        # 작업중 → 갱신 → 완료 → 대기 시나리오 자동 검증 스크립트
│   └── static/             # 투명 오버레이 프론트엔드
│       ├── index.html      # 메인 뷰 (스탠딩 캐릭터 + 말풍선)
│       ├── style.css       # 투명 윈도우 및 말풍선 애니메이션 스타일시트
│       ├── app.js          # SSE 수신, 휠 줌, 말풍선 타이핑 UI 로직
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

## 🚀 빠른 시작 (Quick Start)

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. AvatarHUD 실행
```bash
# 윈도우 원클릭 실행
run.bat

# 또는 파이썬 직접 실행
python core/app.py
```

### 3. 알림 테스트 (수동 호출)
새 터미널 창을 열고 아래 명령어로 캐릭터 말풍선이 실시간 반응하는지 확인합니다:
```bash
# 1) 작업 착수 알림
python notify.py --status working --title "데이터 분석 중" --msg "10만 건의 트랜잭션을 필터링하고 있습니다..." --step "1/3"

# 2) 진행 갱신 알림
python notify.py --status working --title "인공지능 모델 검증" --msg "테스트 세트 평가를 진행 중입니다..." --step "2/3"

# 3) 작업 완료 알림
python notify.py --status done --title "분석 및 모델 검증 완료!" --msg "정확도 98.4% 달성. 리포트 생성을 마쳤습니다." --elapsed 14

# 4) 대기 모드 복귀
python notify.py --status idle
```

---

## 🤖 3대 CLI 지원 안내

각 CLI 에이전트가 코딩 및 작업을 진행할 때 스스로 `notify.py`를 호출하여 바탕화면 캐릭터 말풍선에 보고하도록 사전에 완벽히 구성되어 있습니다.

### 1. Antigravity CLI ([`antigravity/`](./antigravity/README.md))
* `antigravity/install_skill.bat`을 실행하면 `%USERPROFILE%\.gemini\config\skills\avatar-hud\SKILL.md`로 자동 설치됩니다.
* Antigravity 세션에서 에이전트가 도구 착수/진행/완료 시 스스로 말풍선을 업데이트합니다.

### 2. Codex CLI ([`codex/`](./codex/README.md))
* `codex/AGENTS.md` 지침을 복사하여 사용자의 Codex 작업 환경에 배치합니다.
* Codex 에이전트가 단계별 실행 전후로 `codex/notify_codex.py`를 호출합니다.

### 3. Claude CLI / Claude Code ([`claude/`](./claude/README.md))
* 작업 대상 프로젝트 루트에 `claude/CLAUDE.md`를 위치시킵니다.
* Claude Code 에이전트가 시작, 중간 빌드/테스트, 최종 완료 시점에 스스로 `claude/notify_claude.py`를 호출합니다.

---

## 🎨 캐릭터 커스터마이징

* **인물 사진 / 다른 캐릭터로 변경**:
  * 캐릭터 이미지 위에 마우스를 올리면 좌측 상단에 나타나는 **📷 카메라 버튼**을 클릭하여 배경이 투명한 PNG/WebP 파일을 선택하면 즉시 교체됩니다.
  * 또는 `core/static/default_avatar.png` 파일을 원하는 이미지로 덮어쓰기만 해도 됩니다.
* **크기 확대 / 축소**:
  * 캐릭터 위에서 **마우스 휠**을 위/아래로 굴리거나 ➕/➖ 버튼을 클릭합니다.
* **위치 이동**:
  * 캐릭터 본체를 마우스 왼쪽 버튼으로 **클릭한 채 드래그**하면 화면 원하는 구석으로 자유롭게 이동됩니다.

---

## 📡 REST API 레퍼런스

HUD는 로컬 `http://127.0.0.1:8765`에서 경량 HTTP 서비스를 제공합니다:

| 엔드포인트 | 메서드 | 설명 | 페이로드 예시 |
|------------|--------|------|---------------|
| `/api/status` | `POST` | 상태 업데이트 및 SSE 브로드캐스트 | `{"status": "working", "title": "...", "message": "...", "step": "1/2"}` |
| `/api/status` | `GET` | 현재 상태 JSON 조회 | - |
| `/api/stream` | `GET` | 실시간 Server-Sent Events (SSE) 스트림 | - |
| `/api/config` | `GET`/`POST` | 이미지 경로, 스케일 등 환경설정 조회/저장 | `{"scale": 1.2}` |
| `/api/health` | `GET` | 서버 헬스체크 | - |

---

## 📜 라이선스
MIT License (c) 2026 dotori-007
