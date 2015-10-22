from threading import Thread

from nose.tools import eq_, raises
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
        self.wfile.write(b'{}')

    def do_GET(self):
        self._respond()

    def do_POST(self):
        self._respond()
        self.data = self.rfile.read()

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
    A server is run in a separate thread for processing requests. The server
    captures the request information and makes its attributes available.
    """

    def __init__(self):
        self._server = SimpleHttpServer(('127.0.0.1', 0), SimpleHttpHandler)
        self._server.timeout = 2
        self._thread = Thread(target=self._server.serve_forever, args=[0.1])
        self.port = self._server.server_address[1]

    def __getattr__(self, name):
        return getattr(self._server.request, name)

    def __enter__(self):
        self._server.request = None
        self._thread.start()

    def __exit__(self, type, value, traceback):
        self._server.shutdown()
        self._thread.join()


class TestConnection:
    """
    Run some simple tests to ensure the Connection class works correctly.
    """

    _FROM = 'from@example.com'
    _TO = 'to@example.com'
    _SUBJECT = 'Test'
    _DATA = '0123456789'

    def setUp(self):
        self._r = Request()
        self._c = Connection(port=self._r.port)

    def test_raw(self):
        with self._r:
            self._c.raw(self._FROM, [self._TO], self._DATA)
        eq_(self._r.command, 'POST')
        eq_(self._r.path, '/v1/raw')

    def test_send(self):
        with self._r:
            self._c.send(self._FROM, [self._TO], self._SUBJECT, self._DATA)
        eq_(self._r.command, 'POST')
        eq_(self._r.path, '/v1/send')

    @raises(TypeError)
    def test_send_bad_to(self):
        with self._r:
            self._c.send(self._FROM, self._TO, self._SUBJECT, self._DATA)

    def test_status(self):
        with self._r:
            self._c.status()
        eq_(self._r.command, 'GET')
        eq_(self._r.path, '/v1/status')

    def test_version(self):
        with self._r:
            self._c.version()
        eq_(self._r.command, 'GET')
        eq_(self._r.path, '/v1/version')
