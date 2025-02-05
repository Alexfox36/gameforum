import pyotp
import request
from datetime import datetime, timedelta


def send_otp():
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session['otp_sekret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_date'] = str(valid_date)

    print(f"Ваш код подтверждения {otp}")



