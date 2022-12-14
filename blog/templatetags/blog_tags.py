from django import template
from django.db.models import Count

from ..models import Post, Category

register = template.Library()

@register.simple_tag()
def total_post():
    return Post.published.all()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=6):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

@register.inclusion_tag('blog/post/categories.html')
def category():
    categories =  Category.objects.all()
    return {"categories":categories}

@register.simple_tag()
def get_most_commented_posts(count=6):
    return Post.published.annotate(total_comments=Count('comments')
                                   ).order_by('-total_comments')[:count]