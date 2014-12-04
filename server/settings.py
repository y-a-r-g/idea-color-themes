import os
import dj_database_url
from django.utils.translation import ugettext_lazy as _

DEBUG = os.environ.get('PRODUCTION', 'False') != 'True'

DIR_BASE = os.path.dirname(os.path.dirname(__file__))
# noinspection PyUnresolvedReferences
DIR_DATABASE = os.path.join(DIR_BASE, 'database')
# noinspection PyUnresolvedReferences
DIR_MEDIA = os.path.join(DIR_BASE, 'media')
# noinspection PyUnresolvedReferences
DIR_STATIC = os.path.join(DIR_BASE, 'static')
# noinspection PyUnresolvedReferences
DIR_TEMPLATES = os.path.join(DIR_BASE, 'templates')
# noinspection PyUnresolvedReferences
DIR_LOCALES = os.path.join(DIR_BASE, 'locale')

SECRET_KEY = os.environ.get('ICT_SECRET_KEY', None)

TEMPLATE_DEBUG = DEBUG

ROOT_URL = 'http://www.ideacolorthemes.org'

ALLOWED_HOSTS = ['*'] if DEBUG else [
    '.ideacolorthemes.org',
    '.herokuapp.com'
]

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'postmark',
    'compressor',
    'paypal.standard.ipn',
    'backend',
    'storages',
    'boto'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'server.urls'

WSGI_APPLICATION = 'server.wsgi.application' if DEBUG else 'server.production.wsgi.application'
DATABASES = {'default': dj_database_url.config()}

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = DIR_STATIC

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

TEMPLATE_DIRS = (
    DIR_TEMPLATES,
)

LOCALE_PATHS = (
    DIR_LOCALES,
)


ADMINS = (
    ('admin', 'info@ideacolorthemes.org'),
)

PAYPAL_RECEIVER_EMAIL = 'svdvoynikov@gmail.com'
NOTYFY_EMAIL = 'info@ideacolorthemes.org'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

EMAIL_BACKEND = "postmark.backends.PostmarkBackend"
POSTMARK_API_KEY = os.environ.get('POSTMARK_API_KEY', None)
POSTMARK_SENDER = 'info@ideacolorthemes.org'
POSTMARK_TEST_MODE = False
POSTMARK_TRACK_OPENS = False
DEFAULT_FROM_EMAIL = POSTMARK_SENDER
SERVER_EMAIL = POSTMARK_SENDER

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler"
            },
        },
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins"],
            'propagate': True,
            'level': 'INFO',
            }
    }
}

AWS_STORAGE_BUCKET_NAME = "idea-color-themes-static"
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
MEDIA_URL = "https://%s.s3.amazonaws.com/" % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = ''
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
