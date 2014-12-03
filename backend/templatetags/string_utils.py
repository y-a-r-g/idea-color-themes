from django import template
from backend.templatetags import resolve_string

__author__ = 'yarg'

register = template.Library()


@register.filter(name='starts_with')
def starts_with(value, arg):
    starter = resolve_string(arg)
    return unicode(value).find(starter) == 0