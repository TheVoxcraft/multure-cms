from django.shortcuts import render, redirect
from .models import Author, Category, Article

# Create your views here.

def home(request):
    # Get all articles, order by published_date
    articles = Article.objects.all().order_by('-published_date')
    
    hero_articles = articles[:3]
    trending = articles.order_by('-views')
    return render(request, 'index.html', {'articles': articles, 
                                          'hero_articles': hero_articles, 
                                          'trending_articles': trending})

def article(request, url_title):
    # Style based off https://hiconsumption.com/
    try:
        article = Article.objects.get(url_title=url_title)
    except Article.DoesNotExist:
        return render(request, '404.html')
    
    article.views += 1
    article.save()
    
    return render(request, 'article.html', {'article': article})