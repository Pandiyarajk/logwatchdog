"""
LogWatchdog - Main Entry Point
==============================

This module serves as the main entry point for the LogWatchdog application.
It initializes the log monitoring system and starts monitoring for exceptions
in specified log files.

The application provides real-time monitoring of log files with automatic
alerting via email and system tray notifications when exceptions are detected.
"""

if __name__ == "__main__":
    # Display startup message to indicate monitoring has begun
    print("[START] Monitoring logs for exceptions...")
    print("[INFO] Press Ctrl+C to stop monitoring")
    try:
        from log_monitor import monitor_log    
        # Start the continuous log monitoring process
        # This function runs indefinitely until interrupted
        print("[INFO] Starting log monitoring...")
        monitor_log()
    except Exception as e:
        print(f"[ERROR] LogWatchdog failed to start: {e}")
    print("[INFO] LogWatchdog stopped")
        