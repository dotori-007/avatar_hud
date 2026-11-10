#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Codex CLI - AvatarHUD Notification Adapter
Tailored notification helper for Codex agents and automated pipelines.
"""

import os
import sys

CORE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'core')
sys.path.insert(0, CORE_DIR)

from notify import notify_status, main

if __name__ == '__main__':
    main()
