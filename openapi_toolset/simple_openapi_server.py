from argparse import ArgumentParser
import contextlib
from functools import partial
try:
    from http.server import ThreadingHTTPServer
except ImportError:
    from http.server import HTTPServer as ThreadingHTTPServer
from http.server import SimpleHTTPRequestHandler, test
import os
import posixpath
import socket
import urllib.parse

import openapi_toolset

STATIC_DIR = os.path.join(
    os.path.dirname(os.path.abspath(openapi_toolset.__file__)),
    'static/simple-openapi-server')
DEFAULT_OPENAPI_FILE = os.path.join(STATIC_DIR, 'petstore.yaml')


class OPENAPIRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, openapi_file=None, **kwargs):
        if openapi_file:
            self.openapi_file = os.path.abspath(openapi_file)
        else:
            self.openapi_file = DEFAULT_OPENAPI_FILE
        super().__init__(*args, **kwargs)

    def py38_translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.
        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)
        """
        # abandon query parameters
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        # Don't forget explicit trailing slash when normalizing. Issue17324
        trailing_slash = path.rstrip().endswith('/')
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        path = posixpath.normpath(path)
        words = path.split('/')
        words = filter(None, words)
        # py38: self.directory
        # py36: os.getcwd()
        path = STATIC_DIR
        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                # Ignore components that are not a simple file/directory name
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path

    path_alias = {
        '/': 'index.html',
    }

    def translate_path(self, path):
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        if path in self.path_alias:
            path = self.path_alias[path]
        elif path == '/openapi.yaml':
            return self.openapi_file
        res = self.py38_translate_path(path)
        return res


# ensure dual-stack is not disabled; ref #38907
class DualStackServer(ThreadingHTTPServer):
    def server_bind(self):
        # suppress exception when protocol is IPv4
        with contextlib.suppress(Exception):
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        return super().server_bind()


def add_arguments(parser):
    parser.add_argument('--bind',
                        '-b',
                        default='0.0.0.0',
                        help='Specify alternate bind address '
                        '[default: all interfaces]')
    parser.add_argument('--file',
                        '-f',
                        help='OPENAPI doc file '
                        '[default: openapi.yaml]')
    parser.add_argument('--port',
                        '-p',
                        action='store',
                        default=8000,
                        type=int,
                        help='Specify alternate port [default: 8000]')


def serve(filename, port, bind):
    handler_class = partial(OPENAPIRequestHandler, openapi_file=filename)
    test(
        HandlerClass=handler_class,
        ServerClass=DualStackServer,
        port=port,
        bind=bind,
    )


def cli():
    parser = ArgumentParser()
    add_arguments(parser)
    args = parser.parse_args()
    serve(args.file, args.port, args.bind)


if __name__ == '__main__':
    cli()
