import smtplib
import json
from email.message import EmailMessage

class Alerts:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            cfg = json.load(f)
        self.to = cfg["alert_email"]
        self.server = cfg["smtp_server"]
        self.port = cfg["smtp_port"]
        self.user = cfg["smtp_user"]
        self.password = cfg["smtp_password"]

    def send_email(self, subject: str, body: str):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.user
        msg['To'] = self.to
        msg.set_content(body)
        with smtplib.SMTP_SSL(self.server, self.port) as smtp:
            smtp.login(self.user, self.password)
            smtp.send_message(msg)
