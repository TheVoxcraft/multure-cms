from django.contrib import admin
from .models import Author, Category, Article

# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
    fields = ('name', 'description')
    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
    fields = ('name', 'description')
    

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'tags')
    search_fields = ('title', 'author', 'category', 'tags')
    list_filter = ('title', 'author', 'category', 'tags')
    ordering = ('title',)
    


# register
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)