import json
import os

from .conftest import assert_compat_as_expected

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = os.path.join(BASE_DIR, 'schemas')


def test_complex_schema():
    with open(os.path.join(SCHEMA_DIR, 'schema-1.json')) as f:
        schema = json.load(f)
    with open(os.path.join(SCHEMA_DIR, 'schema-1-expected.json')) as f:
        expected = json.load(f)
    assert_compat_as_expected(schema, expected)


def test_complete_api_doc():
    with open(os.path.join(SCHEMA_DIR, 'webhook-example.yaml')) as f:
        schema = f.read()
    with open(os.path.join(SCHEMA_DIR, 'webhook-example-expected.yaml')) as f:
        expected = f.read()
    assert_compat_as_expected(schema, expected)
