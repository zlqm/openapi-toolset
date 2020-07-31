from .conftest import assert_compat_as_expected


def test_plain_string_is_untoched():
    schema = '''
    type: string
    '''
    expected = schema
    assert_compat_as_expected(schema, expected)


def test_date_format():
    schema = '''
    type: string
    format: date
    '''
    expected = '''
    type: string
    format: date
    '''
    assert_compat_as_expected(schema, expected)


def test_byte_format():
    schema = '''
    type: string
    format: byte
    '''
    expected = '''
    type: string
    format: byte
    pattern: '^[\\w\\d+\\/=]*$'
    '''
    assert_compat_as_expected(schema, expected)


def test_retaining_custom_format():
    schema = '''
    type: string
    format: custom_email
    '''
    expected = '''
    type: string
    format: custom_email
    '''
    assert_compat_as_expected(schema, expected)


def test_retaining_password_format():
    schema = '''
    type: string
    format: password
    '''
    expected = '''
    type: string
    format: password
    '''
    assert_compat_as_expected(schema, expected)
