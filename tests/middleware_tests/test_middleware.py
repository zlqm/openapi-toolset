import json
import os
import shutil
import tempfile
from unittest.mock import patch

from django.core.management import call_command
from django.http import JsonResponse
from django.test import TestCase

from openapi_toolset.django_plugin import exceptions

from . import fake_data
from .conftest import DOC_FILE


def custom_missing_doc_handler(request, response, **kwargs):
    response_value = json.loads(response.content.decode(response.charset))
    content = {'err_msg': 'api doc missing', 'response': response_value}
    return JsonResponse(content, status=513)


def custom_mismatch_handler(request, response, **kwargs):
    response_value = json.loads(response.content.decode(response.charset))
    content = {'err_msg': 'api doc mismatch', 'response': response_value}
    return JsonResponse(content, status=513)


class MiddlewareTest(TestCase):
    DEBUG = False

    @classmethod
    def setUpTestData(cls):
        call_command('make_openapi_doc', '-f', DOC_FILE)

    def test_match(self):
        with self.settings(OPENAPI_CHECK_FAIL_FAST=False, DEBUG=self.DEBUG):
            response = self.client.get('/pets')
            assert response.json() == fake_data.valid_pet_list

    def test_match_fail_fast(self):
        with self.settings(OPENAPI_CHECK_FAIL_FAST=True, DEBUG=self.DEBUG):
            response = self.client.get('/pets')
            assert response.json() == fake_data.valid_pet_list

    def test_mismatch(self):
        with self.settings(OPENAPI_CHECK_FAIL_FAST=False, DEBUG=self.DEBUG):
            response = self.client.get('/pets?force_invalid=true')
            assert response.json() == fake_data.invalid_pet_list

    def test_mismatch_fail_fast(self):
        with self.settings(OPENAPI_CHECK_FAIL_FAST=True, DEBUG=self.DEBUG):
            response = self.client.get('/pets?force_invalid=true')
            assert response.json() == {'err_msg': 'api doc mismatch'}

    def test_miss_doc(self):
        with self.settings(OPENAPI_CHECK_FAIL_ON_MISSING=False,
                           DEBUG=self.DEBUG):
            response = self.client.get('/pets/bear')
            assert response.json() == fake_data.valid_pet_list

    def test_miss_doc_fail_on_missing(self):
        with self.settings(OPENAPI_CHECK_FAIL_ON_MISSING=True,
                           DEBUG=self.DEBUG):
            response = self.client.get('/pets/bear')
            assert response.json() == {'err_msg': 'api doc missing'}

    def test_custom_miss_doc_handler(self):
        with self.settings(
                OPENAPI_CHECK_MISSING_DOC_HANDLER=custom_missing_doc_handler):
            response = self.client.get('/pets/bear')
            assert response.status_code == 513
            assert response.json()['err_msg'] == 'api doc missing'
            assert response.json()['response'] == fake_data.valid_pet_list

    def test_custom_mismatch_handler(self):
        with self.settings(
                OPENAPI_CHECK_MISMATCH_HANDLER=custom_mismatch_handler):
            response = self.client.get('/pets?force_invalid=true')
            assert response.status_code == 513
            assert response.json()['err_msg'] == 'api doc mismatch'
            assert response.json()['response'] == fake_data.invalid_pet_list

    @patch('urllib.request.urlretrieve')
    def test_spec_from_url(self, mock_urlretrieve):
        ext = os.path.splitext(DOC_FILE)[-1]
        with tempfile.NamedTemporaryFile(suffix=ext) as f:
            url = 'http://mock.server/swagger' + ext
            shutil.copy(DOC_FILE, f.name)
            mock_urlretrieve.return_value = f.name, {}
            with self.settings(OPENAPI_CHECK_FAIL_FAST=False,
                               DEBUG=self.DEBUG,
                               OPENAPI_CHECK_DOC=url):
                response = self.client.get('/pets?force_invalid=true')
                assert response.json() == fake_data.invalid_pet_list


class DebugMiddlewareTest(MiddlewareTest):
    DEBUG = True

    def test_mismatch_fail_fast(self):
        with self.settings(OPENAPI_CHECK_FAIL_FAST=True, DEBUG=self.DEBUG):
            with self.assertRaises(exceptions.APIMismatchDoc):
                self.client.get('/pets?force_invalid=true')

    def test_miss_doc_fail_on_missing(self):
        with self.settings(OPENAPI_CHECK_FAIL_ON_MISSING=True,
                           DEBUG=self.DEBUG):
            with self.assertRaises(exceptions.APIMissDoc):
                self.client.get('/pets/bear')
