#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AvatarHUD - macOS Notification Helper
"""

import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(DIR)
CORE_DIR = os.path.join(ROOT_DIR, 'core')
sys.path.insert(0, CORE_DIR)

from notify import (
    notify_status,
    notify_working,
    notify_done,
    notify_error,
    notify_idle,
    main
)

if __name__ == '__main__':
    main()
