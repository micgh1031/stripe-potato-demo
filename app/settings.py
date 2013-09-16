import os
import sys


PROJECT_ROOT = os.path.dirname(__file__)

DEBUG = bool(os.environ.get('DJANGO_DEBUG', ''))

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')

# Secret Stuff
SECRET_KEY = 'SUPER SECRET HASH VALUE'

# Stripe Keys
STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", '')
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", '')

SSL_URLS = ['/signup', '/login', '/admin', '/subscribe-vanilla', '/subscribe-modal']

# Crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap'

# Django Stripe Payments settings
PAYMENTS_INVOICE_FROM_EMAIL = 'billing@p.ota.to'

PAYMENTS_PLANS = {
    "potato_normal": {
        "stripe_plan_id": "potato_normal",
        "name": "Monthly Potato Delivery",
        "description": "Monthly potato delivery to your door.",
        "price": 1500,
        "currency": "gbp",
        "interval": "month"
    },

    "potato_premier": {
        "stripe_plan_id": "potato_premier",
        "name": "Monthly Premier Potato Delivery",
        "description": "Monthly PREMIER potato delivery to your door.",
        "price": 3000,
        "currency": "gbp",
        "interval": "month",
    },
}


# Timezone settings
TIME_ZONE = 'Europe/London'
USE_TZ = True


TEMPLATE_DEBUG = DEBUG

ADMINS = []

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'stripe_demo',
        'USER': 'potato',
        'PASSWORD': 'potato',
        'HOST': 'localhost'
    }
}

ALLOWED_HOSTS = []

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT,'media')

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'collected_static')


STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


#S3 SETTINGS
AWS_STORAGE_BUCKET_NAME = 'stripe-django-demo'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

STATIC_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'


# List of callables that know how to import templates from various sources.
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


ROOT_URLCONF = 'app.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',

    'django.contrib.admin',
    'django.contrib.messages',

    'gunicorn',
    'django_extensions',
    'storages',
    'crispy_forms',
    'south',

    'payments',
    'django_forms_bootstrap',

    #Voice apps
    'main',
)

#DEBUG TOOLBAR
INTERNAL_IPS = ('127.0.0.1',)

#dd/mm/yyyy and dd/mm/yy date & datetime input field settings
DATE_INPUT_FORMATS = ('%d-%m-%Y', '%d/%m/%Y', '%d/%m/%y', '%d %b %Y',
                      '%d %b, %Y', '%d %b %Y', '%d %b, %Y', '%d %B, %Y',
                      '%d %B %Y')
DATETIME_INPUT_FORMATS = ('%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M', '%d/%m/%Y',
                          '%d/%m/%y %H:%M:%S', '%d/%m/%y %H:%M', '%d/%m/%y',
                          '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d')


DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False
}

#LOGIN URL SETTINGS
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login'
LOGOUT_URL = '/logout'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'fqa.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            # 'class': 'ssweb.logger.FQAdminEmailHandler',
            'class': 'logging.StreamHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console', 'default'],
            'level': 'ERROR',
            'propagate': True,
        },
        '': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': True
        },
    }
}

# Parse database configuration from $DATABASE_URL
import dj_database_url

dbconfig = dj_database_url.config()
if dbconfig:
    DATABASES['default'] = dbconfig

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

try:
    from local_settings import *
except ImportError:
    pass
