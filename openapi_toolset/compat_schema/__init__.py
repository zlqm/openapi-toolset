import abc
from copy import deepcopy

from . import exceptions, node_type, utils

number_format_range_mapping = {
    'int32': (0 - 2**31, 2**31 - 1),
    'int64': (0 - 2**63, 2**63 - 1),
    'float': (0 - 2**128, 2**128 - 1),
}

string_format_pattern_mapping = {
    'byte': '^[\\w\\d+\\/=]*$',
}


class BaseParser(abc.ABC):
    def handle(self, obj):
        return self._handle(obj)

    def _handle(self, obj):
        obj_type = self._get_obj_type(obj)
        func_name = 'handle_{}'.format(obj_type.__name__)
        func = getattr(self, func_name, None)
        if func is None:
            return self.generic_handle(obj)
        return func(obj)

    @abc.abstractmethod
    def _get_obj_type(self):
        pass

    def generic_handle(self, obj):
        return obj


class OAIParser(BaseParser):
    def __init__(self):
        self.fields_to_be_deleted = ['example']

    def _get_obj_type(self, obj):
        return node_type.get_node_type(obj)

    def generic_handle(self, obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                obj[key] = self.handle(value)
        elif isinstance(obj, list):
            for index, value in enumerate(obj):
                obj[index] = self.handle(value)
        return obj

    def handle_schema_generic(self, obj):
        obj = self.handle_schema_nullable(obj)
        obj = self.handle_schema_keywords(obj)
        return obj

    def handle_schema_nullable(self, obj):
        if 'nullable' not in obj:
            return obj
        if obj.get('nullable') is False:
            del obj['nullable']
            return obj
        # handle type
        _type = utils.ensure_list(obj['type'])
        _type.append('null')
        obj['type'] = _type
        del obj['nullable']
        # handle enum
        if 'enum' in obj:
            enum = utils.ensure_list(obj['enum'])
            if None not in enum:
                enum.append(None)
            obj['enum'] = enum
        return obj

    def handle_schema_keywords(self, obj):
        excess_keywords = [
            'example',
            'readOnly',
            'writeOnly',
            'discriminator',
            'xml',
            'externalDocs',
            'deprecated',
        ]
        for keyword in excess_keywords:
            if keyword in obj:
                del obj[keyword]
        return obj

    def handle_object_properties(self, obj):
        if 'properties' not in obj:
            return obj
        if obj['properties'] is None:
            del obj['properties']
            return obj
        malformed_keys = []
        for key, value in obj['properties'].items():
            if not node_type.Schema.isinstance(value):
                malformed_keys.append(key)
            else:
                obj['properties'][key] = self.handle(value)
        for key in malformed_keys:
            del obj['properties'][key]
        return obj

    def handle_object_additional_properties(self, obj):
        return obj

    def handle_Object(self, obj):
        obj = self.handle_schema_generic(obj)
        obj = self.handle_object_properties(obj)
        obj = self.handle_object_additional_properties(obj)
        return obj

    def handle_String(self, obj):
        obj = self.handle_schema_generic(obj)
        if obj.get('format') in string_format_pattern_mapping:
            obj['pattern'] = string_format_pattern_mapping[obj['format']]
        return obj

    def handle_Number(self, obj):
        obj = self.handle_schema_generic(obj)
        obj = self.handle_number_generic(obj)
        return obj

    def handle_Integer(self, obj):
        return self.handle_Number(obj)

    def handle_Array(self, obj):
        obj = self.handle_schema_generic(obj)
        if obj.get('items'):
            if isinstance(obj['items'], dict):
                obj['items'] = self.handle(obj['items'])
            elif isinstance(obj['items'], list):
                for index, item in enumerate(obj['items']):
                    if not node_type.Schema.isinstance(item):
                        raise exceptions.InvalidItemValue
                    obj['items'][index] = self.handle(item)
        return obj

    def handle_Schema(self, obj):
        obj = self.handle_schema_generic(obj)
        return obj

    def handle_combiner_generic(self, obj, combiner_key):
        obj = self.handle_schema_generic(obj)
        if obj[combiner_key] is None:
            del obj[combiner_key]
            return obj
        for index, item in enumerate(obj[combiner_key]):
            obj[combiner_key][index] = self.handle(item)
        return obj

    def handle_allOf(self, obj):
        return self.handle_combiner_generic(obj, 'allOf')

    def handle_anyOf(self, obj):
        return self.handle_combiner_generic(obj, 'anyOf')

    def handle_oneOf(self, obj):
        return self.handle_combiner_generic(obj, 'oneOf')

    def handle_number_generic(self, obj):
        if obj.get('format') and obj['format'] in number_format_range_mapping:
            minimum, maximum = number_format_range_mapping[obj['format']]
            obj_minimum = obj.get('minimum', minimum)
            if obj_minimum < minimum or obj_minimum > maximum:
                obj_minimum = minimum
            obj_maximum = obj.get('maximum', maximum)
            if obj_maximum < minimum or obj_maximum > maximum:
                obj_maximum = maximum
            obj['minimum'] = obj_minimum
            obj['maximum'] = obj_maximum
        return obj

    '''
    def visit_array(self, obj):
        if not obj.get('items'):
            return obj
        if isinstance(obj['items'], (list, tuple)):
            obj['items'] = list(obj['items'])
            for index, item in enumerate(obj['items']):
                obj['items'][index] = self.visit(item)
        else:
            obj['items'] = self.visit(obj['items'])
        obj = self.handle_generic_object(obj)
        return obj

    def handle_object_properties(self, obj):
        if 'properties' not in obj:
            return obj
        for key, value in obj['properties'].items():
            obj['properties'][key] = self.visit(value)
        return obj
    '''


def compat_jsonschema(schema):
    schema = deepcopy(schema)
    parser = OAIParser()
    return parser.handle(schema)
