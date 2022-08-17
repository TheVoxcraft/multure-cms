from django.contrib import admin
from .models import Author, Category, Article, ArticleMetadata
from . import tasks

# Admin functions

@admin.action(description='Generate metadata for selected articles')
def generate_article_metadata(modeladmin, request, queryset):
    for article in queryset:
        tasks.generate_article_metadata(article) # TODO: convert to celery task call instead of directly calling the function

@admin.action(description='Generate content for selected articles')
def generate_article_content(modeladmin, request, queryset):
    for article in queryset:
        tasks.generate_article_content(article) # TODO: convert to celery task call instead of directly calling the function

# Admin models

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
    
class ArticleMetadataAdmin(admin.ModelAdmin):
    list_display = ('parent', 'topic', 'short_summary', 'tokens_used')
    search_fields = ('parent',)
    ordering = ('parent',)
    fields = ('parent', 'topic', 'short_summary', 'tokens_used')

class ArticleMetadataInline(admin.StackedInline):
    model = ArticleMetadata
    fields = ('topic', 'short_summary', 'tokens_used')
    readonly_fields = ('topic', 'short_summary', 'tokens_used')
    extra = 0

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'tags', 'published', 'published_date', 'views')
    search_fields = ('title','author', 'category', 'tags')
    list_filter = ('author__name', 'category',)
    ordering = ('-published_date',)
    inlines = [ArticleMetadataInline]
    
    actions = [generate_article_content, generate_article_metadata]
    
    def __str__(self):
        return self.title + ' by ' + self.author.name


# Register models

admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleMetadata, ArticleMetadataAdmin)