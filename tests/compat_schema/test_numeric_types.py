from .conftest import assert_compat_as_expected


def test_int32_format():
    schema = '''
    type: integer
    format: int32
    '''
    expected = '''
    type: integer
    format: int32
    minimum: -2147483648
    maximum:  2147483647
    '''
    assert_compat_as_expected(schema, expected)


def test_int32_format_with_specified_minimum():
    schema = '''
    type: integer
    format: int32
    minimum: 500
    '''
    expected = '''
    type: integer
    format: int32
    minimum: 500
    maximum:  2147483647
    '''
    assert_compat_as_expected(schema, expected)


def test_int32_format_with_specified_minimum_too_small():
    schema = '''
    type: integer
    format: int32
    minimum: -21474836480
    '''
    expected = '''
    type: integer
    format: int32
    minimum: -2147483648
    maximum:  2147483647
    '''
    assert_compat_as_expected(schema, expected)


def test_int32_format_with_specified_maximum():
    schema = '''
    type: integer
    format: int32
    maximum: 500
    '''
    expected = '''
    type: integer
    format: int32
    minimum: -2147483648
    maximum:  500
    '''
    assert_compat_as_expected(schema, expected)


def test_int32_format_with_specified_maximum_too_larger():
    schema = '''
    type: integer
    format: int32
    maximum: 21474836470
    '''
    expected = '''
    type: integer
    format: int32
    minimum: -2147483648
    maximum:  2147483647
    '''
    assert_compat_as_expected(schema, expected)


def test_int64_format():
    schema = '''
    type: integer
    format: int64
    '''
    expected = '''
    type: integer
    format: int64
    minimum: -9223372036854775808
    maximum:  9223372036854775807
    '''
    assert_compat_as_expected(schema, expected)


def test_int64_format_with_specified_minimum():
    schema = '''
    type: integer
    format: int64
    minimum: 500
    '''
    expected = '''
    type: integer
    format: int64
    minimum: 500
    maximum:  9223372036854775807
    '''
    assert_compat_as_expected(schema, expected)


def test_int64_format_with_specified_minimum_too_small():
    schema = '''
    type: integer
    format: int64
    minimum: -92233720368547758080
    '''
    expected = '''
    type: integer
    format: int64
    minimum: -9223372036854775808
    maximum:  9223372036854775807
    '''
    assert_compat_as_expected(schema, expected)


def test_int64_format_with_specified_maximum():
    schema = '''
    type: integer
    format: int64
    maximum: 500
    '''
    expected = '''
    type: integer
    format: int64
    minimum: -9223372036854775808
    maximum:  500
    '''
    assert_compat_as_expected(schema, expected)


def test_int64_format_with_specified_maximum_too_larger():
    schema = '''
    type: integer
    format: int64
    maximum: 92233720368547758070
    '''
    expected = '''
    type: integer
    format: int64
    minimum: -9223372036854775808
    maximum:  9223372036854775807
    '''
    assert_compat_as_expected(schema, expected)


def test_float_format():
    schema = '''
    type: number
    format: float
    '''

    expected = '''
    type: number
    format: float
    minimum: -340282366920938463463374607431768211456
    maximum:  340282366920938463463374607431768211455
    '''
    assert_compat_as_expected(schema, expected)


def test_float_format_with_specified_minimum():
    schema = '''
    type: number
    format: float
    minimum: 500
    '''

    expected = '''
    type: number
    format: float
    minimum: 500
    maximum:  340282366920938463463374607431768211455
    '''
    assert_compat_as_expected(schema, expected)


def test_float_format_with_specified_minimum_too_small():
    schema = '''
    type: number
    format: float
    minimum: -3402823669209384634633746074317682114560
    '''

    expected = '''
    type: number
    format: float
    minimum: -340282366920938463463374607431768211456
    maximum:  340282366920938463463374607431768211455
    '''
    assert_compat_as_expected(schema, expected)


def test_float_format_with_specified_maximum():
    schema = '''
    type: number
    format: float
    maximum: 500
    '''
    expected = '''
    type: number
    format: float
    minimum: -340282366920938463463374607431768211456
    maximum:  500
    '''
    assert_compat_as_expected(schema, expected)


def test_float_format_with_specified_maximum_too_larger():
    schema = '''
    type: number
    format: float
    maximum:  3402823669209384634633746074317682114550
    '''
    expected = '''
    type: number
    format: float
    minimum: -340282366920938463463374607431768211456
    maximum:  340282366920938463463374607431768211455
    '''
    assert_compat_as_expected(schema, expected)


# TODO: add double stuff
