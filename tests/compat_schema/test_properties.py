from .conftest import assert_compat_as_expected


def test_properties():
    schema = '''
    type: object
    required:
      - bar
    properties:
      foo:
        type: string
        example: '2017-01-01T12:34:56Z'
      bar:
        type: string
        nullable: true
    '''
    expected = '''
    type: object
    required:
      - bar
    properties:
      foo:
        type: string
      bar:
        type:
          - string
          - 'null'
    '''
    assert_compat_as_expected(schema, expected)


def test_properies_value_is_null():
    schema = '''
    type: object
    properties: null
    '''
    expected = '''
    type: object
    '''
    assert_compat_as_expected(schema, expected)


def test_strip_malformed_properties_children():
    # TODO: should we handle malformed schema?
    schema = '''
    type: object
    required:
      - bar
    properties:
      for:
        type: string
        example: '2017-01-01T12:34:56Z'
      foobar: 2
      bar:
        type: string
        nullable: true
      baz: null
    '''
    expected = '''
    type: object
    required:
      - bar
    properties:
      for:
        type: string
      bar:
        type:
          - string
          - 'null'
    '''
    assert_compat_as_expected(schema, expected)


def test_additionalProperties_is_false():
    schema = '''
    type: object
    properties:
      foo:
        type: string
        example: '2017-01-01T12:34:56Z'
    additionalProperties: false
    '''
    expected = '''
    type: object
    properties:
      foo:
        type: string
    additionalProperties: false
    '''
    assert_compat_as_expected(schema, expected)


def test_additionalProperties_is_true():
    schema = '''
    type: object
    properties:
      foo:
        type: string
        example: '2017-01-01T12:34:56Z'
    additionalProperties: true
    '''
    expected = '''
    type: object
    properties:
      foo:
        type: string
    additionalProperties: true
    '''
    assert_compat_as_expected(schema, expected)


def test_additionalProperties_is_object():
    schema = '''
    type: object
    properties:
      foo:
        type: string
        example: '2017-01-01T12:34:56Z'
    additionalProperties:
      type: object
      properties:
        type: string
    '''
    expected = '''
    type: object
    properties:
      foo:
        type: string
    additionalProperties:
      type: object
      properties:
        type: string
    '''
    assert_compat_as_expected(schema, expected)
