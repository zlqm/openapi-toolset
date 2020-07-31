from .conftest import assert_compat_as_expected


def test_iterates_allOfs():
    schema = '''
    allOf:
      - type: object
        required:
          - foo
        properties:
          foo:
            type: integer
      - allOf:
        - type: number
    '''
    expected = '''
    allOf:
      - type: object
        required:
          - foo
        properties:
          foo:
            type: integer
      - allOf:
        - type: number
    '''
    assert_compat_as_expected(schema, expected)


def test_iterates_anyOfs():
    schema = '''
    anyOf:
      - type: object
        required:
          - foo
        properties:
          foo:
            type: integer
      - anyOf:
        - type: number
    '''
    expected = '''
    anyOf:
      - type: object
        required:
          - foo
        properties:
          foo:
            type: integer
      - anyOf:
        - type: number
    '''
    assert_compat_as_expected(schema, expected)


def test_iterates_oneOfs():
    schema = '''
    oneOf:
      - type: object
        required:
          - foo
        properties:
          foo:
            type: integer
      - oneOf:
        - type: number
    '''
    expected = '''
    oneOf:
      - type: object
        required:
          - foo
        properties:
          foo:
            type: integer
      - oneOf:
        - type: number
    '''
    assert_compat_as_expected(schema, expected)


def test_types_in_not():
    schema = '''
    type: object
    properties:
      not:
        type: string
        minLength: 8
    '''
    expected = '''
    type: object
    properties:
      not:
        type: string
        minLength: 8
    '''
    assert_compat_as_expected(schema, expected)

    schema = '''
    not:
      type: string
      minLength: 8
    '''
    expected = '''
    not:
      type: string
      minLength: 8
    '''
    assert_compat_as_expected(schema, expected)


def test_nested_combination_keywords():
    schema = '''
    anyOf:
      - allOf:
        - type: object
          properties:
            foo:
              type: string
              nullable: true
        - type: object
          properties:
            bar:
              type: integer
              nullable: true
      - type: object
        properties:
          foo:
            type: string
            nullable: true
      - not:
        type: string
        example: foobar
    '''
    expected = '''
    anyOf:
      - allOf:
        - type: object
          properties:
            foo:
              type:
                - string
                - 'null'
        - type: object
          properties:
            bar:
              type:
                - integer
                - 'null'
      - type: object
        properties:
          foo:
            type:
              - string
              - 'null'
      - not:
        type: string
    '''
    assert_compat_as_expected(schema, expected)
