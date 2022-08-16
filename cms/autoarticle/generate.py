from .model import OpenAIAPI, OpenAIModelTypes
from . import builder
from random import randint, shuffle, choice


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
    
    def write_independant_article(self, title):
        introduction, ctx = self._introduction(title)
        chapter_1, ctx = self._next_chapter(ctx, ' Things to keep in mind')
        chapter_2, ctx = self._next_chapter(ctx)
        chapter_3, ctx = self._next_chapter(ctx)
        chapter_4, ctx = self._next_chapter(ctx)
        
        
        article = builder.ArticleBuilder()
        article.add(builder.Text(introduction))
        
        c_name, c_next = self.__split_chapter(chapter_1)
        article.add(builder.Chapter(' Things to keep in mind '))
        article.add(builder.Text(c_next+'\n'+c_name))
        
        c_name, c_next = self.__split_chapter(chapter_2)
        article.add(builder.Chapter(c_name))
        article.add(builder.Text(c_next))
        
        c_name, c_next = self.__split_chapter(chapter_3)
        article.add(builder.Chapter(c_name))
        article.add(builder.Text(c_next))
        
        c_name, c_next = self.__split_chapter(chapter_4)
        article.add(builder.Chapter(c_name))
        article.add(builder.Text(c_next))
        
        if 'conclusion' not in ctx and 'Conclusion' not in ctx:
            conclusion, ctx = self._conclusion(ctx)
            article.add(builder.Chapter('Conclusion'))
            article.add(builder.Text(conclusion))
        
        print(ctx)
        return article.build()
    
    def __split_chapter(self, chapter_txt):
        arr = chapter_txt.split("\n")
        return arr[0], '\n'.join(arr[1:])
    def _introduction(self, title):
        prompt = f"""Article title: {title}
Task: Write an interesting and introspective introduction to this article.

# Introduction
"""
        output = self.model.prompt(prompt, model=OpenAIModelTypes.curie, temperature=0.77, max_tokens=256, stop='#')
        full_context = prompt + output
        return output.strip(), full_context

    def _next_chapter(self, ctx, chapter=""):
        prompt = ctx + f"\n\n# Chapter:{chapter}"
        output = self.model.prompt(prompt, model=OpenAIModelTypes.curie, temperature=0.8, max_tokens=256, stop='#', frequency_penalty=0.2, presence_penalty=0.6)
        full_context = prompt + output
        return output.strip(), full_context
    
    def _conclusion(self, ctx):
        prompt = ctx + """
# Conclusion
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