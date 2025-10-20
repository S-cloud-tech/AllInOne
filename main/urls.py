from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('ajax/search/', views.ajax_search_suggestions, name='ajax_search_suggestions'),
    path('products/', views.product, name='products'),
    path('<slug:slug>/', views.product_detail, name='product_details'),
    path("catalog/", views.catalog, name="catalog"),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path("category/<slug:slug>/", views.category_products, name="category_products"),
    path("products/exclusive/", views.exclusive_products, name="exclusive_products"),
    path("wishlist/", views.wishlist, name="wishlist"),
]

