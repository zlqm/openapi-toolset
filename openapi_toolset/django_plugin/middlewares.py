import json
import logging

from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import SimpleLazyObject

import jsonschema

from openapi_toolset.spec import OpenAPISpec
from .exceptions import APIMismatchDoc, APIMissDoc


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
        # only check response in json format
        if not content_type == 'application/json':
            return response

        path = request.path
        method = request.method.lower()
        api_spec = API_SPEC.get_operation_spec(path, method)
        if not api_spec:
            return self.raise_missing_doc(response)
        try:
            content = response.content.decode(response.charset)
            json_content = json.loads(content)
            schema = api_spec.get_response_body_schema()
            if not schema:
                return self.missing_doc_handler(request, response)
            jsonschema.validate(json_content, schema)
            self.log(request, 'info', 'resp match doc')
            return response
        except jsonschema.exceptions.ValidationError as err:
            return self.mismatch_handler(request, response, schema, json_content, err)

    def missing_doc_handler(self, request, response):
        self.log(request, 'warning', 'doc missing')
        if not OPENAPI_CHECK_FAIL_ON_MISSING:
            return response
        raise APIMissDoc('cannot get api doc')

    def mismatch_handler(self, request, response, schema, content, exc):
        self.log(request, 'error', 'resp does not match doc')
        if not OPENAPI_CHECK_FAIL_FAST:
            return response
        exc_dct = {
            'schema_content': json.dumps(schema, indent=2),
            'resp_content': json.dumps(content, indent=2),
            'reason': str(exc)
        }
        exc_msg = 'API Schema:\n{schema_content}\n' \
            'Response Content:\n{resp_content}\n' \
            'Mismatch:\n{reason}'.format(**exc_dct)
        raise APIMismatchDoc(exc_msg)

    def log(self, request, level, msg, *args, **kwargs):
        log_func = getattr(logger, level.lower())
        msg = '{} {} {}'.format(
            request.method.upper(), request.path, msg)

        log_func(msg, *args, **kwargs)
