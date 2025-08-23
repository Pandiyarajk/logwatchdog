# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- Additional notification channels
- Web dashboard interface
- Log analysis and reporting features
