from collections import OrderedDict
import json
import os
import re

from django.conf import settings
from django.core.management import BaseCommand
try:
    from django.core.urlresolvers import get_resolver
except ImportError:
    from django.urls import get_resolver
from django.utils.functional import cached_property

from openapi_toolset.validator import validate, InvalidDoc
from openapi_toolset.django_plugin.utils import (yaml_dumps, yaml_loads)


class DjangoAPI:
    OPENAPI_VERSION_DOC = 'openapi: 3.0.0'
    OPENAPI_INFO_DOC = '''
    title: DjangoAPI
    description: this is a auto generatead doc by openapi-toolset
    version: 1.0.0
    '''
    OPENAPI_PATH_METHOD_DOC = '''
    summary: undocumented
    responses:
      200:
        description: ok
    '''

    def __init__(self):
        self.version_doc = self.get_version_doc()
        self.info_doc = self.get_info_doc()
        self.servers_doc = self.get_servers_doc()
        self.paths_doc = self.get_paths_doc()
        self.components_doc = self.get_components_doc()
        self.security_doc = self.get_security_doc()
        self.tags_doc = self.get_tags_doc()
        self.external_docs = self.get_external_docs()

    def get_api_doc(self):
        api_doc = OrderedDict(**self.version_doc)
        if self.info_doc:
            api_doc['info'] = self.info_doc
        if self.servers_doc:
            api_doc['servers'] = self.servers_doc
        if self.paths_doc:
            api_doc['paths'] = self.paths_doc
        if self.components_doc:
            api_doc['components'] = self.components_doc
        if self.security_doc:
            api_doc['security'] = self.security_doc
        if self.tags_doc:
            api_doc['tags'] = self.tags_doc
        if self.external_docs:
            api_doc['externalDocs'] = self.external_docs
        return api_doc

    def load_doc_from_settings(self, doc_name, default=None):
        # may be file, yaml string or dict
        doc = getattr(settings, doc_name, None)
        if not doc:
            doc = getattr(self, doc_name, None)
        if not doc:
            return default
        elif os.path.isfile(doc):
            with open(doc) as f:
                doc = f.read()
        if isinstance(doc, str):
            return yaml_loads(doc)
        return doc

    def get_version_doc(self):
        return self.load_doc_from_settings('OPENAPI_VERSION_DOC')

    def get_info_doc(self):
        return self.load_doc_from_settings('OPENAPI_INFO_DOC', {})

    def get_servers_doc(self):
        return self.load_doc_from_settings('OPENAPI_SERVERS_DOC', [])

    def get_components_doc(self):
        return self.load_doc_from_settings('OPENAPI_COMPONENTS_DOC', {})

    def get_security_doc(self):
        return self.load_doc_from_settings('OPENAPI_SECURITY_DOC', [])

    def get_tags_doc(self):
        return self.load_doc_from_settings('OPENAPI_TAGS_DOC', [])

    def get_external_docs(self):
        return self.load_doc_from_settings('OPENAPI_EXTERNAL_DOCS', {})

    def get_paths_doc(self):
        paths_doc = {}
        resolver = get_resolver()
        for view_func, url_pattern in resolver.reverse_dict.items():
            url_path, path_parameters = url_pattern[0][0]
            url_path = self.unify_url_path(url_path)
            view_class = view_func.view_class
            path_doc = OrderedDict()
            paths_doc[url_path] = path_doc
            path_parameter_doc = self.get_path_parameter_doc(view_class)
            if path_parameter_doc:
                path_doc['parameters'] = path_parameter_doc
                doc_parameters = set(parameter['name']
                                     for parameter in path_parameter_doc
                                     if parameter['in'] == 'path')
                real_parameters = set(re.findall(r'\{([^{}/]+)\}', url_path))
                if not doc_parameters == real_parameters:
                    msg = 'doc_parameters {} and real_parameters {} does '\
                        'not match '.format(doc_parameters, real_parameters)
                    raise ValueError(msg)
            # check path parameter match doc or not
            for method in view_class.http_method_names:
                if not hasattr(view_class, method):
                    continue
                method_func = getattr(view_class, method)
                path_method_doc = self.get_path_method_doc(method_func)
                if not path_method_doc:
                    if method == 'options':
                        continue
                    path_method_doc = self.default_path_method_doc
                path_doc[method] = path_method_doc
        return paths_doc

    # /pets/(?P<pet_name>[a-z]+)
    url_path_pattern = re.compile(r'\(\?P%\((.+?)\)s[^/$]+')
    # /pets/<slug:pet_id>
    url_path_pattern2 = re.compile(r'%\((.+?)\)s')

    def unify_url_path(self, path):
        """
        there are re_path and path in django url
        keyword argument will be transformed as (?P%(pet_id)s) or %(pet_id)s
        here we convert id to {pet_id}
        """
        path = self.url_path_pattern.sub(lambda m: '{%s}' % m.group(1), path)
        path = self.url_path_pattern2.sub(lambda m: '{%s}' % m.group(1), path)
        path = path.lstrip('^').rstrip('$')
        return '/{path}'.format(path=path)

    @cached_property
    def default_path_method_doc(self):
        return self.load_doc_from_settings('OPENAPI_PATH_METHOD_DOC')

    def get_openapi_doc(self, py_obj):
        doc_str = py_obj.__doc__ or ''
        split_by = '--api-doc--'
        if split_by in doc_str:
            doc_str = doc_str.split(split_by, 1)[-1]
            return yaml_loads(doc_str)
        return {}

    def get_path_parameter_doc(self, py_obj):
        doc = self.get_openapi_doc(py_obj)
        return doc and doc['parameters']

    def get_path_method_doc(self, py_obj):
        return self.get_openapi_doc(py_obj)


class Command(BaseCommand):
    help = 'generate openapi doc from doc string'

    def add_arguments(self, parser):
        parser.add_argument('--file',
                            '-f',
                            help='where to save openapi doc',
                            required=True)

    def handle(self, *args, **kwargs):
        api = DjangoAPI()
        filename = os.path.abspath(kwargs['file'])
        api_doc = api.get_api_doc()
        if filename.endswith('.json'):
            doc_content = json.dumps(api_doc)
        else:
            doc_content = yaml_dumps(api_doc)
        with open(filename, 'w') as f:
            f.write(doc_content)
        try:
            validate(json.loads(json.dumps(api_doc)))
        except InvalidDoc:
            msg = 'doc file ({}) generatead, but it\'s invalid.\n'\
                'please check it in swagger editor and fix it'.format(filename)
            self.stderr.write(msg)
