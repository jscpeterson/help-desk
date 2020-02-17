from .base import *
import ldap
from django_auth_ldap.config import LDAPSearch, NestedActiveDirectoryGroupType


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)


# LDAP settings

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
AUTH_LDAP_USER_SEARCH = LDAPSearch(LDAP_SEARCH_BASE_DN, ldap.SCOPE_SUBTREE, LDAP_SEARCH_FILTER_STRING)
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(LDAP_GROUP_SEARCH_BASE_DN, ldap.SCOPE_SUBTREE, LDAP_GROUP_SEARCH_FILTER_STRING)
AUTH_LDAP_GROUP_TYPE = NestedActiveDirectoryGroupType()

# Cache settings
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 300

# Information that is extracted from ldap to django user database
AUTH_LDAP_USER_ATTR_MAP = {
    'username': 'sAMAccountName',
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mail',
}

AUTH_LDAP_FIND_GROUP_PERMS = True
