#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AvatarHUD - Automated End-to-End Flow Verification Script
Tests Working -> Progress Update -> Done -> Idle state transitions.
"""

import sys
import time
import urllib.request
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
from notify import notify_status

def test_flow():
    print("=" * 60)
    print("🚀 [AvatarHUD] Starting Flow Verification Test")
    print("=" * 60)

    # 1. Health check
    try:
        with urllib.request.urlopen("http://127.0.0.1:8765/api/health", timeout=2.0) as res:
            data = json.loads(res.read().decode('utf-8'))
            print(f"✅ Server Health: OK ({data.get('app')})")
    except Exception as e:
        print(f"❌ Server is not reachable at http://127.0.0.1:8765: {e}")
        print("💡 Hint: Run `python core/app.py --server-only` in another terminal first.")
        return False

    # 2. Working Step 1
    print("\n[Step 1] Sending Working Status (1/3: 프로젝트 분석)...")
    ok, res = notify_status(
        status="working",
        title="프로젝트 구조 분석 중",
        message="전체 저장소 내 의존성과 모듈 구조를 파악하고 있습니다...",
        step="1/3"
    )
    assert ok, f"Step 1 failed: {res}"
    print("✅ Step 1 delivered successfully.")
    time.sleep(2.5)

    # 3. Working Step 2
    print("\n[Step 2] Sending Working Update (2/3: 코드 빌드 및 테스트)...")
    ok, res = notify_status(
        status="working",
        title="단위 테스트 실행 중",
        message="총 42개의 테스트 케이스를 순차적으로 검증하고 있습니다...",
        step="2/3"
    )
    assert ok, f"Step 2 failed: {res}"
    print("✅ Step 2 delivered successfully.")
    time.sleep(2.5)

    # 4. Done Step
    print("\n[Step 3] Sending Done Status (작업 완료)...")
    ok, res = notify_status(
        status="done",
        title="빌드 및 테스트 대성공!",
        message="42개 테스트 전원 통과 완료. 결과 보고서를 작성했습니다.",
        elapsed=5
    )
    assert ok, f"Step 3 failed: {res}"
    print("✅ Step 3 delivered successfully.")
    time.sleep(3.0)

    # 5. Idle Step
    print("\n[Step 4] Returning to Idle...")
    ok, res = notify_status(
        status="idle",
        title="대기 중",
        message="다음 명령을 기다리고 있습니다."
    )
    assert ok, f"Step 4 failed: {res}"
    print("✅ Step 4 delivered successfully.")

    print("\n" + "=" * 60)
    print("🎉 All 4 state transitions verified successfully!")
    print("=" * 60)
    return True

if __name__ == '__main__':
    success = test_flow()
    sys.exit(0 if success else 1)
