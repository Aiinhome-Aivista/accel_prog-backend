import smtplib
from email.mime.text import MIMEText
import os


def send_otp_email(to_email, otp):
    msg = MIMEText(f"Your OTP is {otp}. Valid for 10 minutes.")
    msg["Subject"] = "OTP Verification"
    msg["From"] = os.getenv("SMTP_EMAIL")
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(os.getenv("SMTP_EMAIL"), os.getenv("SMTP_PASS"))
        server.send_message(msg)
