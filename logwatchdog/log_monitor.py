"""
Log Monitor Module
==================

This module provides continuous monitoring of log files for exception detection.
It watches for specific keywords that indicate errors, exceptions, or issues
and triggers alerts via email and system tray notifications.

The monitor runs continuously, checking for new log entries and analyzing
them for exception-related keywords. When detected, it immediately sends
alerts to configured recipients.

Features:
- Real-time log file monitoring (single file, multiple files, or folder)
- Configurable exception keywords
- Automatic email alerts
- System tray notifications
- INI file-based configuration
- Support for multiple log file extensions
- Folder monitoring with file filtering
"""

import os
import sys
import time
import glob
import configparser
from pathlib import Path
from typing import List, Dict, Set
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv
from logwatchdog.email_service import send_email
from logwatchdog.notifier import show_popup

def load_config():
    """Load configuration from log_config.ini file and environment variables for sensitive data."""
    config = configparser.ConfigParser()
    
    # Handle both development and PyInstaller executable environments
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable - prioritize execution directory
        possible_paths = [
            Path.cwd() / "log_config.ini",  # Current working directory (execution directory)
            Path(sys.executable).parent / "log_config.ini",  # Same directory as executable
            Path(sys._MEIPASS) / "log_config.ini",  # PyInstaller temp directory (fallback)
        ]
        
        config_path = None
        for path in possible_paths:
            if path.exists():
                config_path = path
                print(f"[INFO] Config file found at: {path}")
                break
        
        if config_path is None:
            # If no config file found, use the execution directory for creation
            config_path = possible_paths[0]
            print(f"[INFO] Will create config file at: {config_path}")
    else:
        print(f"[INFO] Running as script")
        # Running as script - try multiple possible locations
        possible_paths = [
            Path.cwd() / "log_config.ini",  # Current working directory
            Path(__file__).parent.parent / "log_config.ini",  # Project root            
            Path(__file__).parent / "log_config.ini",  # Same directory as this module
        ]
        
        config_path = None
        for path in possible_paths:
            if path.exists():
                config_path = path
                print(f"[INFO] Config file found at: {path}")
                break
        
        if config_path is None:
            # If no config file found, use the first possible path for error message
            config_path = possible_paths[0]
    
    if not config_path.exists():
        print(f"[WARNING] Configuration file not found: {config_path}")
        print("[INFO] Creating default configuration file...")
        default_config = get_default_config()
        try:
            # Create the directory if it doesn't exist
            config_path.parent.mkdir(parents=True, exist_ok=True)
            # Write the default configuration to file
            with open(config_path, 'w') as configfile:
                # Add header comment
                configfile.write("# LogWatchdog Configuration File\n")
                configfile.write("# =============================\n")
                configfile.write("# This file was automatically created by LogWatchdog.\n")
                configfile.write("# Modify the values below to customize your monitoring setup.\n\n")
                default_config.write(configfile)
            print(f"[INFO] Default configuration created at: {config_path}")
        except Exception as e:
            print(f"[ERROR] Failed to create configuration file: {e}")
            print("[INFO] Using default configuration values")
        return default_config
    
    try:
        config.read(config_path)
        print(f"[INFO] Loaded configuration from: {config_path}")
        return config
    except Exception as e:
        print(f"[ERROR] Failed to read configuration file: {e}")
        print("[INFO] Using default configuration values")
        return get_default_config()

def load_env_credentials():
    """Load sensitive email credentials from environment file."""
    # Try to load .env file from multiple possible locations
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable - look for .env in the same directory as the executable
        base_path = Path(sys.executable).parent
        env_path = base_path / ".env"
        print(f"[INFO] Looking for .env file at: {env_path}")
    else:
        # Running as script - try multiple possible locations
        possible_env_paths = [
            Path(__file__).parent.parent / ".env",  # Project root
            Path.cwd() / ".env",  # Current working directory
            Path(__file__).parent / ".env",  # Same directory as this module
        ]
        
        print(f"[INFO] Looking for .env file in possible locations:")
        for path in possible_env_paths:
            print(f"  - {path}")
        
        env_path = None
        for path in possible_env_paths:
            if path.exists():
                env_path = path
                break
    
    # Load environment variables from .env file if found
    if env_path and env_path.exists():
        print(f"[INFO] Found .env file at: {env_path}")
        load_dotenv(env_path)
    else:
        print(f"[WARNING] .env file not found in any of the expected locations")
        print(f"[INFO] Searched locations:")
        if getattr(sys, 'frozen', False):
            print(f"  - {env_path}")
        else:
            for path in possible_env_paths:
                print(f"  - {path}")
        print(f"[INFO] Trying default .env locations...")
        load_dotenv()  # Try default locations
    
    # Read sensitive email credentials from environment
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")
    
    if not email_user or not email_password:
        print("[WARNING] Email credentials not found in environment file")
        print("[INFO] Please create a .env file with EMAIL_USER and EMAIL_PASSWORD")
        if getattr(sys, 'frozen', False):
            print(f"[INFO] Create .env file at: {Path(sys.executable).parent / '.env'}")
        else:
            print(f"[INFO] Create .env file at: {Path.cwd() / '.env'}")
        return "", ""
    
    print(f"[INFO] Email credentials loaded successfully")
    return email_user, email_password

