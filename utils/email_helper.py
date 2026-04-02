import smtplib
from email.mime.text import MIMEText
from config import Config


def send_otp_email(to_email, otp):
    smtp_server = Config.MAIL_SERVER
    smtp_port = Config.MAIL_PORT
    smtp_username = Config.MAIL_USERNAME
    smtp_password = Config.MAIL_PASSWORD
    use_ssl = getattr(Config, "MAIL_USE_SSL", False)
    use_tls = getattr(Config, "MAIL_USE_TLS", True)

    if not smtp_username or not smtp_password:
        raise ValueError(
            "SMTP credentials are missing. Set MAIL_USERNAME/MAIL_PASSWORD or SMTP_EMAIL/SMTP_PASS"
        )

    msg = MIMEText(f"Your OTP is {otp}. Valid for 10 minutes.")
    msg["Subject"] = "OTP Verification"
    msg["From"] = smtp_username
    msg["To"] = to_email

    smtp_client = smtplib.SMTP_SSL if use_ssl else smtplib.SMTP
    with smtp_client(smtp_server, smtp_port) as server:
        if use_tls and not use_ssl:
            server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
