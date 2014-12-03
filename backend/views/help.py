from django.shortcuts import render
from backend.views import view

__author__ = 'sdvoynikov'


@view(path=r'^help/?$')
def index(request):
    return render(request, 'help/index.html')