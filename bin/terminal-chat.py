#!/usr/bin/env python3
"""
Terminal Chat - User-Friendly Launcher
Simple interactive launcher for connecting to encrypted chat rooms
"""

import sys
import os
import subprocess

# Add src/lib to path for imports
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(script_dir, 'src'))

from lib.translations import Translator

# ANSI colors
BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
CYAN = "\033[1;36m"
MAGENTA = "\033[1;35m"
RESET = "\033[0m"

def print_banner(t):
    """Print welcome banner"""
    print(f"""
{MAGENTA}╔═══════════════════════════════════════╗
║     {t.t('launcher_title')}    ║
║   {t.t('launcher_subtitle')}   ║
╚═══════════════════════════════════════╝{RESET}
""")

def get_language():
    """Ask user to select language"""
    print(f"{YELLOW}Choose language / Sprache wählen:{RESET}")
    print("  1. English")
    print("  2. Deutsch (German)")
    
    while True:
        choice = input(f"{CYAN}Enter choice (1 or 2): {RESET}").strip()
        if choice == '1':
            return 'en'
        elif choice == '2':
            return 'de'
        print(f"{RED}Invalid choice! Please enter 1 or 2{RESET}")

def get_input(prompt, default=None, t=None):
    """Get user input with optional default"""
    if default:
        response = input(f"{CYAN}{prompt} [{default}]: {RESET}").strip()
        return response if response else default
    else:
        while True:
            response = input(f"{CYAN}{prompt}: {RESET}").strip()
            if response:
                return response
            if t:
                print(f"{RED}{t.t('required_field')}{RESET}")
            else:
                print(f"{RED}This field is required!{RESET}")

def main():
    """Main launcher function"""
    # Get language selection
    lang = get_language()
    t = Translator(lang)
    
    print_banner(t)
    
    # Ask if server or client
    print(f"{YELLOW}{t.t('choose_mode')}{RESET}")
    print(f"  1. {t.t('mode_server')}")
    print(f"  2. {t.t('mode_client')}")
    
    while True:
        mode = input(f"{CYAN}{t.t('enter_choice')} (1 or 2): {RESET}").strip()
        if mode in ['1', '2']:
            break
        print(f"{RED}{t.t('invalid_choice')} 1 or 2{RESET}")
    
    # Get script location (go up from bin/)
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chat_script = os.path.join(script_dir, 'src', 'main.py')
    
    if not os.path.exists(chat_script):
        print(f"{RED}{t.t('error')}: Could not find main.py{RESET}")
        print(f"{YELLOW}Expected location: {chat_script}{RESET}")
        sys.exit(1)
    
    try:
        if mode == '1':
            # Server mode
            print(f"\n{GREEN}{t.t('server_setup')}{RESET}")
            port = get_input(t.t('port_number'), "4444", t)
            password = get_input(t.t('password_shared'), None, t)
            username = get_input(t.t('your_username'), "Admin", t)
            
            print(f"\n{GREEN}{t.t('starting_server')}{RESET}")
            print(f"{CYAN}{t.t('port')}:{RESET} {port}")
            print(f"{CYAN}{t.t('username')}:{RESET} {username}")
            print(f"{YELLOW}{t.t('share_password')}: {password}{RESET}\n")
            
            # Run server with language parameter
            subprocess.run([sys.executable, chat_script, 'listen', port, password, username, '--lang', lang])
            
        else:
            # Client mode
            print(f"\n{GREEN}{t.t('client_setup')}{RESET}")
            host = get_input(t.t('server_ip'), "localhost", t)
            port = get_input(t.t('port_number'), "4444", t)
            password = get_input(t.t('password_from_server'), None, t)
            username = get_input(t.t('your_username'), "Guest", t)
            
            print(f"\n{GREEN}{t.t('connecting')}{RESET}")
            print(f"{CYAN}{t.t('server')}:{RESET} {host}:{port}")
            print(f"{CYAN}{t.t('username')}:{RESET} {username}\n")
            
            # Run client with language parameter
            subprocess.run([sys.executable, chat_script, 'connect', host, port, password, username, '--lang', lang])
    
    except KeyboardInterrupt:
        print(f"\n{YELLOW}{t.t('cancelled')}{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}{t.t('error')}: {e}{RESET}")
        sys.exit(1)

if __name__ == '__main__':
    main()