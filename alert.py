#alert.pu
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import config
def send_alert(subject,body):
    try:
        #build the email
        msg = MIMEMultipart()
        msg['FROM'] = config.EMAIL_SENDER
        msg['TO'] = config.EMAIL_RECEIVER
        msg['Subject'] = f"[ALERT]{subject}"
        msg.attach(MIMEText(body,'plain'))
        with smtplib.SMTP(config.SMTP_SERVER,config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.EMAIL_SENDER,config.EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"Alert sent{subject}")
    except Exception as e:
        print(f"Alert failed:{e}");
