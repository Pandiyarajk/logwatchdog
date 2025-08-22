"""
Email Service Module
====================

This module provides email notification functionality for the Rich Logger system.
It handles sending alert emails when exceptions are detected in monitored log files.

The service uses SMTP to send emails and supports:
- TLS encryption for secure email transmission
- Configurable SMTP server settings
- Multiple recipient support
- Environment-based configuration
- Error handling and logging

Configuration is loaded from environment variables for security and flexibility.
"""

import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env file
# This keeps sensitive information like passwords out of the code
load_dotenv()

# SMTP server configuration loaded from environment variables
# These settings determine how emails are sent
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))  # Default to port 587 (TLS)
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Recipient list - multiple email addresses can be specified
# Comma-separated values are split into a list
RECEIVER_GROUP = os.getenv("RECEIVER_GROUP").split(",")

def send_email(subject: str, body: str):
    """
    Send email to all recipients in the configured receiver group.
    
    This function creates and sends an email alert using the configured SMTP
    server. It supports TLS encryption and handles authentication automatically.
    
    Args:
        subject (str): The email subject line
        body (str): The email body content
        
    Returns:
        None
        
    Raises:
        smtplib.SMTPException: If there's an SMTP-related error
        Exception: For any other unexpected errors during email sending
        
    Note:
        - Uses TLS encryption for security
        - Sends to all recipients in RECEIVER_GROUP
        - Logs success/failure messages to console
    """
    # Create the email message using MIMEText
    # This provides proper email formatting and headers
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = ", ".join(RECEIVER_GROUP)

    try:
        # Establish connection to SMTP server
        # Using 'with' statement ensures proper connection cleanup
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            # Start TLS encryption for secure communication
            # This encrypts the connection between client and server
            server.starttls()
            
            # Authenticate with the SMTP server using provided credentials
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            
            # Send the email to all recipients
            # The email is sent from EMAIL_USER to all addresses in RECEIVER_GROUP
            server.sendmail(EMAIL_USER, RECEIVER_GROUP, msg.as_string())
            
        # Log successful email transmission
        print("[EMAIL] Alert sent successfully.")
        print(f"[EMAIL] Recipients: {', '.join(RECEIVER_GROUP)}")
        
    except smtplib.SMTPAuthenticationError as e:
        # Handle authentication failures (wrong username/password)
        print(f"[EMAIL ERROR] Authentication failed: {e}")
        print("[EMAIL ERROR] Please check your EMAIL_USER and EMAIL_PASSWORD")
        
    except smtplib.SMTPConnectError as e:
        # Handle connection failures (server unreachable, wrong port)
        print(f"[EMAIL ERROR] Connection failed: {e}")
        print(f"[EMAIL ERROR] Please check SMTP_SERVER ({SMTP_SERVER}) and SMTP_PORT ({SMTP_PORT})")
        
    except smtplib.SMTPException as e:
        # Handle other SMTP-related errors
        print(f"[EMAIL ERROR] SMTP error: {e}")
        
    except Exception as e:
        # Handle any other unexpected errors
        print(f"[EMAIL ERROR] Unexpected error: {e}")
        print(f"[EMAIL ERROR] Error type: {type(e).__name__}")
