from .conftest import assert_compat_as_expected


def test_nullable_without_enum():
    schema = '''
    type: string
    nullable: true
    '''
    expected = '''
    type:
      - string
      - 'null'
    '''
    assert_compat_as_expected(schema, expected)

    schema = '''
    type: string
    nullable: false
    '''
    expected = '''
    type: string
    '''
    assert_compat_as_expected(schema, expected)


def test_nullable_with_enum():
    schema = '''
    type: string
    enum:
      - a
      - b
    nullable: true
    '''
    expected = '''
    type:
      - string
      - 'null'
    enum:
      - a
      - b
      - null
    '''
    assert_compat_as_expected(schema, expected)

    schema = '''
    type: string
    enum:
      - a
      - b
    nullable: true
    '''
    expected = '''
    type:
      - string
      - 'null'
    enum:
      - a
      - b
      - null
    '''
    assert_compat_as_expected(schema, expected)
