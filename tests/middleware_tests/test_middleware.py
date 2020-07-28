from django.core.management import call_command
from django.test import TestCase

from openapi_toolset.django_plugin import exceptions
from . import fake_data
from .conftest import DOC_FILE


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
