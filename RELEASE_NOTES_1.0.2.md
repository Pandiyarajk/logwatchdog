# LogWatchdog v1.0.2 Release Notes

**Release Date:** September 13, 2025  
**Version:** 1.0.2  
**Type:** Minor Release with Major New Features

## 🚀 What's New

### Standalone Executable Support
- **PyInstaller Integration**: Complete build system for creating standalone Windows executables
- **Build Scripts**: Advanced `build_exe.py` and simple `build.bat` for easy executable creation
- **Smart Path Resolution**: Intelligent detection of execution directory vs script directory

### Enhanced Notification System
- **Custom Flash Popups**: Beautiful red popup notifications for executables (auto-closes after 3 seconds)
- **Multi-layered Alerts**: Taskbar flashing, system sounds, and visual popups
- **Dual Mode Support**: 
  - Executables: Custom flash popups + taskbar flashing + system sounds
  - Scripts: Native system tray notifications with plyer fallback

### Auto-Configuration
- **Auto-Generated Config**: Automatically creates `log_config.ini` with sensible defaults
- **Enhanced Configuration**: Auto-generated config files with helpful comments and defaults
- **Smart Environment Detection**: Enhanced .env file location detection and error reporting

### Email Improvements
- **Batch Email Processing**: Groups multiple errors from same file into single email
- **Rich Email Content**: Error counts, timestamps, and detailed information
- **Spam Prevention**: Batch processing prevents multiple emails for same file errors

## 🔧 Technical Improvements

### Core Enhancements
- **Threading Support**: Non-blocking notifications and popup handling
- **Windows API Integration**: Direct ctypes integration for taskbar flashing and system sounds
- **Improved Error Handling**: Graceful fallbacks for notification failures
- **Dependency Management**: Streamlined requirements with version specifications

### Bug Fixes
- **Import Issues**: Resolved all PyInstaller import problems with proper module mapping
- **Notification Failures**: Robust fallback system prevents crashes on notification errors
- **Path Handling**: Smart path resolution works in both script and executable modes

## 📦 Installation

### From PyPI (Recommended)
```bash
pip install --upgrade logwatchdog
```

### From Source
```bash
git clone https://github.com/pandiyarajk/logwatchdog.git
cd logwatchdog
pip install -e .
```

### Standalone Executable
1. Download the latest release from [GitHub Releases](https://github.com/pandiyarajk/logwatchdog/releases)
2. Extract and run `LogWatchdog.exe`
3. Configuration will be auto-generated on first run

## 🎯 Key Features

- **Real-time Log Monitoring**: Monitor single files, multiple files, or entire folders
- **Smart Notifications**: Email alerts and system tray notifications for critical events
- **Configurable Alerts**: Customizable exception keywords and notification rules
- **File Discovery**: Automatic detection of new log files
- **Windows Native**: Designed specifically for Windows 10/11 systems
- **Security**: Environment variable-based email credentials (.env file)
- **Standalone Executables**: No Python installation required for end users

## 🔄 Migration from v1.0.1

This is a backward-compatible release. Existing configurations will continue to work. New features are automatically available:

- Executable builds will get enhanced popup notifications
- Script mode will continue to use system tray notifications
- Email batching will automatically group related errors
- Auto-configuration will help new users get started quickly

## 📋 Requirements

- **Python**: 3.7+ (for script mode)
- **OS**: Windows 10/11 (recommended)
- **Dependencies**: Automatically installed with pip

## 🐛 Bug Reports & Support

- **Issues**: [GitHub Issues](https://github.com/pandiyarajk/logwatchdog/issues)
- **Documentation**: [README.md](https://github.com/pandiyarajk/logwatchdog/blob/main/README.md)
- **Changelog**: [CHANGELOG.md](https://github.com/pandiyarajk/logwatchdog/blob/main/CHANGELOG.md)

## 🙏 Acknowledgments

Thank you to all contributors and users who provided feedback and suggestions for this release!

---

**Full Changelog**: [v1.0.1...v1.0.2](https://github.com/pandiyarajk/logwatchdog/compare/v1.0.1...v1.0.2)