def get_default_config():
    """Return default configuration values."""
    config = configparser.ConfigParser()
    
    # Get current working directory for relative paths
    current_dir = Path.cwd()
    logs_dir = current_dir / "logs"
    
    # Set default values
    config['monitoring'] = {
        'monitor_mode': 'folder',
        'log_file_path': str(logs_dir / 'application.log'),
        'log_files': str(logs_dir / 'app.log') + ',' + str(logs_dir / 'application.log'),
        'log_folder_path': str(logs_dir),
        'log_file_extensions': '*.log,*.txt,*.evtx',
        'file_discovery_interval': '30',
        'empty_monitor_delay': '10'
    }
    
    config['notifications'] = {
        'email_enabled': 'false',
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': '587',
        'receiver_group': 'admin@company.com,ops@company.com',
        'system_tray_notifications': 'true',
        'batch_email_enabled': 'true'
    }
    
    config['alerts'] = {
        'exception_keywords': 'Exception,Error,Failure,Fail,Fatal,Issue,Crash,Close,Cannot,Wrong,unsupported,not found,retry,terminated,disconnected'
    }
    
    return config

# Load configuration
config = load_config()

# Load sensitive email credentials from environment
EMAIL_USER, EMAIL_PASSWORD = load_env_credentials()

# Configuration constants loaded from INI file
MONITOR_MODE = config.get('monitoring', 'monitor_mode', fallback='single')
LOG_FILE_PATH = config.get('monitoring', 'log_file_path', fallback='')
LOG_FOLDER_PATH = config.get('monitoring', 'log_folder_path', fallback='')
LOG_FILE_EXTENSIONS = config.get('monitoring', 'log_file_extensions', fallback='*.log,*.txt,*.evtx').split(',')

# File discovery settings
FILE_DISCOVERY_INTERVAL = int(config.get('monitoring', 'file_discovery_interval', fallback='30'))
EMPTY_MONITOR_DELAY = int(config.get('monitoring', 'empty_monitor_delay', fallback='10'))

# Notification settings
EMAIL_ENABLED = config.get('notifications', 'email_enabled', fallback='true').lower() == 'true'
SMTP_SERVER = config.get('notifications', 'smtp_server', fallback='smtp.gmail.com')
SMTP_PORT = int(config.get('notifications', 'smtp_port', fallback='587'))
RECEIVER_GROUP = config.get('notifications', 'receiver_group', fallback='')
SYSTEM_TRAY_NOTIFICATIONS = config.get('notifications', 'system_tray_notifications', fallback='true').lower() == 'true'
BATCH_EMAIL_ENABLED = config.get('notifications', 'batch_email_enabled', fallback='true').lower() == 'true'

# Comprehensive list of keywords that indicate exceptions, errors, or issues
# These keywords are case-insensitive and will trigger alerts when found in logs
EXCEPTION_KEYWORDS = config.get('alerts', 'exception_keywords', fallback='Exception,Error,Failure,Fail,Fatal,Issue,Crash,Close,Cannot,Wrong,unsupported,not found,retry,terminated,disconnected').split(',')

