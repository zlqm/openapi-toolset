from django.core.management.base import BaseCommand

from openapi_toolset.simple_openapi_server import (
    add_arguments, serve
)


class Command(BaseCommand):
    help = 'provide swagger editor/ui for local openapi doc'

    def add_arguments(self, parser):
        add_arguments(parser)

    def handle(self, *args, **kwargs):
        serve(kwargs['file'], kwargs['port'], kwargs['bind'])
