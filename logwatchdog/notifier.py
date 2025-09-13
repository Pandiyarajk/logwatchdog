"""
System Notification Module
=========================

This module provides desktop notification functionality for the LogWatchdog system.
It displays popup notifications when exceptions are detected in monitored logs.

The module uses the 'plyer' library which provides cross-platform notification
support for Windows. Notifications appear as system
tray popups or desktop alerts.

Features:
- Windows compatibility
- Configurable notification duration (5 seconds)
- Clean, simple API
- Automatic fallback handling
"""

import sys
import os
import time

def show_popup(title: str, message: str):
    """
    Display a system tray popup notification.
    
    This function creates a desktop notification that appears as a popup
    in the system tray area. The notification is automatically dismissed
    after the specified timeout period.
    
    Args:
        title (str): The notification title/heading
        message (str): The notification message content
        
    Returns:
        None
        
    Note:
        - Uses plyer library for cross-platform compatibility
        - Notifications automatically disappear after 5 seconds
        - Works on Windows
        - Falls back gracefully if system notifications are unavailable
        
    Example:
        show_popup("Exception Alert", "Database connection failed")
    """
    # Check if we're running as PyInstaller executable and plyer might have issues
    if getattr(sys, 'frozen', False):
        print(f"[INFO] Running as executable, using flash notification")
        # Skip plyer entirely for PyInstaller builds and go straight to flash
        try:
            if sys.platform == "win32":
                import ctypes
                # Flash the taskbar button to get attention
                hwnd = ctypes.windll.kernel32.GetConsoleWindow()
                if hwnd:
                    # Flash the window to get attention (flash 3 times)
                    for _ in range(3):
                        ctypes.windll.user32.FlashWindow(hwnd, True)
                        time.sleep(0.2)
                    
                    # Also play a system sound
                    try:
                        ctypes.windll.user32.MessageBeep(0xFFFFFFFF)  # System default sound
                    except:
                        pass
                    
                    # Show a custom flash popup that auto-closes
                    try:
                        import threading
                        import tkinter as tk
                        from tkinter import ttk
                        
                        def show_flash_popup():
                            # Create a simple popup window
                            popup = tk.Tk()
                            popup.title(title)
                            popup.geometry("400x150")
                            popup.configure(bg='#ff4444')  # Red background for alert
                            
                            # Center the window
                            popup.update_idletasks()
                            x = (popup.winfo_screenwidth() // 2) - (400 // 2)
                            y = (popup.winfo_screenheight() // 2) - (150 // 2)
                            popup.geometry(f"400x150+{x}+{y}")
                            
                            # Make it stay on top
                            popup.attributes('-topmost', True)
                            popup.attributes('-toolwindow', True)  # Remove from taskbar
                            
                            # Add content
                            title_label = tk.Label(popup, text=title, font=('Arial', 14, 'bold'), 
                                                fg='white', bg='#ff4444')
                            title_label.pack(pady=10)
                            
                            message_label = tk.Label(popup, text=message, font=('Arial', 10), 
                                                   fg='white', bg='#ff4444', wraplength=350)
                            message_label.pack(pady=5)
                            
                            # Auto-close after 3 seconds
                            popup.after(3000, popup.destroy)
                            
                            # Start the popup
                            popup.mainloop()
                        
                        # Show popup in a separate thread so it doesn't block
                        thread = threading.Thread(target=show_flash_popup)
                        thread.daemon = True
                        thread.start()
                    except Exception as e:
                        print(f"[DEBUG] Flash popup failed: {e}")
                        # Fallback to simple message box
                        try:
                            ctypes.windll.user32.MessageBoxW(0, message, title, 0x40)
                        except:
                            pass
                    
                    print(f"[INFO] Flash notification sent: {title}")
                    print(f"[NOTIFICATION] {title}: {message}")
                    return
        except Exception as flash_error:
            print(f"[WARNING] Flash notification failed: {flash_error}")
        
        # Final fallback for executable
        print(f"[NOTIFICATION] {title}: {message}")
        return
    
    # For script mode, try plyer first
    try:
        from plyer import notification
        print(f"[DEBUG] Attempting plyer notification...")
        # Display the system notification using plyer
        # This creates a popup that appears in the system tray area
        notification.notify(
            title=title,      # The notification heading
            message=message,  # The notification content
            timeout=5         # Duration in seconds before auto-dismissal
        )
        print(f"[INFO] System notification sent: {title}")
        return
    except ImportError as e:
        print(f"[WARNING] Plyer notification module not available: {e}")
    except Exception as e:
        print(f"[WARNING] Plyer notification failed: {e}")
        print(f"[DEBUG] Error details: {type(e).__name__}: {e}")
    
    # Fallback: Try flash popup notification on Windows
    try:
        if sys.platform == "win32":
            import ctypes
            # Flash the taskbar button to get attention
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                # Flash the window to get attention
                ctypes.windll.user32.FlashWindow(hwnd, True)
                print(f"[INFO] Flash notification sent: {title}")
                return
    except Exception as fallback_error:
        print(f"[WARNING] Flash notification failed: {fallback_error}")
    
    # Final fallback: Print to console
    print(f"[NOTIFICATION] {title}: {message}")
    print(f"[INFO] Using console notification as fallback")