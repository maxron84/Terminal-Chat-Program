"""
File permissions manager for private file sharing
"""

import json
import os
from datetime import datetime


class FilePermissions:
    """Manage file permissions for private sharing"""
    
    def __init__(self, metadata_file='data/file_permissions.json'):
        """
        Initialize file permissions manager
        
        Args:
            metadata_file (str): Path to metadata file
        """
        self.metadata_file = metadata_file
        self.permissions = self.load_permissions()
    
    def load_permissions(self):
        """Load permissions from file"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_permissions(self):
        """Save permissions to file"""
        os.makedirs(os.path.dirname(self.metadata_file), exist_ok=True)
        with open(self.metadata_file, 'w') as f:
            json.dump(self.permissions, f, indent=2)
    
    def add_file(self, filename, uploader, for_user=None, size=0):
        """
        Add file with permissions
        
        Args:
            filename (str): Name of file
            uploader (str): Username who uploaded
            for_user (str): Username who can access (None = public)
            size (int): File size in bytes
        """
        self.permissions[filename] = {
            'uploader': uploader,
            'for': for_user,
            'uploaded_at': datetime.now().isoformat(),
            'size': size
        }
        self.save_permissions()
    
    def can_download(self, filename, username):
        """
        Check if user can download file
        
        Args:
            filename (str): File to check
            username (str): User trying to download
            
        Returns:
            tuple: (bool, str) - (allowed, reason)
        """
        if filename not in self.permissions:
            # File exists but no permissions = public (backward compatibility)
            return True, "Public file"
        
        perm = self.permissions[filename]
        
        # Public file (no 'for' user specified)
        if perm['for'] is None:
            return True, "Public file"
        
        # Private file - check if user is uploader or recipient
        if username == perm['uploader']:
            return True, "You uploaded this file"
        
        if username == perm['for']:
            return True, f"File shared with you by {perm['uploader']}"
        
        # Not allowed
        return False, f"Private file (from {perm['uploader']} for {perm['for']})"
    
    def get_file_info(self, filename, username):
        """
        Get displayable file information
        
        Args:
            filename (str): File name
            username (str): User requesting info
            
        Returns:
            str: Formatted file info
        """
        if filename not in self.permissions:
            return f"{filename} (public)"
        
        perm = self.permissions[filename]
        
        # Public file
        if perm['for'] is None:
            return f"{filename} (public, uploaded by {perm['uploader']})"
        
        # Private file
        if username == perm['uploader']:
            return f"{filename} (private, for {perm['for']})"
        elif username == perm['for']:
            return f"{filename} (private, from {perm['uploader']})"
        else:
            return f"{filename} (private)"
    
    def remove_file(self, filename):
        """Remove file from permissions"""
        if filename in self.permissions:
            del self.permissions[filename]
            self.save_permissions()
    
    def list_files_for_user(self, username, all_files):
        """
        List files with permissions info for specific user
        
        Args:
            username (str): User requesting list
            all_files (list): List of all filenames in shared folder
            
        Returns:
            list: List of tuples (filename, info_str, can_download)
        """
        result = []
        for filename in all_files:
            can_dl, reason = self.can_download(filename, username)
            info = self.get_file_info(filename, username)
            result.append((filename, info, can_dl))
        return result