"""
Encryption module for Terminal Chat
Handles AES-256-CBC encryption/decryption using OpenSSL
"""

import subprocess
import sys
from .utils import RED, RESET


class Encryption:
    """Handle encryption/decryption using OpenSSL"""
    
    def __init__(self, password):
        """
        Initialize encryption with password
        
        Args:
            password (str): Password for encryption/decryption
        """
        self.password = password
    
    def encrypt(self, text):
        """
        Encrypt text using AES-256-CBC
        
        Args:
            text (str): Plain text to encrypt
            
        Returns:
            str: Base64 encoded encrypted text, or None on failure
        """
        try:
            result = subprocess.run(
                ['openssl', 'enc', '-aes-256-cbc', '-pbkdf2', '-a', '-salt',
                 '-pass', f'pass:{self.password}'],
                input=text.encode(),
                capture_output=True,
                check=True
            )
            # Remove ALL newlines from base64 output to keep it on one line
            encrypted = result.stdout.decode().strip().replace('\n', '').replace('\r', '')
            return encrypted
        except subprocess.CalledProcessError:
            return None
    
    def decrypt(self, encrypted_text):
        """
        Decrypt text using AES-256-CBC
        
        Args:
            encrypted_text (str): Base64 encoded encrypted text
            
        Returns:
            str: Decrypted plain text, or None on failure
        """
        try:
            # Ensure encrypted text ends with newline for OpenSSL
            if not encrypted_text.endswith('\n'):
                encrypted_text += '\n'
            
            result = subprocess.run(
                ['openssl', 'enc', '-d', '-aes-256-cbc', '-pbkdf2', '-a',
                 '-pass', f'pass:{self.password}'],
                input=encrypted_text.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            return result.stdout.decode().strip()
        except subprocess.CalledProcessError as e:
            # Capture OpenSSL error for debugging
            error_msg = e.stderr.decode() if e.stderr else "No error message"
            
            # Check if it's a password mismatch (bad decrypt error)
            if "bad decrypt" in error_msg.lower():
                print(f"{RED}╔══════════════════════════════════════════════════════════╗{RESET}", file=sys.stderr)
                print(f"{RED}║              ⚠️  PASSWORD MISMATCH DETECTED             ║{RESET}", file=sys.stderr)
                print(f"{RED}╠══════════════════════════════════════════════════════════╣{RESET}", file=sys.stderr)
                print(f"{RED}║ Cannot decrypt message - wrong password!                ║{RESET}", file=sys.stderr)
                print(f"{RED}║                                                          ║{RESET}", file=sys.stderr)
                print(f"{RED}║ Your password does NOT match the server's password.     ║{RESET}", file=sys.stderr)
                print(f"{RED}║                                                          ║{RESET}", file=sys.stderr)
                print(f"{RED}║ Solutions:                                               ║{RESET}", file=sys.stderr)
                print(f"{RED}║ 1. Disconnect (/quit) and reconnect with correct        ║{RESET}", file=sys.stderr)
                print(f"{RED}║    password from server's .env file                      ║{RESET}", file=sys.stderr)
                print(f"{RED}║ 2. Ask server admin for the correct password            ║{RESET}", file=sys.stderr)
                print(f"{RED}║                                                          ║{RESET}", file=sys.stderr)
                print(f"{RED}║ Note: This error will continue until you reconnect      ║{RESET}", file=sys.stderr)
                print(f"{RED}║ with the correct password.                               ║{RESET}", file=sys.stderr)
                print(f"{RED}╚══════════════════════════════════════════════════════════╝{RESET}", file=sys.stderr)
            else:
                print(f"{RED}[Decryption Error] {error_msg}{RESET}", file=sys.stderr)
            return None