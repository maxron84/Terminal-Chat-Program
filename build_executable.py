#!/usr/bin/env python3
"""
Build standalone executables for Terminal Chat using PyInstaller
Run this script to create executables for your current platform
"""

import sys
import os
import platform
import subprocess
import shutil

def main():
    """Build executable for current platform"""
    
    print("=" * 60)
    print("Terminal Chat - Executable Builder")
    print("=" * 60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("✗ PyInstaller not found!")
        print("\nInstalling PyInstaller (user mode)...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "pyinstaller"])
            print("✓ PyInstaller installed")
        except subprocess.CalledProcessError:
            print(f"\n{RED}Failed to install PyInstaller!{RESET}")
            print("\nPlease install manually:")
            print("  pip install --user pyinstaller")
            print("  OR")
            print("  pipx install pyinstaller")
            sys.exit(1)
    
    # Determine platform
    system = platform.system()
    arch = platform.machine()
    print(f"✓ Platform: {system} ({arch})")
    
    # Set output name based on platform
    if system == "Windows":
        output_name = "terminal-chat-windows"
        icon = None  # Add .ico file if you have one
    elif system == "Darwin":
        output_name = "terminal-chat-macos"
        icon = None  # Add .icns file if you have one
    else:
        output_name = "terminal-chat-linux"
        icon = None
    
    # PyInstaller command
    # We need to add src to the Python path for imports to work
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable
        "--name", output_name,
        "--clean",  # Clean PyInstaller cache
        "--paths", "src",  # Add src to Python path
        "--add-data", f"src{os.pathsep}src",  # Include src directory
        "--add-data", f"bin{os.pathsep}bin",  # Include bin directory
        "bin/terminal-chat.py"
    ]
    
    if icon:
        cmd.extend(["--icon", icon])
    
    print("\n" + "=" * 60)
    print("Building executable...")
    print("=" * 60)
    print(f"Command: {' '.join(cmd)}\n")
    
    # Build
    try:
        subprocess.check_call(cmd)
        print("\n" + "=" * 60)
        print("✓ Build successful!")
        print("=" * 60)
        
        # Find the executable
        dist_dir = "dist"
        if system == "Windows":
            exe_path = os.path.join(dist_dir, f"{output_name}.exe")
        else:
            exe_path = os.path.join(dist_dir, output_name)
        
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"\nExecutable: {exe_path}")
            print(f"Size: {size_mb:.1f} MB")
            print(f"\nTo run: ./{exe_path}")
        
        # Clean up build artifacts
        print("\nCleaning up build files...")
        if os.path.exists("build"):
            shutil.rmtree("build")
        if os.path.exists(f"{output_name}.spec"):
            os.remove(f"{output_name}.spec")
        print("✓ Cleanup complete")
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()