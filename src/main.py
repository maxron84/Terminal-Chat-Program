#!/usr/bin/env python3
"""
Cozy Secure Chat - Modular Version
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
        print("  Server: ./cozy_secure_chat_modular.py listen <port> <password> [username]")
        print("  Client: ./cozy_secure_chat_modular.py connect <ip> <port> <password> [username]")
        print("\nExamples:")
        print("  Server: ./cozy_secure_chat_modular.py listen 4444 mypass Admin")
        print("  Client: ./cozy_secure_chat_modular.py connect 192.168.1.5 4444 mypass Alice")
        sys.exit(1)
    
    mode = sys.argv[1]
    
    if mode == 'listen':
        if len(sys.argv) < 4:
            print("Usage: ./cozy_secure_chat_modular.py listen <port> <password> [username]")
            sys.exit(1)
        port = int(sys.argv[2])
        password = sys.argv[3]
        username = sys.argv[4] if len(sys.argv) > 4 else "Server"
        
        server = ChatServer(port, password, username)
        server.run()
        
    elif mode == 'connect':
        if len(sys.argv) < 5:
            print("Usage: ./cozy_secure_chat_modular.py connect <ip> <port> <password> [username]")
            sys.exit(1)
        host = sys.argv[2]
        port = int(sys.argv[3])
        password = sys.argv[4]
        username = sys.argv[5] if len(sys.argv) > 5 else "Guest"
        
        client = ChatClient(host, port, password, username)
        client.run()
        
    else:
        print(f"Error: MODE must be 'listen' or 'connect'")
        sys.exit(1)


if __name__ == '__main__':
    main()
