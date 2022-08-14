from typing import List, Protocol
from django.utils.html import escape

class ArticleItem(Protocol):
    content: str
    def to_html(self) -> str:
        ...

class Text(ArticleItem):
    def __init__(self, content: str):
        self.content = escape(content.strip())
        
    def to_html(self) -> str:
        content = self.content.replace('\n\n', '\n<br>\n')
        return f"<p>{content}</p>"

class Chapter(ArticleItem):
    def __init__(self, content: str, subtitle: str):
        self.content = escape(content.strip())
        self.subtitle = escape(subtitle.strip())
        
    def to_html(self) -> str:
        return f"""
<div class="chapter">
    <h2>{self.content}</h2>
    <small>{self.subtitle}</small>
</div>
    """

class Image(ArticleItem):
    def __init__(self, content: str, caption: str):
        self.content = escape(content.strip())
        self.caption = escape(caption.strip())
        
    def to_html(self) -> str:
        return f"""
<img src="{self.content}" alt="{self.caption}">
<h3>{self.caption}</h3>
"""

class ArticleBuilder():
    def __init__(self):
        self.article: List[ArticleItem] = []
    
    def add(self, item: ArticleItem):
        self.article.append(item)
    
    def build(self) -> str:
        return '\n'.join(item.to_html() for item in self.article)
        
        