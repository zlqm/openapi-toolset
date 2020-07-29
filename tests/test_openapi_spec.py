import os
import shutil
import tempfile
from unittest.mock import patch

from openapi_toolset.spec import OpenAPISpec

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

openapi_file_yaml = os.path.join(BASE_DIR, 'openapi.yaml')
openapi_file_json = os.path.join(BASE_DIR, 'openapi.json')


@patch('urllib.request.urlretrieve')
def test_from_file(mock_urlretrieve):
    with tempfile.NamedTemporaryFile(suffix='.yaml') as f:
        url = 'http://mock.server/swagger.yaml'
        shutil.copy(openapi_file_yaml, f.name)
        mock_urlretrieve.return_value = f.name, {}
        spec = OpenAPISpec.from_file(url)
        assert spec.spec_dict['openapi'] == '3.0.0'

    with tempfile.NamedTemporaryFile(suffix='.json') as f:
        url = 'http://mock.server/swagger.json'
        shutil.copy(openapi_file_json, f.name)
        mock_urlretrieve.return_value = f.name, {}
        spec = OpenAPISpec.from_file(url)
        assert spec.spec_dict['openapi'] == '3.0.0'

    spec = OpenAPISpec.from_file(openapi_file_yaml)
    assert spec.spec_dict['openapi'] == '3.0.0'

    spec = OpenAPISpec.from_file(openapi_file_json)
    assert spec.spec_dict['openapi'] == '3.0.0'
