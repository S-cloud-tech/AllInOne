from django.shortcuts import render

# Create your views here.
def news(request):
    return render(request, 'blog/blog.html')

def news_detail(request):
    return render(request, 'blog/blog_article.html')

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