class LogFileHandler(FileSystemEventHandler):
    """
    File system event handler for monitoring log files in a folder.
    
    This class handles file creation, modification, and deletion events
    to automatically start/stop monitoring new log files.
    """
    
    def __init__(self, monitor_files: Dict[str, dict]):
        self.monitor_files = monitor_files
        self.observer = Observer()
        
    def on_created(self, event):
        """Handle new file creation events."""
        if not event.is_directory and self._is_log_file(event.src_path):
            self._add_file_to_monitoring(event.src_path)
            
    def on_modified(self, event):
        """Handle file modification events."""
        if not event.is_directory and event.src_path in self.monitor_files:
            # File was modified, this is handled by the file reader
            pass
            
    def on_deleted(self, event):
        """Handle file deletion events."""
        if event.src_path in self.monitor_files:
            self._remove_file_from_monitoring(event.src_path)
            
    def _is_log_file(self, file_path: str) -> bool:
        """Check if a file has a supported log extension."""
        return any(file_path.lower().endswith(ext.strip().lower()) for ext in LOG_FILE_EXTENSIONS)
        
    def _add_file_to_monitoring(self, file_path: str):
        """Add a new file to the monitoring list."""
        if file_path not in self.monitor_files:
            self.monitor_files[file_path] = {
                'position': 0,
                'last_modified': os.path.getmtime(file_path),
                'size': os.path.getsize(file_path)
            }
            print(f"[INFO] Added new log file to monitoring: {file_path}")
            
    def _remove_file_from_monitoring(self, file_path: str):
        """Remove a file from the monitoring list."""
        if file_path in self.monitor_files:
            del self.monitor_files[file_path]
            print(f"[INFO] Removed log file from monitoring: {file_path}")

def get_log_files() -> List[str]:
    """
    Get list of log files to monitor based on configuration.
    
    Returns:
        List of file paths to monitor
    """
    files = []
    
    if MONITOR_MODE == "single" and LOG_FILE_PATH:
        if os.path.exists(LOG_FILE_PATH):
            files.append(LOG_FILE_PATH)
        else:
            print(f"[WARNING] Single log file not found: {LOG_FILE_PATH}")
            
    elif MONITOR_MODE == "multiple" and LOG_FILE_PATH:
        # Support comma-separated list of files
        file_list = [f.strip() for f in LOG_FILE_PATH.split(",")]
        for file_path in file_list:
            if os.path.exists(file_path):
                files.append(file_path)
            else:
                print(f"[WARNING] Log file not found: {file_path}")
                
    elif MONITOR_MODE == "folder" and LOG_FOLDER_PATH:
        if os.path.exists(LOG_FOLDER_PATH) and os.path.isdir(LOG_FOLDER_PATH):
            # Find all files with supported extensions in the folder
            for extension in LOG_FILE_EXTENSIONS:
                pattern = os.path.join(LOG_FOLDER_PATH, extension.strip())
                files.extend(glob.glob(pattern))
            # Remove duplicates and sort
            files = sorted(list(set(files)))
        elif LOG_FILE_PATH == "":
            print("[WARNING] Log file not specified")
        elif LOG_FOLDER_PATH == "":
            print("[WARNING] Log folder not specified")
        else:
            print(f"[WARNING] Log folder not found: {LOG_FOLDER_PATH}")
            
    return files

