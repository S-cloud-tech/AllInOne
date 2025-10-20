from django import template
from main.models import *

register = template.Library()

@register.inclusion_tag('components/partials/top_categories.html')
def top_categories(limit=None):
    """
    Render top categories dynamically anywhere.
    Usage: {% top_categories %} or {% top_categories 4 %}
    """
    categories = Category.objects.filter(is_top_category=True, is_active=True)
    if limit:
        categories = categories[:limit]
    return {'top_categories': categories}

@register.inclusion_tag('components/partials/best_offers_carousel.html')
def best_offers_for_restaurants(limit=None):
    """
    Display best offers for restaurants dynamically.
    You can pass a limit like {% best_offers_for_restaurants 8 %}
    """
    # Best offers logic
    best_offers = Product.objects.filter(is_active=True).order_by('price')[:12]  # Start with low price
    new_products = Product.objects.filter(is_active=True).order_by('-created_at')[:12]
    hot_products = Product.objects.filter(is_hot=True, is_active=True)[:12]

    # Merge and remove duplicates
    best_offers_combined = list({p.id: p for p in list(hot_products) + list(new_products) + list(best_offers)}.values())
    if limit:
        products = best_offers_combined[:limit]
    return {'products': products}
