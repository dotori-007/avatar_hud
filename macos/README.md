# AvatarHUD macOS (MacBook) 호환 가이드

Apple Silicon(M1, M2, M3, M4) 및 Intel 기반 Mac에서 AvatarHUD를 원활하게 실행하고 AI CLI(Antigravity, Codex, Claude CLI)와 연동하는 전용 가이드입니다.

---

## 지원 사양 및 환경

* **지원 기기**: MacBook Air, MacBook Pro, Mac mini, Mac Studio, iMac
* **지원 칩셋**: Apple Silicon (M1 / M2 / M3 / M4) 및 Intel x86_64 Mac
* **지원 OS**: macOS Monterey (12), Ventura (13), Sonoma (14), Sequoia (15) 이상
* **필수 요소**: Python 3.9 이상 (Homebrew 또는 공식 파이썬)

---

## 빠른 시작 (Quick Start on macOS)

### 1단계: 환경 자동 설정
터미널을 열고 프로젝트 루트 또는 `macos/` 폴더에서 설정 스크립트를 실행합니다:
```bash
# macOS 전용 의존성 자동 설치 (가상환경 .venv_mac 생성 및 PyObjC, pywebview 설치)
./macos/setup_mac.sh
```

### 2단계: AvatarHUD 실행
```bash
# 맥북 전용 런처 실행 (투명 Cocoa/WebKit 윈도우 생성)
./macos/run_mac.sh

# 또는 루트 디렉토리에서 실행
./run.sh
```

### 3단계: 환경설정창 열기
```bash
# 브라우저 또는 설정창 원클릭 호출
./macos/open_settings_mac.sh
```
또는 브라우저에서 `http://127.0.0.1:8765/settings` 주소로 접속하여 누끼 이미지를 드래그 앤 드롭으로 변경할 수 있습니다.

---

## macOS 전용 최적화 특징

1. **Cocoa WKWebView 투명 프레임**:
   * macOS의 Cocoa 그래픽 윈도우 엔진을 직접 활용하여 사각 프레임 없는 순수 알파 채널 투명 렌더링을 지원합니다.
2. **Mission Control 및 가상 데스크톱(Spaces) 연동**:
   * 트랙패드로 가상 데스크톱을 넘겨도 캐릭터가 사라지지 않고 항상 화면에 머무르도록 `NSWindowCollectionBehaviorCanJoinAllSpaces` 옵션이 적용됩니다.
3. **트랙패드 제스처 및 다이내믹 말풍선 앵커링**:
   * 캐릭터 위에 마우스 커서를 올리고 트랙패드 두 손가락 스크롤을 통해 부드럽게 크기를 50% ~ 200% 배율로 확대/축소할 수 있습니다.
   * 크기 조절 시 말풍선이 캐릭터 정수리 모서리를 실시간 추적하여 항상 머리 바로 위에 밀착 배치됩니다.
4. **폭넓은 이미지 포맷 지원**:
   * PNG뿐만 아니라 WebP, JPG, GIF, BMP, SVG, AVIF, TIFF, ICO 등 모든 이미지 포맷을 지원합니다.
5. **드래그 이동 지원**:
   * 캐릭터 본체를 클릭한 채로 드래그하면 화면 원하는 구석(Dock 위, 메뉴바 아래 등)으로 자유롭게 이동 가능합니다.

---

## 터미널 및 AI CLI 연동 호출

맥북 환경에서도 아래 단 한 줄로 3대 AI CLI(Antigravity, Codex, Claude Code)를 원스톱 자동 등록할 수 있습니다:
```bash
python3 setup_cli.py --auto
```

터미널이나 쉘 스크립트에서 수동으로 바탕화면 캐릭터 말풍선을 갱신할 수도 있습니다:

```bash
# 1) 작업 착수 알림
python3 macos/notify_mac.py --status working --title "MacBook 작업 착수" --msg "코드베이스 분석을 시작합니다." --step "1/3"

# 2) 진행 단계 갱신
python3 macos/notify_mac.py --status working --title "빌드 및 테스트" --msg "pytest 테스트 스위트를 실행 중입니다." --step "2/3"

# 3) 작업 완료 알림
python3 macos/notify_mac.py --status done --title "작업 완료!" --msg "모든 테스트가 통과되었습니다." --elapsed 8

# 4) 대기 복귀
python3 macos/notify_mac.py --status idle
```

---

## 문제 해결 (Troubleshooting)

* **python3 명령어가 없는 경우**:
  ```bash
  brew install python
  ```
* **권한 오류(Permission denied)가 발생하는 경우**:
  ```bash
  chmod +x macos/*.sh run.sh
  ```
