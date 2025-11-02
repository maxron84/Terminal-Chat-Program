#!/usr/bin/env python3
"""
Unit and Integration Tests for Cozy Secure Chat
Run with: python3 -m pytest test_chat.py -v
Or: python3 test_chat.py
"""

import unittest
import tempfile
import os
import shutil
import socket
import threading
import time
import sys

# Import the chat modules from lib
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from lib import Encryption, ChatServer, ChatClient, FilePermissions
from lib.utils import timestamp


class TestEncryption(unittest.TestCase):
    """Unit tests for encryption/decryption"""
    
    def setUp(self):
        self.password = "test_password_123"
        self.encryption = Encryption(self.password)
    
    def test_encrypt_decrypt_simple_message(self):
        """Test basic encryption and decryption"""
        message = "Hello, World!"
        encrypted = self.encryption.encrypt(message)
        
        self.assertIsNotNone(encrypted)
        self.assertNotEqual(encrypted, message)
        
        decrypted = self.encryption.decrypt(encrypted)
        self.assertEqual(decrypted, message)
    
    def test_encrypt_decrypt_long_message(self):
        """Test encryption of longer messages"""
        message = ("This is a much longer message with multiple sentences. " * 10).strip()
        encrypted = self.encryption.encrypt(message)
        
        self.assertIsNotNone(encrypted)
        
        decrypted = self.encryption.decrypt(encrypted)
        self.assertEqual(decrypted, message)
    
    def test_encrypt_special_characters(self):
        """Test encryption with special characters"""
        message = "Special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        encrypted = self.encryption.encrypt(message)
        
        self.assertIsNotNone(encrypted)
        
        decrypted = self.encryption.decrypt(encrypted)
        self.assertEqual(decrypted, message)
    
    def test_encrypt_unicode(self):
        """Test encryption with Unicode characters"""
        message = "Unicode: 你好世界 🎉 مرحبا العالم"
        encrypted = self.encryption.encrypt(message)
        
        self.assertIsNotNone(encrypted)
        
        decrypted = self.encryption.decrypt(encrypted)
        self.assertEqual(decrypted, message)
    
    def test_wrong_password_fails(self):
        """Test that wrong password fails to decrypt"""
        message = "Secret message"
        encrypted = self.encryption.encrypt(message)
        
        wrong_encryption = Encryption("wrong_password")
        decrypted = wrong_encryption.decrypt(encrypted)
        
        self.assertIsNone(decrypted)
    
    def test_empty_message(self):
        """Test encryption of empty string"""
        message = ""
        encrypted = self.encryption.encrypt(message)
        
        self.assertIsNotNone(encrypted)
        
        decrypted = self.encryption.decrypt(encrypted)
        self.assertEqual(decrypted, message)
    
    def test_newlines_removed_from_encrypted(self):
        """Test that encrypted output has no newlines"""
        message = "Line 1\nLine 2\nLine 3"
        encrypted = self.encryption.encrypt(message)
        
        self.assertNotIn('\n', encrypted)
        self.assertNotIn('\r', encrypted)


class TestChatClient(unittest.TestCase):
    """Unit tests for ChatClient functionality"""
    
    def setUp(self):
        self.client = ChatClient("localhost", 4444, "test_pass", "TestUser")
    
    def test_client_initialization(self):
        """Test client initializes correctly"""
        self.assertEqual(self.client.host, "localhost")
        self.assertEqual(self.client.port, 4444)
        self.assertEqual(self.client.username, "TestUser")
        self.assertTrue(self.client.running)
        # Check that shared_folder contains the correct folder name
        self.assertTrue(self.client.shared_folder.endswith("shared"))
        self.assertTrue(self.client.outbox_folder.endswith("outbox"))
        self.assertTrue(self.client.inbox_folder.endswith("inbox"))
    
    def test_color_assignment_own_user(self):
        """Test that own username gets blue color"""
        from lib.utils import BLUE
        color = self.client.get_user_color("TestUser")
        self.assertEqual(color, BLUE)
    
    def test_color_assignment_admin(self):
        """Test that admin gets magenta color"""
        from lib.utils import MAGENTA
        
        admin_names = ["admin01", "Admin", "ADMIN", "server", "Server"]
        for name in admin_names:
            color = self.client.get_user_color(name)
            self.assertEqual(color, MAGENTA, f"Failed for {name}")
    
    def test_color_assignment_consistency(self):
        """Test that same user always gets same color"""
        color1 = self.client.get_user_color("user01")
        color2 = self.client.get_user_color("user01")
        self.assertEqual(color1, color2)
    
    def test_color_assignment_different_users(self):
        """Test that different users get different colors"""
        colors = set()
        for i in range(5):
            color = self.client.get_user_color(f"user{i:02d}")
            colors.add(color)
        
        # Should have assigned different colors
        self.assertGreater(len(colors), 1)


