from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_detail, name='product_details'),
    path("catalog/", views.catalog, name="catalog"),
    # path("catalog/<slug:slug>/", views.product_detail, name="product_detail"),
    path("wishlist/", views.wishlist, name="wishlist"),
]

