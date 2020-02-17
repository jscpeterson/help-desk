import sys

from django.db import IntegrityError as DjangoDBIntegrityError
from sqlite3 import IntegrityError as Sqlite3IntegrityError
from django.http import HttpResponseServerError, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse

from django.conf import settings


def test_exception(request):
    raise Exception("Test exception raised from error/ URL")


def handler403(request, exception):
    response = render(request, 'errors/403.html', {'support_email': settings.SUPPORT_EMAIL})
    response.status_code = 403
    return HttpResponseForbidden(response)


def handler404(request, exception):
    response = render(request, 'errors/404.html', {'support_email': settings.SUPPORT_EMAIL})
    response.status_code = 404
    return HttpResponseNotFound(response)


def handler500(request):
    response = render(request, 'errors/500.html')
    exception_type, exception_value, traceback = sys.exc_info()

    # Catch if the user is accidentally creating a duplicate account (happens when they login for the first time twice)
    # Redirect the user to the dashboard as they are likely already logged in
    # Catching both exceptions because it's unclear which is getting thrown
    if exception_type in [DjangoDBIntegrityError, Sqlite3IntegrityError]:
        return HttpResponseRedirect(reverse('index'))

    response.status_code = 500
    return HttpResponseServerError(response)
