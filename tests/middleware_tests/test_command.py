from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

import yaml

from .views import PetListView, PetView
from .conftest import DOC_FILE


class CommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('make_openapi_doc', '-f', DOC_FILE)
        with open(DOC_FILE, 'r') as f:
            cls.doc = yaml.safe_load(f)

    @staticmethod
    def get_api_doc(doc):
        return yaml.safe_load(doc.split('--api-doc--')[1])

    def test_doc_generation(self):
        assert '/pets' in self.doc['paths']
        assert self.doc['paths']['/pets']['get'] \
            == self.get_api_doc(PetListView.get.__doc__)
        assert self.doc['paths']['/pets']['post'] \
            == self.get_api_doc(PetListView.post.__doc__)

        assert '/pets/{pet_id}' in self.doc['paths']
        assert self.doc['paths']['/pets/{pet_id}']['get'] \
            == self.get_api_doc(PetView.get.__doc__)
        assert self.doc['paths']['/pets/{pet_id}']['parameters'] \
            == self.get_api_doc(PetView.__doc__)['parameters']

        with open(settings.OPENAPI_COMPONENTS_DOC) as f:
            components = yaml.safe_load(f)
        assert components == self.doc['components']
