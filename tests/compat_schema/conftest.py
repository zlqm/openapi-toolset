import yaml
import pytest

from openapi_toolset.compat_schema import compat_jsonschema


def assert_compat_as_expected(schema, expected, msg=''):
    if isinstance(schema, str):
        schema = yaml.safe_load(schema)
    if isinstance(expected, str):
        expected = yaml.safe_load(expected)
    schema = compat_jsonschema(schema)
    assert schema == expected, msg


def assert_compat_raise_exception(schema, exception):
    if isinstance(schema, str):
        schema = yaml.safe_load(schema)
    with pytest.raises(exception):
        compat_jsonschema(schema)
