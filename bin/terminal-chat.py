#!/usr/bin/env python3
"""
Terminal Chat - User-Friendly Launcher
Simple interactive launcher for connecting to encrypted chat rooms
"""

import sys
import os
import subprocess

# ANSI colors
BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
CYAN = "\033[1;36m"
MAGENTA = "\033[1;35m"
RESET = "\033[0m"

def print_banner():
    """Print welcome banner"""
    print(f"""
{MAGENTA}╔═══════════════════════════════════════╗
║     🎨 Terminal Chat Launcher 🎨    ║
║   Secure Encrypted Chat Experience   ║
╚═══════════════════════════════════════╝{RESET}
""")

def get_input(prompt, default=None):
    """Get user input with optional default"""
    if default:
        response = input(f"{CYAN}{prompt} [{default}]: {RESET}").strip()
        return response if response else default
    else:
        while True:
            response = input(f"{CYAN}{prompt}: {RESET}").strip()
            if response:
                return response
            print(f"{RED}This field is required!{RESET}")

def main():
    """Main launcher function"""
    print_banner()
    
    # Ask if server or client
    print(f"{YELLOW}Choose mode:{RESET}")
    print("  1. Start Server (host a chat room)")
    print("  2. Connect to Server (join a chat room)")
    
    while True:
        mode = input(f"{CYAN}Enter choice (1 or 2): {RESET}").strip()
        if mode in ['1', '2']:
            break
        print(f"{RED}Invalid choice! Please enter 1 or 2{RESET}")
    
    # Get script location (go up from bin/)
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chat_script = os.path.join(script_dir, 'src', 'main.py')
    
    if not os.path.exists(chat_script):
        print(f"{RED}Error: Could not find main.py{RESET}")
        print(f"{YELLOW}Expected location: {chat_script}{RESET}")
        sys.exit(1)
    
    try:
        if mode == '1':
            # Server mode
            print(f"\n{GREEN}╔════ Server Setup ════╗{RESET}")
            port = get_input("Port number", "4444")
            password = get_input("Password (shared with clients)")
            username = get_input("Your username", "Admin")
            
            print(f"\n{GREEN}Starting server...{RESET}")
            print(f"{CYAN}Port:{RESET} {port}")
            print(f"{CYAN}Username:{RESET} {username}")
            print(f"{YELLOW}Share the password with clients: {password}{RESET}\n")
            
            # Run server
            subprocess.run([sys.executable, chat_script, 'listen', port, password, username])
            
        else:
            # Client mode
            print(f"\n{GREEN}╔════ Client Setup ════╗{RESET}")
            host = get_input("Server IP address", "localhost")
            port = get_input("Port number", "4444")
            password = get_input("Password (from server)")
            username = get_input("Your username", "Guest")
            
            print(f"\n{GREEN}Connecting to chat...{RESET}")
            print(f"{CYAN}Server:{RESET} {host}:{port}")
            print(f"{CYAN}Username:{RESET} {username}\n")
            
            # Run client
            subprocess.run([sys.executable, chat_script, 'connect', host, port, password, username])
    
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Cancelled by user{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}Error: {e}{RESET}")
        sys.exit(1)

if __name__ == '__main__':
    main()