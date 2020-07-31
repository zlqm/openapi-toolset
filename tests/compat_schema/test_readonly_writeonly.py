from .conftest import assert_compat_as_expected


def test_not_remove_readOnly_prop():
    schema = '''
    type: object
    required:
      - prop1
      - prop2
    properties:
      prop1:
        type: string
        readOnly: true
      prop2:
        type: string
    '''
    expected = '''
    type: object
    required:
      - prop1
      - prop2
    properties:
      prop1:
        type: string
      prop2:
        type: string
    '''
    assert_compat_as_expected(schema, expected)


def test_not_remove_writeOnly_prop():
    schema = '''
    type: object
    required:
      - prop1
      - prop2
    properties:
      prop1:
        type: string
        writeOnly: true
      prop2:
        type: string
    '''
    expected = '''
    type: object
    required:
      - prop1
      - prop2
    properties:
      prop1:
        type: string
      prop2:
        type: string
    '''
    assert_compat_as_expected(schema, expected)
