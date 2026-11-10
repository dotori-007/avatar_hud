#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AvatarHUD Root Forwarding Wrapper
Delegates to core/notify.py
"""
import sys
import os

CORE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'core')
sys.path.insert(0, CORE_DIR)

from notify import main

if __name__ == '__main__':
    main()