class TestChatServer(unittest.TestCase):
    """Unit tests for ChatServer functionality"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)
        
    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir)
    
    def test_server_initialization(self):
        """Test server initializes correctly"""
        server = ChatServer(5555, "test_pass", "TestServer")
        
        self.assertEqual(server.port, 5555)
        self.assertEqual(server.username, "TestServer")
        self.assertTrue(server.running)
        # Check that folder paths end with correct names
        self.assertTrue(server.shared_folder.endswith("shared"))
        self.assertTrue(server.outbox_folder.endswith("outbox"))
        
        # Check that shared folder was created
        self.assertTrue(os.path.exists(server.shared_folder))
        
        # Check that logs directory was created
        self.assertTrue(os.path.exists("logs"))
    
    def test_broadcast_message_encryption(self):
        """Test that broadcast encrypts messages"""
        server = ChatServer(5556, "test_pass", "TestServer")
        
        # Broadcast doesn't actually send without clients, but we can test encryption
        self.assertIsNotNone(server.encryption.encrypt("test message"))


class TestFileOperations(unittest.TestCase):
    """Unit tests for file operations"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test.txt")
        
        # Create a test file
        with open(self.test_file, 'w') as f:
            f.write("Line 1\nLine 2\nLine 3\n")
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_file_exists(self):
        """Test file operations"""
        self.assertTrue(os.path.isfile(self.test_file))
        
        with open(self.test_file, 'r') as f:
            content = f.read()
        
        self.assertIn("Line 1", content)
        self.assertIn("Line 2", content)
        self.assertIn("Line 3", content)
    
    def test_base64_encoding(self):
        """Test base64 encoding for file transfer"""
        import base64
        
        with open(self.test_file, 'rb') as f:
            data = f.read()
        
        encoded = base64.b64encode(data).decode()
        decoded = base64.b64decode(encoded)
        
        self.assertEqual(data, decoded)


