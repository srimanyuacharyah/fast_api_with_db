import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()
app_password = os.getenv("APP_PASSWORD")
sender_email = os.getenv("SENDER_EMAIL")

# Clean APP_PASSWORD (remove spaces often found in Google App Passwords)
if app_password:
    app_password = app_password.replace(" ", "")

def send_email(receiver_email: str, subject: str, content: str):
    """Send an email to the specified receiver with the given subject and content."""
    
    if not sender_email or not app_password:
        print("Error: SENDER_EMAIL or APP_PASSWORD not set in environment")
        raise ValueError("Email configuration missing. Please check your .env file.")

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.set_content(content)

    try:
        # Send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")
        raise

