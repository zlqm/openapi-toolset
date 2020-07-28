from collections import OrderedDict
import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, JsonResponse

import yaml

from openapi_toolset.spec import OpenAPISpec
""" yaml stuff"""


def yaml_loads(stream, Loader=yaml.SafeLoader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
    return yaml.load(stream, OrderedLoader)


def yaml_dumps(data, stream=None, Dumper=yaml.Dumper, **kwds):
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, data.items())

    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


class RequestLoggingAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        request = self.extra
        msg = '{} {} {}'.format(request.method.upper(), request.path, msg)
        return super().process(msg, kwargs)


def get_request_logger(request):
    logger = logging.getLogger('django.request')
    return RequestLoggingAdapter(logger, request)


def get_exception_response(origin_response, msg_txt, status=503):
    content_type = origin_response.get('Content-Type', '')
    if content_type.startswith('application/json'):
        return JsonResponse({'err_msg': msg_txt}, status=status)
    return HttpResponse(msg_txt, status=status)


def load_api_spec():
    doc_file = getattr(settings, 'OPENAPI_CHECK_DOC', None)
    if not doc_file:
        raise ImproperlyConfigured('OPENAPI_CHECK_DOC has not been set')
    return OpenAPISpec.from_file(doc_file)


class SettingsProxy:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getattribute__(self, key):
        global settings
        try:
            value = super().__getattribute__(key)
        except AttributeError:
            return getattr(settings, key)
        else:
            return getattr(settings, key, value)
