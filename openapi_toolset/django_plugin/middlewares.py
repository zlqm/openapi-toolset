import logging

from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import SimpleLazyObject

from openapi_toolset.spec import (
    OpenAPISpec, MissingDoc, UnmatchDoc)


OPENAPI_CHECK_FAIL_FAST = getattr(
    settings, 'OPENAPI_CHECK_FAIL_FAST', False)
OPENAPI_CHECK_FAIL_ON_MISSING = getattr(
    settings, 'OPENAPI_CHECK_FAIL_ON_MISSING', False)

def get_api_sepc():
    if not getattr(settings, 'OPENAPI_CHECK_DOC', None):
        raise ImproperlyConfigured('cannot get OPENAPI_CHECK_DOC')
    doc_file = getattr(settings, 'OPENAPI_CHECK_DOC')
    return OpenAPISpec.from_file(doc_file)

API_SPEC = SimpleLazyObject(lambda: get_api_sepc())

logger = logging.getLogger('django.request')


class APIDocCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        content_type = response.get('Content-Type')
        # in case of application/json;charset=UTF-8
        content_type = content_type.split(';', 1)[0]
        path = request.path
        method = request.method.lower()
        api_spec = API_SPEC.get_operation_spec(path, method)
        if not api_spec:
            return self.raise_missing_doc(response)
        try:
            api_spec.validate_response(
                response.content,
                content_type=content_type,
                charset=response.charset,
                status_code=response.status_code
            )
            self.log(request, 'info', 'resp match doc')
            return response
        except MissingDoc as err:
            self.log(request, 'warning', 'doc missing')
            return self.raise_missing_doc(response, err)
        except UnmatchDoc as err:
            self.log(request, 'error', 'resp does not match doc')
            return self.raise_mismatch(response, err)

    def raise_missing_doc(self, response, exc=None):
        if OPENAPI_CHECK_FAIL_ON_MISSING:
            return HttpResponse('missing api doc', status_code=503)
        return response


    def raise_mismatch(self, response, exc=None):
        if OPENAPI_CHECK_FAIL_FAST:
            return HttpResponse('resp doesnot match doc', status_code=503)
        return response

    def log(self, request, level, msg, *args, **kwargs):
        log_func = getattr(logger, level.lower())
        msg = '{} {} {}'.format(
            request.method.upper(), request.path, msg)

        log_func(msg, *args, **kwargs)
