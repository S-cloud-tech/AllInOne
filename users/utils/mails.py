from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(user, otp):
    subject = "Your Account Verification Code"
    message = f"Hello {user.first_name or user.username},\n\nYour OTP code is: {otp}\nThis code expires in 10 minutes."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
