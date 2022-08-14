from typing import List

from django.conf import settings

from .autoarticle.model import OpenAIAPI, SentanceSimilarityAPI
from .models import Article, ArticleMetadata, Category
from .autoarticle.metadata import MetadataGenerator

def generate_article_metadata(article : Article):
    # Check if a metadata object already exists for this article
    if article.metadata is None:
        metadata = ArticleMetadata.objects.create()
        article.metadata = metadata
        article.save()
    metadata = article.metadata
    
    # Generate metadata for the article
    gpt_api = OpenAIAPI(settings.OPENAI_API_KEY)
    similarity_api = SentanceSimilarityAPI(settings.HUGGINGFACE_API_KEY)
    generator = MetadataGenerator(gpt_api, similarity_api)
    
    categories = Category.objects.all()
    category_names = [category.name for category in categories]
    
    category = generator.category_similar(category_names, article.title)[0][0]
    article.category = Category.objects.get(name=category)
    article.save()
    
    metadata.topic = generator.topic(article.title, article.content)
    metadata.short_summary = generator.short_summary(article.title, article.content)
    metadata.tokens_used += generator.get_used_tokens()
    metadata.save()

    
    

def generate_article_content(article: Article):
    title = article.title
    author = article.author
    category = article.category
    
    article.content = '<p>This is the content of the article.</p>'
    article.save()