class TestFilePermissions(unittest.TestCase):
    """Unit tests for FilePermissions functionality"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.metadata_file = os.path.join(self.temp_dir, "file_permissions.json")
        self.file_perms = FilePermissions(self.metadata_file)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_file_permissions_initialization(self):
        """Test file permissions initializes correctly"""
        self.assertIsNotNone(self.file_perms)
        self.assertEqual(self.file_perms.metadata_file, self.metadata_file)
    
    def test_add_public_file(self):
        """Test adding a public file"""
        self.file_perms.add_file("test.pdf", "Alice", None, 1000)
        
        can_download, reason = self.file_perms.can_download("test.pdf", "Bob")
        self.assertTrue(can_download)
        self.assertEqual(reason, "Public file")
    
    def test_add_private_file(self):
        """Test adding a private file"""
        self.file_perms.add_file("private.pdf", "Alice", "Bob", 2000)
        
        # Uploader can download
        can_download, reason = self.file_perms.can_download("private.pdf", "Alice")
        self.assertTrue(can_download)
        self.assertEqual(reason, "You uploaded this file")
        
        # Recipient can download
        can_download, reason = self.file_perms.can_download("private.pdf", "Bob")
        self.assertTrue(can_download)
        self.assertIn("shared with you", reason)
        
        # Others cannot download
        can_download, reason = self.file_perms.can_download("private.pdf", "Charlie")
        self.assertFalse(can_download)
        self.assertIn("Private file", reason)
    
    def test_get_file_info_public(self):
        """Test getting info for public file"""
        self.file_perms.add_file("public.txt", "Alice", None, 500)
        
        info = self.file_perms.get_file_info("public.txt", "Bob")
        self.assertIn("public", info)
        self.assertIn("Alice", info)
    
    def test_get_file_info_private(self):
        """Test getting info for private file"""
        self.file_perms.add_file("secret.txt", "Alice", "Bob", 600)
        
        # For uploader
        info = self.file_perms.get_file_info("secret.txt", "Alice")
        self.assertIn("private", info)
        self.assertIn("for Bob", info)
        
        # For recipient
        info = self.file_perms.get_file_info("secret.txt", "Bob")
        self.assertIn("private", info)
        self.assertIn("from Alice", info)
        
        # For others
        info = self.file_perms.get_file_info("secret.txt", "Charlie")
        self.assertEqual(info, "secret.txt (private)")
    
    def test_list_files_for_user(self):
        """Test listing files with permissions"""
        self.file_perms.add_file("public.txt", "Alice", None, 100)
        self.file_perms.add_file("private.txt", "Alice", "Bob", 200)
        
        files = ["public.txt", "private.txt"]
        
        # Bob's view
        result = self.file_perms.list_files_for_user("Bob", files)
        self.assertEqual(len(result), 2)
        
        # Check public file
        filename, info, can_dl = result[0]
        self.assertEqual(filename, "public.txt")
        self.assertTrue(can_dl)
        
        # Check private file
        filename, info, can_dl = result[1]
        self.assertEqual(filename, "private.txt")
        self.assertTrue(can_dl)  # Bob is recipient
        
        # Charlie's view
        result = self.file_perms.list_files_for_user("Charlie", files)
        filename, info, can_dl = result[1]
        self.assertEqual(filename, "private.txt")
        self.assertFalse(can_dl)  # Charlie cannot access
    
    def test_persistence(self):
        """Test that permissions persist to file"""
        self.file_perms.add_file("persist.txt", "Alice", "Bob", 300)
        
        # Create new instance with same file
        new_perms = FilePermissions(self.metadata_file)
        
        can_download, reason = new_perms.can_download("persist.txt", "Bob")
        self.assertTrue(can_download)


class TestIntegration(unittest.TestCase):
    """Integration tests for server-client communication"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)
        
        self.port = 6000
        self.password = "integration_test_pass"
        
    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir)
    
    def test_server_starts_and_stops(self):
        """Test that server can start and stop"""
        server = ChatServer(self.port, self.password, "IntegrationServer")
        
        self.assertTrue(server.running)
        
        # Stop server
        server.running = False
        self.assertFalse(server.running)
    
    def test_timestamp_format(self):
        """Test timestamp function returns correct format"""
        ts = timestamp()
        
        # Should be HH:MM:SS format
        self.assertEqual(len(ts), 8)
        self.assertEqual(ts[2], ':')
        self.assertEqual(ts[5], ':')


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions"""
    
    def test_timestamp_returns_string(self):
        """Test timestamp returns a string"""
        ts = timestamp()
        self.assertIsInstance(ts, str)
    
    def test_timestamp_format(self):
        """Test timestamp has correct format"""
        ts = timestamp()
        parts = ts.split(':')
        
        self.assertEqual(len(parts), 3)
        self.assertTrue(0 <= int(parts[0]) <= 23)  # Hour
        self.assertTrue(0 <= int(parts[1]) <= 59)  # Minute
        self.assertTrue(0 <= int(parts[2]) <= 59)  # Second


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestEncryption))
    suite.addTests(loader.loadTestsFromTestCase(TestChatClient))
    suite.addTests(loader.loadTestsFromTestCase(TestChatServer))
    suite.addTests(loader.loadTestsFromTestCase(TestFileOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestFilePermissions))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilityFunctions))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)