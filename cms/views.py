from django.shortcuts import render, redirect
from .models import Author, Category, Article

# Create your views here.

def home(request):
    return render(request, 'index.html')


def article(request, url_title):
    try:
        article = Article.objects.get(url_title=url_title)
    except Article.DoesNotExist:
        return render(request, '404.html')
    
    return render(request, 'article.html', {'article': article})