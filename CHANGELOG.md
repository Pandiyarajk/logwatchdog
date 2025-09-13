# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [1.0.2] - 09-13-2025

### Added
- **Standalone Executable Support**: PyInstaller build system for creating standalone executables
- **Auto-Configuration**: Automatically creates `log_config.ini` with sensible defaults
- **Custom Flash Popups**: Beautiful red popup notifications for executables (auto-closes after 3 seconds)
- **Batch Email Processing**: Groups multiple errors from same file into single email
- **Enhanced Notifications**: Multi-layered alert system with taskbar flashing, system sounds, and visual popups
- **Build Scripts**: Advanced `build_exe.py` and simple `build.bat` for easy executable creation
- **Smart Path Resolution**: Intelligent detection of execution directory vs script directory
- **Improved Error Handling**: Graceful fallbacks for notification failures

### Enhanced
- **Notification System**: 
  - Executables: Custom flash popups + taskbar flashing + system sounds
  - Scripts: Native system tray notifications with plyer fallback
- **Email Alerts**: Rich content with error counts, timestamps, and detailed information
- **Configuration**: Auto-generated config files with helpful comments and defaults
- **Logging**: Enhanced .env file location detection and error reporting

### Technical
- **PyInstaller Integration**: Complete build system with hidden imports and data files
- **Tkinter Integration**: Custom popup notifications for Windows executables
- **Threading Support**: Non-blocking notifications and popup handling
- **Windows API**: Direct ctypes integration for taskbar flashing and system sounds
- **Dependency Management**: Streamlined requirements with version specifications

### Fixed
- **Import Issues**: Resolved all PyInstaller import problems with proper module mapping
- **Notification Failures**: Robust fallback system prevents crashes on notification errors
- **Path Handling**: Smart path resolution works in both script and executable modes
- **Email Spam**: Batch processing prevents multiple emails for same file errors

---

## [1.0.1] - 08-23-2025

### Fixed
- **PyPI Link Issues**: Fixed broken relative links in README.md that prevented proper display on PyPI
  - CONTRIBUTING.md link now uses absolute GitHub URL
  - LICENSE link now uses absolute GitHub URL  
  - CHANGELOG.md link now uses absolute GitHub URL
- **Badge Updates**: Improved PyPI version badge and added GitHub Actions build badge
- **Documentation**: All links now work correctly on both GitHub and PyPI

### Technical
- Updated package version from 1.0.0 to 1.0.1
- All documentation links use absolute GitHub URLs for cross-platform compatibility

---

## [1.0.0] - 08-23-2025

### Added
- **Real-time Log Monitoring**: Monitor single files, multiple files, or entire folders
- **Smart Notifications**: Email alerts and system tray notifications for critical events
- **Configurable Alerts**: Customizable exception keywords and notification rules
- **File Discovery**: Automatic detection of new log files
- **Windows Native**: Designed specifically for Windows 10/11 systems
- **Security**: Environment variable-based email credentials (.env file)
- **Configuration**: INI-based configuration file (log_config.ini)

### Features
- Three monitoring modes: single file, multiple files, and folder monitoring
- Automatic file discovery with configurable intervals
- SMTP email notifications with secure credential management
- System tray notifications for real-time alerts
- Support for multiple log file extensions (*.log, *.txt, *.evtx)
- Efficient file tailing for large log files

### Technical
- Built with Python 3.7+ compatibility
- Uses watchdog library for file system monitoring
- ConfigParser for INI file configuration
- python-dotenv for secure credential management
- plyer for cross-platform notifications

---

## [Unreleased]

### Planned
- Web dashboard interface
- Log analysis and reporting features
- Configuration GUI
- Remote monitoring capabilities
