from base64 import b64decode, b64encode
from json import loads
from os.path import basename
from tempfile import NamedTemporaryFile
from threading import Thread

from nose.tools import eq_, raises
from six import b, u
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
        self.port = self._server.server_address[1]

    def __getattr__(self, name):
        return getattr(self._server.request, name)

    def __enter__(self):
        self._server.request = None
        self._thread = Thread(target=self._server.serve_forever, args=[0.1])
        self._thread.start()

    def __exit__(self, type, value, traceback):
        self._server.shutdown()
        self._thread.join()


class TestConnection:
    """
    Run simple tests against Connection's methods.
    """

    _USERNAME = 'username'
    _PASSWORD = 'password'

    _FROM = 'from@example.com'
    _TO = 'to@example.com'
    _SUBJECT = 'Test'
    _BDATA = b('\x00\x01\x02')
    _SDATA = u('0123456789')

    def setUp(self):
        self._r = Request()
        self._c = Connection(port=self._r.port)

    def test_auth(self):
        with self._r:
            Connection(port=self._r.port, username=self._USERNAME,
                       password=self._PASSWORD).version()
        eq_(self._r.headers['authorization'], 'Basic {}'.format(
            b64encode('{}:{}'.format(self._USERNAME, self._PASSWORD).encode()).decode(),
        ))

    def test_raw(self):
        with self._r:
            self._c.raw(self._FROM, [self._TO], self._SDATA)
        data = loads(self._r.data.decode())
        eq_(self._r.command, 'POST')
        eq_(self._r.path, '/v1/raw')
        eq_(data['body'], self._SDATA)

    @raises(TypeError)
    def test_raw_bad_to(self):
        with self._r:
            self._c.raw(self._FROM, self._TO, self._SDATA)

    def test_send(self):
        with self._r:
            self._c.send(self._FROM, [self._TO], self._SUBJECT, self._SDATA)
        eq_(self._r.command, 'POST')
        eq_(self._r.path, '/v1/send')

    @raises(TypeError)
    def test_send_bad_to(self):
        with self._r:
            self._c.send(self._FROM, self._TO, self._SUBJECT, self._SDATA)

    @raises(ValueError)
    def test_send_empty_content(self):
        with self._r:
            self._c.send(self._FROM, [self._TO], self._SUBJECT)

    def test_send_attachment_dict(self):
        with self._r:
            self._c.send(self._FROM, [self._TO], self._SUBJECT, self._SDATA,
                         attachments=[{}])
        data = loads(self._r.data.decode())
        eq_(len(data['attachments']), 1)

    def test_send_attachment_file(self):
        with NamedTemporaryFile() as f:
            f.write(self._BDATA)
            f.seek(0)
            for use_name in [True, False]:
                with self._r:
                    self._c.send(self._FROM, [self._TO], self._SUBJECT, self._SDATA,
                                 attachments=[f.name if use_name else f])
                data = loads(self._r.data.decode())
                eq_(data['attachments'][0]['filename'], basename(f.name))
                eq_(data['attachments'][0]['encoded'], True)
                eq_(b64decode(data['attachments'][0]['content']), self._BDATA)

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
