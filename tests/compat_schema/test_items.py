from openapi_toolset.compat_schema import exceptions

from .conftest import assert_compat_as_expected, assert_compat_raise_exception


def test_items():
    schema = '''
    type: array
    items:
      type: string
      example: '2017-01-01T12:34:56Z'
    '''
    expected = '''
    type: array
    items:
      type: string
    '''
    assert_compat_as_expected(schema, expected)


def test_items_with_invalid_values():
    schema = '''
    type: array
    items:
      - type: string
      - 2
      - null
      - type: number
      - foo
      - type: array
    '''
    assert_compat_raise_exception(schema, exceptions.InvalidItemValue)
