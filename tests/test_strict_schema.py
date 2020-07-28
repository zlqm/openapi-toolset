import yaml
from openapi_toolset.jsonschema import strict_schema


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
        oneOf:
          - type: string
          - type: 'null'
      tags:
        type: array
        items:
          type: object
          properties:
            name:
              type: string
            tagged_by:
              oneOf:
                - type: string
                - type: 'null'
    """
    schema = yaml.safe_load(schema_yaml)
    expected_schema = yaml.safe_load(expected_schema_yaml)
    schema = strict_schema(schema)
    assert is_subset(expected_schema, schema) is True


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
    schema = yaml.safe_load(schema_yaml)
    schema = strict_schema(schema)
    assert schema.get('additionalProperties') is False
    assert schema['properties']['tags']['items'].get(
        'additionalProperties') is False

    schema_yaml = """
    type: object
    additionalProperties:
      type: string
    properties:
      name:
        type: string
        nullable: true
      tags:
        type: array
        items:
          type: object
          additionalProperties:
            type: string
          properties:
            name:
              type: string
            tagged_by:
              type: string
              nullable: true
    """
    schema = yaml.safe_load(schema_yaml)
    schema = strict_schema(schema)
    assert schema.get('additionalProperties') == {'type': 'string'}
    assert schema['properties']['tags']['items'].get(
        'additionalProperties') == {'type': 'string'}


def test_required():
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
    schema = yaml.safe_load(schema_yaml)
    schema = strict_schema(schema)
    assert set(schema['required']) == set(['name', 'tags'])
    assert set(schema['properties']['tags']['items']['required']) \
        == set(['name', 'tagged_by'])

    schema_yaml = """
    type: object
    required:
      - name
      - tags
    properties:
      name:
        type: string
        nullable: true
      tags:
        type: array
        items:
          type: object
          required:
            - name
            - tagged_by
          properties:
            name:
              type: string
            tagged_by:
              type: string
              nullable: true
    """
    schema = yaml.safe_load(schema_yaml)
    schema = strict_schema(schema)
    assert set(schema['required']) == set(['name', 'tags'])
    assert set(schema['properties']['tags']['items']['required']) \
        == set(['name', 'tagged_by'])
