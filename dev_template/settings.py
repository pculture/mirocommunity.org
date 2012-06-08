# This settings file will work in a basic way, but should only be considered
# an example of what can be done. Specifically, this is a template for a dev
# site.
from mirocommunity_saas.base_settings import *

DEBUG = TEMPLATE_DEBUG = True
STATIC_ROOT = '{{ project_directory }}/static/'
MEDIA_ROOT = '{{ project_directory }}/media/'
UPLOADTEMPLATE_MEDIA_ROOT = MEDIA_ROOT + 'uploadtemplate/'
SECRET_KEY = '{{ secret_key }}'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '{{ project_directory }}/db.sl3',
    }
}
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': '{{ project_directory }}/whoosh_index',
    }
}
