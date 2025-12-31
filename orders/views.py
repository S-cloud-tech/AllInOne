from django.shortcuts import render, get_object_or_404, redirect
from main.models import Product
from .models import *
from .cart import Cart

# Create your views here.
def cart_detail(request):
    cart = Cart(request)

    context = {
        "cart": cart,
    }
    return render(request, 'cart/cart.html', context)


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('orders:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('orders:cart_detail')

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('orders:cart_detail')

def checkout(request, user):
    addresses = ShippingAddress.objects.filter(user=request.user)

    context ={
        "addresses": addresses
    }
    return render(request, 'cart/checkout.html', context)

def order_history(request):
    return render(request, 'order/order_history.html')

