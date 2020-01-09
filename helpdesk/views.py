from django.http import HttpResponseServerError, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render
from django.template import RequestContext

from helpdesk.settings import SUPPORT_EMAIL


def test_exception(request):
    raise Exception("Test exception raised from error/ URL")


def handler403(request, exception):
    response = render(request, 'errors/403.html', {'support_email': SUPPORT_EMAIL})
    response.status_code = 403
    return HttpResponseForbidden(response)


def handler404(request, exception):
    response = render(request, 'errors/404.html', {'support_email': SUPPORT_EMAIL})
    response.status_code = 404
    return HttpResponseNotFound(response)


def handler500(request):
    response = render(request, 'errors/500.html')
    response.status_code = 500
    return HttpResponseServerError(response)
