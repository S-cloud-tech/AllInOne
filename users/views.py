from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.core.mail import send_mail
from .forms import *
from .models import *
from .utils.mails import send_otp_email

# Create your views here.
def signup_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        tax_number = request.POST.get("tax_number")
        company_name = request.POST.get("company_name")
        password = request.POST.get("password")
        user_type = request.POST.get("user_type")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("users:register")

        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            tax_number=tax_number,
            company_name=company_name,
            user_type=user_type,
            password=password,
            is_active=False
        )

        otp_instance = EmailOTP.create_for_user(user)
        send_otp_email(user, otp_instance.otp)

        messages.info(request, f"OTP sent to {email}. Please verify your account.")
        request.session['pending_user'] = str(user.id)
        return redirect("users:verify_otp")
    return render(request, 'auth/signup.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if not user.is_verified:
                messages.error(request, "Please verify your email before logging in.")
                return redirect("users:verify_otp")
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'auth/login.html')

def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Email not found.")
                return redirect("forgot_password")

            # Generate OTP
            otp_code = PasswordResetOTP.generate_otp()
            PasswordResetOTP.objects.create(user=user, otp=otp_code)

            # Send email
            send_mail(
                "Your Password Reset OTP",
                f"Your OTP for password reset is {otp_code}. It expires in 10 minutes.",
                "noreply@yourdomain.com",
                [email],
            )

            request.session["reset_user_id"] = user.id
            messages.success(request, "OTP sent to your email.")
            return redirect("verify_otp")
    else:
        form = ForgotPasswordForm()
    return render(request, "auth/forgot_password.html")

def reset_password(request):
    user_id = request.session.get("reset_user_id")
    otp_verified = request.session.get("otp_verified")

    if not (user_id and otp_verified):
        return redirect("forgot_password")

    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_pw = form.cleaned_data["new_password"]
            confirm_pw = form.cleaned_data["confirm_password"]

            if new_pw != confirm_pw:
                messages.error(request, "Passwords do not match.")
                return redirect("reset_password")

            user = User.objects.get(id=user_id)
            user.set_password(new_pw)
            user.save()

            # Cleanup
            del request.session["reset_user_id"]
            del request.session["otp_verified"]

            messages.success(request, "Password reset successful. Please log in.")
            return redirect("login")
    else:
        form = ResetPasswordForm()
    return render(request, "auth/rest_password.html")

def verify_otp(request):
    user_id = request.session.get("reset_user_id")
    if not user_id:
        return redirect("forgot_password")

    if request.method == "POST":
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            otp_input = form.cleaned_data["otp"]
            try:
                otp_obj = PasswordResetOTP.objects.filter(
                    user_id=user_id, is_used=False
                ).latest("created_at")
            except PasswordResetOTP.DoesNotExist:
                messages.error(request, "No valid OTP found.")
                return redirect("forgot_password")

            # Check expiry (10 minutes)
            if timezone.now() - otp_obj.created_at > timedelta(minutes=10):
                messages.error(request, "OTP expired.")
                return redirect("forgot_password")

            if otp_input != otp_obj.otp:
                messages.error(request, "Invalid OTP.")
                return redirect("verify_otp")

            otp_obj.is_used = True
            otp_obj.save()

            request.session["otp_verified"] = True
            return redirect("reset_password")
    else:
        form = VerifyOTPForm()

    return render(request, "accounts/verify_otp.html", {"form": form})

def resend_otp_view(request):
    user_id = request.session.get('pending_user')
    if not user_id:
        messages.error(request, "Session expired. Please register again.")
        return redirect("users:register")

    user = User.objects.get(id=user_id)

    if not EmailOTP.can_resend(user):
        remaining = EmailOTP.remaining_cooldown(user)
        minutes, seconds = divmod(remaining, 60)
        messages.warning(request, f"Please wait {minutes} min {seconds} sec before requesting a new OTP.")
        return redirect("users:verify_otp")

    otp_instance = EmailOTP.create_for_user(user)
    send_otp_email(user, otp_instance.otp)
    messages.success(request, f"A new OTP has been sent to {user.email}. It will expire in 10 minutes.")
    return redirect("users:verify_otp")

def account_information(request):
    return render(request, 'account/account_info.html')

def address_book(request):
    return render(request, 'account/address_book.html')

def payment_method(request):
    return render(request, 'account/payment_method.html')

