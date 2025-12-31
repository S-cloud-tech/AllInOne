from django.shortcuts import render, redirect, get_object_or_404
from .models import *

# Create your views here.
def news(request,):
    posts = Post.objects.all()
    context = {
        'posts':posts,
    }
    return render(request, 'blog/blog.html', context)

def news_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post
    }
    return render(request, 'blog/blog_article.html', context)

def our_shops(request):
    return render(request, 'info/shops.html')

def contact(request):
    return render(request, 'info/contact.html')

def about(request):
    return render(request, 'info/about.html')

def faq(request):
    return render(request, 'info/faqs.html')

def privacy_policy(request):
    return render(request, 'info/p&p.html')

def term_conditions(request):
    return render(request, 'info/t&c.html')


