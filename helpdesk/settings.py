"""
Django settings for helpdesk project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dotenv.read_dotenv(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'tickets',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'helpdesk.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'helpdesk.wsgi.application'

AUTH_USER_MODEL = 'users.HelpDeskUser'
# TODO Sync to LDAP

LOGIN_URL = 'index'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Denver'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# Email settings

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587

SYSADMIN_EMAIL = os.environ.get('SYSADMIN_EMAIL')
SUPPORT_EMAIL = os.environ.get('SUPPORT_EMAIL')

ADMINS = [
    (os.environ.get('SYSADMIN_NAME'), os.environ.get('SYSADMIN_EMAIL'))
]


AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# LDAP settings
import ldap
from django_auth_ldap.config import LDAPSearch, NestedActiveDirectoryGroupType
# Server information
LDAP_SERVER_FQDN = os.getenv('LDAP_SERVER_FQDN')
AUTH_LDAP_SERVER_URI = 'ldap://' + LDAP_SERVER_FQDN
# Binding information
AUTH_LDAP_BIND_DN = os.getenv('AUTH_LDAP_BIND_DN')
AUTH_LDAP_BIND_PASSWORD = os.getenv('AUTH_LDAP_BIND_PASSWORD')
AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_DEBUG_LEVEL: 1,
    ldap.OPT_REFERRALS: 0,
}
# User and group search objects and types
LDAP_SEARCH_BASE_DN = os.getenv('LDAP_SEARCH_BASE_DN')
LDAP_SEARCH_FILTER_STRING = os.getenv('LDAP_SEARCH_FILTER_STRING')
LDAP_GROUP_SEARCH_BASE_DN = os.getenv('LDAP_GROUP_SEARCH_BASE_DN')
LDAP_GROUP_SEARCH_FILTER_STRING = os.getenv('LDAP_GROUP_SEARCH_FILTER_STRING')
AUTH_LDAP_USER_SEARCH = LDAPSearch(LDAP_SEARCH_BASE_DN,
                                   ldap.SCOPE_SUBTREE,
                                   LDAP_SEARCH_FILTER_STRING)
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(LDAP_GROUP_SEARCH_BASE_DN,
                                    ldap.SCOPE_SUBTREE,
                                    LDAP_GROUP_SEARCH_FILTER_STRING)
AUTH_LDAP_GROUP_TYPE = NestedActiveDirectoryGroupType()
# Cache settings
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 300
# Information that is extracted from ldap to django user database
AUTH_LDAP_USER_ATTR_MAP = {'username': 'sAMAccountName',
                           'first_name': 'givenName',
                           'last_name': 'sn',
                           'email': 'mail',
                           }
AUTH_LDAP_FIND_GROUP_PERMS = True
