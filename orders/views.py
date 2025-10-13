from django.shortcuts import render

# Create your views here.
def cart(request):
    return render(request, 'cart/cart.html')

def checkout(request):
    return render(request, 'cart/checkout.html')

def order_history(request):
    return render(request, 'order/order_history.html')

