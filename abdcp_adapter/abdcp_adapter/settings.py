# -*- coding: utf-8 -*-

"""
Django settings for abdcp_adapter project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7ngk5o_#+r)c-ps1k22m%waa^26f4#g_!#z*!ig*382ic@!3k!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Dependencies
    'south',
    'sequence_field',
    # Project
    'operators',
    'abdcp_messages',
    'abdcp_processes',
    
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'abdcp_adapter.urls'

WSGI_APPLICATION = 'abdcp_adapter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# Portability API
PORTABILITY_API_BASE_URL = 'http://portability-api-server.com/path/to/api'
PORTABILITY_API_KEY = '<some API key>'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)-15s - %(levelname)-4s - %(module)s - %(process)d - %(thread)d: %(message)s'
        },
        'simple': {
            'format': '%(asctime)-15s - %(levelname)-4s : %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
    'root': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
    },
}

# SEQUENCE_FIELD_DEFAULT_VALUE = 1
# SEQUENCE_FIELD_ADMIN = True
# SEQUENCE_FIELD_DEFAULT_TEMPLATE = '%N'
# SEQUENCE_FIELD_DEFAULT_PATTERN =  r'(\d+)'
# SEQUENCE_FIELD_DEFAULT_EXPANDERS = "Already mentioned in the previous section."


LOCAL_OPERATOR_ID = "45"

ABDCP_OPERATOR_ID = "00"

TELEPHONY_OPERATOR_EMAIL = ""
WEBMASTER_EMAIL = ""
ITP_CONTACT_EMAIL = ""
SMTP_SERVER = ""




# Local settings
try:
    from local_settings import *
except ImportError:
    pass

