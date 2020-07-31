from .conftest import assert_compat_as_expected

# not implemented


def test_minimal_OpenAPI_30_parameter():
    schema = '''
    name: parameter name
    in: cookie
    schema:
      type: string
      nullable: true
    '''
    expected = '''
    type:
      - string
      - 'null'
    '''
    assert_compat_as_expected(schema, expected)


def test_extensive_OpenAPI_30_parameter():
    schema = '''
    name: parameter name
    in: cookie
    schema:
      type: string
      nullable: true
    required: true
    allowEmptyValue: true
    deprecated: true
    allowReserved: true
    style: matrix
    explode: true
    example: 'parameter example'
    '''
    expected = '''
    type:
      - string
      - 'null'
    '''
    assert_compat_as_expected(schema, expected)


def test_OpenAPI_30_parameter_with_mime_schemas():
    schema = '''
    name: parameter name
    in: cookie
    content:
      application/javascript:
        schema:
          type: string
          nullable: true
      text/css:
        schema:
          type: string
          nullable: true
    '''
    expected = '''
    application/javascript:
      type:
        - string
        - 'null'
    text/css:
      type:
        - string
        - null
    '''
    assert_compat_as_expected(schema, expected)


def test_OpenAPI_30_parameter_without_mime_schemas():
    schema = '''
    name: parameter name
    in: cookie
    content:
      application/javascript:
        schema:
          type: string
          nullable: true
      text/css:
    '''
    expected = '''
    application/javascript:
      type:
        - string
        - 'null'
    text/css: {}
    '''
    assert_compat_as_expected(schema, expected)


def test_OpenAPI_30_parameter_with_blank_schema():
    schema = '''
    name: parameter name
    in: cookie
    schema:
      description: parameter description]
    '''
    expected = '''
    description: parameter description]
    '''
    assert_compat_as_expected(schema, expected)


def test_OpenAPI_30_parameter_with_no_schema():
    '''
    name: parameter name
    in: cookie
    '''
