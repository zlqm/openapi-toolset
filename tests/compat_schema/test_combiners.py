from .conftest import assert_compat_as_expected


def test_allOf_is_null():
    schema = '''
    allOf: null
    '''
    expected = '''
    {}
    '''
    assert_compat_as_expected(schema, expected)


def test_anyOf_is_null():
    schema = '''
    anyOf: null
    '''
    expected = '''
    {}
    '''
    assert_compat_as_expected(schema, expected)


def test_oneOf_is_null():
    schema = '''
    oneOf: null
    '''
    expected = '''
    {}
    '''
    assert_compat_as_expected(schema, expected)
