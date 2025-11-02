#!/usr/bin/env python3
# ============================================
# Cozy Secure Chat + File Transfer (AES-256)
# Pure Python implementation with multi-client support
# Dependencies: python3, openssl command-line tool
#
# Usage:
#   Server: ./cozy_secure_chat.py listen <port> <password> [username]
#   Client: ./cozy_secure_chat.py connect <ip> <port> <password> [username]
#
# In chat:
#   /send <file>       → send file (encrypted)  
#   /upload <file>     → upload to shared folder
#   /list              → list shared folder contents
#   /quit              → quit
#   Ctrl+C             → quit
#
# Features:
# - Multi-client chat room with message broadcasting
# - Usernames for identification
# - Encrypted message display
# - Shared folder for file exchange
# ============================================

import sys
import socket
import threading
import subprocess
import base64
import os
import time
import shutil
import logging
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
    """Get current timestamp"""
    return datetime.now().strftime("%H:%M:%S")


class Encryption:
    """Handle encryption/decryption using OpenSSL"""
    
    def __init__(self, password):
        self.password = password
    
    def encrypt(self, text):
        """Encrypt text using AES-256-CBC"""
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
        """Decrypt text using AES-256-CBC"""
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


class ChatServer:
    """Multi-client chat server with shared folder"""
    
    def __init__(self, port, password, username="Server"):
        self.port = port
        self.password = password
        self.username = username
        self.encryption = Encryption(password)
        self.clients = []  # List of (socket, address, username)
        self.clients_lock = threading.Lock()
        self.running = True
        # Data folders in project directory
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        self.shared_folder = os.path.join(data_dir, "shared")
        self.outbox_folder = os.path.join(data_dir, "outbox")
        
        # Configure logging
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        log_filename = f"{log_dir}/chat_server_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler(sys.stderr)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Create shared and outbox folders
        os.makedirs(self.shared_folder, exist_ok=True)
        os.makedirs(self.outbox_folder, exist_ok=True)
        self.logger.info(f"Server initialized - Username: {self.username}, Port: {self.port}")
        self.logger.info(f"Shared folder: {self.shared_folder}/")
        self.logger.info(f"Outbox folder: {self.outbox_folder}/")
        print(f"{CYAN}[{timestamp()}] Shared folder: {self.shared_folder}/{RESET}",
              file=sys.stderr)
        print(f"{CYAN}[{timestamp()}] Outbox folder: {self.outbox_folder}/{RESET}",
              file=sys.stderr)
        print(f"{CYAN}[{timestamp()}] Logging to: {log_filename}{RESET}",
              file=sys.stderr)
    
    def broadcast(self, message, sender_username=None, exclude_server=False):
        """Broadcast encrypted message to all clients"""
        encrypted = self.encryption.encrypt(message)
        if encrypted:
            with self.clients_lock:
                dead_clients = []
                for sock, addr, username in self.clients:
                    if username != sender_username:  # Don't send back to sender
                        try:
                            sock.sendall(encrypted.encode() + b'\n')
                        except:
                            dead_clients.append((sock, addr, username))
                
                # Remove dead clients
                for dead in dead_clients:
                    if dead in self.clients:
                        self.clients.remove(dead)
                        print(f"{YELLOW}[{timestamp()}] {dead[2]} disconnected{RESET}",
                              file=sys.stderr)
    
    def send_to_client(self, username, message):
        """Send message to a specific client"""
        encrypted = self.encryption.encrypt(message)
        if encrypted:
            with self.clients_lock:
                for sock, addr, uname in self.clients:
                    if uname == username:
                        try:
                            sock.sendall(encrypted.encode() + b'\n')
                            sock.sendall(b'')  # Force flush
                            print(f"{CYAN}[{timestamp()}] Sent to {username}: {message[:50]}...{RESET}", file=sys.stderr)
                            return True
                        except Exception as e:
                            print(f"{RED}[{timestamp()}] Failed to send to {username}: {e}{RESET}", file=sys.stderr)
                            return False
        return False
    
    def handle_client(self, sock, addr, username):
        """Handle messages from a single client"""
        self.logger.info(f"Client connected: {username} from {addr}")
        print(f"{GREEN}[{timestamp()}] {username} connected from {addr}{RESET}",
              file=sys.stderr)
        
        # Announce new user to everyone including server display
        announcement = f"*** {username} joined the chat ***"
        print(f"{YELLOW}[{timestamp()}] {announcement}{RESET}", file=sys.stderr)
        self.broadcast(announcement, sender_username=username)
        
        # File reception state
        file_name = None
        temp_file = None
        os.makedirs(self.shared_folder, exist_ok=True)
        
        try:
            sock_file = sock.makefile('r')
            while self.running:
                line = sock_file.readline()
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                # Handle file transfer markers
                if line.startswith("__FILE__:"):
                    file_name = line[9:]
                    temp_file = open(f'{self.shared_folder}/{file_name}.tmp', 'wb')
                    self.logger.info(f"Receiving file from {username}: {file_name}")
                    print(f"{YELLOW}[{timestamp()}] Receiving file from {username}: {file_name}...{RESET}", file=sys.stderr)
                    continue
                elif line == "__END__":
                    if temp_file and file_name:
                        temp_file.close()
                        final_path = f'{self.shared_folder}/{file_name}'
                        os.rename(f'{self.shared_folder}/{file_name}.tmp', final_path)
                        self.logger.info(f"File received from {username}: {file_name}")
                        print(f"{YELLOW}[{timestamp()}] Saved file from {username}: {final_path}{RESET}", file=sys.stderr)
                        # Announce file receipt
                        self.broadcast(f"*** {username} sent file: {file_name} ***")
                    file_name = None
                    temp_file = None
                    continue
                
                # Handle file data - must check BEFORE trying to decrypt as regular message
                if file_name and temp_file:
                    # Decrypt and decode base64 for file data
                    decrypted = self.encryption.decrypt(line)
                    if decrypted:
                        try:
                            file_data = base64.b64decode(decrypted)
                            bytes_written = len(file_data)
                            temp_file.write(file_data)
                            temp_file.flush()  # Ensure data is written immediately
                            print(f"{CYAN}[{timestamp()}] Wrote {bytes_written} bytes of file data{RESET}", file=sys.stderr)
                        except Exception as e:
                            self.logger.error(f"Error writing file data: {e}")
                            print(f"{RED}[{timestamp()}] Failed to write file chunk: {e}{RESET}", file=sys.stderr)
                    else:
                        # Decryption failed for file chunk - this is critical!
                        self.logger.error(f"CRITICAL: Failed to decrypt file chunk from {username} - chunk length: {len(line)}, first 100 chars: {line[:100]}")
                        print(f"{RED}[{timestamp()}] ERROR: Failed to decrypt file chunk! Data will be incomplete!{RESET}", file=sys.stderr)
                    continue
                
                # Debug: show what we received
                print(f"{CYAN}[{timestamp()}] Raw from {username} ({len(line)} chars): {line[:100]}...{RESET}", file=sys.stderr)
                
                # Decrypt message
                msg = self.encryption.decrypt(line)
                if not msg:
                    self.logger.error(f"Decryption failed from {username} - encrypted: {line[:100]}")
                    print(f"{RED}[{timestamp()}] DECRYPTION FAILED from {username}{RESET}", file=sys.stderr)
                    print(f"{RED}    Encrypted text was: {line[:200]}{RESET}", file=sys.stderr)
                    continue
                
                print(f"{GREEN}[{timestamp()}] Decrypted from {username}: {msg[:50]}...{RESET}", file=sys.stderr)
                
                # Handle special commands
                if msg.startswith("__CMD_LIST__"):
                    # Client wants folder listing
                    self.logger.info(f"{username} requested folder listing")
                    print(f"{YELLOW}[{timestamp()}] {username} requested folder listing{RESET}", file=sys.stderr)
                    files = os.listdir(self.shared_folder)
                    if files:
                        response = "Shared folder contents:"
                        for f in files:
                            size = os.path.getsize(os.path.join(self.shared_folder, f))
                            response += f"\n  - {f} ({size} bytes)"
                    else:
                        response = "Shared folder is empty"
                    self.send_to_client(username, response)
                    
                elif msg.startswith("__CMD_UPLOAD__:"):
                    # Handle upload - silently acknowledge (don't send response to avoid decrypt errors)
                    filename = msg[15:]
                    self.logger.info(f"{username} requested upload: {filename}")
                    print(f"{YELLOW}[{timestamp()}] {username} wants to upload: {filename}{RESET}", file=sys.stderr)
                    print(f"{CYAN}[{timestamp()}] Upload feature: File transfer implementation pending{RESET}", file=sys.stderr)
                    # Don't send response back to avoid triggering decrypt errors on client
                    
                else:
                    # Regular message - display on server and broadcast
                    self.logger.info(f"Message from {username}: {msg}")
                    print(f"{GREEN}[{timestamp()}] {username}:{RESET} {msg}", file=sys.stderr)
                    sys.stderr.flush()
                    # Add special color for admin in broadcast
                    if username == self.username:
                        self.broadcast(f"\033[1;35m{username}:\033[0m {msg}", sender_username=username)
                    else:
                        self.broadcast(f"{username}: {msg}", sender_username=username)
                    
        except Exception as e:
            self.logger.error(f"Error handling client {username}: {e}")
            print(f"{RED}[{timestamp()}] {username} error: {e}{RESET}",
                  file=sys.stderr)
        finally:
            # Clean up file if transfer was interrupted
            if temp_file:
                temp_file.close()
                try:
                    if file_name:
                        os.remove(f'{self.shared_folder}/{file_name}.tmp')
                except:
                    pass
            
            with self.clients_lock:
                if (sock, addr, username) in self.clients:
                    self.clients.remove((sock, addr, username))
            sock.close()
            self.logger.info(f"Client disconnected: {username}")
            announcement = f"*** {username} left the chat ***"
            print(f"{YELLOW}[{timestamp()}] {announcement}{RESET}", file=sys.stderr)
            self.broadcast(announcement)
    
    def server_commands(self):
        """Handle server-side commands"""
        print(f"{YELLOW}[{timestamp()}] Server username: {self.username}{RESET}",
              file=sys.stderr)
        print(f"{YELLOW}[{timestamp()}] Commands: /list, /outbox, /upload <file>, regular messages, /quit{RESET}",
              file=sys.stderr)
        
        try:
            while self.running:
                try:
                    msg = input(f"[{self.username}] > ")
                    if not msg:
                        continue
                    
                    if msg == '/quit':
                        break
                    elif msg == '/list':
                        files = os.listdir(self.shared_folder)
                        if files:
                            print(f"{CYAN}Shared folder contents:{RESET}")
                            for f in files:
                                size = os.path.getsize(os.path.join(self.shared_folder, f))
                                print(f"  - {f} ({size} bytes)")
                        else:
                            print(f"{YELLOW}Shared folder is empty{RESET}")
                        continue
                    elif msg == '/outbox':
                        files = os.listdir(self.outbox_folder)
                        if files:
                            print(f"{CYAN}Outbox contents:{RESET}")
                            for f in files:
                                size = os.path.getsize(os.path.join(self.outbox_folder, f))
                                print(f"  - {f} ({size} bytes)")
                        else:
                            print(f"{YELLOW}Outbox is empty{RESET}")
                            print(f"{CYAN}Place files in 'outbox/' folder to upload them{RESET}")
                        continue
                    elif msg.startswith('/upload '):
                        filename = msg[8:].strip()
                        # Restrict to outbox folder only
                        filepath = os.path.join(self.outbox_folder, filename)
                        if os.path.isfile(filepath):
                            shutil.copy(filepath, os.path.join(self.shared_folder, filename))
                            self.logger.info(f"Server uploaded file to shared folder: {filename}")
                            print(f"{CYAN}[{timestamp()}] Uploaded {filename} to shared folder{RESET}")
                            self.broadcast(f"*** {self.username} uploaded {filename} to shared folder ***")
                        else:
                            self.logger.error(f"Server upload failed - file not found in outbox: {filename}")
                            print(f"{RED}File not found in outbox: {filename}{RESET}")
                            print(f"{YELLOW}Hint: Files must be in the 'outbox/' folder{RESET}")
                        continue
                    
                    # Regular message
                    encrypted = self.encryption.encrypt(msg)
                    if encrypted:
                        self.logger.info(f"Server message: {msg}")
                        print(f"{MAGENTA}[{timestamp()}] Encrypted:{RESET} {encrypted}",
                              file=sys.stderr)
                        print(f"{BLUE}[{timestamp()}] {self.username}:{RESET} {msg}",
                              file=sys.stderr)
                        # Broadcast to all clients with special admin color
                        self.broadcast(f"\033[1;35m{self.username}:\033[0m {msg}")
                except EOFError:
                    break
                except KeyboardInterrupt:
                    break
        finally:
            self.running = False
    
    def run(self):
        """Start the server"""
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(('0.0.0.0', self.port))
        server_sock.listen(10)
        
        self.logger.info(f"Server listening on 0.0.0.0:{self.port}")
        print(f"{BLUE}[{timestamp()}] Multi-client server listening on port {self.port}...{RESET}",
              file=sys.stderr)
        
        # Start server command handler
        cmd_thread = threading.Thread(target=self.server_commands)
        cmd_thread.daemon = True
        cmd_thread.start()
        
        try:
            while self.running:
                try:
                    server_sock.settimeout(1.0)
                    sock, addr = server_sock.accept()
                    
                    # Receive username from client
                    try:
                        username = sock.recv(1024).decode().strip()
                        if not username:
                            username = f"User{addr[1]}"
                    except:
                        username = f"User{addr[1]}"
                    
                    with self.clients_lock:
                        self.clients.append((sock, addr, username))
                    
                    # Start thread for this client
                    thread = threading.Thread(
                        target=self.handle_client,
                        args=(sock, addr, username)
                    )
                    thread.daemon = True
                    thread.start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            self.logger.info("Server shutdown initiated by user")
            print(f"\n{YELLOW}[{timestamp()}] Server shutting down...{RESET}",
                  file=sys.stderr)
        finally:
            self.running = False
            # Notify all clients that server is shutting down
            self.broadcast("*** Server is shutting down ***")
            time.sleep(0.5)  # Give time for message to be sent
            # Close all client connections
            with self.clients_lock:
                for sock, addr, username in self.clients:
                    try:
                        sock.close()
                    except:
                        pass
            self.logger.info("Server shutdown complete")
            server_sock.close()


