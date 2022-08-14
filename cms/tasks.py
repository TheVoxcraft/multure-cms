from typing import List

from django.conf import settings

from .autoarticle.model import OpenAIAPI, SentanceSimilarityAPI, ZeroShotClassificationAPI
from .models import Article, ArticleMetadata, Category
from .autoarticle.metadata import MetadataGenerator

def generate_article_metadata(article : Article):
    # Check if a metadata object already exists for this article
    try:
        metadata = ArticleMetadata.objects.filter(parent=article).first()
    except ArticleMetadata.DoesNotExist:
        # Create a new metadata object
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
    metadata.topic = topic_tags
    metadata.short_summary = generator.short_summary(article.title, article.content)
    metadata.tokens_used += generator.get_used_tokens()
    
    article.save()
    metadata.save()

    
    

def generate_article_content(article: Article):
    title = article.title
    author = article.author
    category = article.category
    
    article.content = '<p>This is the content of the article.</p>'
    article.save()