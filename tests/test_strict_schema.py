import yaml
from openapi_toolset.spec import strict_schema

def is_subset(smaller, larger):
    for key, value in smaller.items():
        if isinstance(value, dict):
            if isinstance(larger.get(key), dict):
                if not is_subset(value, larger[key]):
                    return False
            else:
                return False
        else:
            if value != larger.get(key):
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
          - null
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
                - null
    """
    schema = yaml.load(schema_yaml)
    expected_schema = yaml.load(expected_schema_yaml)
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
    schema = yaml.load(schema_yaml)
    schema = strict_schema(schema)
    assert schema.get('allow_additional_properties') is False
    assert schema['properties']['tags']['items'].get('allow_additional_properties') is False

    schema_yaml = """
    type: object
    allow_additional_properties: true
    properties:
      name:
        type: string
        nullable: true
      tags:
        type: array
        items:
          type: object
          allow_additional_properties: true
          properties:
            name:
              type: string
            tagged_by:
              type: string
              nullable: true
    """
    schema = yaml.load(schema_yaml)
    schema = strict_schema(schema)
    assert schema.get('allow_additional_properties') is True
    assert schema['properties']['tags']['items'].get('allow_additional_properties') is True


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
    schema = yaml.load(schema_yaml)
    schema = strict_schema(schema)
    assert set(schema['required']) == set(['tags'])
    assert set(schema['properties']['tags']['items']['required']) == set(['name'])

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
    schema = yaml.load(schema_yaml)
    schema = strict_schema(schema)
    assert set(schema['required']) == set(['name', 'tags'])
    assert set(schema['properties']['tags']['items']['required']) == set(['name', 'tagged_by'])
