import random

from django import template

register = template.Library()


@register.simple_tag
def rand_num(value):
    return random.randint(1, value)
