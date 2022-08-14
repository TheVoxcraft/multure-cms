from django.db import models

# Create your models here.    
    
class Author(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name

class ArticleMetadata(models.Model):
    parent = models.OneToOneField('Article', on_delete=models.CASCADE, null=True, blank=True)
    topic = models.CharField(max_length=100, null=True, blank=True)
    short_summary = models.TextField(null=True, blank=True)
    tokens_used = models.IntegerField(default=0)
    

class Article(models.Model):
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    title = models.CharField(max_length=128)
    published = models.BooleanField(default=True)
    published_date = models.DateTimeField(auto_now_add=True)
    url_title = models.SlugField(max_length=256, unique=True)
    tags = models.CharField(max_length=128, blank=True, null=True)
    article_image = models.CharField(max_length=256, blank=True)
    content = models.TextField(blank=True)
    
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title + ' by ' + self.author.name