def monitor_log():
    """
    Monitor log files for exceptions and send alerts.
    
    This function supports three monitoring modes:
    1. Single file monitoring (MONITOR_MODE=single)
    2. Multiple file monitoring (MONITOR_MODE=multiple)
    3. Folder monitoring (MONITOR_MODE=folder)
    
    When exceptions are detected, it triggers:
    1. Email alerts to configured recipients
    2. System tray popup notifications
    
    The function runs indefinitely until interrupted (Ctrl+C) and uses
    efficient file tailing to monitor only new log entries.
    
    Returns:
        None
        
    Raises:
        FileNotFoundError: If specified log files don't exist
        PermissionError: If log files cannot be read
        KeyboardInterrupt: When user stops the monitoring (Ctrl+C)
    """
    # Get list of files to monitor
    log_files = get_log_files()
    
    if not log_files:
        print("[ERROR] No log files found to monitor")
        print("[ERROR] Please check your configuration:")
        print(f"  - MONITOR_MODE: {MONITOR_MODE}")
        print(f"  - LOG_FILE_PATH: {LOG_FILE_PATH}")
        print(f"  - LOG_FOLDER_PATH: {LOG_FOLDER_PATH}")
        print(f"  - LOG_FILE_EXTENSIONS: {LOG_FILE_EXTENSIONS}")
        return

    print(f"[INFO] Monitoring mode: {MONITOR_MODE}")
    print(f"[INFO] Found {len(log_files)} log file(s) to monitor:")
    for file_path in log_files:
        print(f"  - {file_path}")
    print(f"[INFO] Watching for keywords: {', '.join(EXCEPTION_KEYWORDS)}")
    print(f"[DEBUG] Exception keywords (lowercase): {[kw.lower() for kw in EXCEPTION_KEYWORDS]}")

    # Initialize file monitoring state
    monitor_files = {}
    for file_path in log_files:
        try:
            monitor_files[file_path] = {
                'position': os.path.getsize(file_path),
                'last_modified': os.path.getmtime(file_path),
                'size': os.path.getsize(file_path)
            }
        except (OSError, PermissionError) as e:
            print(f"[WARNING] Cannot access file {file_path}: {e}")
            continue
    
    # Dictionary to collect errors per file for batch email sending
    file_errors = {}

    # Set up folder monitoring if in folder mode
    observer = None
    if MONITOR_MODE == "folder" and LOG_FOLDER_PATH:
        try:
            event_handler = LogFileHandler(monitor_files)
            observer = Observer()
            observer.schedule(event_handler, LOG_FOLDER_PATH, recursive=False)
            observer.start()
            print(f"[INFO] Started folder monitoring: {LOG_FOLDER_PATH}")
            print(f"[INFO] Watching for files with extensions: {', '.join(LOG_FILE_EXTENSIONS)}")
        except Exception as e:
            print(f"[WARNING] Could not start folder monitoring: {e}")
            print(f"[INFO] Will use periodic file discovery instead")

    try:
        # Continuous monitoring loop
        while True:
            if len(monitor_files) == 0:
                print("[INFO] No log files found to monitor")
                print(f"[INFO] Waiting {EMPTY_MONITOR_DELAY} seconds before checking for new files...")
                
                # Wait longer when no files are found, then check for new files
                time.sleep(EMPTY_MONITOR_DELAY)
                
                # Try to find new log files
                new_log_files = get_log_files()
                if new_log_files:
                    print(f"[INFO] Found {len(new_log_files)} new log file(s) to monitor")
                    # Initialize monitoring for new files
                    for file_path in new_log_files:
                        if file_path not in monitor_files:
                            try:
                                monitor_files[file_path] = {
                                    'position': os.path.getsize(file_path),
                                    'last_modified': os.path.getmtime(file_path),
                                    'size': os.path.getsize(file_path)
                                }
                                print(f"[INFO] Started monitoring new file: {file_path}")
                            except (OSError, PermissionError) as e:
                                print(f"[WARNING] Cannot access new file {file_path}: {e}")
                                continue
                else:
                    print("[INFO] Still no log files found, continuing to wait...")
                    continue
            
            # Check each monitored file for new content
            for file_path in list(monitor_files.keys()):
                try:
                    if not os.path.exists(file_path):
                        print(f"[WARNING] Log file no longer exists: {file_path}")
                        del monitor_files[file_path]
                        continue
                        
                    current_size = os.path.getsize(file_path)
                    current_modified = os.path.getmtime(file_path)
                    
                    # Debug: Log file size changes
                    if current_size != monitor_files[file_path]['size']:
                        print(f"[DEBUG] File {os.path.basename(file_path)} size changed: {monitor_files[file_path]['size']} -> {current_size}")
                    
                    # Check if file has new content
                    if current_size > monitor_files[file_path]['size']:
                        try:
                            # Read new content from the file
                            with open(file_path, "r", encoding='utf-8', errors='ignore') as f:
                                f.seek(monitor_files[file_path]['size'])
                                new_content = f.read()
                                
                            print(f"[DEBUG] Read {len(new_content)} bytes of new content from {os.path.basename(file_path)}")
                            
                            # Process new lines
                            new_lines = new_content.splitlines()
                            for line in new_lines:
                                if line.strip():  # Skip empty lines
                                    # Check for exception keywords (case-insensitive)
                                    line_lower = line.lower()
                                    for keyword in EXCEPTION_KEYWORDS:
                                        if keyword.lower() in line_lower:
                                            # Exception detected - collect for batch processing
                                            print(f"[ALERT] Exception detected in {os.path.basename(file_path)}: {line.strip()}")
                                            print(f"[ALERT] Line content: {line.strip()}")

                                            # Show system tray popup notification
                                            show_popup(
                                                f"Exception Alert - {os.path.basename(file_path)}", 
                                                line.strip()
                                            )

                                            # Collect error for batch email sending
                                            if file_path not in file_errors:
                                                file_errors[file_path] = []
                                            file_errors[file_path].append({
                                                'line': line.strip(),
                                                'keyword': keyword,
                                                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                                            })
                                            break  # Only alert once per line
                            
                            # Update file monitoring state
                            monitor_files[file_path]['size'] = current_size
                            monitor_files[file_path]['last_modified'] = current_modified
                            
                        except Exception as e:
                            print(f"[ERROR] Error reading file {file_path}: {e}")
                            continue
                        
                except (OSError, PermissionError) as e:
                    print(f"[WARNING] Error accessing file {file_path}: {e}")
                    continue
                except Exception as e:
                    print(f"[ERROR] Unexpected error monitoring {file_path}: {e}")
                    continue
            
            # Send batch emails for collected errors
            if file_errors and EMAIL_ENABLED and BATCH_EMAIL_ENABLED:
                for file_path, errors in file_errors.items():
                    if errors:  # Only send if there are errors
                        # Create batch email content
                        error_count = len(errors)
                        subject = f"Exception Alert - {os.path.basename(file_path)} ({error_count} error{'s' if error_count > 1 else ''})"
                        
                        body_lines = [
                            f"Multiple exceptions detected in log file: {file_path}",
                            f"Total errors found: {error_count}",
                            f"Detection time: {time.strftime('%Y-%m-%d %H:%M:%S')}",
                            "",
                            "Error Details:",
                            "=" * 50
                        ]
                        
                        for i, error in enumerate(errors, 1):
                            body_lines.extend([
                                f"{i}. [{error['timestamp']}] {error['keyword']}",
                                f"   {error['line']}",
                                ""
                            ])
                        
                        body = "\n".join(body_lines)
                        
                        try:
                            send_email(
                                subject=subject,
                                body=body,
                                smtp_server=SMTP_SERVER,
                                smtp_port=SMTP_PORT,
                                email_user=EMAIL_USER,
                                email_password=EMAIL_PASSWORD,
                                receiver_group=RECEIVER_GROUP
                            )
                            # print(f"[INFO] Batch email sent for {file_path} with {error_count} error(s)")
                        except Exception as e:
                            print(f"[ERROR] Failed to send batch email for {file_path}: {e}")
                
                # Clear the collected errors after sending
                file_errors.clear()
            
            # Brief pause between monitoring cycles
            time.sleep(1)
            
            # Periodically check for new files
            # This is especially useful for folder monitoring
            if time.time() % FILE_DISCOVERY_INTERVAL < 1:  # Check every FILE_DISCOVERY_INTERVAL seconds
                try:
                    new_log_files = get_log_files()
                    for file_path in new_log_files:
                        if file_path not in monitor_files:
                            try:
                                monitor_files[file_path] = {
                                    'position': os.path.getsize(file_path),
                                    'last_modified': os.path.getmtime(file_path),
                                    'size': os.path.getsize(file_path)
                                }
                                print(f"[INFO] Started monitoring new file: {file_path}")
                            except (OSError, PermissionError) as e:
                                print(f"[WARNING] Cannot access new file {file_path}: {e}")
                                continue
                except Exception as e:
                    print(f"[WARNING] Error checking for new files: {e}")
            
    except KeyboardInterrupt:
        # Handle graceful shutdown when user presses Ctrl+C
        print("\n[INFO] Monitoring stopped by user")
    except Exception as e:
        # Log any unexpected errors during monitoring
        print(f"[ERROR] Unexpected error during monitoring: {e}")
    finally:
        # Clean up folder monitoring
        if observer:
            observer.stop()
            observer.join()
            print("[INFO] Folder monitoring stopped")

def monitor_single_file(file_path: str):
    """
    Monitor a single log file (legacy function for backward compatibility).
    
    Args:
        file_path: Path to the log file to monitor
        
    Returns:
        None
    """
    global LOG_FILE_PATH
    original_path = LOG_FILE_PATH
    LOG_FILE_PATH = file_path
    monitor_log()
    LOG_FILE_PATH = original_path

if __name__ == "__main__":
    # Run the monitor when script is executed directly
    monitor_log()
