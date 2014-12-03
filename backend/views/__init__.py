import os
import inspect
from django.conf.urls import url

__author__ = 'sdvoynikov'

app_urls = ()


def view(path, **kwargs):
    def wrapper(fn):
        global app_urls
        app_urls += (url(path, fn, **kwargs),)
        return fn
    return wrapper


module_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
for path, dirs, files in os.walk(module_dir):
    for f in files:
        name, ext = os.path.splitext(f)
        if ext == '.py' and not name == '__init__':
            module = os.path.join(path, f)
            execfile(module)
