from .conftest import assert_compat_as_expected


def test_remove_discriminator():
    schema = '''
    oneOf:
      - type: object
        required:
          - foo
        properties:
          foo:
            type: string
      - type: object
        required:
          - foo
        properties:
          foo:
            type: string
    discriminator:
      propertyName: foo
    '''
    expected = '''
    oneOf:
      - type: object
        required:
          - foo
        properties:
          foo:
            type: string
      - type: object
        required:
          - foo
        properties:
          foo:
            type: string
    '''
    assert_compat_as_expected(schema, expected)


def test_remove_readOnly():
    schema = '''
    type: object
    properties:
      readOnly:
        type: string
        readOnly: true
    '''
    expected = '''
    type: object
    properties:
      readOnly:
        type: string
    '''
    assert_compat_as_expected(schema, expected)


def test_remove_writeOnly():
    schema = '''
    type: object
    properties:
      writeOnly:
        type: string
        writeOnly: true
    '''
    expected = '''
    type: object
    properties:
      writeOnly:
        type: string
    '''
    assert_compat_as_expected(schema, expected)


def test_remove_xml():
    schema = '''
    type: object
    properties:
      foo:
        type: string
        xml:
          attribute: true
    '''
    expected = '''
    type: object
    properties:
      foo:
        type: string
    '''
    assert_compat_as_expected(schema, expected)


def test_remove_externalDocs():
    schema = '''
    type: object
    properties:
      foo:
        type: string
    externalDocs:
      url: 'http://foo.bar'
    '''
    expected = '''
    type: object
    properties:
      foo:
        type: string
    '''
    assert_compat_as_expected(schema, expected)


def test_remove_example():
    schema = '''
    type: string
    example: foo
    '''
    expected = '''
    type: string
    '''
    assert_compat_as_expected(schema, expected)


def test_remove_deprecated():
    schema = '''
    type: string
    deprecated: true
    '''

    expected = '''
    type: string
    '''
    assert_compat_as_expected(schema, expected)


def test_retaining_fields():
    schema = '''
    type: object
    properties:
      readOnly:
        type: string
        readOnly: true
        example: foo
      anotherProp:
        type: object
        properties:
          writeOnly:
            type: string
            writeOnly: true
    discriminator: bar
    '''
    expected = '''
    type: object
    properties:
      readOnly:
        type: string
      anotherProp:
        type: object
        properties:
          writeOnly:
            type: string
     '''
    assert_compat_as_expected(schema, expected)
