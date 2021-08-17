import urllib.parse
import urllib.request
import math
import random
from datetime import datetime, timezone

from django.conf import settings

from users.models import OTP

# function to generate OTP


def generate_otp():

    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""

   # length of password can be chaged
   # by changing value in range
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP


def verify_otp(user, otp, otp_type):
    current_time = datetime.now(timezone.utc)
    OTP_object = OTP.objects.get(user=user, active=True, otp_type=otp_type)
    time_difference = (current_time - OTP_object.created).total_seconds()

    if(OTP_object.otp == otp and time_difference <= int(settings.OTP_VALIDATION_TIME) * 60):
        OTP_object.matched = True
        OTP_object.save()
        return True

    return False


def send_sms(numbers, message):
    data = dict(api_key=settings.TEXTLOCAL_API_KEY,
                username=settings.TEXTLOCAL_USERNAME, hash=settings.TEXTLOCAL_PASSWORD_HASH, numbers=numbers, message=message, sender=settings.SMS_SENDER)
    data = urllib.parse.urlencode(data).encode('utf-8')
    request = urllib.request.Request(settings.TEXTLOCAL_SEND_URL)
    f = urllib.request.urlopen(request, data=data)
    fr = f.read()
    return(fr)

def approved_account_message(numbers):
    send_sms(numbers, settings.ACCOUNT_APPROVAL_TEMPLATE.format(settings.SOCIETY_NAME))

def create_otp(mobile_number, data, message_template, otp_type, user=None):
    otp_exist = OTP.objects.filter(user=mobile_number, otp_type=otp_type)
    if(otp_exist):
        for obj in otp_exist:
            if(obj.active):
                obj.delete()
    
    otp = generate_otp()
    if user:
        if otp_type == OTP.Type.SIGNUP:
            res = send_sms(mobile_number, message_template.format(user['full_name'], otp, settings.SOCIETY_NAME))
        else:
            res = send_sms(mobile_number, message_template.format(
                user.full_name, settings.SOCIETY_NAME, otp))
    else:
        res = send_sms(mobile_number, message_template.format(
            mobile_number, settings.SOCIETY_NAME, otp))
    OTP.objects.create(
        otp=otp,
        user=mobile_number,
        data=data,
        otp_type=otp_type
    )


def get_message_template(otp_type):
    if otp_type == OTP.Type.SIGNUP:
        return settings.SIGNUP_TEMPLATE
    elif otp_type == OTP.Type.NUMBER_CHANGE:
        return settings.NUMBER_CHANGE_TEMPLATE
    elif otp_type == OTP.Type.PASSWORD:
        return settings.PASSWORD_TEMPLATE
