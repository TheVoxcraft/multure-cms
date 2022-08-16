from django.shortcuts import render, redirect
from .models import Author, Category, Article
from . import tasks


# Create your views here.

def home(request):
    # Get all articles, order by published_date
    articles = Article.objects.all().filter(published=True).order_by('-published_date')
    
    hero_articles = sorted(articles[:3], key=lambda x: x.views, reverse=True) # latest 3 articles sorted by views
    trending = articles.order_by('-views')
    return render(request, 'index.html', {'articles': articles[:8], 
                                          'hero_articles': hero_articles, 
                                          'trending_articles': trending[:6]})

def article(request, url_title):
    # Style based off https://hiconsumption.com/
    try:
        article = Article.objects.get(url_title=url_title)
    except Article.DoesNotExist:
        return render(request, '404.html')
    
    article.views += 1
    article.save()
    
    return render(request, 'article.html', {'article': article})

MAX_ARTICLES_PER_PAGE = 20
def search(request, category, order_by, page, search_term=None):
    articles = Article.objects.all().filter(published=True)
    
    # Filter search results
    if order_by == 'trending':
        articles = articles.order_by('-views')
    elif order_by == 'latest':
        articles = articles.order_by('-published_date')
    else: # Fail
        return render(request, '404.html')
    if category != 'all':
        if category in [c.name for c in Category.objects.all()]:
            articles = articles.filter(category__name=category)
        else:
            return render(request, '404.html')

    if search_term:
        articles = articles.filter(title__icontains=search_term)
    
    articles = articles[(page-1)*MAX_ARTICLES_PER_PAGE : page*MAX_ARTICLES_PER_PAGE]
    
    page = int(page)
    next_page = page + 1
    prev_page = page - 1 if page > 1 else 1
    next_page_url = f'/search/{category}/{order_by}/{next_page}/{search_term}' if search_term else f'/search/{category}/{order_by}/{next_page}'
    prev_page_url = f'/search/{category}/{order_by}/{prev_page}/{search_term}' if search_term else f'/search/{category}/{order_by}/{prev_page}'
    
    return render(request, 'search.html', {'articles': articles, 'category': category, 'order_by': order_by, 'page': page, 'search_term': search_term,
                                           'next_page_url' : next_page_url, 'prev_page_url' : prev_page_url})
        

def create_independant_article(request):
    if not request.user.is_superuser:
        # return 404 error
        return render(request, '404.html')
    tasks.generate_independant_article()
    return redirect('/')