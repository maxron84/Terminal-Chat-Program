"""
Utility functions and constants for Vibe Cozy Chat
"""

from datetime import datetime

# ANSI color codes
BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
CYAN = "\033[1;36m"
MAGENTA = "\033[1;35m"
RESET = "\033[0m"


def timestamp():
    """Get current timestamp in HH:MM:SS format"""
    return datetime.now().strftime("%H:%M:%S")