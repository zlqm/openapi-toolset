from .conftest import assert_compat_as_expected


def test_additional_properties_of_same_type_string():
    schema = '''
    type: object
    additionalProperties:
      type: string
    x-patternProperties:
      '^[a-z]*$':
        type: string
    '''
    expected = '''
    type: object
    additionalProperties: false
    patternProperties:
      '^[a-z]*$':
        type: string
    '''
    assert_compat_as_expected(schema, expected)


def test_additional_properties_of_same_type_numer():
    schema = '''
    type: object
    additionalProperties:
      type: number
    x-patternProperties:
      '^[a-z]*$':
        type: number
    '''
    expected = '''
    type: object
    additionalProperties: false
    patternProperties:
      '^[a-z]*$':
        type: number
    '''
    assert_compat_as_expected(schema, expected)


def test_additional_properties_with_one_of_patternProperty_types():
    schema = '''
    type: object
    additionalProperties:
      type: number
    x-patternProperties:
      '^[a-z]*$':
        type: number
      '^[A-Z]*$':
        type: string
    '''
    expected = '''
    type: object
    additionalProperties: false
    x-patternProperties:
      '^[a-z]*$':
        type: number
      '^[A-Z]*$':
        type: string
    '''
    assert_compat_as_expected(schema, expected)


def test_additional_properties_with_matching_objects():
    schema = '''
    type: object
    additionalProperties:
      type: object
      properties:
        test:
          type: string
    x-patternProperties:
      '^[a-z]*$':
        type: number
      '^[A-Z]*$':
        type: object
        properties:
          test:
            type: string
    '''
    expected = '''
    type: object
    x-patternProperties:
      '^[a-z]*$':
        type: number
      '^[A-Z]*$':
        type: object
        properties:
          test:
            type: string
    '''
    assert_compat_as_expected(schema, expected)


def test_additional_properties_with_none_matching_objects():
    schema = '''
    type: object
    additionalProperties:
      type: object
      properties:
        test:
          type: string
    x-patternProperties:
      '^[a-z]*$':
        type: number
      '^[A-Z]*$':
        type: object
        properties:
          test:
            type: integer
    '''
    expected = '''
    type: object
    additionalProperties:
      type: object
      properties:
        test:
          type: string
    x-patternProperties:
      '^[a-z]*$':
        type: number
      '^[A-Z]*$':
        type: object
        properties:
          test:
            type: integer
    '''
    assert_compat_as_expected(schema, expected)


def test_additional_properties_with_matching_array():
    schema = '''
    type: object
    additionalProperties:
      type: array
      items:
        type: object
        properties:
          test:
            type: string
    x-patternProperties:
      '^[a-z]*$':
        type: number
      '^[A-Z]*$':
        type: array
        items:
          type: object
          properties:
            test:
              type: string
    '''
    expected = '''
    type: object
    x-patternProperties:
      '^[a-z]*$':
        type: number
      '^[A-Z]*$':
        type: array
        items:
          type: object
          properties:
            test:
              type: string
    '''
    assert_compat_as_expected(schema, expected)


def test_additional_properties_with_composition_types():
    schema = '''
    type: object
    additionalProperties:
      oneOf:
        - type: string
        - type: integer
    x-patternProperties:
      '^[a-z]*$':
        oneOf:
          - type: string
          - type: integer
    '''
    expected = '''
    type: object
    additionalProperties: false
    x-patternProperties:
      '^[a-z]*$':
        oneOf:
          - type: string
          - type: integer
    '''
    assert_compat_as_expected(schema, expected)


def test_null_x_patternProperties():
    schema = '''
    type: object
    additionalProperties:
      type: object
      properties:
        test:
          type: string
    x-patternProperties: null
    '''
    expected = '''
    type: object
    additionalProperties:
      type: object
      properties:
        test:
          type: string
    '''
    assert_compat_as_expected(schema, expected)
