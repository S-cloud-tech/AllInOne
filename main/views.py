from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import *
from orders.cart import Cart

# Create your views here.
def home(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    featured_categories = Category.objects.filter(
        is_featured=True, 
        is_active=True
    )
    exclusive_products = Product.objects.filter(is_hot=True)[:4]
    top_categories = Category.objects.filter(is_top_category=True)[:4]
    best_offers = Product.objects.filter(
        is_active=True
        ).filter(
            models.Q(is_hot=True) | models.Q(is_new=True)
        ).order_by('-id')[:4]
    offers = Product.objects.filter(
        category__name__icontains="Beer",
        is_on_sale=True
    ).order_by("-discount_percent")[:8]
    alcohol_products = Product.objects.filter(category__slug='alcohol')[:4]
    household_products = Product.objects.filter(category__slug='household')[:4]
    cart = Cart(request)

    context = {
        'categories': categories,
        'products':products,
        'featured_categories': featured_categories,
        "exclusive_products": exclusive_products,
        "top_categories": top_categories,
        "best_offers": best_offers,
        "offers": offers,
        "alcohol_products": alcohol_products,
        "household_products": household_products,
        "cart": cart,
    }
    return render(request, 'home/index.html', context)

def product(request):
    products = Product.objects.all()

    context = {
        "products": products,
    }
    return render(request, 'products/products.html', context)

def exclusive_products(request):
    products = Product.objects.filter(is_exclusive=True)
    return render(request, "products/products.html", {"products": products, "section": "exclusive"})

def discount_products(request):
    products = Product.objects.filter(discount_percent__gt=0)
    return render(request, "products/products.html", {"products": products, "section": "discount"})

def product_detail(request, slug, pk):
    product = get_object_or_404(Product, slug=slug, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)

def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query) if query else []
    categories = Category.objects.filter(name__icontains=query) if query else []

    context = {
        'products': products, 
        'query': query,
        'categories': categories,
    }
    return render(request, 'home/search_results.html', context)

def ajax_search_suggestions(request):
    query = request.GET.get("q", "")
    results = []
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query)
        )[:5]  # Limit results
        results = [
            {
                "name": p.name,
                "price": str(p.price),
                "image": p.image.url if p.image else "",
                "slug": p.slug,
            }
            for p in products
        ]
    return JsonResponse({"results": results})

def categories(request):
    return render(request,)

def category_detail(request, slug):
    categories = Category.objects.filter(is_active=True)
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    
    context = {
        'categories': categories,
        'category': category,
        'products': products,
    }
    return render(request, 'category/category_products.html', context)

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)

    context = {
        "products": products, 
        "category": category,
        }

    return render(request, "category/category_products.html", context)

def catalog(request):
        """Coffee catalog page with filtering, sorting, and pagination."""
        products = Product.objects.filter(is_active=True)
        categories = Category.objects.all()
        brands = Brand.objects.all()

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
        category = request.GET.get('category')
        brand = request.GET.get('brand')
        search = request.GET.get('search')
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")
        if category:
            products = products.filter(category__slug=category)
        if brand:
            products = products.filter(brand__name__iexact=brand)
        if search:
            products = products.filter(name__icontains=search)
        if min_price and max_price:
            products = products.filter(price__gte=min_price, price__lte=max_price)
        elif min_price:
            products = products.filter(price__gte=min_price)
        elif max_price:
            products = products.filter(price__lte=max_price)

        # --- Category Filter ---
        selected_categories = request.GET.getlist("category")
        if selected_categories:
            products = products.filter(category__slug=category)

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

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data = []
            for product in page_obj:
                data.append({
                    'name': product.name,
                    'price': str(product.price),
                    'image_url': product.image.url if product.image else '',
                    'brand': product.brand.name,
                    'category': product.category.name,
                })
            return JsonResponse({'products': data})

        context = {
            "products": page_obj,
            "page_obj": page_obj,
            "is_paginated": page_obj.has_other_pages(),
            "brands": brands,
            "categories": categories,
            "countries": countries,
            "query_string": query_string,
        }
        return render(request, 'products/products.html', context)

def wishlist(request):
    return render(request, 'products/wishlist.html')

