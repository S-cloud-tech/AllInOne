from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('signup/', views.signup_view, name="signup"),
    path('logout/', LogoutView.as_view(next_page=""), name="logout"),

    path('account/', views.account_information, name="account"),
    path('address/', views.address_book, name="address_book"),
    path('payment_method/', views.payment_method, name="payment_method"),
]


