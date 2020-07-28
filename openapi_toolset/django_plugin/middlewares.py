import json

from django.utils.functional import SimpleLazyObject

import jsonschema

from .exceptions import APIMismatchDoc, APIMissDoc
from .utils import (get_request_logger, get_exception_response, load_api_spec,
                    SettingsProxy)

settings = None


def missing_doc_handler(request, response, **kwargs):
    kwargs['logger'].warning('api doc missing')
    if not settings.OPENAPI_CHECK_FAIL_ON_MISSING:
        return response
    if settings.DEBUG:
        raise APIMissDoc('api doc missing')
    else:
        return get_exception_response(response, 'api doc missing')


def mismatch_handler(request, response, **kwargs):
    kwargs['logger'].error('response does not match doc')
    if not settings.OPENAPI_CHECK_FAIL_FAST:
        return response
    if settings.DEBUG:
        exc_dct = {
            'schema_content': json.dumps(kwargs['schema'], indent=2),
            'resp_content': json.dumps(kwargs['content'], indent=2),
            'reason': str(kwargs['err'])
        }
        exc_msg = 'API Schema:\n{schema_content}\n' \
            'Response Schema:\n{resp_content}\n' \
            'Mismatch:\n{reason}'.format(**exc_dct)
        raise APIMismatchDoc(exc_msg)
    else:
        return get_exception_response(response, 'api doc mismatch')


def middleware_exception_handler(request, response, **kwargs):
    err = kwargs['err']
    kwargs['logger'].error('unexpected {} occured.'.format(type(err)),
                           exc_info=err)
    if settings.OPENAPI_CHECK_FAIL_FAST and settings.DEBUG:
        raise err
    return response


settings = SimpleLazyObject(lambda: SettingsProxy(
    OPENAPI_CHECK_FAIL_FAST=False,
    OPENAPI_CHECK_FAIL_ON_MISSING=False,
    OPENAPI_CHECK_MISSING_DOC_HANDLER=missing_doc_handler,
    OPENAPI_CHECK_MISMATCH_HANDLER=mismatch_handler,
    OPENAPI_CHECK_EXCEPTION_HANDLER=middleware_exception_handler,
))
API_SPEC = load_api_spec()


class APIDocCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger = get_request_logger(request)
        response = self.get_response(request)
        content_type = response.get('Content-Type', '').split(';', 1)[0]
        # only check response in json format
        if not content_type.startswith('application/json'):
            return response

        path = request.path
        method = request.method.lower()

        schema = json_content = schema = None
        err_handler_args = (request, response)
        err_handler_kwargs = {'logger': logger}
        try:
            api_spec = API_SPEC.get_operation_spec(path, method)
            if api_spec:
                schema = api_spec.get_response_body_schema()
                if schema:
                    content = response.content.decode(response.charset)
                    json_content = json.loads(content)
                    jsonschema.validate(json_content, schema)
                    logger.info('resp match doc')
                    return response
        except jsonschema.exceptions.ValidationError as err:
            err_handler_kwargs['schema'] = schema
            err_handler_kwargs['content'] = content
            err_handler_kwargs['err'] = err
            return settings.OPENAPI_CHECK_MISMATCH_HANDLER(
                *err_handler_args, **err_handler_kwargs)
        except Exception as err:
            err_handler_kwargs['err'] = err
            return settings.OPENAPI_CHECK_EXCEPTION_HANDLER(
                *err_handler_args, **err_handler_kwargs)
        else:
            return settings.OPENAPI_CHECK_MISSING_DOC_HANDLER(
                *err_handler_args, **err_handler_kwargs)
