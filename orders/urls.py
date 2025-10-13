from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('order_history/', views.order_history, name="order_history"),
]

