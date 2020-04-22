import contextlib
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer, test
import os

STATIC_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'static')


class OPENAPIRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, openapi_file='openapi.yaml', **kwargs):
        self.openapi_file = os.path.abspath(openapi_file)
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

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
        return super().translate_path(path)

    def send_head(self):
        path = self.translate_path(self.path)
        return super().send_head()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--bind', '-b', metavar='ADDRESS',
                        help='Specify alternate bind address '
                             '[default: all interfaces]')
    parser.add_argument('--file', '-f', metavar='FILE',
                        help='OPENAPI doc file '
                             '[default: openapi.yaml]')
    parser.add_argument('port', action='store',
                        default=8000, type=int,
                        nargs='?',
                        help='Specify alternate port [default: 8000]')
    args = parser.parse_args()

    handler_class = partial(OPENAPIRequestHandler, openapi_file=args.file)

    # ensure dual-stack is not disabled; ref #38907
    class DualStackServer(ThreadingHTTPServer):
        def server_bind(self):
            # suppress exception when protocol is IPv4
            with contextlib.suppress(Exception):
                self.socket.setsockopt(
                    socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            return super().server_bind()

    test(
        HandlerClass=handler_class,
        ServerClass=DualStackServer,
        port=args.port,
        bind=args.bind,
    )
