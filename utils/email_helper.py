import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import Config

WELCOME_EMAIL_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #F8F4F0;
            margin: 0;
            padding: 0;
            color: #2D3E50;
        }
        .container {
            max-width: 600px;
            margin: 20px auto;
            background-color: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
        .header {
            background-color: #ffffff;
            padding: 30px;
            text-align: center;
            border-bottom: 1px solid #eee;
        }
        .logo-text {
            color: #E67E22; /* Orange from your logo */
            font-size: 24px;
            font-weight: bold;
            text-decoration: none;
        }
        .hero {
            padding: 40px 30px;
            text-align: center;
        }
        .hero h1 {
            color: #2D3E50; /* Dark blue/grey from text */
            font-size: 28px;
            margin-bottom: 10px;
        }
        .hero span {
            color: #E67E22;
        }
        .content {
            padding: 0 30px 30px;
            line-height: 1.6;
            color: #555;
            text-align: center;
        }
        .button {
            display: inline-block;
            padding: 14px 30px;
            background-color: #E67E22;
            color: #ffffff !important;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            margin-top: 20px;
        }
        .footer {
            background-color: #FDFBF9;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #999;
        }
        .accent-box {
            background-color: #FFF5EC;
            border-left: 4px solid #E67E22;
            padding: 15px;
            margin: 20px 0;
            text-align: left;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo-text">Moksh<span style="color: #2D3E50;">Path</span></div>
            <p style="font-size: 12px; margin: 5px 0 0; color: #888;">Guided Path to True Learning</p>
        </div>

        <div class="hero">
            <h1>Where Does Your <span>Journey</span> Begin?</h1>
            <p>Every learner's path is unique. We are here to guide yours.</p>
        </div>

        <div class="content">
            <p>Namaste! Thank you for showing interest in <strong>MokshPath</strong>. Whether you are looking for academic excellence or industry-ready AI skills, we have a curated path for you.</p>
            
            <div class="accent-box">
                <strong>Our Programs:</strong>
                <ul style="margin: 10px 0;">
                    <li>Academia (Semester-long courses)</li>
                    <li>Accelerated Program (AI & Prompt Engineering)</li>
                    <li>School Olympiad</li>
                </ul>
            </div>

            <a href="#" class="button">Explore Your Path</a>
        </div>

        <div class="footer">
            <p>&copy; 2026 MokshPath. All rights reserved.</p>
            <p>You received this email because you signed up on our website.</p>
        </div>
    </div>
</body>
</html>"""


def build_otp_email_html(otp):
    return f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #F8F4F0;
            margin: 0;
            padding: 0;
            color: #2D3E50;
        }}
        .container {{
            max-width: 600px;
            margin: 20px auto;
            background-color: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }}
        .header {{
            background-color: #ffffff;
            padding: 30px;
            text-align: center;
            border-bottom: 1px solid #eee;
        }}
        .logo-text {{
            color: #E67E22;
            font-size: 24px;
            font-weight: bold;
            text-decoration: none;
        }}
        .hero {{
            padding: 40px 30px;
            text-align: center;
        }}
        .hero h1 {{
            color: #2D3E50;
            font-size: 28px;
            margin-bottom: 10px;
        }}
        .hero span {{
            color: #E67E22;
        }}
        .content {{
            padding: 0 30px 30px;
            line-height: 1.6;
            color: #555;
            text-align: center;
        }}
        .button {{
            display: inline-block;
            padding: 14px 30px;
            background-color: #E67E22;
            color: #ffffff !important;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            margin-top: 20px;
        }}
        .footer {{
            background-color: #FDFBF9;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #999;
        }}
        .accent-box {{
            background-color: #FFF5EC;
            border-left: 4px solid #E67E22;
            padding: 15px;
            margin: 20px 0;
            text-align: left;
        }}
        .otp-code {{
            display: inline-block;
            margin-top: 12px;
            font-size: 24px;
            letter-spacing: 4px;
            font-weight: bold;
            color: #2D3E50;
            background-color: #ffffff;
            padding: 10px 18px;
            border-radius: 8px;
            border: 1px dashed #E67E22;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo-text">Moksh<span style="color: #2D3E50;">Path</span></div>
            <p style="font-size: 12px; margin: 5px 0 0; color: #888;">Guided Path to True Learning</p>
        </div>

        <div class="hero">
            <h1>Where Does Your <span>Journey</span> Begin?</h1>
            <p>Every learner's path is unique. We are here to guide yours.</p>
        </div>

        <div class="content">

            <div class="accent-box" style="border-left: none;">
                <strong>Your OTP for verification:</strong><br />
                <div style="text-align: center;">
                    <span class="otp-code">{otp}</span>
                </div>
                <p style="margin: 10px 0 0;">This OTP is valid for 10 minutes. Do not share it with anyone.</p>
            </div>

           
        </div>

        <div class="footer">
            <p>&copy; 2026 MokshPath. All rights reserved.</p>
            <p>You received this email because you signed up on our website.</p>
        </div>
    </div>
</body>
</html>
"""


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

    plain_text = (
        f"Your OTP is {otp}. Valid for 10 minutes. Do not share it with anyone."
    )
    html_content = build_otp_email_html(otp)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "OTP Verification"
    msg["From"] = smtp_username
    msg["To"] = to_email

    msg.attach(MIMEText(plain_text, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    smtp_client = smtplib.SMTP_SSL if use_ssl else smtplib.SMTP
    with smtp_client(smtp_server, smtp_port) as server:
        if use_tls and not use_ssl:
            server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
 