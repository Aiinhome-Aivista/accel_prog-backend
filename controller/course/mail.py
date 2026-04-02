from flask import Flask
from flask_mail import Mail, Message
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)

def send_email():
    with app.app_context():

        # 🔍 Debug (remove after working)
        print("SERVER:", app.config["SMTP_SERVER"])
        print("PORT:", app.config["SMTP_PORT"])

        msg = Message(
            subject="Test Email",
            sender=app.config["SMTP_USERNAME"],
            recipients=["2002anirbanpal@gmail.com"]
        )

        msg.body = "Hello! This email is sent using Flask-Mail."

        mail.send(msg)
        print("✅ Email sent successfully!")

if __name__ == "__main__":
    send_email()