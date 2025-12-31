from django import forms

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

class VerifyOTPForm(forms.Form):
    otp = forms.CharField(max_length=6)

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
