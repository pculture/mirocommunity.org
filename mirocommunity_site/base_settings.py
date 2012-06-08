DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	("Miro Community Devs", "dev@mirocommunity.org"),
)

MANAGERS = (
	("Miro Community Support", "support@mirocommunity.org"),
)

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = True
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mirocommunity_site',
    # We need to have access to the Tier model.
    'mirocommunity_saas',
    # And thus we need paypal.
    'paypal.standard.ipn',
)

ROOT_URLCONF = 'mirocommunity_site.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.media",
    "django.core.context_processors.request",
)

# The following settings are needed per-environment:
# - SECRET_KEY
# - MEDIA_ROOT
# - STATIC_ROOT
# - DATABASES
# - logging/tracing settings (if applicable)
# - PROJECT_ROOT
# - PROJECT_TEMPLATE - see django project creation templating
# - PROJECT_NAMESPACE - use this for dev/staging/prod namespacing.
# - PROJECT_POST_CREATION_SCRIPT - this does anything secret before site creation.