from typing import List

from django.conf import settings
from django.utils.text import slugify

from .autoarticle.generate import ArticleGenerator

from .autoarticle.model import OpenAIAPI, SentanceSimilarityAPI, ZeroShotClassificationAPI
from .models import Article, ArticleMetadata, Author, Category
from .autoarticle.metadata import MetadataGenerator
from . import unsplash

import celery

@celery.shared_task()
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
        _set_image_from_tags(article)


@celery.shared_task()
def generate_independant_article(category_name : str=None):
    model = OpenAIAPI(settings.OPENAI_API_KEY)
    generator = ArticleGenerator(model)
    
    if category_name is None:
        article_title = generator.new_article_name()
    else:
        article_title = generator.new_category_article_name(category_name)
    
    print(f"Writing a {category_name} article: {article_title}")
    article_body = generator.write_independant_article(article_title, category_name)
    
    # Random author
    selected_author = Author.objects.order_by('?').first()
    
    # Create article object
    article = Article.objects.create(title=article_title, content=article_body, url_title=slugify(article_title), author=selected_author)
    generate_article_metadata(article)


def _set_image_from_tags(article : Article):
    tags = article.tags.split(',')
    image_src = unsplash.get_image_by_query(' '.join(tags[:3]), settings.UNSPLASH_API_KEY)
    article.article_image = image_src
    article.save()
    