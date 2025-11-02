#!/usr/bin/env python3
"""
Terminal Chat Launcher - Entry point for pip installation
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import and run the actual launcher
from bin.terminal_chat import main

if __name__ == '__main__':
    main()