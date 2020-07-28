import yaml

from openapi_toolset.spec import OpenAPISpec


def _get_processed_schema(schema):
    """Wraps a schema in a doc."""
    if isinstance(schema, str):
        schema = yaml.load(schema)

    fake_doc = {
        'version': '3.0.4',
        'paths': [],
        'components': {
            'schemas': {
                'foo': schema,
            },
        },
    }

    doc = OpenAPISpec(fake_doc).spec_dict
    return doc['components']['schemas']['foo']


def is_equal(a, b):
    if isinstance(a, (list, tuple)) and \
            isinstance(b, (list, tuple)):
        return all(item in b for item in a) and \
            all(item in a for item in b)
    return a == b


def is_subset(smaller, larger):
    for key, value in smaller.items():
        if isinstance(value, dict):
            if isinstance(larger.get(key), dict):
                if not is_subset(value, larger[key]):
                    return False
            else:
                return False
        else:
            if not is_equal(value, larger.get(key)):
                return False
    return True


def test_is_subset():
    smaller = {'a': '1'}
    larger = {'a': '1'}
    assert is_subset(smaller, larger) is True

    smaller = {'a': '1'}
    larger = {'a': '1', 'b': '1'}
    assert is_subset(smaller, larger) is True

    smaller = {'a': '1'}
    larger = {'a': 1, 'b': '1'}
    assert is_subset(smaller, larger) is False

    smaller = {'a': {'b': {'c': 1}}}
    larger = {'a': {'b': {'c': 1, 'd': 2}, 'e': 3}, 'b': '1'}
    assert is_subset(smaller, larger) is True


def test_nullable():
    schema_yaml = """
    type: object
    properties:
      name:
        type: string
        nullable: true
      tags:
        type: array
        items:
          type: object
          properties:
            name:
              type: string
            tagged_by:
              type: string
              nullable: true
    """
    expected_schema_yaml = """
    type: object
    properties:
      name:
        type:
          - string
          - 'null'
      tags:
        type: array
        items:
          type: object
          properties:
            name:
              type: string
            tagged_by:
              type:
                - string
                - 'null'
    """
    schema = _get_processed_schema(schema_yaml)

    expected_schema = yaml.load(expected_schema_yaml)
    assert schema == expected_schema


def test_allow_additional_properties():
    schema_yaml = """
    type: object
    properties:
      name:
        type: string
        nullable: true
      tags:
        type: array
        items:
          type: object
          properties:
            name:
              type: string
            tagged_by:
              type: string
              nullable: true
    """
    schema = _get_processed_schema(schema_yaml)
    assert schema['properties']['tags']['items']['properties']['tagged_by']


def test_required_none():
    schema_yaml = """
    type: object
    properties:
      name:
        type: string
        nullable: true
      tags:
        type: array
        items:
          type: object
          properties:
            name:
              type: string
            tagged_by:
              type: string
              nullable: true
    """
    schema = _get_processed_schema(schema_yaml)
    assert not schema.get('required')
