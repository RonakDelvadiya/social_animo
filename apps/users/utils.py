import string
import random
import traceback
import smtplib
from pytz import timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from social_animo.settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_HOST


def otp_genertor():
    try:
        length_of_string = 7
        random_string = ''.join(random.choices(string.ascii_uppercase +string.digits, k = length_of_string))
        if usr_email_verification.objects.filter(generated_otp=random_string).exists() :
            otp_genertor()
        return random_string
    except Exception as e :
        print (e)
        logger.error(str(e))
        print (traceback.print_exc())
        return False


def send_email_for_verification(generated_otp,email):
    try:
        msg = create_meseg_body(generated_otp, [email])
        server = smtplib.SMTP(EMAIL_HOST, 587)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.sendmail(EMAIL_HOST_USER, [email], msg.as_string())
        return True
    except Exception as e :
        logger.error("Error: unable to send email")
        return 0


def create_meseg_body(generated_otp, email):
    try:
        msg = MIMEMultipart('alternative')
        format = "%Y-%m-%d %H:%M:%S %Z%z"
        now_utc = datetime.now(timezone('UTC'))
        now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
        now_asia = now_asia.strftime(format)
        msg['Subject'] = 'Email verification for social animo regestration'
        msg['From'] = EMAIL_HOST_USER
        msg['To'] = ', '.join(email)
        text = 'Please verify your email, your OTP is %s.'%(generated_otp)
        part1 = MIMEText(text, 'plain')
        msg.attach(part1)
        return msg
    except Exception as e:
        logger.error("Error: unable to send msg body")
        return None