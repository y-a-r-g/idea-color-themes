import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
os.environ['PRODUCTION'] = 'False' if os.environ.get('DEV', None) else 'True'

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())
