"""
Encryption module for Vibe Cozy Chat
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
            print(f"{RED}[OpenSSL Error] {error_msg}{RESET}", file=sys.stderr)
            return None