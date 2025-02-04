import random
import string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import smtplib
from core.settings import auth, sender,EMAIL_HOST, EMAIL_PORT
from email.mime.text import MIMEText



def generate_otp(length=6):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp


def Send_email_with_zoho_server(to_email, message):
    print('hello you!')
    msg = MIMEText(message)
    msg['Subject'] = "OTP from Sample Projects"
    msg['From'] = sender
    to = [to_email],

    server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
    server.login(sender, auth)
    server.sendmail(sender, to, msg.as_string())

    server.quit()
