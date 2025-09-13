# LogWatchdog

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/logwatchdog.svg)](https://pypi.org/project/logwatchdog/)
[![GitHub](https://img.shields.io/badge/github-logwatchdog-green.svg)](https://github.com/pandiyarajk/logwatchdog)
[![Build Log Watchdog Executable](https://github.com/Pandiyarajk/logwatchdog/actions/workflows/build-exe.yml/badge.svg)](https://github.com/Pandiyarajk/logwatchdog/actions/workflows/build-exe.yml)
[![Windows](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/windows)
[![PyInstaller](https://img.shields.io/badge/build-PyInstaller-green.svg)](https://pyinstaller.org/)


**LogWatchdog** is a powerful real-time log monitoring solution that detects exceptions and errors in log files, providing instant alerts through multiple notification channels.

## 🚀 Features

- **Real-time Log Monitoring**: Monitor single files, multiple files, or entire folders
- **Smart Exception Detection**: Configurable keywords for error detection
- **Multi-channel Notifications**: 
  - Custom flash popups (executables)
  - System tray notifications (script mode)
  - Email alerts with batch processing
  - Console output with detailed logging
- **Auto-configuration**: Creates default config files automatically
- **Standalone Executable**: No Python installation required on target systems
- **Batch Email Processing**: Groups multiple errors from same file into single email
- **File Discovery**: Automatic detection of new log files
- **Windows Optimized**: Designed specifically for Windows 10/11 systems

## 📋 Requirements

- **Python 3.7+**
- **Windows 10/11** (primary target)

## 🛠️ Installation

### Option 1: Standalone Executable (Recommended)

1. **Download** the latest `LogWatchdog.exe` from releases
2. **Run** the executable - it will create default configuration automatically
3. **Configure** your settings in the generated `log_config.ini` file

### Option 2: From Source

```bash
git clone https://github.com/pandiyarajk/logwatchdog.git
cd logwatchdog
pip install -r requirements.txt
```

### Option 3: Build Your Own Executable

```bash
# Install dependencies
pip install -r requirements.txt

# Build executable
python build_exe.py

# Or use the simple batch file
build.bat
```

## 🚀 Quick Start

### 1. Run the Application

**For Executable:**
```bash
# Just run the executable - it creates config automatically
LogWatchdog.exe
```

**For Script:**
```bash
python -m logwatchdog.main
```

### 2. Auto-Generated Configuration

The application automatically creates `log_config.ini` with sensible defaults:

```ini
# LogWatchdog Configuration File
# =============================
# This file was automatically created by LogWatchdog.
# Modify the values below to customize your monitoring setup.

[monitoring]
monitor_mode = folder
log_folder_path = C:\path\to\execution\directory\logs
log_file_extensions = *.log,*.txt,*.evtx
file_discovery_interval = 30
empty_monitor_delay = 10

[notifications]
email_enabled = false
smtp_server = smtp.gmail.com
smtp_port = 587
receiver_group = admin@company.com
system_tray_notifications = true
batch_email_enabled = true

[alerts]
exception_keywords = Exception,Error,Failure,Fail,Fatal,Issue,Crash,Close,Cannot,Wrong,unsupported,not found,retry,terminated,disconnected
```

### 3. Email Setup (Optional)

Create `.env` file for email notifications:

```bash
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

**Security Note**: Never commit the `.env` file to version control.

## 📁 Monitoring Modes

- **Single File**: Monitor one specific log file
- **Multiple Files**: Monitor multiple specific log files simultaneously  
- **Folder**: Monitor all log files in a folder with automatic file detection

## 🔧 Configuration

### Main Settings (`log_config.ini`)

- **Monitoring**: Mode, file paths, discovery intervals
- **Notifications**: Email settings, batch processing, system alerts
- **Alerts**: Exception keywords and detection rules

### Email Credentials (`.env`)

- `EMAIL_USER`: Your email address
- `EMAIL_PASSWORD`: Your email password or app password

## 🎯 Key Features Explained

### Smart Notifications

**For Executables:**
- **Flash Popup**: Custom red popup that auto-closes after 3 seconds
- **Taskbar Flashing**: Console window flashes 3 times
- **System Sound**: Windows beep plays with alerts
- **Console Output**: Detailed logging information

**For Scripts:**
- **System Tray**: Native Windows toast notifications
- **Fallback Support**: Graceful degradation if notifications fail

### Batch Email Processing

- **Groups Errors**: Multiple errors from same file = single email
- **Rich Content**: Error count, timestamps, detailed information
- **Configurable**: Can be disabled via `batch_email_enabled = false`

### Auto-Configuration

- **Creates Config**: Automatically generates `log_config.ini` if missing
- **Sensible Defaults**: Works out-of-the-box with minimal setup
- **Path Resolution**: Smart detection of execution directory vs script directory

## 🛠️ Build Scripts

### `build_exe.py` - Advanced Build Script
- **Dependency checking** with proper package mapping
- **Clean build artifacts** before building
- **Hidden imports** for all modules
- **Data file inclusion** (config files, README, etc.)
- **Debug mode** for troubleshooting
- **Installer script generation**

### `build.bat` - Simple Windows Batch File
- **Automatic dependency installation**
- **User-friendly interface**
- **Error handling**

## 📚 Documentation

- **User Guide**: See the code comments and configuration examples
- **Issues**: [GitHub Issues](https://github.com/pandiyarajk/logwatchdog/issues)
- **Support**: pandiyarajk@live.com

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](https://github.com/pandiyarajk/logwatchdog/blob/main/CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/pandiyarajk/logwatchdog/blob/main/LICENSE) file for details.

## 🔄 Changelog

See [CHANGELOG.md](https://github.com/pandiyarajk/logwatchdog/blob/main/CHANGELOG.md) for version history.

---

**Made with ❤️ by [Pandiyaraj Karuppasamy](https://github.com/pandiyarajk)**

*LogWatchdog - Your Windows Log Monitoring Companion*
