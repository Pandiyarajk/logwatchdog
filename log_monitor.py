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
- Real-time log file monitoring
- Configurable exception keywords
- Automatic email alerts
- System tray notifications
- Environment-based configuration
"""

import os
import time
from dotenv import load_dotenv
from email_service import send_email
from notifier import show_popup

# Load environment variables from .env file
# This allows for easy configuration without code changes
load_dotenv()

# Configuration constants loaded from environment variables
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH")
EXCEPTION_KEYWORD = os.getenv("EXCEPTION_KEYWORD", "Exception")

# Comprehensive list of keywords that indicate exceptions, errors, or issues
# These keywords are case-insensitive and will trigger alerts when found in logs
EXCEPTION_KEYWORDS = [
    "Exception", "Error", "Failure", "Fail", "Fatal", "Issue",
    "Crash", "Close", "Cannot", "Wrong",
    "unsupported", "not found", "retry", "terminated", "disconnected"
]

def monitor_log():
    """
    Monitor a log file for exceptions and send alerts.
    
    This function continuously monitors the specified log file for new entries
    containing exception-related keywords. When detected, it triggers:
    1. Email alerts to configured recipients
    2. System tray popup notifications
    
    The function runs indefinitely until interrupted (Ctrl+C) and uses
    efficient file tailing to monitor only new log entries.
    
    Returns:
        None
        
    Raises:
        FileNotFoundError: If the specified log file doesn't exist
        PermissionError: If the log file cannot be read
        KeyboardInterrupt: When user stops the monitoring (Ctrl+C)
    """
    # Verify that the specified log file exists before starting monitoring
    if not os.path.exists(LOG_FILE_PATH):
        print(f"[ERROR] Log file not found: {LOG_FILE_PATH}")
        print("[ERROR] Please check your LOG_FILE_PATH environment variable")
        return

    print(f"[INFO] Monitoring log file: {LOG_FILE_PATH}")
    print(f"[INFO] Watching for keywords: {', '.join(EXCEPTION_KEYWORDS)}")

    # Open the log file for reading
    with open(LOG_FILE_PATH, "r") as f:
        # Move to the end of the file to start monitoring from current position
        # This prevents processing of old log entries
        f.seek(0, os.SEEK_END)

        # Continuous monitoring loop
        while True:
            try:
                # Read the next line from the log file
                line = f.readline()
                
                # If no new line is available, wait briefly and continue
                if not line:
                    time.sleep(1)  # Wait 1 second before checking again
                    continue

                # Check if the current line contains any exception keywords
                # Convert both the line and keywords to lowercase for case-insensitive matching
                if any(word.lower() in line.lower() for word in EXCEPTION_KEYWORDS):
                    # Exception detected - log the alert
                    print(f"[ALERT] Exception detected: {line.strip()}")

                    # Show system tray popup notification
                    # This provides immediate visual feedback on the desktop
                    show_popup("🚨 Exception Alert", line.strip())

                    # Send email alert to configured recipients
                    # This provides immediate notification to team members
                    send_email(
                        subject="🚨 Exception Alert",
                        body=f"An exception was detected in logs:\n\n{line}"
                    )

                    
            except KeyboardInterrupt:
                # Handle graceful shutdown when user presses Ctrl+C
                print("\n[INFO] Monitoring stopped by user")
                break
            except Exception as e:
                # Log any unexpected errors during monitoring
                print(f"[ERROR] Unexpected error during monitoring: {e}")
                time.sleep(5)  # Wait before retrying
