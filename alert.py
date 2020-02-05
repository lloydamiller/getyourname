import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

with open("credentials.json", 'r') as f:
    email_login = json.load(f)["email_login"]


def send_alert_by_email(recipient, subject, message):
    sender = email_login["user"]
    msg = MIMEMultipart()
    msg["From"] = "Twitter Alert"
    msg["To"] = recipient
    msg["Subject"] = subject

    msg.attach(MIMEText(message, 'plain'))
    text = msg.as_string()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(email_login["user"], email_login["pass"])
        server.sendmail(sender, recipient, text)
        server.close()
        print(f"[*] Sent alert to {recipient}")
    except:
        print(f"[!] Error sending alert to {recipient}")
