@echo off
echo LogWatchdog Build Script
echo ========================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Install PyInstaller if not already installed
echo [INFO] Checking for PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] Failed to install PyInstaller
        pause
        exit /b 1
    )
)

REM Install other dependencies
echo [INFO] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

REM Run the build script
echo [INFO] Starting build process...
python build_exe.py --clean --onefile

if errorlevel 1 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Build completed!
echo [INFO] Executable created: dist\LogWatchdog.exe
echo.
pause
