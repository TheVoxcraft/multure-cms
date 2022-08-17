from .model import OpenAIAPI, OpenAIModelTypes
from . import builder
from random import randint, shuffle, choice
import re

class ArticleGenerator():
    def __init__(self, model_api : OpenAIAPI):
        self.model : OpenAIAPI = model_api
    
    def new_article_name(self):
        base_articles = """* The Complete Guide to Rum Styles
* The Definitive Guide to Collector watches
* Finding the best gift for your friend""".split("\n")
        shuffle(base_articles)
        prompt_base_articles = '\n'.join(base_articles)
        new_articles = self.model.prompt(f"# List over interesting article titles for a lifestyle and technology magazine:\n{prompt_base_articles}\n",
                                        model=OpenAIModelTypes.curie, temperature=0.8, max_tokens=96, frequency_penalty=0.3, presence_penalty=0.8)
        return choice(new_articles.strip().replace("*", "").split("\n")).strip()
    
    def new_category_article_name(self, category_name : str):
        base_articles = """* Vices: The Complete Guide to Rum Styles
* Style: The Definitive Guide to Collector watches
* Life: Finding the best gift for your friend""".split("\n")
        shuffle(base_articles)
        prompt_base_articles = '\n'.join(base_articles)
        new_articles = self.model.prompt(f"# List over interesting article titles for a lifestyle and technology magazine:\n{prompt_base_articles}\n* {category_name}:",
                                        model=OpenAIModelTypes.curie, temperature=0.8, max_tokens=72, frequency_penalty=0.3, presence_penalty=0.8)
        if '\n' in new_articles:
            return choice(new_articles.strip().replace("*", "").split("\n")).strip()
        return new_articles.strip()
    
    def write_independant_article(self, title, category=None):
        intro, full_text = self._introduction(title, category)
        chapter_1, full_text = self._next_chapter(full_text, ' Things to keep in mind')
        
        for _ in range(randint(2, 6)):
            _, full_text = self._next_chapter(full_text)
        
        if 'conclusion' not in full_text and 'Conclusion' not in full_text:
            _, full_text = self._conclusion(full_text)
        
        article = full_text.strip() + '\n' # Strip and add newline to end of article to make valid p tags
        
        article = re.sub(r"(.+)\n", "<p>\\1</p>\n", article) # Replace paragraphs with <p> tags
        article = article.replace("\n\n", "\n<br>\n") # Replace double newlines with <br> tags
        article = re.sub(r"#\s*[c|C]hapter:\s*(.+)\n", '\n<div class="chapter">\n<h2>\\1</h2>\n</div>\n', article) # Replace chapters with chapter tags
                
        print(article)
        return article
    

    def _introduction(self, title, category=None):
        category_str = f"Category: {category}" if category else ""
        base_prompt = f"""Article title: {title}
{category_str}
Task: Write an interesting and introspective introduction to this article.
"""
        prompt = base_prompt + "\n# Chapter: Introduction"
        output = self.model.prompt(prompt, model=OpenAIModelTypes.curie, temperature=0.77, max_tokens=256, stop='#')
        full_context = prompt + output
        return output.strip(), full_context[len(base_prompt):].strip()

    def _next_chapter(self, ctx, chapter=""):
        prompt = ctx + f"\n\n# Chapter:{chapter}"
        output = self.model.prompt(prompt, model=OpenAIModelTypes.curie, temperature=0.8, max_tokens=256, stop='#', frequency_penalty=0.2, presence_penalty=0.6)
        full_context = prompt + output
        return output.strip(), full_context
    
    def _conclusion(self, ctx):
        prompt = ctx + """
# Chapter: Conclusion
"""
        output = self.model.prompt(prompt, model=OpenAIModelTypes.curie, temperature=0.77, max_tokens=256, stop='#')
        full_context = prompt + output
        return output.strip(), full_context


if __name__ == '__main__':
    key = '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'
    api = OpenAIAPI(key)
    ag = ArticleGenerator(api)
    title = ag.new_article_name()
    print(title)
    article = ag.write_independant_article(title)
    print(article)