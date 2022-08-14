from typing import List
from .model import OpenAIAPI, OpenAIModelTypes, SentanceSimilarityAPI, ZeroShotClassificationAPI

class MetadataGenerator():
    def __init__(self, model_api : OpenAIAPI, classify_api : SentanceSimilarityAPI,):
        self.model_api = model_api
        self.classify_api = classify_api
        
    def get_used_tokens(self):
        return self.model_api.used_tokens
    
    def topics(self, article_title, article_content): # TODO: needs work
        article_content = article_content[:128] + "..."
        prompt = f"""# Article: {article_title}
{article_content}

# Keywords comma separated:"""
        return self.model_api.prompt(prompt, model=OpenAIModelTypes.babbage, max_tokens=64, temperature=0.4)

    def short_summary(self, article_title, article_content):
        article_content = article_content[:256] + "..."
        prompt = f"""# Article: {article_title}
{article_content}

# Short summary of this article:
"""
        return self.model_api.prompt(prompt, model=OpenAIModelTypes.babbage, max_tokens=128)
    
    def category_gpt(self, categories: List[str], article_title: str, article_content: str):
        article_content = article_content[:128] + "..."
        prompt = f"""# Article: {article_title}
{article_content}

Q: What is the closest category of this article?
Available categories: {', '.join(categories)}
A:"""
        return self.model_api.prompt(prompt, model=OpenAIModelTypes.curie, temperature=0.5, max_tokens=32)
    
    def category_classify(self, categories: List[str], article_title: str):
        return self.classify_api.query(article_title, categories)