from typing import List
from .model import OpenAIAPI, OpenAIModelTypes, SentanceSimilarityAPI

class MetadataGenerator():
    def __init__(self, model_api : OpenAIAPI, similarity_api : SentanceSimilarityAPI):
        self.model_api = model_api
        self.similarity_api = similarity_api
        
    def get_used_tokens(self):
        return self.model_api.used_tokens
    
    def topic(self, article_title, article_content, target_word_prompt="one word"):
        article_content = article_content[:128] + "..."
        prompt = f"""# Article: {article_title}
{article_content}

Q:What is the topic of this article in {target_word_prompt}?
A:"""
        return self.model_api.prompt(prompt, model=OpenAIModelTypes.ada, max_tokens=64)

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

Q:What is the closest category of this article?
Available categories: {', '.join(categories)}
A:"""
        return self.model_api.prompt(prompt, model=OpenAIModelTypes.curie, temperature=0.5, max_tokens=32)
    
    def category_similar(self, categories: List[str], article_title: str):
        return self.similarity_api.query(article_title, categories)