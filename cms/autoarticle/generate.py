from model import OpenAIAPI, OpenAIModelTypes
import builder
from random import randint, shuffle, choice


class ArticleGenerator():
    def __init__(self, model_api : OpenAIAPI):
        self.model : OpenAIAPI = model_api
    
    def new_article_name(self):
        base_articles = """* The Complete Guide to Rum Styles
* The Definitive Guide to Collector watches
* Finding the best gift for your friend's dad
* What to wear on a first date
* How to be a better husband
* The art of the pickup 
* How to make your man fall in love with you 
* 5 signs your man is cheating
* The ultimate guide to understanding your man
* 10 signs your man is interested in you
* How to make your husband a better father
* 10 things only men understand""".split("\n")
        shuffle(base_articles)
        prompt_base_articles = '\n'.join(base_articles)
        new_articles = self.model.prompt(f"# List over informative and interesting articles titles for men's magazine:\n{prompt_base_articles}\n",
                                        model=OpenAIModelTypes.curie, temperature=0.8, max_tokens=96, frequency_penalty=0.3, presence_penalty=0.9)
        return choice(new_articles.strip().replace("*", "").split("\n")).strip()
    
    def write_independant_article(self, title):
        introduction, ctx = self._introduction(title)
        chapter_1, ctx = self._next_chapter(ctx, ' Things to keep in mind')
        chapter_2, ctx = self._next_chapter(ctx)
        chapter_3, ctx = self._next_chapter(ctx)
        conclusion, full_output = self._conclusion(ctx)
        
        article = builder.ArticleBuilder()
        article.add(builder.Text(introduction))
        
        c1_name, c1 = self.__split_chapter(chapter_1)
        article.add(builder.Chapter(' Things to keep in mind'+c1_name))
        article.add(builder.Text(c1))
        
        c2_name, c2 = self.__split_chapter(chapter_2)
        article.add(builder.Chapter(c2_name))
        article.add(builder.Text(c2))
        
        c3_name, c3 = self.__split_chapter(chapter_3)
        article.add(builder.Chapter(c3_name))
        article.add(builder.Text(c3))
        
        c_name, c = self.__split_chapter(chapter_3)
        article.add(builder.Chapter(c_name))
        article.add(builder.Text(c))
        
        return article.build()
    
    def __split_chapter(self, chapter_txt):
        arr = chapter_txt.split("\n")
        return arr[0], '\n'.join(arr[1:])
    def _introduction(self, title):
        prompt = """Article title: What to wear on a first date
Task: Write an interesting and introspective introduction to this article.

# Introduction
"""
        output = self.model.prompt(prompt, model=OpenAIModelTypes.curie, temperature=0.77, max_tokens=256, stop='#')
        full_context = prompt + output
        return output.strip(), full_context

    def _next_chapter(self, ctx, chapter=""):
        prompt = ctx + f"\n\n# Chapter:{chapter}"
        output = self.model.prompt(prompt, model=OpenAIModelTypes.curie, temperature=0.77, max_tokens=256, stop='#')
        full_context = prompt + output
        return output.strip(), full_context
    
    def _conclusion(self, ctx):
        prompt = ctx + """
# Conclusion:
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