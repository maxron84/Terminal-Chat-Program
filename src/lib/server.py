"""
Server module for Vibe Cozy Chat
Multi-client chat server with file sharing and encryption
"""

import socket
import threading
import os
import shutil
import logging
import sys
import base64
import time
from datetime import datetime
from .utils import BLUE, GREEN, YELLOW, RED, CYAN, MAGENTA, RESET, timestamp
from .encryption import Encryption
from .file_permissions import FilePermissions


class ChatServer:
    """Multi-client chat server with shared folder"""
    
    def __init__(self, port, password, username="Server"):
        """
        Initialize chat server
        
        Args:
            port (int): Port to listen on
            password (str): Encryption password
            username (str): Server username
        """
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
        
        # File permissions manager
        metadata_file = os.path.join(data_dir, 'file_permissions.json')
        self.file_perms = FilePermissions(metadata_file)
        
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
        """
        Broadcast encrypted message to all clients
        
        Args:
            message (str): Message to broadcast
            sender_username (str): Username of sender (to exclude from broadcast)
            exclude_server (bool): Whether to exclude server from broadcast
        """
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
        """
        Send message to a specific client
        
        Args:
            username (str): Target client username
            message (str): Message to send
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
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
    
    def send_file_to_client(self, sock, filepath, filename):
        """
        Send a file from shared folder to a specific client
        
        Args:
            sock: Client socket
            filepath (str): Full path to file
            filename (str): Name of file
        """
        try:
            # Send file header
            sock.sendall(f"__FILE__:{filename}\n".encode())
            
            # Send file content
            with open(filepath, 'rb') as f:
                file_data = f.read()
                b64_data = base64.b64encode(file_data).decode()
                
                # Send in chunks
                chunk_size = 512
                for i in range(0, len(b64_data), chunk_size):
                    chunk = b64_data[i:i+chunk_size]
                    encrypted = self.encryption.encrypt(chunk)
                    if encrypted:
                        sock.sendall(encrypted.encode() + b'\n')
            
            # Send end marker
            sock.sendall(b"__END__\n")
            self.logger.info(f"File sent successfully: {filename}")
            print(f"{GREEN}[{timestamp()}] Sent {filename} successfully{RESET}", file=sys.stderr)
        except Exception as e:
            self.logger.error(f"Error sending file {filename}: {e}")
            print(f"{RED}[{timestamp()}] Failed to send {filename}: {e}{RESET}", file=sys.stderr)
    
    def handle_client(self, sock, addr, username):
        """
        Handle messages from a single client
        
        Args:
            sock: Client socket
            addr: Client address
            username (str): Client username
        """
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
                    # Format: __FILE__:<filename>[@target_user]
                    file_data = line[9:]
                    
                    if '@' in file_data:
                        file_name, target_user = file_data.rsplit('@', 1)
                        file_target = target_user
                    else:
                        file_name = file_data
                        file_target = None
                    
                    temp_file = open(f'{self.shared_folder}/{file_name}.tmp', 'wb')
                    self.logger.info(f"Receiving file from {username}: {file_name}" +
                                   (f" for {file_target}" if file_target else ""))
                    print(f"{YELLOW}[{timestamp()}] Receiving file from {username}: {file_name}" +
                          (f" for {file_target}" if file_target else "") + "...{RESET}", file=sys.stderr)
                    continue
                elif line == "__END__":
                    if temp_file and file_name:
                        temp_file.close()
                        final_path = f'{self.shared_folder}/{file_name}'
                        os.rename(f'{self.shared_folder}/{file_name}.tmp', final_path)
                        
                        # Set file permissions
                        file_size = os.path.getsize(final_path)
                        self.file_perms.add_file(file_name, username, file_target, file_size)
                        
                        self.logger.info(f"File received from {username}: {file_name}")
                        print(f"{YELLOW}[{timestamp()}] Saved file from {username}: {final_path}{RESET}", file=sys.stderr)
                        
                        # Announce file receipt
                        if file_target:
                            # Private file - notify sender and recipient only
                            self.send_to_client(username, f"✓ File {file_name} uploaded privately for {file_target}")
                            self.send_to_client(file_target, f"*** {username} sent you a private file: {file_name} ***")
                            print(f"{MAGENTA}[{timestamp()}] Private file: {username} → {file_target}: {file_name}{RESET}", file=sys.stderr)
                        else:
                            # Public file - broadcast to all
                            self.broadcast(f"*** {username} uploaded file: {file_name} ***")
                    
                    file_name = None
                    file_target = None
                    temp_file = None
                    continue
                
                # Handle file data
                if file_name and temp_file:
                    decrypted = self.encryption.decrypt(line)
                    if decrypted:
                        try:
                            file_data = base64.b64decode(decrypted)
                            temp_file.write(file_data)
                            temp_file.flush()
                        except Exception as e:
                            self.logger.error(f"Error writing file data: {e}")
                    continue
                
                # Decrypt message
                msg = self.encryption.decrypt(line)
                if not msg:
                    continue
                
                # Handle special commands
                if msg.startswith("__CMD_LIST__"):
                    files = os.listdir(self.shared_folder)
                    if files:
                        response = "Shared folder contents:"
                        file_list = self.file_perms.list_files_for_user(username, files)
                        for filename, info, can_download in file_list:
                            size = os.path.getsize(os.path.join(self.shared_folder, filename))
                            if can_download:
                                response += f"\n  ✓ {info} ({size} bytes)"
                            else:
                                response += f"\n  ✗ {info} ({size} bytes)"
                    else:
                        response = "Shared folder is empty"
                    self.send_to_client(username, response)
                    
                elif msg.startswith("__CMD_UPLOAD__:"):
                    # Format: __CMD_UPLOAD__:<filename>[@target_user]
                    upload_data = msg[15:]
                    
                    if '@' in upload_data:
                        filename, target_user = upload_data.rsplit('@', 1)
                        # Private upload
                        # Check if target user exists
                        with self.clients_lock:
                            target_exists = any(u == target_user for s, a, u in self.clients)
                        
                        if not target_exists:
                            self.send_to_client(username, f"Error: User '{target_user}' not found or offline")
                            self.logger.warning(f"{username} tried to upload for non-existent user: {target_user}")
                        else:
                            self.logger.info(f"{username} uploading private file for {target_user}: {filename}")
                            # File will be received and permissions set when upload completes
                    else:
                        filename = upload_data
                        self.logger.info(f"{username} uploading public file: {filename}")
                    
                elif msg.startswith("__CMD_DOWNLOAD__:"):
                    filename = msg[17:]
                    filepath = os.path.join(self.shared_folder, filename)
                    
                    if not os.path.isfile(filepath):
                        self.send_to_client(username, f"Error: File '{filename}' not found in shared folder")
                        self.logger.warning(f"{username} requested non-existent file: {filename}")
                    else:
                        # Check permissions
                        can_download, reason = self.file_perms.can_download(filename, username)
                        
                        if not can_download:
                            self.send_to_client(username, f"Error: Cannot download '{filename}'. {reason}")
                            self.logger.warning(f"{username} denied download of {filename}: {reason}")
                        else:
                            # Send file to client
                            self.logger.info(f"Sending {filename} to {username} - {reason}")
                            print(f"{CYAN}[{timestamp()}] Sending {filename} to {username}...{RESET}", file=sys.stderr)
                            self.send_file_to_client(sock, filepath, filename)
                
                elif msg.startswith("__CMD_SEND_TO__:"):
                    # Direct file transfer: __CMD_SEND_TO__:<target_username>:<filename>
                    parts = msg[16:].split(':', 1)
                    if len(parts) == 2:
                        target_username, filename = parts
                        
                        # Check if target exists
                        with self.clients_lock:
                            target_exists = any(u == target_username for s, a, u in self.clients)
                        
                        if not target_exists:
                            self.send_to_client(username, f"Error: User '{target_username}' not found or offline")
                            self.logger.warning(f"{username} tried to send to non-existent user: {target_username}")
                        else:
                            # Store the target for file relay
                            self.relay_target = (target_username, filename)
                            self.relay_sender = username
                            self.logger.info(f"{username} initiating direct send to {target_username}: {filename}")
                            print(f"{CYAN}[{timestamp()}] {username} sending {filename} to {target_username}...{RESET}", file=sys.stderr)
                    
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
        finally:
            # Clean up
            if temp_file:
                temp_file.close()
            
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
                        continue
                    elif msg.startswith('/upload '):
                        filename = msg[8:].strip()
                        filepath = os.path.join(self.outbox_folder, filename)
                        if os.path.isfile(filepath):
                            shutil.copy(filepath, os.path.join(self.shared_folder, filename))
                            self.logger.info(f"Server uploaded file to shared folder: {filename}")
                            print(f"{CYAN}[{timestamp()}] Uploaded {filename} to shared folder{RESET}")
                            self.broadcast(f"*** {self.username} uploaded {filename} to shared folder ***")
                        else:
                            print(f"{RED}File not found in outbox: {filename}{RESET}")
                        continue
                    
                    # Regular message
                    encrypted = self.encryption.encrypt(msg)
                    if encrypted:
                        self.logger.info(f"Server message: {msg}")
                        print(f"{BLUE}[{timestamp()}] {self.username}:{RESET} {msg}",
                              file=sys.stderr)
                        self.broadcast(f"\033[1;35m{self.username}:\033[0m {msg}")
                except (EOFError, KeyboardInterrupt):
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
                    
                    # Check for duplicate username
                    with self.clients_lock:
                        existing_usernames = [u for s, a, u in self.clients]
                        if username in existing_usernames:
                            # Send error and close connection
                            error_msg = f"Error: Username '{username}' is already taken. Please reconnect with a different username."
                            encrypted_error = self.encryption.encrypt(error_msg)
                            if encrypted_error:
                                sock.sendall(encrypted_error.encode() + b'\n')
                            time.sleep(0.5)  # Give time for message to be received
                            sock.close()
                            self.logger.warning(f"Rejected duplicate username: {username} from {addr}")
                            print(f"{RED}[{timestamp()}] Rejected duplicate username: {username}{RESET}", file=sys.stderr)
                            continue
                        
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
            # Notify all clients
            self.broadcast("*** Server is shutting down ***")
            time.sleep(0.5)
            # Close all client connections
            with self.clients_lock:
                for sock, addr, username in self.clients:
                    try:
                        sock.close()
                    except:
                        pass
            self.logger.info("Server shutdown complete")
            server_sock.close()