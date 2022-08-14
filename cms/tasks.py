from typing import List

from django.conf import settings
from django.utils.text import slugify

from .autoarticle.generate import ArticleGenerator

from .autoarticle.model import OpenAIAPI, SentanceSimilarityAPI, ZeroShotClassificationAPI
from .models import Article, ArticleMetadata, Author, Category
from .autoarticle.metadata import MetadataGenerator
from . import unsplash

def generate_article_metadata(article : Article):
    # Check if a metadata object already exists for this article
    metadata = ArticleMetadata.objects.filter(parent=article).first()
    if metadata is None:
        metadata = ArticleMetadata.objects.create(parent=article)
        
    
    # Generate metadata for the article
    gpt_api = OpenAIAPI(settings.OPENAI_API_KEY)
    classify_api = ZeroShotClassificationAPI(settings.HUGGINGFACE_API_KEY)
    generator = MetadataGenerator(gpt_api, classify_api)
    
    categories = Category.objects.all()
    category_names = [category.name for category in categories]
    
    category = generator.category_classify(category_names, article.title)[0][0]
    article.category = Category.objects.get(name=category)
    
    topic_tags = generator.topics(article.title, article.content)
    article.tags = topic_tags
    metadata.topic = topic_tags.strip()
    metadata.short_summary = generator.short_summary(article.title, article.content).strip()
    metadata.tokens_used += generator.get_used_tokens()
    
    article.save()
    metadata.save()
    
    if article.article_image is None or article.article_image == '':
        print("Setting image for article")
        set_image_from_tags(article)


def generate_article_content(article: Article):
    pass


def generate_independant_article():
    model = OpenAIAPI(settings.OPENAI_API_KEY)
    generator = ArticleGenerator(model)
    
    article_title = generator.new_article_name()
    article_body = generator.write_independant_article(article_title)
    
    # Create article object
    article = Article.objects.create(title=article_title, content=article_body, url_title=slugify(article_title), author=Author.objects.first())
    generate_article_metadata(article)


def set_image_from_tags(article : Article):
    tags = article.tags.split(',')
    image_src = unsplash.get_image_by_query(' '.join(tags[:3]), settings.UNSPLASH_API_KEY)
    article.article_image = image_src
    article.save()
    