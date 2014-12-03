from django.utils.translation import ugettext_lazy as _

__author__ = 'sdvoynikov'


def resolve_string(string):
    localize = len(string) > 3 and string[0:2] == '_(' and string[-1] == ')'
    if localize:
        string = string[2:-1]
    if string[0] == string[-1] and string[0] in ['"', '\'']:
        string = string[1:-1]
    else:
        string = string.strip()
    if localize:
        string = _(string)
    return string
