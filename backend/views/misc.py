from django.http import HttpResponseRedirect
from backend.views import view

__author__ = 'sdvoynikov'


@view(path=r'^twitter/?$')
def index(_):
    return HttpResponseRedirect('https://twitter.com/IdeaColorThemes')