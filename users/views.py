from django.shortcuts import render

# Create your views here.
def signup_view(request):
    return render(request, 'auth/signup.html')

def login_view(request):
    return render(request, 'auth/login.html')


def account_information(request):
    return render(request, 'account/account_info.html')

def address_book(request):
    return render(request, 'account/address_book.html')

def payment_method(request):
    return render(request, 'account/payment_method.html')

