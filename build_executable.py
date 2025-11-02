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

# ANSI colors
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
RESET = "\033[0m"

def main():
    """Build executable for current platform"""
    
    print("=" * 60)
    print("Terminal Chat - Executable Builder")
    print("=" * 60)
    
    # Check if PyInstaller is installed
    pyinstaller_found = False
    
    # Try importing (works for pip/venv installs)
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} found")
        pyinstaller_found = True
    except ImportError:
        # Try command (works for pipx installs)
        try:
            result = subprocess.run(["pyinstaller", "--version"],
                                  capture_output=True, text=True, check=True)
            version = result.stdout.strip()
            print(f"✓ PyInstaller {version} found (via pipx)")
            pyinstaller_found = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    
    if not pyinstaller_found:
        print("✗ PyInstaller not found!")
        print(f"\n{RED}ERROR: PyInstaller is required but not installed{RESET}")
        print(f"\n{YELLOW}This system has externally-managed Python.{RESET}")
        print(f"{YELLOW}Please install PyInstaller manually using ONE of these methods:{RESET}\n")
        print(f"{CYAN}Option 1 - Using pipx (recommended):{RESET}")
        print("  sudo apt install pipx")
        print("  pipx install pyinstaller")
        print(f"\n{CYAN}Option 2 - Using venv:{RESET}")
        print("  python3 -m venv venv")
        print("  source venv/bin/activate")
        print("  pip install pyinstaller")
        print("  python build_executable.py")
        print(f"\n{CYAN}Option 3 - System package:{RESET}")
        print("  sudo apt install pyinstaller")
        print(f"\n{YELLOW}Note: The executable already exists in dist/ and works!{RESET}")
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