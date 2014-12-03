from django import template
from backend.templatetags import resolve_string

__author__ = 'yarg'

register = template.Library()


@register.filter(name='widget_attr')
def widget_attr(value, arg):
    attrName, attrValue = resolve_string(arg).split(":")
    return value.as_widget(attrs={attrName: attrValue})