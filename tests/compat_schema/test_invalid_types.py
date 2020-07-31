from openapi_toolset.compat_schema import exceptions

from .conftest import assert_compat_as_expected, assert_compat_raise_exception


def test_invalid_types():
    schema = '''
    type: dateTime
    '''
    assert_compat_raise_exception(schema, exceptions.InvalidSchemaType)

    schema = '''
    type: foo
    '''
    assert_compat_raise_exception(schema, exceptions.InvalidSchemaType)

    schema = '''
    type:
      - string
      - null
    '''
    assert_compat_raise_exception(schema, exceptions.InvalidSchemaType)


def test_valid_types():
    types = [
        'integer', 'number', 'string', 'boolean', 'object', 'array', "'null'"
    ]

    for _type in types:
        schema = '''
        type: {}
        '''.format(_type)
        expected = schema
        assert_compat_as_expected(schema, expected)


"""
def test_invalid_type_allowed_when_strict_mode_is_false():
    schema = '''
    type: nonsense
    '''
    expected = '''
    type: nonsense
    '''
    assert_compat_as_expected(schema, expected)
"""
