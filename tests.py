from threading import Thread

from nose.tools import eq_
from six.moves import BaseHTTPServer

from pyhectane import Connection


class SimpleHttpHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """
    Simple handler that responds to all GET and POST requests with an empty
    JSON response. Logging is also disabled.
    """

    def _respond(self):
        self.send_response(200)
        self.send_header('Content-length', '2')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('{}')

    def do_GET(self):
        self._respond()

    def do_POST(self):
        self._respond()

    def log_message(self, format, *args):
        pass


class SimpleHttpServer(BaseHTTPServer.HTTPServer):
    """
    Extremely simple HTTP server that captures requests and stores them for
    later retrieval and examination.
    """

    def process_request(self, request, client_address):
        """
        Store the request before processing it.
        """
        self.request = self.RequestHandlerClass(request, client_address, self)


class Request:
    """
    Allows a single request to be processed by using Python's "with" statement.
    """

    def __getattr__(self, name):
        return getattr(self._server.request, name)

    def __enter__(self):
        self._server = SimpleHttpServer(('127.0.0.1', 8025), SimpleHttpHandler)
        self._thread = Thread(target=self._server.handle_request)
        self._thread.start()

    def __exit__(self, type, value, traceback):
        self._thread.join()


class TestConnection:
    """
    Run some simple tests to ensure the Connection class works correctly.
    """

    def test_version(self):
        r = Request()
        with r:
            Connection().version()
        eq_(r.command, 'GET')
        eq_(r.path, '/v1/version')
