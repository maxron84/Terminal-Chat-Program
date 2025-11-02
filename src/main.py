#!/usr/bin/env python3
"""
Terminal Chat - Modular Version
Uses the lib/ components for better maintainability

This version imports from the lib/ directory for:
- Better code organization
- Easier testing
- Better maintainability
- Reusable components
"""

import sys
import os

# Add parent directory to path to import lib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import ChatServer, ChatClient


def main():
    """Main entry point"""
    if len(sys.argv) < 4:
        print("Usage:")
        print("  Server: ./main.py listen <port> <password> [username] [--lang <en|de>]")
        print("  Client: ./main.py connect <ip> <port> <password> [username] [--lang <en|de>]")
        print("\nExamples:")
        print("  Server: ./main.py listen 4444 mypass Admin")
        print("  Client: ./main.py connect 192.168.1.5 4444 mypass Alice")
        print("  German: ./main.py connect 192.168.1.5 4444 mypass Alice --lang de")
        sys.exit(1)
    
    # Parse --lang parameter
    lang = 'en'  # default
    if '--lang' in sys.argv:
        lang_idx = sys.argv.index('--lang')
        if lang_idx + 1 < len(sys.argv):
            lang = sys.argv[lang_idx + 1]
            # Remove --lang and its value from argv for easier parsing
            sys.argv = sys.argv[:lang_idx] + sys.argv[lang_idx+2:]
    
    mode = sys.argv[1]
    
    if mode == 'listen':
        if len(sys.argv) < 4:
            print("Usage: ./main.py listen <port> <password> [username] [--lang <en|de>]")
            sys.exit(1)
        port = int(sys.argv[2])
        password = sys.argv[3]
        username = sys.argv[4] if len(sys.argv) > 4 else "Server"
        
        server = ChatServer(port, password, username, lang=lang)
        server.run()
        
    elif mode == 'connect':
        if len(sys.argv) < 5:
            print("Usage: ./main.py connect <ip> <port> <password> [username] [--lang <en|de>]")
            sys.exit(1)
        host = sys.argv[2]
        port = int(sys.argv[3])
        password = sys.argv[4]
        username = sys.argv[5] if len(sys.argv) > 5 else "Guest"
        
        client = ChatClient(host, port, password, username, lang=lang)
        client.run()
        
    else:
        print(f"Error: MODE must be 'listen' or 'connect'")
        sys.exit(1)


if __name__ == '__main__':
    main()
