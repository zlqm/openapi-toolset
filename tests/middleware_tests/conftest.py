import logging
import os

import django


logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_FILE = os.path.join(BASE_DIR, 'api_doc.yaml')
OPENAPI_COMPONENTS_DOC = os.path.join(BASE_DIR, 'components.yaml')


def pytest_configure():
    from django.conf import settings

    settings.configure(
        ALLOWED_HOSTS=['*'],
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        SITE_ID=1,
        SECRET_KEY='not very secret in tests',
        STATIC_URL='/static/',
        ROOT_URLCONF='tests.middleware_tests.urls',
        TEMPLATE_LOADERS=(
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
        MIDDLEWARE=(
            'openapi_toolset.django_plugin.middlewares.APIDocCheckMiddleware',
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'openapi_toolset.django_plugin',
        ),
        PASSWORD_HASHERS=('django.contrib.auth.hashers.MD5PasswordHasher', ),

        OPENAPI_COMPONENTS_DOC=OPENAPI_COMPONENTS_DOC,
        OPENAPI_CHECK_DOC=DOC_FILE,
    )

    django.setup()
