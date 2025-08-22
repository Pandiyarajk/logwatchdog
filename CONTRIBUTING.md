# Contributing to LogWatchdog

Thank you for your interest in contributing to LogWatchdog! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

- Use the [GitHub Issues](https://github.com/pandiyarajk/logwatchdog/issues) page
- Include detailed information about your environment
- Provide steps to reproduce the issue
- Include relevant log files and error messages

### Suggesting Features

- Open a [GitHub Discussion](https://github.com/pandiyarajk/logwatchdog/discussions)
- Describe the feature and its benefits
- Provide use cases and examples
- Consider implementation complexity

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**: `git commit -m 'Add amazing feature'`
6. **Push to your fork**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

## 🛠️ Development Setup

### Prerequisites

- Python 3.7+
- Git
- Windows 10/11 (for testing)

### Local Development

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/logwatchdog.git
cd logwatchdog

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=logwatchdog

# Run specific test file
pytest tests/test_monitor.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
black logwatchdog/

# Lint code
flake8 logwatchdog/

# Type checking
mypy logwatchdog/

# Run all quality checks
pre-commit run --all-files
```

## 📋 Code Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and under 50 lines when possible

### Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions and classes
- Update CHANGELOG.md for significant changes
- Include examples in documentation

### Testing

- Write tests for new functionality
- Maintain test coverage above 80%
- Use descriptive test names
- Test both success and failure cases

## 🏗️ Project Structure

```
logwatchdog/
├── core/                 # Core monitoring engine
├── monitors/            # Log monitoring modules
├── notifiers/           # Notification systems
├── utils/               # Utility functions
├── config/              # Configuration management
├── cli/                 # Command line interface
├── gui/                 # Graphical user interface
└── tests/               # Test suite
```

## 🚀 Release Process

### Platform Focus
**LogWatchdog is a Windows-only solution.** All development, testing, and releases are focused on Windows 10/11 compatibility.

### Version Numbers

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

Current stable version: **v1.0.0** (Windows Production Ready)

### Release Checklist

- [ ] Update version in `setup.py`
- [ ] Update `CHANGELOG.md`
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create GitHub release
- [ ] Tag release in git
- [ ] Publish to PyPI

## 📝 Commit Messages

Use clear, descriptive commit messages:

```
feat: add Windows Event Viewer monitoring
fix: resolve email notification threading issue
docs: update installation instructions
test: add coverage for notification system
refactor: improve configuration management
```

## 🔒 Security

- Never commit sensitive information
- Report security issues privately to pandiyarajk@live.com
- Follow security best practices
- Validate all user inputs

## 📞 Getting Help

- **Documentation**: Check README.md and inline docs
- **Issues**: Search existing issues first
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact pandiyarajk@live.com

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to LogWatchdog!** 🎉
