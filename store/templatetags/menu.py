#nella documentazione di django si chiama  poll_extras.py  link: https://docs.djangoproject.com/en/4.2/howto/custom-template-tags/

from django import template
from store.models import Category

register = template.Library()

@register.inclusion_tag("core/menu.html")
def menu():
    categories = Category.objects.all()
    return {"categories": categories}