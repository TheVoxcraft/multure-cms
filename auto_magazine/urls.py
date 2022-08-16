"""auto_magazine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView

import cms.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', cms.views.home, name='home'),
    path('a/<str:url_title>/', cms.views.article, name='article'),
    path('search/<str:category>/<str:order_by>/<int:page>/', cms.views.search, name='category_search'),
    path('search/<str:category>/<str:order_by>/<int:page>/<str:search_term>/', cms.views.search, name='search'),
    #path('category/<str:category_name>/', cms.views.category, name='category'),
    path('endpoint/createnow', cms.views.create_independant_article, name='create_article'),
    
]