class ChatClient:
    """Chat client with username and shared folder access"""
    
    def __init__(self, host, port, password, username="Guest"):
        self.host = host
        self.port = port
        self.password = password
        self.username = username
        self.encryption = Encryption(password)
        self.running = True
        self.sock = None
        # Data folders in project directory
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        self.shared_folder = os.path.join(data_dir, "shared")
        self.outbox_folder = os.path.join(data_dir, "outbox")
        self.inbox_folder = os.path.join(data_dir, "inbox")
        self.user_colors = {}  # Map usernames to colors
        self.color_pool = [
            "\033[1;36m",  # Cyan
            "\033[1;33m",  # Yellow
            "\033[1;32m",  # Green
            "\033[1;34m",  # Blue
            "\033[1;37m",  # White
        ]
        self.next_color_index = 0
        
        # Create data folders
        os.makedirs(self.outbox_folder, exist_ok=True)
        os.makedirs(self.inbox_folder, exist_ok=True)
    
    def get_user_color(self, username):
        """Get consistent color for a username"""
        # Admin always gets magenta
        if username.lower().startswith('admin') or username.lower() == 'server':
            return MAGENTA
        # Own messages get blue
        if username == self.username:
            return BLUE
        # Other users get assigned colors
        if username not in self.user_colors:
            self.user_colors[username] = self.color_pool[self.next_color_index % len(self.color_pool)]
            self.next_color_index += 1
        return self.user_colors[username]
    
    def receive_messages(self):
        """Receive and display messages from server"""
        os.makedirs(self.inbox_folder, exist_ok=True)
        
        file_name = None
        temp_file = None
        
        try:
            sock_file = self.sock.makefile('r')
            while self.running:
                line = sock_file.readline()
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                # Check for file transfer markers
                if line.startswith("__FILE__:"):
                    file_name = line[9:]
                    temp_file = open(os.path.join(self.inbox_folder, f'{file_name}.tmp'), 'wb')
                    print(f"{YELLOW}[{timestamp()}] Receiving {file_name}...{RESET}",
                          file=sys.stderr)
                    continue
                elif line == "__END__":
                    if temp_file and file_name:
                        temp_file.close()
                        tmp_path = os.path.join(self.inbox_folder, f'{file_name}.tmp')
                        final_path = os.path.join(self.inbox_folder, file_name)
                        os.rename(tmp_path, final_path)
                        print(f"{YELLOW}[{timestamp()}] Saved to {final_path}{RESET}",
                              file=sys.stderr)
                    file_name = None
                    temp_file = None
                    continue
                
                # Handle file data or regular message
                if file_name and temp_file:
                    # Decrypt and decode base64 for file data
                    decrypted = self.encryption.decrypt(line)
                    if decrypted:
                        try:
                            file_data = base64.b64decode(decrypted)
                            temp_file.write(file_data)
                        except:
                            pass
                else:
                    # Regular message
                    msg = self.encryption.decrypt(line)
                    if msg:
                        # Check for server shutdown message
                        if msg == "*** Server is shutting down ***":
                            print(f"\n{YELLOW}[{timestamp()}] {msg}{RESET}", file=sys.stderr)
                            print(f"{YELLOW}[{timestamp()}] Disconnecting...{RESET}", file=sys.stderr)
                            self.running = False
                            if self.sock:
                                try:
                                    self.sock.shutdown(socket.SHUT_RDWR)
                                except:
                                    pass
                                self.sock.close()
                            print(f"{GREEN}[{timestamp()}] Disconnected.{RESET}", file=sys.stderr)
                            # Exit the program completely
                            os._exit(0)
                        
                        # Parse username from message
                        if ': ' in msg:
                            username_part, message_part = msg.split(': ', 1)
                            color = self.get_user_color(username_part)
                            print(f"\n{color}[{timestamp()}] {username_part}:{RESET} {message_part}", file=sys.stderr)
                        else:
                            # System message or announcement
                            print(f"\n{YELLOW}[{timestamp()}] {msg}{RESET}", file=sys.stderr)
                        
                        # Reprint the prompt
                        print(f"[{self.username}] > ", end='', flush=True)
        except Exception as e:
            if self.running:
                print(f"{RED}[{timestamp()}] Receive error: {e}{RESET}",
                      file=sys.stderr)
        finally:
            if temp_file:
                temp_file.close()
            # Ensure client stops completely
            self.running = False
    
    def send_file(self, filepath):
        """Send a file directly to other clients"""
        if not os.path.isfile(filepath):
            print(f"{RED}[{timestamp()}] Error: File '{filepath}' not found{RESET}",
                  file=sys.stderr)
            return
        
        filename = os.path.basename(filepath)
        
        # Send file header
        self.sock.sendall(f"__FILE__:{filename}\n".encode())
        
        # Send file content
        with open(filepath, 'rb') as f:
            file_data = f.read()
            b64_data = base64.b64encode(file_data).decode()
            
            # Send in chunks - use smaller chunks to avoid encryption issues
            chunk_size = 512
            for i in range(0, len(b64_data), chunk_size):
                chunk = b64_data[i:i+chunk_size]
                encrypted = self.encryption.encrypt(chunk)
                if encrypted:
                    self.sock.sendall(encrypted.encode() + b'\n')
        
        # Send end marker
        self.sock.sendall(b"__END__\n")
        print(f"{YELLOW}[{timestamp()}] Sent {filename}{RESET}", file=sys.stderr)
    
    def send_messages(self):
        """Send messages from user input"""
        print(f"{CYAN}Commands: /send <file>, /upload <file>, /list, /outbox, /quit{RESET}")
        
        try:
            while self.running:
                try:
                    msg = input(f"[{self.username}] > ")
                    if not msg:
                        continue
                    
                    if msg == '/quit':
                        break
                    elif msg.startswith('/send '):
                        filename = msg[6:].strip()
                        # Restrict to outbox folder only
                        filepath = os.path.join(self.outbox_folder, filename)
                        if not os.path.isfile(filepath):
                            print(f"{RED}File not found in outbox: {filename}{RESET}")
                            print(f"{YELLOW}Hint: Files must be in the 'outbox/' folder{RESET}")
                            continue
                        self.send_file(filepath)
                    elif msg.startswith('/upload '):
                        filename = msg[8:].strip()
                        # Restrict to outbox folder only
                        filepath = os.path.join(self.outbox_folder, filename)
                        if os.path.isfile(filepath):
                            # Send upload command to server, then send the file
                            self.send_file(filepath)
                            print(f"{CYAN}[{timestamp()}] Uploaded {filename} to shared folder{RESET}")
                        else:
                            print(f"{RED}File not found in outbox: {filename}{RESET}")
                            print(f"{YELLOW}Hint: Files must be in the 'outbox/' folder{RESET}")
                    elif msg == '/outbox':
                        # List outbox contents
                        files = os.listdir(self.outbox_folder)
                        if files:
                            print(f"{CYAN}Outbox contents:{RESET}")
                            for f in files:
                                size = os.path.getsize(os.path.join(self.outbox_folder, f))
                                print(f"  - {f} ({size} bytes)")
                        else:
                            print(f"{YELLOW}Outbox is empty{RESET}")
                            print(f"{CYAN}Place files in 'outbox/' folder to upload them{RESET}")
                        continue
                    elif msg == '/list':
                        # Request folder listing from server
                        cmd = "__CMD_LIST__"
                        encrypted = self.encryption.encrypt(cmd)
                        if encrypted:
                            self.sock.sendall(encrypted.encode() + b'\n')
                    else:
                        encrypted = self.encryption.encrypt(msg)
                        if encrypted:
                            self.sock.sendall(encrypted.encode() + b'\n')
                            # Message sent - no echo needed
                except EOFError:
                    break
                except KeyboardInterrupt:
                    break
        finally:
            self.running = False
    
    def run(self):
        """Connect and run the client"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            
            # Send username to server
            self.sock.sendall(self.username.encode() + b'\n')
            
            print(f"{BLUE}[{timestamp()}] Connecting to {self.host}:{self.port}...{RESET}",
                  file=sys.stderr)
            print(f"{GREEN}[{timestamp()}] Connected as '{self.username}'!{RESET}",
                  file=sys.stderr)
            
            # Start receiver thread
            recv_thread = threading.Thread(target=self.receive_messages)
            recv_thread.daemon = True
            recv_thread.start()
            
            # Send messages (blocks on input)
            self.send_messages()
            
        except ConnectionRefusedError:
            print(f"{RED}[{timestamp()}] Failed to connect to {self.host}:{self.port}{RESET}",
                  file=sys.stderr)
        except KeyboardInterrupt:
            print(f"\n{YELLOW}[{timestamp()}] Disconnecting...{RESET}",
                  file=sys.stderr)
        finally:
            self.running = False
            if self.sock:
                try:
                    self.sock.shutdown(socket.SHUT_RDWR)
                except:
                    pass
                self.sock.close()
            print(f"{GREEN}[{timestamp()}] Disconnected.{RESET}", file=sys.stderr)


def main():
    """Main entry point"""
    if len(sys.argv) < 4:
        print("Usage:")
        print("  Server: ./cozy_secure_chat.py listen <port> <password> [username]")
        print("  Client: ./cozy_secure_chat.py connect <ip> <port> <password> [username]")
        print("\nExamples:")
        print("  Server: ./cozy_secure_chat.py listen 4444 mypass Admin")
        print("  Client: ./cozy_secure_chat.py connect 192.168.1.5 4444 mypass Alice")
        sys.exit(1)
    
    mode = sys.argv[1]
    
    if mode == 'listen':
        if len(sys.argv) < 4:
            print("Usage: ./cozy_secure_chat.py listen <port> <password> [username]")
            sys.exit(1)
        port = int(sys.argv[2])
        password = sys.argv[3]
        username = sys.argv[4] if len(sys.argv) > 4 else "Server"
        
        server = ChatServer(port, password, username)
        server.run()
        
    elif mode == 'connect':
        if len(sys.argv) < 5:
            print("Usage: ./cozy_secure_chat.py connect <ip> <port> <password> [username]")
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
