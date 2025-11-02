"""
Client module for Terminal Chat
Chat client with encryption, color-coded messages, and file transfer
"""

import socket
import threading
import os
import base64
import sys
from .utils import BLUE, GREEN, YELLOW, RED, CYAN, MAGENTA, RESET, timestamp
from .encryption import Encryption
from .translations import Translator


class ChatClient:
    """Chat client with username and shared folder access"""
    
    def __init__(self, host, port, password, username="Guest", lang='en'):
        """
        Initialize chat client
        
        Args:
            host (str): Server hostname/IP
            port (int): Server port
            password (str): Encryption password
            username (str): Client username
            lang (str): Language code ('en' or 'de')
        """
        self.host = host
        self.port = port
        self.password = password
        self.username = username
        self.lang = lang
        self.t = Translator(lang)
        self.encryption = Encryption(password)
        self.running = True
        self.sock = None
        
        # Data folders in project root directory
        # Go from src/lib/client.py -> src/lib/ -> src/ -> project_root/
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data_dir = os.path.join(project_root, 'data')
        self.shared_folder = os.path.join(data_dir, "shared")
        self.outbox_folder = os.path.join(data_dir, "outbox")
        self.inbox_folder = os.path.join(data_dir, "inbox")
        
        # Color assignment for users
        self.user_colors = {}
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
        """
        Get consistent color for a username
        
        Args:
            username (str): Username to get color for
            
        Returns:
            str: ANSI color code
        """
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
            self.running = False
    
    def send_file(self, filepath):
        """
        Send a file directly to other clients
        
        Args:
            filepath (str): Path to file to send
        """
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
            
            # Send in chunks
            chunk_size = 512
            for i in range(0, len(b64_data), chunk_size):
                chunk = b64_data[i:i+chunk_size]
                encrypted = self.encryption.encrypt(chunk)
                if encrypted:
                    self.sock.sendall(encrypted.encode() + b'\n')
        
        # Send end marker
        self.sock.sendall(b"__END__\n")
        print(f"{YELLOW}[{timestamp()}] Sent {filename}{RESET}", file=sys.stderr)
    
    def send_file_private(self, filepath, target_user):
        """
        Send a file privately to a specific user
        
        Args:
            filepath (str): Path to file to send
            target_user (str): Username of recipient
        """
        if not os.path.isfile(filepath):
            print(f"{RED}[{timestamp()}] Error: File '{filepath}' not found{RESET}",
                  file=sys.stderr)
            return
        
        filename = os.path.basename(filepath)
        
        # Send file header with target tag
        self.sock.sendall(f"__FILE__:{filename}@{target_user}\n".encode())
        
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
                    self.sock.sendall(encrypted.encode() + b'\n')
        
        # Send end marker
        self.sock.sendall(b"__END__\n")
        print(f"{MAGENTA}[{timestamp()}] Sent {filename} privately to {target_user}{RESET}", file=sys.stderr)
    
    def send_messages(self):
        """Send messages from user input"""
        print(f"{CYAN}{self.t.t('commands_available')}{RESET}")
        
        try:
            while self.running:
                try:
                    msg = input(f"[{self.username}] > ")
                    if not msg:
                        continue
                    
                    if msg == '/quit':
                        break
                    elif msg == '/help':
                        print(f"{CYAN}╔══════════════════════════════════════════════════════════╗{RESET}")
                        print(f"{CYAN}║                    {self.t.t('help_title'):^34}                    ║{RESET}")
                        print(f"{CYAN}╠══════════════════════════════════════════════════════════╣{RESET}")
                        print(f"{GREEN}{self.t.t('cmd_list')}{RESET}                → {self.t.t('help_list')}")
                        print(f"{GREEN}{self.t.t('cmd_inbox')}{RESET}               → {self.t.t('help_inbox')}")
                        print(f"{GREEN}{self.t.t('cmd_outbox')}{RESET}              → {self.t.t('help_outbox')}")
                        print(f"{GREEN}{self.t.t('cmd_upload')} <file>{RESET}       → {self.t.t('help_upload')}")
                        print(f"{MAGENTA}{self.t.t('cmd_upload')} <file> @user{RESET} → {MAGENTA}{self.t.t('help_upload_private')}{RESET}")
                        print(f"{GREEN}{self.t.t('cmd_download')} <file>{RESET}     → {self.t.t('help_download')}")
                        print(f"{GREEN}{self.t.t('cmd_quit')}{RESET}                → {self.t.t('help_quit')}")
                        print(f"{GREEN}{self.t.t('cmd_help')}{RESET}                → {self.t.t('help_help')}")
                        print(f"{CYAN}╠══════════════════════════════════════════════════════════╣{RESET}")
                        print(f"{YELLOW}{self.t.t('help_regular_msg')}{RESET} {self.t.t('help_regular_desc')}")
                        print(f"{YELLOW}{self.t.t('help_files')}{RESET} {self.t.t('help_files_desc')}")
                        print(f"{CYAN}╠══════════════════════════════════════════════════════════╣{RESET}")
                        print(f"{MAGENTA}{self.t.t('help_private_title')}{RESET}")
                        print(f"  {self.t.t('help_private_desc')}")
                        print(f"  {self.t.t('help_private_example')} {GREEN}{self.t.t('cmd_upload')} document.pdf @Alice{RESET}")
                        print(f"  {self.t.t('help_private_download')} {GREEN}{self.t.t('cmd_download')} document.pdf{RESET}")
                        print(f"{CYAN}╚══════════════════════════════════════════════════════════╝{RESET}")
                        continue
                    elif msg.startswith('/send '):
                        filename = msg[6:].strip()
                        filepath = os.path.join(self.outbox_folder, filename)
                        if not os.path.isfile(filepath):
                            print(f"{RED}File not found in outbox: {filename}{RESET}")
                            print(f"{YELLOW}Hint: Files must be in the 'data/outbox/' folder{RESET}")
                            continue
                        self.send_file(filepath)
                    elif msg.startswith('/upload '):
                        filename = msg[8:].strip()
                        filepath = os.path.join(self.outbox_folder, filename)
                        if os.path.isfile(filepath):
                            self.send_file(filepath)
                            print(f"{CYAN}[{timestamp()}] Uploaded {filename} to shared folder{RESET}")
                        else:
                            print(f"{RED}File not found in outbox: {filename}{RESET}")
                            print(f"{YELLOW}Hint: Files must be in the 'data/outbox/' folder{RESET}")
                    elif msg == '/outbox':
                        files = [f for f in os.listdir(self.outbox_folder) if not f.startswith('.')]
                        if files:
                            print(f"{CYAN}Outbox contents:{RESET}")
                            for f in files:
                                size = os.path.getsize(os.path.join(self.outbox_folder, f))
                                print(f"  - {f} ({size} bytes)")
                        else:
                            print(f"{YELLOW}Outbox is empty{RESET}")
                            print(f"{CYAN}Place files in 'data/outbox/' folder to upload them{RESET}")
                        continue
                    elif msg.startswith('/download '):
                        filename = msg[10:].strip()
                        # Request file download from shared folder
                        cmd = f"__CMD_DOWNLOAD__:{filename}"
                        encrypted = self.encryption.encrypt(cmd)
                        if encrypted:
                            self.sock.sendall(encrypted.encode() + b'\n')
                            print(f"{CYAN}[{timestamp()}] Requesting {filename} from shared folder...{RESET}")
                    elif msg == '/inbox':
                        files = [f for f in os.listdir(self.inbox_folder) if not f.startswith('.')]
                        if files:
                            print(f"{CYAN}Inbox contents:{RESET}")
                            for f in files:
                                size = os.path.getsize(os.path.join(self.inbox_folder, f))
                                print(f"  - {f} ({size} bytes)")
                        else:
                            print(f"{YELLOW}Inbox is empty{RESET}")
                            print(f"{CYAN}Downloaded files will appear here{RESET}")
                        continue
                    elif msg == '/list':
                        cmd = "__CMD_LIST__"
                        encrypted = self.encryption.encrypt(cmd)
                        if encrypted:
                            self.sock.sendall(encrypted.encode() + b'\n')
                    else:
                        encrypted = self.encryption.encrypt(msg)
                        if encrypted:
                            self.sock.sendall(encrypted.encode() + b'\n')
                except (EOFError, KeyboardInterrupt):
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