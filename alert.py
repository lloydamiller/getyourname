import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from creds import email_login


def send_alert_by_email(recipient, subject, message):
    sender = email_login["USER"]
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
        server.login(email_login["USER"], email_login["PASS"])
        server.sendmail(sender, recipient, text)
        server.close()
        print(f"[*] Sent alert to {recipient}")
    except:
        print(f"[!] Error sending alert to {recipient}")
