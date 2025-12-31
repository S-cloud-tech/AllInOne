from django.urls import path
from . import views

app_name = 'homeinfo'

urlpatterns = [
    path('news/', views.news, name="news"),
    path('info/post/<uuid:pk>/', views.news_detail, name="news_detail"),
    path('shops/', views.our_shops, name="shop"),
    path('contact_us/', views.contact, name="contact"),
    path('about_us/', views.about, name="about"),
    path('faq/', views.faq, name="faq"),
    path('terms&conditions/', views.term_conditions, name="t&c"),
    path('privacy_policy/', views.privacy_policy, name="p&p"),
]

