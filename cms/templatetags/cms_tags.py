from django import template
from ..models import Author, Category, Article
register = template.Library()

@register.simple_tag
def get_category_list():
    return Category.objects.all()