#!/usr/bin/env python3
"""
LogWatchdog - PyInstaller Build Script
======================================

This script builds a standalone executable for LogWatchdog using PyInstaller.
It handles all necessary configurations, dependencies, and file inclusions.

Usage:
    python build_exe.py [options]

Options:
    --onefile    Create a single executable file (default)
    --onedir     Create a directory with executable and dependencies
    --clean      Clean build artifacts before building
    --debug      Enable debug mode for PyInstaller
"""

import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path

# Build configuration
APP_NAME = "LogWatchdog"
MAIN_SCRIPT = "logwatchdog/main.py"
VERSION = "1.0.0"
AUTHOR = "Pandiyaraj Karuppasamy"

# Required files to include
DATA_FILES = [
    ("logwatchdog", "logwatchdog"),  # Include the entire logwatchdog package
    ("log_config.ini", "."),
    ("env_example.txt", "."),
    ("README.md", "."),
    ("CHANGELOG.md", "."),
    ("LICENSE", "."),
]

# Hidden imports (modules that PyInstaller might miss)
HIDDEN_IMPORTS = [
    "logwatchdog.log_monitor",
    "logwatchdog.email_service", 
    "logwatchdog.notifier",
    "logwatchdog.tray_notifier",
    "watchdog.observers",
    "watchdog.events",
    "plyer",
    "plyer.platforms",
    "plyer.platforms.win",
    "plyer.platforms.win.notification",
    "plyer.platforms.win.libs",
    "plyer.platforms.win.libs.win32gui",
    "plyer.platforms.win.libs.win32con",
    "plyer.platforms.win.libs.win32api",
    "plyer.utils",
    "plyer.facades",
    "plyer.facades.notification",
    "email.mime.text",
    "email.mime.multipart",
    "smtplib",
    "configparser",
    "dotenv",
    "psutil",
    "ctypes",
    "ctypes.wintypes",
    "tkinter",
    "tkinter.ttk",
    "threading",
]

# Exclude modules to reduce size
EXCLUDES = [
    "matplotlib",
    "numpy",
    "pandas",
    "scipy",
    "PIL",
    "PyQt5",
    "PyQt6",
    "PySide2",
    "PySide6",
    "wx",
    "jupyter",
    "notebook",
    "IPython",
]

def clean_build_artifacts():
    """Clean previous build artifacts."""
    print("[INFO] Cleaning build artifacts...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    files_to_clean = ["*.spec"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"[INFO] Removed directory: {dir_name}")
    
    # Clean .spec files
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"[INFO] Removed spec file: {spec_file}")

def check_dependencies():
    """Check if required dependencies are installed."""
    print("[INFO] Checking dependencies...")
    
    # Map package names to their import names
    package_imports = {
        "pyinstaller": "PyInstaller",
        "watchdog": "watchdog",
        "plyer": "plyer", 
        "python-dotenv": "dotenv",
        "psutil": "psutil"
    }
    
    missing_packages = []
    
    for package, import_name in package_imports.items():
        try:
            __import__(import_name)
            print(f"[INFO] ✓ {package} ({import_name})")
        except ImportError:
            missing_packages.append(package)
            print(f"[WARNING] ✗ {package} ({import_name})")
    
    if missing_packages:
        print(f"[ERROR] Missing required packages: {', '.join(missing_packages)}")
        print("[INFO] Install missing packages with: pip install -r requirements.txt")
        return False
    
    print("[INFO] All dependencies are available")
    return True

def build_executable(onefile=True, debug=False):
    """Build the executable using PyInstaller."""
    print(f"[INFO] Building {'single file' if onefile else 'directory'} executable...")
    
    # Base PyInstaller command
    cmd = [
        "pyinstaller",
        "--name", APP_NAME,
        "--version", VERSION,
        "--author", AUTHOR,
        "--description", "Real-time log file monitoring with exception detection",
        "--onefile" if onefile else "--onedir",
        "--windowed",  # Hide console window
        "--noconfirm",  # Overwrite output directory
    ]
    
    # Add hidden imports
    for module in HIDDEN_IMPORTS:
        cmd.extend(["--hidden-import", module])
    
    # Add excluded modules
    for module in EXCLUDES:
        cmd.extend(["--exclude-module", module])
    
    # Add data files
    for src, dst in DATA_FILES:
        if os.path.exists(src):
            cmd.extend(["--add-data", f"{src};{dst}"])
        else:
            print(f"[WARNING] Data file not found: {src}")
    
    # Add debug options
    if debug:
        cmd.append("--debug=all")
        cmd.append("--log-level=DEBUG")
    
    # Add the main script
    cmd.append(MAIN_SCRIPT)
    
    print(f"[INFO] Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("[INFO] Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build failed with return code {e.returncode}")
        print(f"[ERROR] stdout: {e.stdout}")
        print(f"[ERROR] stderr: {e.stderr}")
        return False

def create_installer_script():
    """Create a simple installer script for the built executable."""
    installer_content = f'''@echo off
echo Installing {APP_NAME}...
echo.

REM Create application directory
if not exist "%PROGRAMFILES%\\{APP_NAME}" mkdir "%PROGRAMFILES%\\{APP_NAME}"

REM Copy executable
copy "dist\\{APP_NAME}.exe" "%PROGRAMFILES%\\{APP_NAME}\\"

REM Copy configuration files
copy "log_config.ini" "%PROGRAMFILES%\\{APP_NAME}\\"
copy "env_example.txt" "%PROGRAMFILES%\\{APP_NAME}\\"

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\{APP_NAME}.lnk'); $Shortcut.TargetPath = '%PROGRAMFILES%\\{APP_NAME}\\{APP_NAME}.exe'; $Shortcut.Save()"

echo.
echo {APP_NAME} has been installed successfully!
echo You can find the application in: %PROGRAMFILES%\\{APP_NAME}\\
echo Desktop shortcut has been created.
echo.
pause
'''
    
    with open("install.bat", "w") as f:
        f.write(installer_content)
    
    print("[INFO] Created installer script: install.bat")

def main():
    """Main build function."""
    parser = argparse.ArgumentParser(description="Build LogWatchdog executable")
    parser.add_argument("--onefile", action="store_true", default=True,
                       help="Create a single executable file (default)")
    parser.add_argument("--onedir", action="store_true",
                       help="Create a directory with executable and dependencies")
    parser.add_argument("--clean", action="store_true",
                       help="Clean build artifacts before building")
    parser.add_argument("--debug", action="store_true",
                       help="Enable debug mode for PyInstaller")
    
    args = parser.parse_args()
    
    print(f"[INFO] {APP_NAME} Build Script")
    print("=" * 50)
    
    # Clean if requested
    if args.clean:
        clean_build_artifacts()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Determine build mode
    onefile = args.onefile and not args.onedir
    
    # Build executable
    if build_executable(onefile=onefile, debug=args.debug):
        print("\n[SUCCESS] Build completed successfully!")
        print(f"[INFO] Executable location: dist/{APP_NAME}.exe")
        print(f"[INFO] Build type: {'Single file' if onefile else 'Directory'}")
        
        # Create installer script
        create_installer_script()
        
        print("\n[INFO] Next steps:")
        print("1. Test the executable: dist/LogWatchdog.exe")
        print("2. Copy log_config.ini to the same directory as the executable")
        print("3. Create a .env file with your email credentials")
        print("4. Run the executable to start monitoring")
        
    else:
        print("\n[ERROR] Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
