from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Brand

# Create your views here.
def home(request):
    return render(request, 'home/index.html')

def product(request):
    return render(request, 'products/products.html')

def product_detail(request):
    return render(request, 'products/product_detail.html')

def catalog(request):
        """Coffee catalog page with filtering, sorting, and pagination."""
        products = Product.objects.filter(is_active=True)

        # --- Search ---
        query = request.GET.get("q")
        if query:
            products = products.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(brand__name__icontains=query)
                | Q(country__icontains=query)
            )

        # --- Price Range ---
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")
        if min_price and max_price:
            products = products.filter(price__gte=min_price, price__lte=max_price)
        elif min_price:
            products = products.filter(price__gte=min_price)
        elif max_price:
            products = products.filter(price__lte=max_price)

        # --- Country Filter ---
        selected_countries = request.GET.getlist("country")
        if selected_countries:
            products = products.filter(country__in=selected_countries)

        # --- Brand Filter ---
        selected_brands = request.GET.getlist("brand")
        if selected_brands:
            products = products.filter(brand_id__in=selected_brands)

        # --- Discount Filter ---
        if request.GET.get("discount"):
            products = products.filter(discount_price__isnull=False)

        # --- Sorting ---
        sort_option = request.GET.get("sort")
        if sort_option == "price_asc":
            products = products.order_by("price")
        elif sort_option == "price_desc":
            products = products.order_by("-price")
        elif sort_option == "newest":
            products = products.order_by("-created_at")
        else:
            products = products.order_by("name")

        # --- Distinct Countries and Brands for Filters ---
        countries = Product.objects.values_list("country", flat=True).distinct().order_by("country")
        brands = Brand.objects.all().order_by("name")

        # --- Pagination ---
        paginator = Paginator(products, 12)  # 12 products per page
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # --- Preserve Query Parameters for Pagination ---
        query_string = "".join([f"&{k}={v}" for k, v in request.GET.items() if k != "page"])

        context = {
            "products": page_obj,
            "page_obj": page_obj,
            "is_paginated": page_obj.has_other_pages(),
            "brands": brands,
            "countries": countries,
            "query_string": query_string,
        }
        return render(request, 'products/products.html', context)

def wishlist(request):
    return render(request, 'products/wishlist.html')

