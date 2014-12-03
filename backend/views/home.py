from django.http.response import HttpResponseRedirect
from backend.logic.themes.themes import get_page
from backend.views import view
from django.shortcuts import render

__author__ = 'sdvoynikov'


@view(path=r'^$')
def index(_):
    return HttpResponseRedirect('/home/')


@view(path=r'^home/$')
def index(request):
    themes, _, _ = get_page(order='downloads', nameFilter='', page=0, count=8, adCount=0, promoCount=0)
    return render(request, 'home/index.html', {
        'themes': themes
    })
