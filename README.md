# LogWatchdog

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/logwatchdog.svg)](https://badge.fury.io/py/logwatchdog)
[![GitHub release](https://img.shields.io/github/release/pandiyarajk/logwatchdog.svg)](https://github.com/pandiyarajk/logwatchdog/releases)

**LogWatchdog** is a production-ready Windows log monitoring and management solution that provides real-time monitoring, notifications, and automated log management capabilities.

## 🚀 Features

> **Windows-Only Solution**: LogWatchdog is specifically designed for Windows 10/11 systems with native Windows integration and features.

- **Real-time Log Monitoring**: Monitor application logs, custom log files, and network logs
- **Smart Notifications**: Email, desktop, and system tray notifications for critical events
- **Event Filtering**: Filter events by severity, category, and custom criteria
- **Automated Log Management**: Automatic log rotation, archiving, and cleanup
- **Log File Integration**: Native support for various log file formats
- **Configurable Alerts**: Customizable alert thresholds and notification rules
- **System Tray Integration**: Background monitoring with system tray access
- **Windows Native**: Designed specifically for Windows with native system integration

## 📋 Requirements

- **Python 3.7+**
- **Windows 10/11** (primary target)
- **Administrator privileges** (for system monitoring)

## 🛠️ Installation

### From PyPI (Recommended)

```bash
pip install logwatchdog
```

### From Source

```bash
git clone https://github.com/pandiyarajk/logwatchdog.git
cd logwatchdog
pip install -r requirements.txt
```

### Windows Executable (Recommended)

Download the latest release from [GitHub Releases](https://github.com/pandiyarajk/logwatchdog/releases) for a standalone Windows executable. This is the recommended installation method for Windows users.

## 🚀 Quick Start

### Basic Usage

```python
from logwatchdog import LogWatchdog

# Initialize the watchdog
watchdog = LogWatchdog()

# Start monitoring
watchdog.start_monitoring()
```

### Command Line Interface

```bash
# Start monitoring with default settings
python -m logwatchdog

# Monitor specific log files
python -m logwatchdog --files app.log,system.log,security.log

# Set custom notification thresholds
python -m logwatchdog --threshold Error --email admin@company.com
```

### Configuration File

Create `config.ini` for custom settings:

```ini
[monitoring]
log_files = app.log,system.log,security.log
threshold = Error
max_events = 1000

[notifications]
email_enabled = true
email_address = admin@company.com
desktop_notifications = true
tray_notifications = true

[logging]
log_level = INFO
log_file = logwatchdog.log
rotation_size = 10MB
backup_count = 5
```

## 📚 Documentation

- **[User Guide](docs/user-guide.md)** - Complete usage instructions
- **[API Reference](docs/api-reference.md)** - Developer documentation
- **[Configuration Guide](docs/configuration.md)** - Configuration options
- **[Examples](examples/)** - Code examples and use cases

## 🏗️ Architecture

```
logwatchdog/
├── core/                 # Core monitoring engine
├── monitors/            # Log monitoring modules
├── notifiers/           # Notification systems
├── utils/               # Utility functions
├── config/              # Configuration management
└── cli/                 # Command line interface
```

## 🔧 Configuration

### Environment Variables

```bash
LOGWATCHDOG_CONFIG_PATH=/path/to/config.ini
LOGWATCHDOG_LOG_LEVEL=INFO
LOGWATCHDOG_EMAIL_SMTP=smtp.gmail.com
LOGWATCHDOG_EMAIL_PORT=587
```

### Configuration File Locations

1. `./config.ini` (current directory)
2. `~/.config/logwatchdog/config.ini` (user config)
3. `/etc/logwatchdog/config.ini` (system config)

## 📊 Monitoring Capabilities

### Log File Monitoring

- **Application Logs**: Application software log files and errors
- **System Logs**: System and hardware log files
- **Custom Logs**: User-defined log file sources
- **Real-time Monitoring**: Live log file monitoring and analysis

### File Logs

- **Text Logs**: Plain text log files
- **JSON Logs**: Structured JSON log files
- **CSV Logs**: Comma-separated value logs
- **Custom Formats**: Extensible log format support

### Network Logs

- **Syslog**: RFC 3164/5424 syslog support
- **Windows Event Forwarding**: Native Windows event collection
- **Custom Protocols**: Extensible network monitoring

## 🔔 Notification Systems

### Email Notifications

- SMTP support with authentication
- HTML and plain text formats
- Customizable templates
- Rate limiting and throttling

### Desktop Notifications

- Native Windows toast notifications
- Windows 10/11 notification center integration
- Custom notification styles
- Click-through actions
- Persistent notifications

### System Tray

- Background monitoring
- Quick access menu
- Status indicators
- Silent operation

## 🚨 Alert Management

### Severity Levels

- **Critical**: Immediate attention required
- **Error**: Error conditions affecting functionality
- **Warning**: Potential issues requiring monitoring
- **Information**: General informational messages
- **Debug**: Detailed diagnostic information

### Alert Rules

- **Threshold-based**: Alert when events exceed thresholds
- **Pattern-based**: Alert on specific event patterns
- **Time-based**: Alert during specific time windows
- **Custom**: User-defined alert conditions

## 🔒 Security Features

- **Authentication**: Secure access to monitoring systems
- **Encryption**: Encrypted communication channels
- **Audit Logging**: Comprehensive audit trails
- **Access Control**: Role-based permissions
- **Secure Storage**: Encrypted configuration storage

## 📈 Performance

- **Efficient Monitoring**: Low resource usage
- **Scalable Architecture**: Handle thousands of events
- **Memory Management**: Automatic memory cleanup
- **Performance Metrics**: Built-in performance monitoring

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/pandiyarajk/logwatchdog.git
cd logwatchdog
pip install -e .
pip install -r requirements-dev.txt
```

### Running Tests

```bash
pytest tests/
pytest tests/ --cov=logwatchdog
```

### Code Quality

```bash
flake8 logwatchdog/
black logwatchdog/
mypy logwatchdog/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Windows Event Log API** for native Windows integration
- **Python community** for excellent libraries and tools
- **Contributors** who help improve this project

## 📞 Support

- **Documentation**: [docs.logwatchdog.dev](https://docs.logwatchdog.dev)
- **Issues**: [GitHub Issues](https://github.com/pandiyarajk/logwatchdog/issues)
- **Discussions**: [GitHub Discussions](https://github.com/pandiyarajk/logwatchdog/discussions)
- **Email**: pandiyarajk@live.com

## 🔄 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a complete list of changes and version history.

---

**Made with ❤️ by [Pandiyaraj Karuppasamy](https://github.com/pandiyarajk)**

*LogWatchdog - Your Windows Log Monitoring Companion*
