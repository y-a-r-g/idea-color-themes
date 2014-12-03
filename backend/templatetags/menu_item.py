from django import template
from django.template.loader import get_template
from backend.templatetags import resolve_string

__author__ = 'sdvoynikov'

register = template.Library()


class MenuItemNode(template.Node):
    def __init__(self, _, url, label, template="menu-item.html"):
        self.url = resolve_string(url)
        self.label = resolve_string(label)
        self.template = resolve_string(template)

    def render(self, context):
        tpl = get_template(self.template)
        context['menu_item_label'] = self.label
        context['menu_item_url'] = self.url
        return tpl.render(context)


@register.tag
def menu_item(_, token):
    tokens = token.split_contents()
    if len(tokens) < 3 or len(tokens) > 4:
        raise template.TemplateSyntaxError("%r tag requires two or three arguments" % tokens[0])
    return MenuItemNode(*tokens)