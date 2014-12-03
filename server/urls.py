from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
from backend.views import app_urls
from server import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^paypal/', include('paypal.standard.ipn.urls')),
)

urlpatterns += app_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)